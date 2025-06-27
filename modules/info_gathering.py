#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة جمع المعلومات
"""

import socket
import whois
import dns.resolver
import requests
import json
import subprocess
import re
from colorama import Fore, Style
from bs4 import BeautifulSoup
from .utils import print_status, is_valid_ip, is_valid_domain, resolve_host, run_command

class InfoGathering:
    """
    فئة جمع المعلومات عن الهدف
    """
    def __init__(self, target, logger, quiet=False, debug=False):
        """
        تهيئة الفئة
        """
        self.target = target
        self.logger = logger
        self.quiet = quiet
        self.debug = debug
        self.results = {}
        
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
    
    def gather_all(self):
        """
        جمع جميع المعلومات المتاحة عن الهدف
        """
        if not self.quiet:
            print_status(f"بدء جمع المعلومات عن الهدف: {self.target}", "info")
        
        self.logger.info(f"بدء جمع المعلومات عن الهدف: {self.target}")
        
        # جمع معلومات DNS
        self.gather_dns_info()
        
        # جمع معلومات Whois
        self.gather_whois_info()
        
        # جمع معلومات الشبكة
        self.gather_network_info()
        
        # جمع معلومات الويب
        self.gather_web_info()
        
        # جمع معلومات إضافية
        self.gather_additional_info()
        
        if not self.quiet:
            print_status(f"اكتمال جمع المعلومات عن الهدف: {self.target}", "success")
        
        self.logger.info(f"اكتمال جمع المعلومات عن الهدف: {self.target}")
        
        return self.results
    
    def gather_dns_info(self):
        """
        جمع معلومات DNS
        """
        if not self.quiet:
            print_status("جمع معلومات DNS...", "info")
        
        dns_info = {}
        
        if self.target_type == "domain":
            # الحصول على سجلات A
            try:
                a_records = dns.resolver.resolve(self.target, 'A')
                dns_info["a_records"] = [record.to_text() for record in a_records]
                if not self.quiet:
                    print_status(f"سجلات A: {', '.join(dns_info['a_records'])}", "success")
            except Exception as e:
                dns_info["a_records"] = []
                if self.debug:
                    print_status(f"فشل في الحصول على سجلات A: {str(e)}", "error")
            
            # الحصول على سجلات MX
            try:
                mx_records = dns.resolver.resolve(self.target, 'MX')
                dns_info["mx_records"] = [record.to_text() for record in mx_records]
                if not self.quiet:
                    print_status(f"سجلات MX: {', '.join(dns_info['mx_records'])}", "success")
            except Exception as e:
                dns_info["mx_records"] = []
                if self.debug:
                    print_status(f"فشل في الحصول على سجلات MX: {str(e)}", "error")
            
            # الحصول على سجلات NS
            try:
                ns_records = dns.resolver.resolve(self.target, 'NS')
                dns_info["ns_records"] = [record.to_text() for record in ns_records]
                if not self.quiet:
                    print_status(f"سجلات NS: {', '.join(dns_info['ns_records'])}", "success")
            except Exception as e:
                dns_info["ns_records"] = []
                if self.debug:
                    print_status(f"فشل في الحصول على سجلات NS: {str(e)}", "error")
            
            # الحصول على سجلات TXT
            try:
                txt_records = dns.resolver.resolve(self.target, 'TXT')
                dns_info["txt_records"] = [record.to_text() for record in txt_records]
                if not self.quiet:
                    print_status(f"سجلات TXT: {', '.join(dns_info['txt_records'])}", "success")
            except Exception as e:
                dns_info["txt_records"] = []
                if self.debug:
                    print_status(f"فشل في الحصول على سجلات TXT: {str(e)}", "error")
        
        self.results["dns_info"] = dns_info
    
    def gather_whois_info(self):
        """
        جمع معلومات Whois
        """
        if not self.quiet:
            print_status("جمع معلومات Whois...", "info")
        
        whois_info = {}
        
        try:
            if self.target_type == "domain":
                w = whois.whois(self.target)
                whois_info = {
                    "domain_name": w.domain_name,
                    "registrar": w.registrar,
                    "creation_date": w.creation_date,
                    "expiration_date": w.expiration_date,
                    "name_servers": w.name_servers,
                    "status": w.status,
                    "emails": w.emails,
                    "dnssec": w.dnssec,
                    "name": w.name,
                    "org": w.org,
                    "address": w.address,
                    "city": w.city,
                    "state": w.state,
                    "zipcode": w.zipcode,
                    "country": w.country
                }
                
                if not self.quiet:
                    print_status(f"اسم المجال: {whois_info['domain_name']}", "success")
                    print_status(f"المسجل: {whois_info['registrar']}", "success")
                    print_status(f"تاريخ الإنشاء: {whois_info['creation_date']}", "success")
                    print_status(f"تاريخ الانتهاء: {whois_info['expiration_date']}", "success")
            elif self.target_type == "ip":
                # استخدام أمر whois للحصول على معلومات IP
                result = run_command(f"whois {self.target}")
                if result["success"]:
                    whois_info["raw"] = result["stdout"]
                    
                    # استخراج المعلومات المهمة من النتيجة
                    patterns = {
                        "netname": r"NetName:\s+(.+)",
                        "organization": r"Organization:\s+(.+)",
                        "country": r"Country:\s+(.+)",
                        "cidr": r"CIDR:\s+(.+)",
                        "abuse_email": r"Abuse Email:\s+(.+)"
                    }
                    
                    for key, pattern in patterns.items():
                        match = re.search(pattern, result["stdout"])
                        if match:
                            whois_info[key] = match.group(1).strip()
                    
                    if not self.quiet:
                        for key, value in whois_info.items():
                            if key != "raw":
                                print_status(f"{key}: {value}", "success")
        except Exception as e:
            if self.debug:
                print_status(f"فشل في الحصول على معلومات Whois: {str(e)}", "error")
        
        self.results["whois_info"] = whois_info
    
    def gather_network_info(self):
        """
        جمع معلومات الشبكة
        """
        if not self.quiet:
            print_status("جمع معلومات الشبكة...", "info")
        
        network_info = {}
        
        # التحقق من وجود عنوان IP
        if self.ip:
            # الحصول على معلومات الموقع الجغرافي
            try:
                response = requests.get(f"https://ipinfo.io/{self.ip}/json", timeout=5)
                if response.status_code == 200:
                    geo_data = response.json()
                    network_info["geo"] = geo_data
                    
                    if not self.quiet:
                        print_status(f"الموقع الجغرافي: {geo_data.get('city', '')}, {geo_data.get('region', '')}, {geo_data.get('country', '')}", "success")
                        print_status(f"المزود: {geo_data.get('org', '')}", "success")
                        print_status(f"نطاق IP: {geo_data.get('loc', '')}", "success")
            except Exception as e:
                if self.debug:
                    print_status(f"فشل في الحصول على معلومات الموقع الجغرافي: {str(e)}", "error")
            
            # التحقق من وجود الهدف في قوائم RBL
            try:
                rbls = [
                    "zen.spamhaus.org",
                    "bl.spamcop.net",
                    "dnsbl.sorbs.net"
                ]
                
                rbl_results = {}
                
                for rbl in rbls:
                    # عكس عنوان IP
                    ip_parts = self.ip.split('.')
                    ip_parts.reverse()
                    reversed_ip = '.'.join(ip_parts)
                    
                    # التحقق من وجود الهدف في قائمة RBL
                    try:
                        socket.gethostbyname(f"{reversed_ip}.{rbl}")
                        rbl_results[rbl] = True
                        if not self.quiet:
                            print_status(f"الهدف موجود في قائمة {rbl}", "warning")
                    except socket.gaierror:
                        rbl_results[rbl] = False
                
                network_info["rbl"] = rbl_results
            except Exception as e:
                if self.debug:
                    print_status(f"فشل في التحقق من قوائم RBL: {str(e)}", "error")
        
        self.results["network_info"] = network_info
    
    def gather_web_info(self):
        """
        جمع معلومات الويب
        """
        if not self.quiet:
            print_status("جمع معلومات الويب...", "info")
        
        web_info = {}
        
        # التحقق من توفر HTTP و HTTPS
        try:
            http_url = f"http://{self.target}"
            https_url = f"https://{self.target}"
            
            # التحقق من HTTP
            try:
                response = requests.get(http_url, timeout=5, verify=False)
                web_info["http"] = {
                    "available": True,
                    "status_code": response.status_code,
                    "title": self._extract_title(response.text),
                    "server": response.headers.get("Server", "Unknown"),
                    "headers": dict(response.headers)
                }
                
                if not self.quiet:
                    print_status(f"HTTP متاح (كود الحالة: {response.status_code})", "success")
                    print_status(f"عنوان الصفحة: {web_info['http']['title']}", "success")
                    print_status(f"خادم الويب: {web_info['http']['server']}", "success")
            except requests.RequestException:
                web_info["http"] = {"available": False}
                if not self.quiet:
                    print_status("HTTP غير متاح", "warning")
            
            # التحقق من HTTPS
            try:
                response = requests.get(https_url, timeout=5, verify=False)
                web_info["https"] = {
                    "available": True,
                    "status_code": response.status_code,
                    "title": self._extract_title(response.text),
                    "server": response.headers.get("Server", "Unknown"),
                    "headers": dict(response.headers)
                }
                
                if not self.quiet:
                    print_status(f"HTTPS متاح (كود الحالة: {response.status_code})", "success")
                    print_status(f"عنوان الصفحة: {web_info['https']['title']}", "success")
                    print_status(f"خادم الويب: {web_info['https']['server']}", "success")
            except requests.RequestException:
                web_info["https"] = {"available": False}
                if not self.quiet:
                    print_status("HTTPS غير متاح", "warning")
        except Exception as e:
            if self.debug:
                print_status(f"فشل في جمع معلومات الويب: {str(e)}", "error")
        
        self.results["web_info"] = web_info
    
    def gather_additional_info(self):
        """
        جمع معلومات إضافية
        """
        if not self.quiet:
            print_status("جمع معلومات إضافية...", "info")
        
        additional_info = {}
        
        # التحقق من وجود روبوتس
        try:
            if "web_info" in self.results:
                if self.results["web_info"].get("http", {}).get("available", False):
                    robots_url = f"http://{self.target}/robots.txt"
                elif self.results["web_info"].get("https", {}).get("available", False):
                    robots_url = f"https://{self.target}/robots.txt"
                else:
                    robots_url = None
                
                if robots_url:
                    response = requests.get(robots_url, timeout=5, verify=False)
                    if response.status_code == 200:
                        additional_info["robots_txt"] = response.text
                        if not self.quiet:
                            print_status("تم العثور على ملف robots.txt", "success")
                            
                            # استخراج المسارات المحظورة
                            disallowed_paths = re.findall(r"Disallow:\s*(.+)", response.text)
                            if disallowed_paths:
                                print_status(f"المسارات المحظورة: {', '.join(disallowed_paths[:5])}{' وأكثر...' if len(disallowed_paths) > 5 else ''}", "info")
        except Exception as e:
            if self.debug:
                print_status(f"فشل في التحقق من وجود robots.txt: {str(e)}", "error")
        
        # التحقق من وجود sitemap
        try:
            if "web_info" in self.results:
                if self.results["web_info"].get("http", {}).get("available", False):
                    sitemap_url = f"http://{self.target}/sitemap.xml"
                elif self.results["web_info"].get("https", {}).get("available", False):
                    sitemap_url = f"https://{self.target}/sitemap.xml"
                else:
                    sitemap_url = None
                
                if sitemap_url:
                    response = requests.get(sitemap_url, timeout=5, verify=False)
                    if response.status_code == 200:
                        additional_info["sitemap_xml"] = response.text
                        if not self.quiet:
                            print_status("تم العثور على ملف sitemap.xml", "success")
                            
                            # استخراج عدد الروابط
                            urls_count = response.text.count("<url>")
                            if urls_count > 0:
                                print_status(f"عدد الروابط في sitemap: {urls_count}", "info")
        except Exception as e:
            if self.debug:
                print_status(f"فشل في التحقق من وجود sitemap.xml: {str(e)}", "error")
        
        self.results["additional_info"] = additional_info
    
    def _extract_title(self, html):
        """
        استخراج عنوان الصفحة من HTML
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.string if soup.title else "No Title"
            return title.strip()
        except Exception:
            return "Unknown"

if __name__ == "__main__":
    # اختبار الوحدة
    import logging
    logger = logging.getLogger("test")
    
    target = "example.com"
    info_gatherer = InfoGathering(target, logger, quiet=False, debug=True)
    results = info_gatherer.gather_all()
    
    print(json.dumps(results, indent=4, default=str))