#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة فحص خادم الويب وتطبيقات الويب
"""

import json
import requests
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from colorama import Fore, Style
from .utils import print_status, is_valid_ip, is_valid_domain, resolve_host, run_command

class WebScanner:
    """
    فئة فحص خادم الويب وتطبيقات الويب
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
            self.base_url = f"http://{target}"
        elif is_valid_domain(target):
            self.target_type = "domain"
            self.ip = resolve_host(target)
            self.base_url = f"http://{target}"
        else:
            self.target_type = "unknown"
            self.ip = None
            self.base_url = None
        
        # تعطيل تحذيرات SSL
        requests.packages.urllib3.disable_warnings()
    
    def scan(self):
        """
        فحص خادم الويب وتطبيقات الويب
        """
        if not self.ip or not self.base_url:
            if not self.quiet:
                print_status(f"لا يمكن تحليل الهدف: {self.target}", "error")
            self.logger.error(f"لا يمكن تحليل الهدف: {self.target}")
            return {"error": f"لا يمكن تحليل الهدف: {self.target}"}
        
        if not self.quiet:
            print_status(f"بدء فحص خادم الويب للهدف: {self.target} ({self.ip})", "info")
        
        self.logger.info(f"بدء فحص خادم الويب للهدف: {self.target} ({self.ip})")
        
        # فحص معلومات خادم الويب
        self._scan_web_server_info()
        
        # فحص الرؤوس الأمنية
        self._scan_security_headers()
        
        # فحص ملفات وأدلة حساسة
        self._scan_sensitive_files()
        
        # فحص نقاط النهاية API
        self._scan_api_endpoints()
        
        # فحص نماذج الإدخال
        self._scan_input_forms()
        
        # فحص تكوين CORS
        self._scan_cors_config()
        
        # فحص تكوين CSP
        self._scan_csp_config()
        
        if not self.quiet:
            print_status(f"اكتمال فحص خادم الويب للهدف: {self.target}", "success")
        
        self.logger.info(f"اكتمال فحص خادم الويب للهدف: {self.target}")
        
        return self.results
    
    def _scan_web_server_info(self):
        """
        فحص معلومات خادم الويب
        """
        if not self.quiet:
            print_status("فحص معلومات خادم الويب...", "info")
        
        web_server_info = {}
        
        # التحقق من HTTP
        try:
            response = requests.get(self.base_url, timeout=5, verify=False, allow_redirects=True)
            
            web_server_info["http"] = {
                "status_code": response.status_code,
                "server": response.headers.get("Server", "Unknown"),
                "powered_by": response.headers.get("X-Powered-By", "Unknown"),
                "content_type": response.headers.get("Content-Type", "Unknown"),
                "title": self._extract_title(response.text),
                "final_url": response.url,
                "redirect": response.url != self.base_url,
                "headers": dict(response.headers)
            }
            
            if not self.quiet:
                print_status(f"خادم HTTP: {web_server_info['http']['server']}", "success")
                print_status(f"مدعوم بواسطة: {web_server_info['http']['powered_by']}", "success")
                print_status(f"عنوان الصفحة: {web_server_info['http']['title']}", "success")
                
                if web_server_info["http"]["redirect"]:
                    print_status(f"تم إعادة التوجيه إلى: {web_server_info['http']['final_url']}", "info")
        except requests.RequestException as e:
            web_server_info["http"] = {"error": str(e)}
            if not self.quiet:
                print_status(f"فشل في الوصول إلى HTTP: {str(e)}", "error")
        
        # التحقق من HTTPS
        try:
            https_url = f"https://{self.target}"
            response = requests.get(https_url, timeout=5, verify=False, allow_redirects=True)
            
            web_server_info["https"] = {
                "status_code": response.status_code,
                "server": response.headers.get("Server", "Unknown"),
                "powered_by": response.headers.get("X-Powered-By", "Unknown"),
                "content_type": response.headers.get("Content-Type", "Unknown"),
                "title": self._extract_title(response.text),
                "final_url": response.url,
                "redirect": response.url != https_url,
                "headers": dict(response.headers)
            }
            
            if not self.quiet:
                print_status(f"خادم HTTPS: {web_server_info['https']['server']}", "success")
                print_status(f"مدعوم بواسطة: {web_server_info['https']['powered_by']}", "success")
                print_status(f"عنوان الصفحة: {web_server_info['https']['title']}", "success")
                
                if web_server_info["https"]["redirect"]:
                    print_status(f"تم إعادة التوجيه إلى: {web_server_info['https']['final_url']}", "info")
        except requests.RequestException as e:
            web_server_info["https"] = {"error": str(e)}
            if not self.quiet:
                print_status(f"فشل في الوصول إلى HTTPS: {str(e)}", "error")
        
        # تحديد URL الأساسي للفحص
        if "https" in web_server_info and "status_code" in web_server_info["https"] and web_server_info["https"]["status_code"] < 400:
            self.base_url = f"https://{self.target}"
        
        self.results["web_server_info"] = web_server_info
    
    def _scan_security_headers(self):
        """
        فحص الرؤوس الأمنية
        """
        if not self.quiet:
            print_status("فحص الرؤوس الأمنية...", "info")
        
        security_headers = {}
        
        try:
            response = requests.get(self.base_url, timeout=5, verify=False)
            
            # قائمة الرؤوس الأمنية المهمة
            important_headers = {
                "Strict-Transport-Security": "HSTS",
                "Content-Security-Policy": "CSP",
                "X-Content-Type-Options": "X-Content-Type-Options",
                "X-Frame-Options": "X-Frame-Options",
                "X-XSS-Protection": "X-XSS-Protection",
                "Referrer-Policy": "Referrer-Policy",
                "Feature-Policy": "Feature-Policy",
                "Permissions-Policy": "Permissions-Policy"
            }
            
            # التحقق من وجود الرؤوس الأمنية
            for header, header_name in important_headers.items():
                if header in response.headers:
                    security_headers[header] = {
                        "present": True,
                        "value": response.headers[header]
                    }
                    
                    if not self.quiet:
                        print_status(f"رأس {header_name} موجود: {response.headers[header]}", "success")
                else:
                    security_headers[header] = {
                        "present": False
                    }
                    
                    if not self.quiet:
                        print_status(f"رأس {header_name} مفقود", "warning")
        except requests.RequestException as e:
            if not self.quiet:
                print_status(f"فشل في فحص الرؤوس الأمنية: {str(e)}", "error")
        
        self.results["security_headers"] = security_headers
    
    def _scan_sensitive_files(self):
        """
        فحص ملفات وأدلة حساسة
        """
        if not self.quiet:
            print_status("فحص ملفات وأدلة حساسة...", "info")
        
        sensitive_files = []
        
        # قائمة الملفات والأدلة الحساسة
        files_to_check = [
            "/robots.txt",
            "/sitemap.xml",
            "/.git/HEAD",
            "/.env",
            "/.htaccess",
            "/backup/",
            "/backup.zip",
            "/backup.tar.gz",
            "/phpinfo.php",
            "/info.php",
            "/server-status",
            "/server-info",
            "/wp-config.php",
            "/config.php",
            "/configuration.php",
            "/admin/",
            "/administrator/",
            "/wp-admin/",
            "/wp-login.php",
            "/login/",
            "/login.php",
            "/phpmyadmin/",
            "/adminer.php",
            "/console/",
            "/api/",
            "/api/v1/",
            "/api/v2/",
            "/swagger/",
            "/swagger-ui.html",
            "/api-docs/"
        ]
        
        for file_path in files_to_check:
            try:
                url = urljoin(self.base_url, file_path)
                response = requests.get(url, timeout=5, verify=False, allow_redirects=False)
                
                if response.status_code < 400:
                    sensitive_files.append({
                        "url": url,
                        "status_code": response.status_code,
                        "content_type": response.headers.get("Content-Type", "Unknown"),
                        "content_length": len(response.content)
                    })
                    
                    if not self.quiet:
                        print_status(f"ملف حساس موجود: {url} (كود الحالة: {response.status_code})", "warning")
            except requests.RequestException:
                pass
        
        self.results["sensitive_files"] = sensitive_files
    
    def _scan_api_endpoints(self):
        """
        فحص نقاط النهاية API
        """
        if not self.quiet:
            print_status("فحص نقاط النهاية API...", "info")
        
        api_endpoints = []
        
        # قائمة نقاط النهاية API الشائعة
        api_paths = [
            "/api",
            "/api/v1",
            "/api/v2",
            "/rest",
            "/graphql",
            "/graphiql",
            "/swagger",
            "/swagger-ui.html",
            "/api-docs",
            "/docs",
            "/openapi.json",
            "/wp-json",
            "/wp-json/wp/v2"
        ]
        
        for api_path in api_paths:
            try:
                url = urljoin(self.base_url, api_path)
                response = requests.get(url, timeout=5, verify=False, allow_redirects=False)
                
                if response.status_code < 400:
                    # التحقق مما إذا كانت الاستجابة JSON
                    content_type = response.headers.get("Content-Type", "")
                    is_json = "json" in content_type.lower()
                    
                    api_endpoints.append({
                        "url": url,
                        "status_code": response.status_code,
                        "content_type": content_type,
                        "is_json": is_json,
                        "content_length": len(response.content)
                    })
                    
                    if not self.quiet:
                        print_status(f"نقطة نهاية API موجودة: {url} (كود الحالة: {response.status_code})", "warning")
            except requests.RequestException:
                pass
        
        self.results["api_endpoints"] = api_endpoints
    
    def _scan_input_forms(self):
        """
        فحص نماذج الإدخال
        """
        if not self.quiet:
            print_status("فحص نماذج الإدخال...", "info")
        
        input_forms = []
        
        try:
            response = requests.get(self.base_url, timeout=5, verify=False)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                forms = soup.find_all("form")
                
                for i, form in enumerate(forms):
                    form_info = {
                        "id": i + 1,
                        "action": form.get("action", ""),
                        "method": form.get("method", "get").upper(),
                        "inputs": []
                    }
                    
                    # تحديد URL النموذج
                    if form_info["action"]:
                        form_info["url"] = urljoin(self.base_url, form_info["action"])
                    else:
                        form_info["url"] = self.base_url
                    
                    # جمع معلومات حقول الإدخال
                    inputs = form.find_all("input")
                    for input_field in inputs:
                        input_info = {
                            "name": input_field.get("name", ""),
                            "type": input_field.get("type", "text"),
                            "id": input_field.get("id", ""),
                            "required": input_field.has_attr("required")
                        }
                        form_info["inputs"].append(input_info)
                    
                    input_forms.append(form_info)
                    
                    if not self.quiet:
                        print_status(f"نموذج #{i+1}: {form_info['method']} {form_info['url']} ({len(form_info['inputs'])} حقل)", "info")
        except requests.RequestException as e:
            if not self.quiet:
                print_status(f"فشل في فحص نماذج الإدخال: {str(e)}", "error")
        
        self.results["input_forms"] = input_forms
    
    def _scan_cors_config(self):
        """
        فحص تكوين CORS
        """
        if not self.quiet:
            print_status("فحص تكوين CORS...", "info")
        
        cors_config = {}
        
        try:
            headers = {
                "Origin": "https://evil.com"
            }
            
            response = requests.get(self.base_url, headers=headers, timeout=5, verify=False)
            
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin", None),
                "Access-Control-Allow-Credentials": response.headers.get("Access-Control-Allow-Credentials", None),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods", None),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers", None),
                "Access-Control-Expose-Headers": response.headers.get("Access-Control-Expose-Headers", None)
            }
            
            cors_config["headers"] = cors_headers
            
            # التحقق من وجود إعدادات CORS غير آمنة
            if cors_headers["Access-Control-Allow-Origin"] == "*" or cors_headers["Access-Control-Allow-Origin"] == "https://evil.com":
                cors_config["insecure"] = True
                cors_config["issue"] = "تكوين CORS غير آمن: يسمح بالوصول من أي أصل"
                
                if not self.quiet:
                    print_status(f"تكوين CORS غير آمن: {cors_headers['Access-Control-Allow-Origin']}", "warning")
            elif cors_headers["Access-Control-Allow-Origin"] and cors_headers["Access-Control-Allow-Credentials"] == "true":
                cors_config["insecure"] = True
                cors_config["issue"] = "تكوين CORS غير آمن: يسمح بالوصول مع بيانات الاعتماد"
                
                if not self.quiet:
                    print_status("تكوين CORS غير آمن: يسمح بالوصول مع بيانات الاعتماد", "warning")
            else:
                cors_config["insecure"] = False
                
                if not self.quiet:
                    if cors_headers["Access-Control-Allow-Origin"]:
                        print_status(f"تكوين CORS: {cors_headers['Access-Control-Allow-Origin']}", "success")
                    else:
                        print_status("لم يتم العثور على رؤوس CORS", "info")
        except requests.RequestException as e:
            if not self.quiet:
                print_status(f"فشل في فحص تكوين CORS: {str(e)}", "error")
        
        self.results["cors_config"] = cors_config
    
    def _scan_csp_config(self):
        """
        فحص تكوين CSP
        """
        if not self.quiet:
            print_status("فحص تكوين CSP...", "info")
        
        csp_config = {}
        
        try:
            response = requests.get(self.base_url, timeout=5, verify=False)
            
            csp_header = response.headers.get("Content-Security-Policy", None)
            csp_config["header"] = csp_header
            
            if csp_header:
                # تحليل سياسة CSP
                csp_directives = {}
                
                for directive in csp_header.split(";"):
                    directive = directive.strip()
                    if directive:
                        parts = directive.split(" ")
                        directive_name = parts[0]
                        directive_values = parts[1:] if len(parts) > 1 else []
                        csp_directives[directive_name] = directive_values
                
                csp_config["directives"] = csp_directives
                
                # التحقق من وجود إعدادات CSP غير آمنة
                insecure_directives = []
                
                if "default-src" in csp_directives and "'unsafe-inline'" in csp_directives["default-src"]:
                    insecure_directives.append("default-src 'unsafe-inline'")
                
                if "script-src" in csp_directives and "'unsafe-inline'" in csp_directives["script-src"]:
                    insecure_directives.append("script-src 'unsafe-inline'")
                
                if "script-src" in csp_directives and "'unsafe-eval'" in csp_directives["script-src"]:
                    insecure_directives.append("script-src 'unsafe-eval'")
                
                if insecure_directives:
                    csp_config["insecure"] = True
                    csp_config["issues"] = insecure_directives
                    
                    if not self.quiet:
                        print_status(f"تكوين CSP غير آمن: {', '.join(insecure_directives)}", "warning")
                else:
                    csp_config["insecure"] = False
                    
                    if not self.quiet:
                        print_status("تكوين CSP آمن", "success")
            else:
                csp_config["missing"] = True
                
                if not self.quiet:
                    print_status("رأس Content-Security-Policy مفقود", "warning")
        except requests.RequestException as e:
            if not self.quiet:
                print_status(f"فشل في فحص تكوين CSP: {str(e)}", "error")
        
        self.results["csp_config"] = csp_config
    
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
    scanner = WebScanner(target, logger, quiet=False, debug=True)
    results = scanner.scan()
    
    print(json.dumps(results, indent=4, default=str))