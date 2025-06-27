#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة إنشاء التقارير
"""

import os
import json
import time
import datetime
from colorama import Fore, Style
import matplotlib.pyplot as plt
import pandas as pd
from .utils import print_status

class ReportGenerator:
    """
    فئة إنشاء التقارير
    """
    def __init__(self, target, output_file=None, logger=None, quiet=False, debug=False):
        """
        تهيئة الفئة
        """
        self.target = target
        self.output_file = output_file
        self.logger = logger
        self.quiet = quiet
        self.debug = debug
        self.results = {}
        self.start_time = time.time()
        self.end_time = None
        
        # إنشاء مجلد التقارير إذا لم يكن موجودًا
        self.reports_dir = os.path.join(os.getcwd(), "reports")
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
        
        # إذا لم يتم تحديد ملف الإخراج، قم بإنشاء اسم ملف افتراضي
        if not self.output_file:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_file = os.path.join(self.reports_dir, f"report_{self.target.replace('.', '_').replace(':', '_')}_{timestamp}.html")
    
    def add_results(self, module_name, results):
        """
        إضافة نتائج من وحدة معينة
        """
        self.results[module_name] = results
        
        if not self.quiet:
            print_status(f"تمت إضافة نتائج من {module_name} إلى التقرير", "info")
        
        if self.logger:
            self.logger.info(f"تمت إضافة نتائج من {module_name} إلى التقرير")
    
    def set_scan_time(self, end_time=None):
        """
        تعيين وقت انتهاء الفحص
        """
        if end_time:
            self.end_time = end_time
        else:
            self.end_time = time.time()
    
    def generate_report(self):
        """
        إنشاء التقرير
        """
        if not self.end_time:
            self.set_scan_time()
        
        if not self.quiet:
            print_status(f"إنشاء التقرير في {self.output_file}", "info")
        
        if self.logger:
            self.logger.info(f"إنشاء التقرير في {self.output_file}")
        
        # إنشاء التقرير بتنسيق HTML
        self._generate_html_report()
        
        # إنشاء التقرير بتنسيق JSON (للاستخدام البرمجي)
        json_file = self.output_file.replace(".html", ".json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4, default=str)
        
        if not self.quiet:
            print_status(f"تم إنشاء التقرير بنجاح في {self.output_file}", "success")
            print_status(f"تم إنشاء ملف JSON في {json_file}", "success")
        
        if self.logger:
            self.logger.info(f"تم إنشاء التقرير بنجاح في {self.output_file}")
            self.logger.info(f"تم إنشاء ملف JSON في {json_file}")
        
        return self.output_file
    
    def _generate_html_report(self):
        """
        إنشاء تقرير HTML
        """
        # إنشاء الرسوم البيانية
        charts_dir = os.path.join(os.path.dirname(self.output_file), "charts")
        if not os.path.exists(charts_dir):
            os.makedirs(charts_dir)
        
        # إنشاء الرسوم البيانية إذا كانت البيانات متوفرة
        chart_files = {}
        
        # رسم بياني للمنافذ المفتوحة
        if "port_scanner" in self.results:
            chart_files["open_ports"] = self._generate_ports_chart(charts_dir)
        
        # رسم بياني للثغرات
        if "vulnerability_scanner" in self.results or "web_scanner" in self.results or "cms_scanner" in self.results:
            chart_files["vulnerabilities"] = self._generate_vulnerabilities_chart(charts_dir)
        
        # إنشاء ملف HTML
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(self._get_html_template(chart_files))
    
    def _generate_ports_chart(self, charts_dir):
        """
        إنشاء رسم بياني للمنافذ المفتوحة
        """
        try:
            # الحصول على بيانات المنافذ المفتوحة
            port_data = self.results.get("port_scanner", {})
            open_ports = port_data.get("open_ports", [])
            
            if not open_ports:
                return None
            
            # تحضير البيانات للرسم البياني
            ports = []
            services = []
            
            for port_info in open_ports:
                port = port_info.get("port")
                service = port_info.get("service", "unknown")
                
                ports.append(port)
                services.append(service)
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(10, 6))
            plt.bar(ports, [1] * len(ports), color='skyblue')
            plt.xlabel('المنافذ')
            plt.ylabel('الحالة')
            plt.title('المنافذ المفتوحة')
            plt.xticks(ports, rotation=45)
            
            # إضافة أسماء الخدمات
            for i, port in enumerate(ports):
                plt.text(port, 0.5, services[i], ha='center', va='center', rotation=90, color='black')
            
            # حفظ الرسم البياني
            chart_file = os.path.join(charts_dir, f"open_ports_{self.target.replace('.', '_').replace(':', '_')}.png")
            plt.tight_layout()
            plt.savefig(chart_file)
            plt.close()
            
            return os.path.relpath(chart_file, os.path.dirname(self.output_file))
        except Exception as e:
            if self.logger:
                self.logger.error(f"فشل في إنشاء رسم بياني للمنافذ: {str(e)}")
            return None
    
    def _generate_vulnerabilities_chart(self, charts_dir):
        """
        إنشاء رسم بياني للثغرات
        """
        try:
            # جمع بيانات الثغرات من جميع الوحدات
            vulnerabilities = []
            
            # الثغرات من وحدة فحص الثغرات
            if "vulnerability_scanner" in self.results:
                vuln_data = self.results["vulnerability_scanner"].get("vulnerabilities", [])
                vulnerabilities.extend(vuln_data)
            
            # الثغرات من وحدة فحص الويب
            if "web_scanner" in self.results:
                web_vuln_data = self.results["web_scanner"].get("vulnerabilities", [])
                vulnerabilities.extend(web_vuln_data)
            
            # الثغرات من وحدة فحص أنظمة إدارة المحتوى
            if "cms_scanner" in self.results:
                if "wordpress" in self.results["cms_scanner"]:
                    wp_vuln_data = self.results["cms_scanner"]["wordpress"].get("vulnerabilities", [])
                    vulnerabilities.extend(wp_vuln_data)
                
                if "joomla" in self.results["cms_scanner"]:
                    joomla_vuln_data = self.results["cms_scanner"]["joomla"].get("vulnerabilities", [])
                    vulnerabilities.extend(joomla_vuln_data)
            
            if not vulnerabilities:
                return None
            
            # تصنيف الثغرات حسب الخطورة
            severity_counts = {"عالية": 0, "متوسطة": 0, "منخفضة": 0, "معلومات": 0}
            
            for vuln in vulnerabilities:
                severity = vuln.get("severity", "معلومات").lower()
                
                if "high" in severity or "عالية" in severity:
                    severity_counts["عالية"] += 1
                elif "medium" in severity or "متوسطة" in severity:
                    severity_counts["متوسطة"] += 1
                elif "low" in severity or "منخفضة" in severity:
                    severity_counts["منخفضة"] += 1
                else:
                    severity_counts["معلومات"] += 1
            
            # إنشاء الرسم البياني
            labels = list(severity_counts.keys())
            sizes = list(severity_counts.values())
            colors = ['red', 'orange', 'yellow', 'blue']
            
            plt.figure(figsize=(8, 8))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            plt.title('توزيع الثغرات حسب الخطورة')
            
            # حفظ الرسم البياني
            chart_file = os.path.join(charts_dir, f"vulnerabilities_{self.target.replace('.', '_').replace(':', '_')}.png")
            plt.savefig(chart_file)
            plt.close()
            
            return os.path.relpath(chart_file, os.path.dirname(self.output_file))
        except Exception as e:
            if self.logger:
                self.logger.error(f"فشل في إنشاء رسم بياني للثغرات: {str(e)}")
            return None
    
    def _get_html_template(self, chart_files):
        """
        الحصول على قالب HTML للتقرير
        """
        scan_duration = self.end_time - self.start_time
        timestamp = datetime.datetime.fromtimestamp(self.end_time).strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير فحص الأمان - {self.target}</title>
    <style>
        body {{font-family: Arial, sans-serif; margin: 0; padding: 20px; direction: rtl; text-align: right;}}
        .container {{max-width: 1200px; margin: 0 auto; background-color: #f9f9f9; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1);}}
        h1, h2, h3, h4 {{color: #333;}}
        .header {{background-color: #4CAF50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px;}}
        .section {{margin-bottom: 30px; background-color: white; padding: 15px; border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.05);}}
        .subsection {{margin-bottom: 20px;}}
        table {{width: 100%; border-collapse: collapse; margin-bottom: 20px;}}
        th, td {{padding: 12px 15px; text-align: right; border-bottom: 1px solid #ddd;}}
        th {{background-color: #f2f2f2;}}
        tr:hover {{background-color: #f5f5f5;}}
        .severity-high {{color: #d9534f; font-weight: bold;}}
        .severity-medium {{color: #f0ad4e; font-weight: bold;}}
        .severity-low {{color: #5bc0de; font-weight: bold;}}
        .severity-info {{color: #5cb85c; font-weight: bold;}}
        .chart {{margin: 20px 0; text-align: center;}}
        .chart img {{max-width: 100%; height: auto;}}
        .footer {{text-align: center; margin-top: 30px; color: #777; font-size: 14px;}}
        .summary {{display: flex; justify-content: space-between; flex-wrap: wrap;}}
        .summary-box {{flex: 1; min-width: 200px; margin: 10px; padding: 15px; border-radius: 5px; color: white; text-align: center;}}
        .summary-box h3 {{margin-top: 0;}}
        .summary-box.red {{background-color: #d9534f;}}
        .summary-box.orange {{background-color: #f0ad4e;}}
        .summary-box.blue {{background-color: #5bc0de;}}
        .summary-box.green {{background-color: #5cb85c;}}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>تقرير فحص الأمان</h1>
            <p>تم إنشاؤه بواسطة أداة SaudiAttacks</p>
        </div>
        
        <div class="section">
            <h2>ملخص الفحص</h2>
            <p><strong>الهدف:</strong> {self.target}</p>
            <p><strong>تاريخ الفحص:</strong> {timestamp}</p>
            <p><strong>مدة الفحص:</strong> {scan_duration:.2f} ثانية</p>
            
            <div class="summary">
"""
        
        # إضافة مربعات الملخص
        vuln_count = 0
        high_vuln_count = 0
        medium_vuln_count = 0
        low_vuln_count = 0
        open_ports_count = 0
        
        
        # حساب عدد الثغرات والمنافذ المفتوحة
        if "vulnerability_scanner" in self.results:
            vuln_data = self.results["vulnerability_scanner"].get("vulnerabilities", [])
            vuln_count += len(vuln_data)
            
            for vuln in vuln_data:
                severity = vuln.get("severity", "").lower()
                if "high" in severity or "عالية" in severity:
                    high_vuln_count += 1
                elif "medium" in severity or "متوسطة" in severity:
                    medium_vuln_count += 1
                elif "low" in severity or "منخفضة" in severity:
                    low_vuln_count += 1
        
        if "web_scanner" in self.results:
            web_vuln_data = self.results["web_scanner"].get("vulnerabilities", [])
            vuln_count += len(web_vuln_data)
            
            for vuln in web_vuln_data:
                severity = vuln.get("severity", "").lower()
                if "high" in severity or "عالية" in severity:
                    high_vuln_count += 1
                elif "medium" in severity or "متوسطة" in severity:
                    medium_vuln_count += 1
                elif "low" in severity or "منخفضة" in severity:
                    low_vuln_count += 1
        
        if "cms_scanner" in self.results:
            if "wordpress" in self.results["cms_scanner"]:
                wp_vuln_data = self.results["cms_scanner"]["wordpress"].get("vulnerabilities", [])
                vuln_count += len(wp_vuln_data)
                
                for vuln in wp_vuln_data:
                    severity = vuln.get("severity", "").lower()
                    if "high" in severity or "عالية" in severity:
                        high_vuln_count += 1
                    elif "medium" in severity or "متوسطة" in severity:
                        medium_vuln_count += 1
                    elif "low" in severity or "منخفضة" in severity:
                        low_vuln_count += 1
            
            if "joomla" in self.results["cms_scanner"]:
                joomla_vuln_data = self.results["cms_scanner"]["joomla"].get("vulnerabilities", [])
                vuln_count += len(joomla_vuln_data)
                
                for vuln in joomla_vuln_data:
                    severity = vuln.get("severity", "").lower()
                    if "high" in severity or "عالية" in severity:
                        high_vuln_count += 1
                    elif "medium" in severity or "متوسطة" in severity:
                        medium_vuln_count += 1
                    elif "low" in severity or "منخفضة" in severity:
                        low_vuln_count += 1
        
        if "port_scanner" in self.results:
            port_data = self.results.get("port_scanner", {})
            open_ports = port_data.get("open_ports", [])
            open_ports_count = len(open_ports)
        
        html += f"""
                <div class="summary-box red">
                    <h3>الثغرات عالية الخطورة</h3>
                    <h2>{high_vuln_count}</h2>
                </div>
                <div class="summary-box orange">
                    <h3>الثغرات متوسطة الخطورة</h3>
                    <h2>{medium_vuln_count}</h2>
                </div>
                <div class="summary-box blue">
                    <h3>الثغرات منخفضة الخطورة</h3>
                    <h2>{low_vuln_count}</h2>
                </div>
                <div class="summary-box green">
                    <h3>المنافذ المفتوحة</h3>
                    <h2>{open_ports_count}</h2>
                </div>
            </div>
        </div>
"""
        
        # إضافة الرسوم البيانية
        if chart_files:
            html += """<div class="section">
            <h2>الرسوم البيانية</h2>
"""
            
            if "open_ports" in chart_files and chart_files["open_ports"]:
                html += f"""
                <div class="chart">
                    <h3>المنافذ المفتوحة</h3>
                    <img src="{chart_files['open_ports']}" alt="رسم بياني للمنافذ المفتوحة">
                </div>
"""
            
            if "vulnerabilities" in chart_files and chart_files["vulnerabilities"]:
                html += f"""
                <div class="chart">
                    <h3>توزيع الثغرات حسب الخطورة</h3>
                    <img src="{chart_files['vulnerabilities']}" alt="رسم بياني للثغرات">
                </div>
"""
            
            html += """</div>
"""
        
        # إضافة معلومات الهدف
        if "info_gathering" in self.results:
            info_data = self.results["info_gathering"]
            
            html += """<div class="section">
            <h2>معلومات الهدف</h2>
"""
            
            # معلومات DNS
            if "dns_records" in info_data:
                html += """<div class="subsection">
                <h3>سجلات DNS</h3>
                <table>
                    <tr>
                        <th>النوع</th>
                        <th>القيمة</th>
                    </tr>
"""
                
                dns_records = info_data["dns_records"]
                for record_type, records in dns_records.items():
                    if isinstance(records, list):
                        for record in records:
                            html += f"""
                    <tr>
                        <td>{record_type}</td>
                        <td>{record}</td>
                    </tr>
"""
                    else:
                        html += f"""
                    <tr>
                        <td>{record_type}</td>
                        <td>{records}</td>
                    </tr>
"""
                
                html += """</table>
            </div>
"""
            
            # معلومات Whois
            if "whois_data" in info_data:
                html += """<div class="subsection">
                <h3>معلومات Whois</h3>
                <table>
                    <tr>
                        <th>الحقل</th>
                        <th>القيمة</th>
                    </tr>
"""
                
                whois_data = info_data["whois_data"]
                for field, value in whois_data.items():
                    if isinstance(value, (list, dict)):
                        value = str(value)
                    
                    html += f"""
                    <tr>
                        <td>{field}</td>
                        <td>{value}</td>
                    </tr>
"""
                
                html += """</table>
            </div>
"""
            
            # معلومات الشبكة
            if "network_info" in info_data:
                html += """<div class="subsection">
                <h3>معلومات الشبكة</h3>
                <table>
                    <tr>
                        <th>الحقل</th>
                        <th>القيمة</th>
                    </tr>
"""
                
                network_info = info_data["network_info"]
                for field, value in network_info.items():
                    if isinstance(value, (list, dict)):
                        value = str(value)
                    
                    html += f"""
                    <tr>
                        <td>{field}</td>
                        <td>{value}</td>
                    </tr>
"""
                
                html += """</table>
            </div>
"""
            
            # معلومات الويب
            if "web_info" in info_data:
                html += """<div class="subsection">
                <h3>معلومات الويب</h3>
                <table>
                    <tr>
                        <th>الحقل</th>
                        <th>القيمة</th>
                    </tr>
"""
                
                web_info = info_data["web_info"]
                for field, value in web_info.items():
                    if isinstance(value, (list, dict)):
                        value = str(value)
                    
                    html += f"""
                    <tr>
                        <td>{field}</td>
                        <td>{value}</td>
                    </tr>
"""
                
                html += """</table>
            </div>
"""
            
            html += """</div>
"""
        
        # إضافة نتائج فحص المنافذ
        if "port_scanner" in self.results:
            port_data = self.results["port_scanner"]
            
            html += """<div class="section">
            <h2>نتائج فحص المنافذ</h2>
"""
            
            if "open_ports" in port_data and port_data["open_ports"]:
                html += """<div class="subsection">
                <h3>المنافذ المفتوحة</h3>
                <table>
                    <tr>
                        <th>المنفذ</th>
                        <th>البروتوكول</th>
                        <th>الخدمة</th>
                        <th>الإصدار</th>
                        <th>الحالة</th>
                    </tr>
"""
                
                for port_info in port_data["open_ports"]:
                    port = port_info.get("port", "")
                    protocol = port_info.get("protocol", "")
                    service = port_info.get("service", "")
                    version = port_info.get("version", "")
                    state = port_info.get("state", "")
                    
                    html += f"""
                    <tr>
                        <td>{port}</td>
                        <td>{protocol}</td>
                        <td>{service}</td>
                        <td>{version}</td>
                        <td>{state}</td>
                    </tr>
"""
                
                html += """</table>
            </div>
"""
            
            # معلومات نظام التشغيل
            if "os_detection" in port_data and port_data["os_detection"]:
                html += """<div class="subsection">
                <h3>اكتشاف نظام التشغيل</h3>
                <table>
                    <tr>
                        <th>نظام التشغيل</th>
                        <th>الدقة</th>
                    </tr>
"""
                
                os_info = port_data["os_detection"]
                for os_name, accuracy in os_info.items():
                    html += f"""
                    <tr>
                        <td>{os_name}</td>
                        <td>{accuracy}%</td>
                    </tr>
"""
                
                html += """</table>
            </div>
"""
            
            html += """</div>
"""
        
        # إضافة نتائج فحص الثغرات
        if "vulnerability_scanner" in self.results:
            vuln_data = self.results["vulnerability_scanner"]
            
            html += """<div class="section">
            <h2>نتائج فحص الثغرات</h2>
"""
            
            if "vulnerabilities" in vuln_data and vuln_data["vulnerabilities"]:
                html += """<div class="subsection">
                <h3>الثغرات المكتشفة</h3>
                <table>
                    <tr>
                        <th>الاسم</th>
                        <th>الوصف</th>
                        <th>الخطورة</th>
                        <th>التفاصيل</th>
                    </tr>
"""
                
                for vuln in vuln_data["vulnerabilities"]:
                    name = vuln.get("name", "")
                    description = vuln.get("description", "")
                    severity = vuln.get("severity", "")
                    details = vuln.get("details", "")
                    
                    severity_class = ""
                    if "high" in severity.lower() or "عالية" in severity.lower():
                        severity_class = "severity-high"
                    elif "medium" in severity.lower() or "متوسطة" in severity.lower():
                        severity_class = "severity-medium"
                    elif "low" in severity.lower() or "منخفضة" in severity.lower():
                        severity_class = "severity-low"
                    else:
                        severity_class = "severity-info"
                    
                    html += f"""
                    <tr>
                        <td>{name}</td>
                        <td>{description}</td>
                        <td class="{severity_class}">{severity}</td>
                        <td>{details}</td>
                    </tr>
"""
                
                html += """</table>
            </div>
"""
            
            html += """</div>
"""
        
        # إضافة نتائج فحص الويب
        if "web_scanner" in self.results:
            web_data = self.results["web_scanner"]
            
            html += """<div class="section">
            <h2>نتائج فحص الويب</h2>
"""
            
            # معلومات خادم الويب
            if "server_info" in web_data:
                html += """<div class="subsection">
                <h3>معلومات خادم الويب</h3>
                <table>
                    <tr>
                        <th>الحقل</th>
                        <th>القيمة</th>
                    </tr>
"""
                
                server_info = web_data["server_info"]
                for field, value in server_info.items():
                    if isinstance(value, (list, dict)):
                        value = str(value)
                    
                    html += f"""
                    <tr>
                        <td>{field}</td>
                        <td>{value}</td>
                    </tr>
"""
                
                html += """</table>
            </div>
"""
            
            # ترويسات الأمان
            if "security_headers" in web_data:
                html += """<div class="subsection">
                <h3>ترويسات الأمان</h3>
                <table>
                    <tr>
                        <th>الترويسة</th>
                        <th>القيمة</th>
                        <th>الحالة</th>
                    </tr>
"""
                
                security_headers = web_data["security_headers"]
                for header, header_info in security_headers.items():
                    value = header_info.get("value", "")
                    status = header_info.get("status", "")
                    
                    status_class = ""
                    if status.lower() == "missing" or status.lower() == "مفقود":
                        status_class = "severity-high"
                    elif status.lower() == "insecure" or status.lower() == "غير آمن":
                        status_class = "severity-medium"
                    elif status.lower() == "ok" or status.lower() == "جيد":
                        status_class = "severity-info"
                    
                    html += f"""
                    <tr>
                        <td>{header}</td>
                        <td>{value}</td>
                        <td class="{status_class}">{status}</td>
                    </tr>
"""
                
                html += """</table>
            </div>
"""
            
            # الملفات الحساسة
            if "sensitive_files" in web_data and web_data["sensitive_files"]:
                html += """<div class="subsection">
                <h3>الملفات الحساسة</h3>
                <table>
                    <tr>
                        <th>المسار</th>
                        <th>الحالة</th>
                        <th>الوصف</th>
                    </tr>
"""
                
                for file_info in web_data["sensitive_files"]:
                    path = file_info.get("path", "")
                    status = file_info.get("status", "")
                    description = file_info.get("description", "")
                    
                    status_class = ""
                    if status == 200:
                        status_class = "severity-high"
                    elif status >= 300 and status < 400:
                        status_class = "severity-medium"
                    else:
                        status_class = "severity-info"
                    
                    html += f"""
                    <tr>
                        <td>{path}</td>
                        <td class="{status_class}">{status}</td>
                        <td>{description}</td>
                    </tr>
"""
                
                html += """</table>
            </div>
"""
            
            # ثغرات الويب
            if "vulnerabilities" in web_data and web_data["vulnerabilities"]:
                html += """<div class="subsection">
                <h3>ثغرات الويب</h3>
                <table>
                    <tr>
                        <th>الاسم</th>
                        <th>الوصف</th>
                        <th>الخطورة</th>
                        <th>التفاصيل</th>
                    </tr>
"""
                
                for vuln in web_data["vulnerabilities"]:
                    name = vuln.get("name", "")
                    description = vuln.get("description", "")
                    severity = vuln.get("severity", "")
                    details = vuln.get("details", "")
                    
                    severity_class = ""
                    if "high" in severity.lower() or "عالية" in severity.lower():
                        severity_class = "severity-high"
                    elif "medium" in severity.lower() or "متوسطة" in severity.lower():
                        severity_class = "severity-medium"
                    elif "low" in severity.lower() or "منخفضة" in severity.lower():
                        severity_class = "severity-low"
                    else:
                        severity_class = "severity-info"
                    
                    html += f"""
                    <tr>
                        <td>{name}</td>
                        <td>{description}</td>
                        <td class="{severity_class}">{severity}</td>
                        <td>{details}</td>
                    </tr>
"""
                
                html += """</table>
            </div>
"""
            
            html += """</div>
"""
        
        # إضافة نتائج فحص أنظمة إدارة المحتوى
        if "cms_scanner" in self.results:
            cms_data = self.results["cms_scanner"]
            
            html += """<div class="section">
            <h2>نتائج فحص أنظمة إدارة المحتوى</h2>
"""
            
            # معلومات نظام إدارة المحتوى
            if "cms_info" in cms_data:
                cms_info = cms_data["cms_info"]
                cms_type = cms_info.get("cms_type", "غير معروف")
                cms_version = cms_info.get("cms_version", "غير معروف")
                
                html += f"""
                <div class="subsection">
                    <h3>معلومات نظام إدارة المحتوى</h3>
                    <p><strong>النوع:</strong> {cms_type}</p>
                    <p><strong>الإصدار:</strong> {cms_version}</p>
                </div>
"""
            
            # نتائج فحص ووردبريس
            if "wordpress" in cms_data:
                wp_data = cms_data["wordpress"]
                
                html += """<div class="subsection">
                <h3>نتائج فحص ووردبريس</h3>
"""
                
                # المستخدمين
                if "users" in wp_data and wp_data["users"]:
                    html += """<h4>المستخدمين</h4>
                    <table>
                        <tr>
                            <th>المعرف</th>
                            <th>الاسم</th>
                            <th>المعرف المختصر</th>
                            <th>الرابط</th>
                        </tr>
"""
                    
                    for user in wp_data["users"]:
                        user_id = user.get("id", "")
                        name = user.get("name", "")
                        slug = user.get("slug", "")
                        link = user.get("link", "")
                        
                        html += f"""
                        <tr>
                            <td>{user_id}</td>
                            <td>{name}</td>
                            <td>{slug}</td>
                            <td><a href="{link}" target="_blank">{link}</a></td>
                        </tr>
"""
                    
                    html += """</table>
"""
                
                # الإضافات
                if "plugins" in wp_data and wp_data["plugins"]:
                    html += """<h4>الإضافات</h4>
                    <table>
                        <tr>
                            <th>الاسم</th>
                            <th>الإصدار</th>
                            <th>الرابط</th>
                        </tr>
"""
                    
                    for plugin in wp_data["plugins"]:
                        name = plugin.get("name", "")
                        version = plugin.get("version", "غير معروف")
                        url = plugin.get("url", "")
                        
                        html += f"""
                        <tr>
                            <td>{name}</td>
                            <td>{version}</td>
                            <td><a href="{url}" target="_blank">{url}</a></td>
                        </tr>
"""
                    
                    html += """</table>
"""
                
                # القوالب
                if "themes" in wp_data and wp_data["themes"]:
                    html += """<h4>القوالب</h4>
                    <table>
                        <tr>
                            <th>الاسم</th>
                            <th>الإصدار</th>
                            <th>الحالة</th>
                            <th>الرابط</th>
                        </tr>
"""
                    
                    for theme in wp_data["themes"]:
                        name = theme.get("name", "")
                        version = theme.get("version", "غير معروف")
                        active = "نشط" if theme.get("active", False) else "غير نشط"
                        url = theme.get("url", "")
                        
                        html += f"""
                        <tr>
                            <td>{name}</td>
                            <td>{version}</td>
                            <td>{active}</td>
                            <td><a href="{url}" target="_blank">{url}</a></td>
                        </tr>
"""
                    
                    html += """</table>
"""
                
                # الثغرات
                if "vulnerabilities" in wp_data and wp_data["vulnerabilities"]:
                    html += """<h4>الثغرات</h4>
                    <table>
                        <tr>
                            <th>النوع</th>
                            <th>الاسم</th>
                            <th>الإصدار</th>
                            <th>الخطورة</th>
                        </tr>
"""
                    
                    for vuln in wp_data["vulnerabilities"]:
                        vuln_type = vuln.get("type", "")
                        name = vuln.get("name", "")
                        version = vuln.get("version", "")
                        severity = vuln.get("severity", "")
                        
                        severity_class = ""
                        if "high" in severity.lower() or "عالية" in severity.lower():
                            severity_class = "severity-high"
                        elif "medium" in severity.lower() or "متوسطة" in severity.lower():
                            severity_class = "severity-medium"
                        elif "low" in severity.lower() or "منخفضة" in severity.lower():
                            severity_class = "severity-low"
                        else:
                            severity_class = "severity-info"
                        
                        html += f"""
                        <tr>
                            <td>{vuln_type}</td>
                            <td>{name}</td>
                            <td>{version}</td>
                            <td class="{severity_class}">{severity}</td>
                        </tr>
"""
                    
                    html += """</table>
"""
                
                html += """</div>
"""
            
            # نتائج فحص جوملا
            if "joomla" in cms_data:
                joomla_data = cms_data["joomla"]
                
                html += """<div class="subsection">
                <h3>نتائج فحص جوملا</h3>
"""
                
                # المكونات
                if "components" in joomla_data and joomla_data["components"]:
                    html += """<h4>المكونات</h4>
                    <table>
                        <tr>
                            <th>الاسم</th>
                            <th>الرابط</th>
                        </tr>
"""
                    
                    for component in joomla_data["components"]:
                        name = component.get("name", "")
                        url = component.get("url", "")
                        
                        html += f"""
                        <tr>
                            <td>{name}</td>
                            <td><a href="{url}" target="_blank">{url}</a></td>
                        </tr>
"""
                    
                    html += """</table>
"""
                
                # الإضافات
                if "plugins" in joomla_data and joomla_data["plugins"]:
                    html += """<h4>الإضافات</h4>
                    <table>
                        <tr>
                            <th>الاسم</th>
                            <th>النوع</th>
                            <th>الرابط</th>
                        </tr>
"""
                    
                    for plugin in joomla_data["plugins"]:
                        name = plugin.get("name", "")
                        plugin_type = plugin.get("type", "")
                        url = plugin.get("url", "")
                        
                        html += f"""
                        <tr>
                            <td>{name}</td>
                            <td>{plugin_type}</td>
                            <td><a href="{url}" target="_blank">{url}</a></td>
                        </tr>
"""
                    
                    html += """</table>
"""
                
                # القوالب
                if "templates" in joomla_data and joomla_data["templates"]:
                    html += """<h4>القوالب</h4>
                    <table>
                        <tr>
                            <th>الاسم</th>
                            <th>الإصدار</th>
                            <th>الحالة</th>
                            <th>الرابط</th>
                        </tr>
"""
                    
                    for template in joomla_data["templates"]:
                        name = template.get("name", "")
                        version = template.get("version", "غير معروف")
                        active = "نشط" if template.get("active", False) else "غير نشط"
                        url = template.get("url", "")
                        
                        html += f"""
                        <tr>
                            <td>{name}</td>
                            <td>{version}</td>
                            <td>{active}</td>
                            <td><a href="{url}" target="_blank">{url}</a></td>
                        </tr>
"""
                    
                    html += """</table>
"""
                
                # الثغرات
                if "vulnerabilities" in joomla_data and joomla_data["vulnerabilities"]:
                    html += """<h4>الثغرات</h4>
                    <table>
                        <tr>
                            <th>النوع</th>
                            <th>الاسم</th>
                            <th>الإصدار</th>
                            <th>الخطورة</th>
                        </tr>
"""
                    
                    for vuln in joomla_data["vulnerabilities"]:
                        vuln_type = vuln.get("type", "")
                        name = vuln.get("name", "")
                        version = vuln.get("version", "")
                        severity = vuln.get("severity", "")
                        
                        severity_class = ""
                        if "high" in severity.lower() or "عالية" in severity.lower():
                            severity_class = "severity-high"
                        elif "medium" in severity.lower() or "متوسطة" in severity.lower():
                            severity_class = "severity-medium"
                        elif "low" in severity.lower() or "منخفضة" in severity.lower():
                            severity_class = "severity-low"
                        else:
                            severity_class = "severity-info"
                        
                        html += f"""
                        <tr>
                            <td>{vuln_type}</td>
                            <td>{name}</td>
                            <td>{version}</td>
                            <td class="{severity_class}">{severity}</td>
                        </tr>
"""
                    
                    html += """</table>
"""
                
                html += """</div>
"""
            
            html += """</div>
"""
        
        # إضافة التذييل
        html += f"""
        <div class="footer">
            <p>تم إنشاء هذا التقرير بواسطة أداة SaudiAttacks | المطور: Saudi Linux | البريد الإلكتروني: SaudiLinux7@gmail.com</p>
            <p>تاريخ التقرير: {timestamp}</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html

if __name__ == "__main__":
    # اختبار الوحدة
    import logging
    logger = logging.getLogger("test")
    
    target = "example.com"
    report_gen = ReportGenerator(target, logger=logger, quiet=False, debug=True)
    
    # إضافة نتائج وهمية للاختبار
    report_gen.add_results("info_gathering", {
        "dns_records": {
            "A": ["93.184.216.34"],
            "MX": ["0 ."],
            "NS": ["a.iana-servers.net", "b.iana-servers.net"]
        },
        "whois_data": {
            "domain_name": "EXAMPLE.COM",
            "registrar": "RESERVED-Internet Assigned Numbers Authority",
            "creation_date": "1995-08-14T04:00:00Z",
            "expiration_date": "2021-08-13T04:00:00Z"
        }
    })
    
    report_gen.add_results("port_scanner", {
        "open_ports": [
            {"port": 80, "protocol": "tcp", "service": "http", "version": "Apache httpd 2.4.29", "state": "open"},
            {"port": 443, "protocol": "tcp", "service": "https", "version": "Apache httpd 2.4.29", "state": "open"}
        ],
        "os_detection": {
            "Linux 3.x": 90,
            "Linux 4.x": 85
        }
    })
    
    report_gen.add_results("vulnerability_scanner", {
        "vulnerabilities": [
            {"name": "CVE-2019-0211", "description": "Apache HTTP Server privilege escalation", "severity": "عالية", "details": "Apache HTTP Server 2.4.17 to 2.4.38 vulnerability"},
            {"name": "CVE-2018-1312", "description": "Apache HTTP Server CRAM-MD5 authentication", "severity": "متوسطة", "details": "Apache HTTP Server 2.2.0 to 2.4.29 vulnerability"}
        ]
    })
    
    # إنشاء التقرير
    report_file = report_gen.generate_report()
    print(f"تم إنشاء التقرير في: {report_file}")