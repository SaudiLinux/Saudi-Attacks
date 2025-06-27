#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة فحص المنافذ
"""

import nmap
import json
from colorama import Fore, Style
from tqdm import tqdm
from .utils import print_status, is_valid_ip, is_valid_domain, resolve_host

class PortScanner:
    """
    فئة فحص المنافذ باستخدام Nmap
    """
    def __init__(self, target, logger, quiet=False, debug=False):
        """
        تهيئة الفئة
        """
        self.target = target
        self.logger = logger
        self.quiet = quiet
        self.debug = debug
        try:
            self.nm = nmap.PortScanner()
        except Exception as e:
            self.logger.error(f"خطأ في تهيئة PortScanner: {str(e)}")
            if not self.quiet:
                print_status(f"خطأ في تهيئة PortScanner: {str(e)}", "error")
            self.nm = None
        
        # تحديد نوع الهدف (IP أو اسم مجال)
        if is_valid_ip(target):
            self.target_type = "ip"
            self.ip = target
        elif is_valid_domain(target):
            self.target_type = "domain"
            self.ip = resolve_host(target)
        else:
            self.target_type = "unknown"
            self.ip = None
    
    def scan(self, ports="1-1000", scan_type="-sV"):
        """
        فحص المنافذ باستخدام Nmap
        
        المعلمات:
            ports (str): المنافذ المراد فحصها (مثال: "22,80,443" أو "1-1000")
            scan_type (str): نوع الفحص (مثال: "-sV" لفحص الإصدار، "-sS" لفحص SYN)
        
        الإرجاع:
            dict: نتائج الفحص
        """
        if not self.ip:
            if not self.quiet:
                print_status(f"لا يمكن تحليل الهدف: {self.target}", "error")
            self.logger.error(f"لا يمكن تحليل الهدف: {self.target}")
            return {"error": f"لا يمكن تحليل الهدف: {self.target}"}
        
        if not self.nm:
            error_msg = "لم يتم تهيئة PortScanner بشكل صحيح. تأكد من تثبيت Nmap وإضافته إلى متغير PATH."
            if not self.quiet:
                print_status(error_msg, "error")
            self.logger.error(error_msg)
            return {"error": error_msg}
        
        if not self.quiet:
            print_status(f"بدء فحص المنافذ للهدف: {self.target} ({self.ip})", "info")
            print_status(f"المنافذ: {ports} | نوع الفحص: {scan_type}", "info")
        
        self.logger.info(f"بدء فحص المنافذ للهدف: {self.target} ({self.ip})")
        self.logger.info(f"المنافذ: {ports} | نوع الفحص: {scan_type}")
        
        try:
            # تنفيذ الفحص
            if not self.quiet:
                print_status("جاري الفحص... (قد يستغرق هذا بعض الوقت)", "info")
            
            # تنفيذ فحص Nmap
            self.nm.scan(self.ip, ports, arguments=scan_type)
            
            # تحضير النتائج
            results = {}
            
            if self.ip in self.nm.all_hosts():
                host_data = self.nm[self.ip]
                
                # معلومات المضيف
                results["host"] = {
                    "ip": self.ip,
                    "hostname": ",".join(host_data["hostnames"]) if "hostnames" in host_data else "",
                    "state": host_data["status"]["state"] if "status" in host_data else "unknown"
                }
                
                # معلومات المنافذ
                results["ports"] = []
                
                if "tcp" in host_data:
                    for port, port_data in host_data["tcp"].items():
                        port_info = {
                            "port": port,
                            "protocol": "tcp",
                            "state": port_data["state"],
                            "service": port_data["name"],
                            "product": port_data.get("product", ""),
                            "version": port_data.get("version", ""),
                            "extrainfo": port_data.get("extrainfo", "")
                        }
                        results["ports"].append(port_info)
                
                if "udp" in host_data:
                    for port, port_data in host_data["udp"].items():
                        port_info = {
                            "port": port,
                            "protocol": "udp",
                            "state": port_data["state"],
                            "service": port_data["name"],
                            "product": port_data.get("product", ""),
                            "version": port_data.get("version", ""),
                            "extrainfo": port_data.get("extrainfo", "")
                        }
                        results["ports"].append(port_info)
                
                # ترتيب المنافذ حسب الرقم
                results["ports"] = sorted(results["ports"], key=lambda x: int(x["port"]))
                
                # عرض النتائج
                if not self.quiet:
                    print_status(f"تم العثور على {len(results['ports'])} منفذ مفتوح", "success")
                    
                    for port_info in results["ports"]:
                        port_str = f"{port_info['port']}/{port_info['protocol']}"
                        service_str = f"{port_info['service']}"
                        version_str = f"{port_info['product']} {port_info['version']} {port_info['extrainfo']}".strip()
                        
                        print(f"{Fore.GREEN}[+] {port_str:<10} {service_str:<15} {version_str}{Style.RESET_ALL}")
            else:
                if not self.quiet:
                    print_status(f"لم يتم العثور على منافذ مفتوحة للهدف: {self.target}", "warning")
                
                self.logger.warning(f"لم يتم العثور على منافذ مفتوحة للهدف: {self.target}")
                results = {"error": "لم يتم العثور على منافذ مفتوحة"}
            
            return results
        
        except Exception as e:
            error_msg = f"فشل في فحص المنافذ: {str(e)}"
            
            if not self.quiet:
                print_status(error_msg, "error")
            
            self.logger.error(error_msg)
            return {"error": error_msg}
    
    def scan_common_ports(self):
        """
        فحص المنافذ الشائعة
        """
        common_ports = "21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080"
        return self.scan(ports=common_ports)
    
    def scan_all_ports(self):
        """
        فحص جميع المنافذ
        """
        return self.scan(ports="1-65535")
    
    def scan_web_ports(self):
        """
        فحص منافذ الويب
        """
        web_ports = "80,443,8080,8443,8000,8888"
        return self.scan(ports=web_ports)
    
    def scan_service_detection(self, ports="1-1000"):
        """
        فحص واكتشاف الخدمات
        """
        return self.scan(ports=ports, scan_type="-sV")
    
    def scan_os_detection(self, ports="1-1000"):
        """
        فحص واكتشاف نظام التشغيل
        """
        return self.scan(ports=ports, scan_type="-sV -O")

if __name__ == "__main__":
    # اختبار الوحدة
    import logging
    logger = logging.getLogger("test")
    
    target = "127.0.0.1"  # استخدم عنوان IP محلي للاختبار
    scanner = PortScanner(target, logger, quiet=False, debug=True)
    results = scanner.scan_common_ports()
    
    print(json.dumps(results, indent=4))