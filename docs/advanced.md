# استخدامات متقدمة لأداة SaudiAttacks

يوفر هذا المستند معلومات متقدمة حول استخدام أداة SaudiAttacks، بما في ذلك تخصيص الأداة، تكاملها مع أدوات أخرى، وأفضل الممارسات للاختبار الأمني.

## جدول المحتويات

- [تخصيص الأداة](#تخصيص-الأداة)
- [تكامل مع أدوات أخرى](#تكامل-مع-أدوات-أخرى)
- [استراتيجيات الفحص المتقدمة](#استراتيجيات-الفحص-المتقدمة)
- [أتمتة عمليات الفحص](#أتمتة-عمليات-الفحص)
- [تحليل النتائج المتقدم](#تحليل-النتائج-المتقدم)
- [أفضل الممارسات](#أفضل-الممارسات)

## تخصيص الأداة

### إضافة وحدات مخصصة

يمكنك توسيع وظائف الأداة عن طريق إضافة وحدات مخصصة. لإنشاء وحدة جديدة، اتبع الخطوات التالية:

1. أنشئ ملفًا جديدًا في مجلد `modules/` باسم مناسب، مثل `custom_scanner.py`
2. قم بتنفيذ الفئة الرئيسية للوحدة مع طريقة `scan()` على الأقل
3. قم بتسجيل الوحدة في الملف الرئيسي `saudi_attacks.py`

مثال على وحدة مخصصة:

```python
# modules/custom_scanner.py
class CustomScanner:
    def __init__(self, target, options=None):
        self.target = target
        self.options = options or {}
        self.results = {}
    
    def scan(self):
        # تنفيذ منطق الفحص المخصص هنا
        print(f"[+] بدء الفحص المخصص على الهدف {self.target}")
        
        # مثال على منطق الفحص
        self.results = {
            "custom_scan_results": {
                "finding_1": "نتيجة مخصصة 1",
                "finding_2": "نتيجة مخصصة 2"
            }
        }
        
        return self.results
```

ثم قم بتسجيل الوحدة في الملف الرئيسي:

```python
# saudi_attacks.py (إضافة استيراد)
from modules.custom_scanner import CustomScanner

# في فئة SaudiAttacks، أضف الوحدة إلى طريقة run()
if self.scan_type == "custom" or self.scan_type == "all":
    custom_scanner = CustomScanner(self.target, options={
        "custom_option": self.custom_option
    })
    custom_results = custom_scanner.scan()
    self.results.update(custom_results)
```

### تخصيص التقارير

يمكنك تخصيص تنسيق التقارير عن طريق تعديل قوالب HTML أو إضافة تنسيقات تقارير جديدة:

1. قم بتعديل قالب HTML الموجود في `templates/report_template.html`
2. أو قم بإنشاء تنسيق تقرير جديد عن طريق تعديل فئة `ReportGenerator`

مثال على إضافة تنسيق تقرير جديد (XML):

```python
# modules/report_generator.py (إضافة طريقة جديدة)
def generate_xml_report(self):
    xml_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    xml_content += "<scan_results>\n"
    xml_content += f"  <target>{self.target}</target>\n"
    xml_content += f"  <scan_date>{self.scan_date}</scan_date>\n"
    
    # إضافة نتائج الفحص
    xml_content += "  <findings>\n"
    for module, results in self.results.items():
        xml_content += f"    <module name=\"{module}\">\n"
        for key, value in results.items():
            if isinstance(value, dict):
                xml_content += f"      <{key}>\n"
                for sub_key, sub_value in value.items():
                    xml_content += f"        <{sub_key}>{sub_value}</{sub_key}>\n"
                xml_content += f"      </{key}>\n"
            else:
                xml_content += f"      <{key}>{value}</{key}>\n"
        xml_content += "    </module>\n"
    xml_content += "  </findings>\n"
    
    xml_content += "</scan_results>"
    
    return xml_content

# ثم أضف الحالة في طريقة generate_report()
if self.format.lower() == "xml":
    report_content = self.generate_xml_report()
```

### تخصيص خيارات الفحص

يمكنك إضافة خيارات فحص جديدة عن طريق تعديل محلل الأوامر في الملف الرئيسي:

```python
# saudi_attacks.py (إضافة خيارات جديدة)
parser.add_argument("--custom-option", help="خيار مخصص للفحص", default=None)
parser.add_argument("--custom-scan", action="store_true", help="تنفيذ الفحص المخصص")

# ثم استخدم الخيارات في الكود
self.custom_option = args.custom_option
if args.custom_scan:
    self.scan_type = "custom"
```

## تكامل مع أدوات أخرى

### تكامل مع Metasploit Framework

يمكنك تكامل SaudiAttacks مع Metasploit Framework لاستغلال الثغرات المكتشفة تلقائيًا:

```python
# modules/metasploit_integration.py
import subprocess
import time

class MetasploitIntegration:
    def __init__(self, target, vulnerabilities):
        self.target = target
        self.vulnerabilities = vulnerabilities
        self.results = {}
    
    def exploit(self):
        print(f"[+] بدء استغلال الثغرات باستخدام Metasploit على الهدف {self.target}")
        
        for vuln in self.vulnerabilities:
            if vuln.get("cve_id") and vuln.get("port"):
                # البحث عن وحدة Metasploit المناسبة
                search_cmd = f"msfconsole -q -x 'search {vuln["cve_id"]}; exit'"
                search_output = subprocess.check_output(search_cmd, shell=True).decode()
                
                # استخراج اسم وحدة الاستغلال
                # هذا مثال مبسط، قد تحتاج إلى تحسينه للاستخدام الفعلي
                exploit_modules = []
                for line in search_output.split("\n"):
                    if "exploit/" in line:
                        module_name = line.split()[0]
                        exploit_modules.append(module_name)
                
                if exploit_modules:
                    # تنفيذ الاستغلال باستخدام الوحدة الأولى المتاحة
                    exploit_cmd = (
                        f"msfconsole -q -x 'use {exploit_modules[0]}; "
                        f"set RHOSTS {self.target}; "
                        f"set RPORT {vuln["port"]}; "
                        f"exploit -j; "
                        f"sleep 10; "
                        f"sessions -l; "
                        f"exit'"
                    )
                    
                    try:
                        exploit_output = subprocess.check_output(exploit_cmd, shell=True).decode()
                        self.results[vuln["cve_id"]] = {
                            "module": exploit_modules[0],
                            "output": exploit_output,
                            "success": "Meterpreter session" in exploit_output
                        }
                    except subprocess.CalledProcessError as e:
                        self.results[vuln["cve_id"]] = {
                            "module": exploit_modules[0],
                            "error": str(e),
                            "success": False
                        }
        
        return self.results
```

### تكامل مع OWASP ZAP

يمكنك تكامل SaudiAttacks مع OWASP ZAP لفحص تطبيقات الويب بشكل أكثر تفصيلاً:

```python
# modules/zap_integration.py
from zapv2 import ZAPv2
import time

class ZAPIntegration:
    def __init__(self, target, api_key=None, proxy="localhost:8080"):
        self.target = target
        self.api_key = api_key
        self.proxy = proxy
        self.zap = ZAPv2(apikey=api_key, proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'})
        self.results = {}
    
    def scan(self):
        print(f"[+] بدء فحص تطبيق الويب باستخدام OWASP ZAP على الهدف {self.target}")
        
        # بدء فحص نشط
        self.zap.urlopen(self.target)
        # انتظار حتى يتم تحميل الصفحة
        time.sleep(2)
        
        # فحص سلبي
        print("[+] بدء الفحص السلبي...")
        self.zap.spider.scan(self.target)
        
        # انتظار حتى ينتهي الفحص السلبي
        time.sleep(2)
        while int(self.zap.spider.status()) < 100:
            print(f"[*] تقدم الفحص السلبي: {self.zap.spider.status()}%")
            time.sleep(2)
        
        # فحص نشط
        print("[+] بدء الفحص النشط...")
        scan_id = self.zap.ascan.scan(self.target)
        
        # انتظار حتى ينتهي الفحص النشط
        while int(self.zap.ascan.status(scan_id)) < 100:
            print(f"[*] تقدم الفحص النشط: {self.zap.ascan.status(scan_id)}%")
            time.sleep(5)
        
        # الحصول على التنبيهات
        alerts = self.zap.core.alerts()
        
        # تنظيم النتائج
        self.results = {
            "high_alerts": [],
            "medium_alerts": [],
            "low_alerts": [],
            "info_alerts": []
        }
        
        for alert in alerts:
            alert_detail = {
                "name": alert.get("name"),
                "url": alert.get("url"),
                "risk": alert.get("risk"),
                "confidence": alert.get("confidence"),
                "description": alert.get("description"),
                "solution": alert.get("solution")
            }
            
            if alert.get("risk") == "High":
                self.results["high_alerts"].append(alert_detail)
            elif alert.get("risk") == "Medium":
                self.results["medium_alerts"].append(alert_detail)
            elif alert.get("risk") == "Low":
                self.results["low_alerts"].append(alert_detail)
            else:
                self.results["info_alerts"].append(alert_detail)
        
        return self.results
```

### تكامل مع Elasticsearch للتخزين والتحليل

يمكنك تخزين نتائج الفحص في Elasticsearch للتحليل المتقدم:

```python
# modules/elasticsearch_integration.py
from elasticsearch import Elasticsearch
import datetime
import json
import uuid

class ElasticsearchIntegration:
    def __init__(self, es_host="localhost", es_port=9200, index_prefix="saudi_attacks"):
        self.es = Elasticsearch([{"host": es_host, "port": es_port}])
        self.index_prefix = index_prefix
        self.index_name = f"{index_prefix}-{datetime.datetime.now().strftime('%Y.%m.%d')}"
    
    def store_results(self, target, results):
        print(f"[+] تخزين نتائج الفحص في Elasticsearch للهدف {target}")
        
        # إنشاء الفهرس إذا لم يكن موجودًا
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name)
        
        # تحضير البيانات للتخزين
        document = {
            "target": target,
            "timestamp": datetime.datetime.now().isoformat(),
            "scan_id": str(uuid.uuid4()),
            "results": results
        }
        
        # تخزين البيانات
        response = self.es.index(index=self.index_name, body=document)
        
        return response
    
    def search_results(self, target=None, time_range=None, query=None):
        # بناء استعلام البحث
        search_query = {"query": {"bool": {"must": []}}}
        
        if target:
            search_query["query"]["bool"]["must"].append({"match": {"target": target}})
        
        if time_range:
            search_query["query"]["bool"]["must"].append({
                "range": {
                    "timestamp": {
                        "gte": time_range["from"],
                        "lte": time_range["to"]
                    }
                }
            })
        
        if query:
            search_query["query"]["bool"]["must"].append({"query_string": {"query": query}})
        
        # تنفيذ البحث
        response = self.es.search(index=f"{self.index_prefix}-*", body=search_query)
        
        return response
```

## استراتيجيات الفحص المتقدمة

### فحص متعدد المراحل

يمكنك تنفيذ استراتيجية فحص متعددة المراحل لتحسين الدقة وتقليل الإيجابيات الكاذبة:

1. **المرحلة الأولى**: فحص سريع للاكتشاف الأولي
2. **المرحلة الثانية**: فحص مستهدف للمنافذ والخدمات المكتشفة
3. **المرحلة الثالثة**: فحص عميق للثغرات المحتملة
4. **المرحلة الرابعة**: التحقق من الثغرات المكتشفة

مثال على تنفيذ استراتيجية الفحص متعددة المراحل:

```python
# استراتيجية فحص متعددة المراحل
def multi_stage_scan(target):
    results = {}
    
    # المرحلة الأولى: فحص سريع
    print("[+] المرحلة الأولى: فحص سريع للاكتشاف الأولي")
    scanner = SaudiAttacks(target=target, scan_type="port", ports="common", fast=True)
    stage1_results = scanner.run()
    results["stage1"] = stage1_results
    
    # المرحلة الثانية: فحص مستهدف
    print("[+] المرحلة الثانية: فحص مستهدف للمنافذ والخدمات المكتشفة")
    open_ports = []
    if "port_scanner" in stage1_results and "open_ports" in stage1_results["port_scanner"]:
        open_ports = stage1_results["port_scanner"]["open_ports"]
    
    if open_ports:
        ports_str = ",".join(map(str, open_ports))
        scanner = SaudiAttacks(target=target, scan_type="port", ports=ports_str, fast=False)
        stage2_results = scanner.run()
        results["stage2"] = stage2_results
    
    # المرحلة الثالثة: فحص عميق للثغرات
    print("[+] المرحلة الثالثة: فحص عميق للثغرات المحتملة")
    scanner = SaudiAttacks(target=target, scan_type="vuln", ports=ports_str)
    stage3_results = scanner.run()
    results["stage3"] = stage3_results
    
    # المرحلة الرابعة: التحقق من الثغرات المكتشفة
    print("[+] المرحلة الرابعة: التحقق من الثغرات المكتشفة")
    vulnerabilities = []
    if "vulnerability_scanner" in stage3_results and "vulnerabilities" in stage3_results["vulnerability_scanner"]:
        vulnerabilities = stage3_results["vulnerability_scanner"]["vulnerabilities"]
    
    verified_vulns = []
    for vuln in vulnerabilities:
        # تنفيذ التحقق من الثغرة
        # هذا مثال مبسط، قد تحتاج إلى تنفيذ منطق تحقق أكثر تعقيدًا
        if verify_vulnerability(target, vuln):
            verified_vulns.append(vuln)
    
    results["stage4"] = {"verified_vulnerabilities": verified_vulns}
    
    return results

def verify_vulnerability(target, vulnerability):
    # تنفيذ منطق التحقق من الثغرة
    # هذا مثال مبسط، قد تحتاج إلى تنفيذ منطق تحقق أكثر تعقيدًا
    print(f"[*] التحقق من الثغرة: {vulnerability.get('name')} على الهدف {target}")
    
    # في هذا المثال، نفترض أن جميع الثغرات صحيحة
    # في التنفيذ الفعلي، يجب تنفيذ اختبارات محددة للتحقق من كل ثغرة
    return True
```

### فحص مستهدف للقطاعات

يمكنك تخصيص استراتيجيات الفحص بناءً على القطاع أو نوع التطبيق:

```python
def scan_by_sector(target, sector):
    if sector == "banking":
        return scan_banking_target(target)
    elif sector == "healthcare":
        return scan_healthcare_target(target)
    elif sector == "ecommerce":
        return scan_ecommerce_target(target)
    else:
        # فحص عام
        scanner = SaudiAttacks(target=target, scan_type="all")
        return scanner.run()

def scan_banking_target(target):
    # استراتيجية فحص مخصصة للبنوك
    results = {}
    
    # فحص SSL/TLS بشكل مكثف
    print(f"[+] فحص SSL/TLS للهدف {target}")
    # تنفيذ فحص SSL/TLS مكثف
    
    # فحص تطبيقات الويب مع التركيز على ثغرات OWASP Top 10
    print(f"[+] فحص تطبيقات الويب للهدف {target}")
    # تنفيذ فحص تطبيقات الويب مع التركيز على OWASP Top 10
    
    # فحص API المصرفية
    print(f"[+] فحص API المصرفية للهدف {target}")
    # تنفيذ فحص API المصرفية
    
    return results

# يمكن تنفيذ دوال مماثلة للقطاعات الأخرى
```

## أتمتة عمليات الفحص

### جدولة الفحوصات الدورية

يمكنك إعداد نظام لجدولة الفحوصات الدورية باستخدام cron (على Linux) أو Task Scheduler (على Windows):

```python
# scheduled_scan.py
import argparse
import datetime
import json
import os
from saudi_attacks import SaudiAttacks

def main():
    parser = argparse.ArgumentParser(description="جدولة فحوصات دورية باستخدام SaudiAttacks")
    parser.add_argument("--targets-file", required=True, help="ملف يحتوي على قائمة الأهداف")
    parser.add_argument("--output-dir", required=True, help="مجلد لحفظ تقارير الفحص")
    parser.add_argument("--scan-type", default="all", help="نوع الفحص")
    args = parser.parse_args()
    
    # قراءة قائمة الأهداف
    with open(args.targets_file, "r") as f:
        targets = [line.strip() for line in f if line.strip()]
    
    # إنشاء مجلد للتقارير إذا لم يكن موجودًا
    os.makedirs(args.output_dir, exist_ok=True)
    
    # تاريخ ووقت الفحص
    scan_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # فحص كل هدف
    for target in targets:
        print(f"[+] بدء فحص الهدف: {target}")
        
        # إنشاء اسم ملف التقرير
        report_file = os.path.join(
            args.output_dir,
            f"{target.replace('.', '_').replace(':', '_')}_{scan_date}.html"
        )
        
        # تنفيذ الفحص
        scanner = SaudiAttacks(
            target=target,
            scan_type=args.scan_type,
            output=report_file,
            format="html"
        )
        
        results = scanner.run()
        
        # حفظ النتائج الخام بتنسيق JSON أيضًا
        json_file = report_file.replace(".html", ".json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        
        print(f"[+] اكتمل فحص الهدف: {target}")
        print(f"[+] تم حفظ التقرير في: {report_file}")
        print(f"[+] تم حفظ النتائج الخام في: {json_file}")

if __name__ == "__main__":
    main()
```

يمكنك جدولة هذا السكريبت للتشغيل بشكل دوري:

**على Linux (باستخدام cron):**

```bash
# تشغيل الفحص كل يوم في الساعة 2 صباحًا
0 2 * * * /usr/bin/python3 /path/to/scheduled_scan.py --targets-file /path/to/targets.txt --output-dir /path/to/reports --scan-type all
```

**على Windows (باستخدام Task Scheduler):**

```powershell
# إنشاء مهمة مجدولة
schtasks /create /tn "SaudiAttacks_Daily_Scan" /tr "python C:\path\to\scheduled_scan.py --targets-file C:\path\to\targets.txt --output-dir C:\path\to\reports --scan-type all" /sc daily /st 02:00
```

### تكامل مع أنظمة CI/CD

يمكنك دمج SaudiAttacks في خطوط أنابيب CI/CD لفحص التطبيقات قبل النشر:

**مثال على ملف GitHub Actions:**

```yaml
# .github/workflows/security_scan.yml
name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  security_scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install saudi-attacks
    
    - name: Run security scan
      run: |
        # بدء خادم التطبيق المحلي للفحص
        python -m http.server 8000 &
        SERVER_PID=$!
        
        # انتظار بدء الخادم
        sleep 5
        
        # تنفيذ الفحص
        python -m saudi_attacks localhost:8000 --scan-type web --output scan_report.html
        
        # إيقاف الخادم
        kill $SERVER_PID
    
    - name: Upload scan report
      uses: actions/upload-artifact@v2
      with:
        name: security-scan-report
        path: scan_report.html
```

## تحليل النتائج المتقدم

### تحليل الاتجاهات

يمكنك تحليل نتائج الفحوصات المتعددة لتحديد الاتجاهات والتغييرات في الوضع الأمني:

```python
# trend_analysis.py
import argparse
import json
import os
import glob
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def load_scan_results(results_dir):
    # البحث عن جميع ملفات JSON في مجلد النتائج
    json_files = glob.glob(os.path.join(results_dir, "*.json"))
    
    all_results = []
    for json_file in json_files:
        try:
            # استخراج تاريخ الفحص من اسم الملف
            filename = os.path.basename(json_file)
            date_str = filename.split("_")[-2] + "_" + filename.split("_")[-1].replace(".json", "")
            scan_date = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
            
            # قراءة نتائج الفحص
            with open(json_file, "r", encoding="utf-8") as f:
                results = json.load(f)
            
            # إضافة تاريخ الفحص والهدف إلى النتائج
            target = filename.split("_")[0].replace("_", ".")
            results["scan_date"] = scan_date.isoformat()
            results["target"] = target
            
            all_results.append(results)
        except Exception as e:
            print(f"[!] خطأ في قراءة الملف {json_file}: {str(e)}")
    
    return all_results

def analyze_vulnerability_trends(all_results):
    # تحضير البيانات للتحليل
    trend_data = []
    
    for result in all_results:
        scan_date = result.get("scan_date")
        target = result.get("target")
        
        # استخراج عدد الثغرات حسب مستوى الخطورة
        high_vulns = 0
        medium_vulns = 0
        low_vulns = 0
        
        if "vulnerability_scanner" in result and "vulnerabilities" in result["vulnerability_scanner"]:
            for vuln in result["vulnerability_scanner"]["vulnerabilities"]:
                severity = vuln.get("severity", "").lower()
                if severity == "high":
                    high_vulns += 1
                elif severity == "medium":
                    medium_vulns += 1
                elif severity == "low":
                    low_vulns += 1
        
        trend_data.append({
            "scan_date": scan_date,
            "target": target,
            "high_vulnerabilities": high_vulns,
            "medium_vulnerabilities": medium_vulns,
            "low_vulnerabilities": low_vulns,
            "total_vulnerabilities": high_vulns + medium_vulns + low_vulns
        })
    
    # تحويل البيانات إلى DataFrame
    df = pd.DataFrame(trend_data)
    df["scan_date"] = pd.to_datetime(df["scan_date"])
    df = df.sort_values("scan_date")
    
    return df

def plot_vulnerability_trends(df, output_file):
    # إنشاء رسم بياني للاتجاهات
    plt.figure(figsize=(12, 8))
    
    for target in df["target"].unique():
        target_df = df[df["target"] == target]
        plt.plot(
            target_df["scan_date"],
            target_df["total_vulnerabilities"],
            marker="o",
            label=f"{target} (Total)"
        )
        plt.plot(
            target_df["scan_date"],
            target_df["high_vulnerabilities"],
            marker="^",
            linestyle="--",
            label=f"{target} (High)"
        )
    
    plt.title("Vulnerability Trends Over Time")
    plt.xlabel("Scan Date")
    plt.ylabel("Number of Vulnerabilities")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # حفظ الرسم البياني
    plt.savefig(output_file)
    print(f"[+] تم حفظ الرسم البياني في: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="تحليل اتجاهات الثغرات من نتائج فحوصات SaudiAttacks")
    parser.add_argument("--results-dir", required=True, help="مجلد يحتوي على ملفات نتائج الفحص بتنسيق JSON")
    parser.add_argument("--output", default="vulnerability_trends.png", help="ملف الرسم البياني الناتج")
    args = parser.parse_args()
    
    # تحميل نتائج الفحص
    all_results = load_scan_results(args.results_dir)
    print(f"[+] تم تحميل {len(all_results)} نتيجة فحص")
    
    # تحليل اتجاهات الثغرات
    trend_df = analyze_vulnerability_trends(all_results)
    
    # رسم اتجاهات الثغرات
    plot_vulnerability_trends(trend_df, args.output)

if __name__ == "__main__":
    main()
```

### مقارنة النتائج

يمكنك مقارنة نتائج الفحوصات لتحديد الثغرات الجديدة أو التي تم إصلاحها:

```python
# compare_scans.py
import argparse
import json
import os

def load_scan_result(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_vulnerabilities(scan_result):
    vulnerabilities = []
    
    if "vulnerability_scanner" in scan_result and "vulnerabilities" in scan_result["vulnerability_scanner"]:
        for vuln in scan_result["vulnerability_scanner"]["vulnerabilities"]:
            # إنشاء معرف فريد للثغرة
            vuln_id = f"{vuln.get('name', '')}-{vuln.get('cve_id', '')}-{vuln.get('port', '')}"
            vulnerabilities.append({
                "id": vuln_id,
                "details": vuln
            })
    
    return vulnerabilities

def compare_vulnerabilities(old_vulns, new_vulns):
    old_vuln_ids = {vuln["id"] for vuln in old_vulns}
    new_vuln_ids = {vuln["id"] for vuln in new_vulns}
    
    # الثغرات التي تم إصلاحها
    fixed_vulns = old_vuln_ids - new_vuln_ids
    fixed = [vuln for vuln in old_vulns if vuln["id"] in fixed_vulns]
    
    # الثغرات الجديدة
    new_vuln_ids = new_vuln_ids - old_vuln_ids
    new = [vuln for vuln in new_vulns if vuln["id"] in new_vuln_ids]
    
    # الثغرات المستمرة
    persistent_vuln_ids = old_vuln_ids.intersection(new_vuln_ids)
    persistent = [vuln for vuln in new_vulns if vuln["id"] in persistent_vuln_ids]
    
    return {
        "fixed": fixed,
        "new": new,
        "persistent": persistent
    }

def main():
    parser = argparse.ArgumentParser(description="مقارنة نتائج فحوصات SaudiAttacks")
    parser.add_argument("--old-scan", required=True, help="ملف نتائج الفحص القديم بتنسيق JSON")
    parser.add_argument("--new-scan", required=True, help="ملف نتائج الفحص الجديد بتنسيق JSON")
    parser.add_argument("--output", help="ملف لحفظ نتائج المقارنة بتنسيق JSON")
    args = parser.parse_args()
    
    # تحميل نتائج الفحص
    old_result = load_scan_result(args.old_scan)
    new_result = load_scan_result(args.new_scan)
    
    # استخراج الثغرات
    old_vulns = extract_vulnerabilities(old_result)
    new_vulns = extract_vulnerabilities(new_result)
    
    # مقارنة الثغرات
    comparison = compare_vulnerabilities(old_vulns, new_vulns)
    
    # طباعة ملخص المقارنة
    print(f"[+] ملخص المقارنة:")
    print(f"    - الثغرات التي تم إصلاحها: {len(comparison['fixed'])}")
    print(f"    - الثغرات الجديدة: {len(comparison['new'])}")
    print(f"    - الثغرات المستمرة: {len(comparison['persistent'])}")
    
    # حفظ نتائج المقارنة
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(comparison, f, ensure_ascii=False, indent=4)
        print(f"[+] تم حفظ نتائج المقارنة في: {args.output}")
    
    # طباعة تفاصيل الثغرات الجديدة
    if comparison["new"]:
        print("\n[+] الثغرات الجديدة:")
        for vuln in comparison["new"]:
            details = vuln["details"]
            print(f"    - {details.get('name', 'N/A')} (CVE: {details.get('cve_id', 'N/A')})")
            print(f"      الخطورة: {details.get('severity', 'N/A')}")
            print(f"      المنفذ: {details.get('port', 'N/A')}")
            print(f"      الوصف: {details.get('description', 'N/A')}")
            print()

if __name__ == "__main__":
    main()
```

## أفضل الممارسات

### تحسين أداء الفحص

1. **استخدام الفحص المتوازي**: قم بتنفيذ عمليات الفحص بشكل متوازٍ لتحسين الأداء

```python
# تنفيذ الفحص المتوازي
from concurrent.futures import ThreadPoolExecutor

def parallel_scan(targets, scan_type="all", max_workers=5):
    results = {}
    
    def scan_target(target):
        print(f"[+] بدء فحص الهدف: {target}")
        scanner = SaudiAttacks(target=target, scan_type=scan_type)
        return {target: scanner.run()}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scan_target, target) for target in targets]
        for future in futures:
            result = future.result()
            results.update(result)
    
    return results
```

2. **تقسيم الفحص**: قسّم الفحوصات الكبيرة إلى أجزاء أصغر

```python
# تقسيم نطاق IP إلى أجزاء أصغر
import ipaddress

def split_ip_range(ip_range, chunk_size=16):
    network = ipaddress.ip_network(ip_range)
    all_hosts = list(network.hosts())
    
    # تقسيم القائمة إلى أجزاء
    chunks = []
    for i in range(0, len(all_hosts), chunk_size):
        chunks.append(all_hosts[i:i + chunk_size])
    
    return chunks

def scan_ip_range_in_chunks(ip_range, scan_type="port", chunk_size=16, max_workers=5):
    chunks = split_ip_range(ip_range, chunk_size)
    all_results = {}
    
    for i, chunk in enumerate(chunks):
        print(f"[+] فحص الجزء {i+1}/{len(chunks)} ({len(chunk)} هدف)")
        chunk_targets = [str(ip) for ip in chunk]
        chunk_results = parallel_scan(chunk_targets, scan_type, max_workers)
        all_results.update(chunk_results)
    
    return all_results
```

### تقليل الإيجابيات الكاذبة

1. **التحقق من الثغرات**: قم بالتحقق من الثغرات المكتشفة للتأكد من صحتها

```python
# التحقق من الثغرات المكتشفة
def verify_vulnerabilities(target, vulnerabilities):
    verified_vulns = []
    false_positives = []
    
    for vuln in vulnerabilities:
        if verify_vulnerability(target, vuln):
            verified_vulns.append(vuln)
        else:
            false_positives.append(vuln)
    
    return {
        "verified": verified_vulns,
        "false_positives": false_positives
    }
```

2. **ضبط حساسية الفحص**: قم بضبط حساسية الفحص بناءً على احتياجاتك

```python
# ضبط حساسية الفحص
class CustomVulnerabilityScanner:
    def __init__(self, target, sensitivity="medium"):
        self.target = target
        self.sensitivity = sensitivity
        self.results = {}
    
    def scan(self):
        # تنفيذ الفحص بناءً على مستوى الحساسية
        if self.sensitivity == "high":
            # فحص شامل مع احتمال وجود إيجابيات كاذبة
            pass
        elif self.sensitivity == "medium":
            # توازن بين الشمولية والدقة
            pass
        elif self.sensitivity == "low":
            # فحص محافظ مع تقليل الإيجابيات الكاذبة
            pass
        
        return self.results
```

### الفحص الآمن

1. **تقليل التأثير**: قم بتقليل تأثير الفحص على الأنظمة المستهدفة

```python
# تقليل تأثير الفحص
def low_impact_scan(target):
    # فحص بطيء مع فترات انتظار بين الطلبات
    scanner = SaudiAttacks(
        target=target,
        scan_type="all",
        timeout=30,  # زيادة مهلة الانتظار
        threads=1,   # تقليل عدد المسارات المتوازية
        delay=2      # إضافة تأخير بين الطلبات
    )
    
    return scanner.run()
```

2. **تجنب الفحوصات الضارة**: تجنب الفحوصات التي قد تسبب ضررًا للأنظمة المستهدفة

```python
# تجنب الفحوصات الضارة
def safe_scan(target, avoid_dos=True, avoid_brute_force=True):
    scan_options = {
        "target": target,
        "scan_type": "all"
    }
    
    if avoid_dos:
        scan_options["avoid_dos_modules"] = True
    
    if avoid_brute_force:
        scan_options["avoid_brute_force"] = True
    
    scanner = SaudiAttacks(**scan_options)
    return scanner.run()
```

### توثيق الفحوصات

1. **سجل الفحوصات**: احتفظ بسجل مفصل لجميع الفحوصات التي تم إجراؤها

```python
# سجل الفحوصات
import logging
import datetime

def setup_logging(log_file=None):
    if log_file is None:
        log_file = f"saudi_attacks_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # إضافة معالج للطباعة على وحدة التحكم
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logging.getLogger().addHandler(console_handler)

def log_scan(target, scan_type, results):
    logging.info(f"بدء فحص الهدف: {target} (نوع الفحص: {scan_type})")
    
    # تسجيل نتائج الفحص
    if "port_scanner" in results:
        open_ports = results["port_scanner"].get("open_ports", [])
        logging.info(f"تم اكتشاف {len(open_ports)} منفذ مفتوح")
        for port in open_ports:
            service = results["port_scanner"].get("services", {}).get(port, "غير معروف")
            logging.info(f"المنفذ {port}: {service}")
    
    if "vulnerability_scanner" in results:
        vulns = results["vulnerability_scanner"].get("vulnerabilities", [])
        logging.info(f"تم اكتشاف {len(vulns)} ثغرة")
        for vuln in vulns:
            logging.info(f"الثغرة: {vuln.get('name')} (الخطورة: {vuln.get('severity')})")
    
    logging.info(f"اكتمل فحص الهدف: {target}")
```

2. **الحفاظ على سجل التغييرات**: احتفظ بسجل للتغييرات في الوضع الأمني

```python
# سجل التغييرات في الوضع الأمني
def track_security_changes(target, old_scan_file, new_scan_file, output_file=None):
    # تحميل نتائج الفحص
    with open(old_scan_file, "r", encoding="utf-8") as f:
        old_results = json.load(f)
    
    with open(new_scan_file, "r", encoding="utf-8") as f:
        new_results = json.load(f)
    
    # استخراج المعلومات الأمنية
    old_security_info = extract_security_info(old_results)
    new_security_info = extract_security_info(new_results)
    
    # مقارنة المعلومات الأمنية
    changes = compare_security_info(old_security_info, new_security_info)
    
    # حفظ التغييرات
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(changes, f, ensure_ascii=False, indent=4)
    
    return changes

def extract_security_info(results):
    # استخراج المعلومات الأمنية من نتائج الفحص
    security_info = {
        "open_ports": [],
        "services": {},
        "vulnerabilities": [],
        "web_info": {},
        "cms_info": {}
    }
    
    # استخراج معلومات المنافذ
    if "port_scanner" in results:
        security_info["open_ports"] = results["port_scanner"].get("open_ports", [])
        security_info["services"] = results["port_scanner"].get("services", {})
    
    # استخراج معلومات الثغرات
    if "vulnerability_scanner" in results:
        security_info["vulnerabilities"] = results["vulnerability_scanner"].get("vulnerabilities", [])
    
    # استخراج معلومات الويب
    if "web_scanner" in results:
        security_info["web_info"] = results["web_scanner"]
    
    # استخراج معلومات أنظمة إدارة المحتوى
    if "cms_scanner" in results:
        security_info["cms_info"] = results["cms_scanner"]
    
    return security_info

def compare_security_info(old_info, new_info):
    changes = {
        "ports": {
            "added": [],
            "removed": []
        },
        "services": {
            "added": {},
            "changed": {},
            "removed": {}
        },
        "vulnerabilities": {
            "added": [],
            "removed": []
        }
    }
    
    # مقارنة المنافذ
    old_ports = set(old_info["open_ports"])
    new_ports = set(new_info["open_ports"])
    changes["ports"]["added"] = list(new_ports - old_ports)
    changes["ports"]["removed"] = list(old_ports - new_ports)
    
    # مقارنة الخدمات
    for port in new_info["services"]:
        if port not in old_info["services"]:
            changes["services"]["added"][port] = new_info["services"][port]
        elif old_info["services"][port] != new_info["services"][port]:
            changes["services"]["changed"][port] = {
                "old": old_info["services"][port],
                "new": new_info["services"][port]
            }
    
    for port in old_info["services"]:
        if port not in new_info["services"]:
            changes["services"]["removed"][port] = old_info["services"][port]
    
    # مقارنة الثغرات (مبسطة، قد تحتاج إلى تحسين للاستخدام الفعلي)
    old_vuln_ids = {f"{v.get('name')}-{v.get('cve_id')}" for v in old_info["vulnerabilities"]}
    new_vuln_ids = {f"{v.get('name')}-{v.get('cve_id')}" for v in new_info["vulnerabilities"]}
    
    for vuln in new_info["vulnerabilities"]:
        vuln_id = f"{vuln.get('name')}-{vuln.get('cve_id')}"
        if vuln_id not in old_vuln_ids:
            changes["vulnerabilities"]["added"].append(vuln)
    
    for vuln in old_info["vulnerabilities"]:
        vuln_id = f"{vuln.get('name')}-{vuln.get('cve_id')}"
        if vuln_id not in new_vuln_ids:
            changes["vulnerabilities"]["removed"].append(vuln)
    
    return changes
```

## خاتمة

توفر هذه الوثيقة معلومات متقدمة حول استخدام أداة SaudiAttacks، بما في ذلك تخصيص الأداة، تكاملها مع أدوات أخرى، واستراتيجيات الفحص المتقدمة. يمكنك استخدام هذه المعلومات لتحسين عمليات الفحص الأمني وتحقيق أقصى استفادة من الأداة.

للمزيد من المعلومات، راجع الوثائق الأخرى المتاحة في مجلد `docs/` والمصادر المذكورة في [دليل التطوير](development.md).