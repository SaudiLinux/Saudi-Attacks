#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة فحص أنظمة إدارة المحتوى (CMS)
"""

import json
import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from colorama import Fore, Style
from .utils import print_status, is_valid_ip, is_valid_domain, resolve_host, run_command

class CMSScanner:
    """
    فئة فحص أنظمة إدارة المحتوى
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
        
        # التحقق من HTTPS
        try:
            https_url = f"https://{self.target}"
            response = requests.get(https_url, timeout=5, verify=False, allow_redirects=True)
            if response.status_code < 400:
                self.base_url = https_url
        except requests.RequestException:
            pass
    
    def detect_cms(self):
        """
        اكتشاف نظام إدارة المحتوى
        """
        if not self.ip or not self.base_url:
            if not self.quiet:
                print_status(f"لا يمكن تحليل الهدف: {self.target}", "error")
            self.logger.error(f"لا يمكن تحليل الهدف: {self.target}")
            return None
        
        if not self.quiet:
            print_status(f"اكتشاف نظام إدارة المحتوى للهدف: {self.target}", "info")
        
        self.logger.info(f"اكتشاف نظام إدارة المحتوى للهدف: {self.target}")
        
        cms_type = None
        cms_version = None
        
        try:
            response = requests.get(self.base_url, timeout=5, verify=False)
            
            if response.status_code == 200:
                html = response.text
                headers = response.headers
                
                # التحقق من ووردبريس
                if self._is_wordpress(html, headers):
                    cms_type = "wordpress"
                    cms_version = self._get_wordpress_version(html, headers)
                    
                    if not self.quiet:
                        print_status(f"تم اكتشاف ووردبريس (الإصدار: {cms_version if cms_version else 'غير معروف'})", "success")
                
                # التحقق من جوملا
                elif self._is_joomla(html, headers):
                    cms_type = "joomla"
                    cms_version = self._get_joomla_version(html, headers)
                    
                    if not self.quiet:
                        print_status(f"تم اكتشاف جوملا (الإصدار: {cms_version if cms_version else 'غير معروف'})", "success")
                
                # التحقق من دروبال
                elif self._is_drupal(html, headers):
                    cms_type = "drupal"
                    cms_version = self._get_drupal_version(html, headers)
                    
                    if not self.quiet:
                        print_status(f"تم اكتشاف دروبال (الإصدار: {cms_version if cms_version else 'غير معروف'})", "success")
                
                # التحقق من ماجنتو
                elif self._is_magento(html, headers):
                    cms_type = "magento"
                    cms_version = self._get_magento_version(html, headers)
                    
                    if not self.quiet:
                        print_status(f"تم اكتشاف ماجنتو (الإصدار: {cms_version if cms_version else 'غير معروف'})", "success")
                
                else:
                    if not self.quiet:
                        print_status("لم يتم اكتشاف نظام إدارة محتوى معروف", "info")
        except requests.RequestException as e:
            if not self.quiet:
                print_status(f"فشل في اكتشاف نظام إدارة المحتوى: {str(e)}", "error")
        
        return {
            "cms_type": cms_type,
            "cms_version": cms_version
        }
    
    def scan_wordpress(self):
        """
        فحص ووردبريس
        """
        if not self.ip or not self.base_url:
            if not self.quiet:
                print_status(f"لا يمكن تحليل الهدف: {self.target}", "error")
            self.logger.error(f"لا يمكن تحليل الهدف: {self.target}")
            return {"error": f"لا يمكن تحليل الهدف: {self.target}"}
        
        if not self.quiet:
            print_status(f"بدء فحص ووردبريس للهدف: {self.target}", "info")
        
        self.logger.info(f"بدء فحص ووردبريس للهدف: {self.target}")
        
        results = {}
        
        # اكتشاف ووردبريس
        cms_info = self.detect_cms()
        results["cms_info"] = cms_info
        
        if cms_info["cms_type"] != "wordpress":
            if not self.quiet:
                print_status("لم يتم اكتشاف ووردبريس على الهدف", "warning")
            
            self.logger.warning(f"لم يتم اكتشاف ووردبريس على الهدف: {self.target}")
            return results
        
        # فحص الإصدار
        results["version"] = cms_info["cms_version"]
        
        # فحص المستخدمين
        results["users"] = self._scan_wordpress_users()
        
        # فحص الإضافات
        results["plugins"] = self._scan_wordpress_plugins()
        
        # فحص القوالب
        results["themes"] = self._scan_wordpress_themes()
        
        # فحص نقاط الضعف
        results["vulnerabilities"] = self._scan_wordpress_vulnerabilities(results)
        
        if not self.quiet:
            print_status(f"اكتمال فحص ووردبريس للهدف: {self.target}", "success")
        
        self.logger.info(f"اكتمال فحص ووردبريس للهدف: {self.target}")
        
        return results
    
    def scan_joomla(self):
        """
        فحص جوملا
        """
        if not self.ip or not self.base_url:
            if not self.quiet:
                print_status(f"لا يمكن تحليل الهدف: {self.target}", "error")
            self.logger.error(f"لا يمكن تحليل الهدف: {self.target}")
            return {"error": f"لا يمكن تحليل الهدف: {self.target}"}
        
        if not self.quiet:
            print_status(f"بدء فحص جوملا للهدف: {self.target}", "info")
        
        self.logger.info(f"بدء فحص جوملا للهدف: {self.target}")
        
        results = {}
        
        # اكتشاف جوملا
        cms_info = self.detect_cms()
        results["cms_info"] = cms_info
        
        if cms_info["cms_type"] != "joomla":
            if not self.quiet:
                print_status("لم يتم اكتشاف جوملا على الهدف", "warning")
            
            self.logger.warning(f"لم يتم اكتشاف جوملا على الهدف: {self.target}")
            return results
        
        # فحص الإصدار
        results["version"] = cms_info["cms_version"]
        
        # فحص المكونات
        results["components"] = self._scan_joomla_components()
        
        # فحص الإضافات
        results["plugins"] = self._scan_joomla_plugins()
        
        # فحص القوالب
        results["templates"] = self._scan_joomla_templates()
        
        # فحص نقاط الضعف
        results["vulnerabilities"] = self._scan_joomla_vulnerabilities(results)
        
        if not self.quiet:
            print_status(f"اكتمال فحص جوملا للهدف: {self.target}", "success")
        
        self.logger.info(f"اكتمال فحص جوملا للهدف: {self.target}")
        
        return results
    
    # دوال اكتشاف أنظمة إدارة المحتوى
    
    def _is_wordpress(self, html, headers):
        """
        التحقق مما إذا كان الموقع يستخدم ووردبريس
        """
        # التحقق من وجود علامات ووردبريس في HTML
        wp_signs = [
            "wp-content",
            "wp-includes",
            "wp-admin",
            "WordPress",
            "xmlrpc.php"
        ]
        
        for sign in wp_signs:
            if sign in html:
                return True
        
        # التحقق من وجود ملفات ووردبريس
        try:
            wp_login_url = urljoin(self.base_url, "wp-login.php")
            response = requests.get(wp_login_url, timeout=5, verify=False, allow_redirects=False)
            if response.status_code == 200 and "WordPress" in response.text:
                return True
        except requests.RequestException:
            pass
        
        return False
    
    def _is_joomla(self, html, headers):
        """
        التحقق مما إذا كان الموقع يستخدم جوملا
        """
        # التحقق من وجود علامات جوملا في HTML
        joomla_signs = [
            "joomla",
            "Joomla",
            "com_content",
            "com_users",
            "com_contact",
            "com_wrapper",
            "com_banners",
            "com_mailto"
        ]
        
        for sign in joomla_signs:
            if sign in html:
                return True
        
        # التحقق من وجود ملفات جوملا
        try:
            joomla_admin_url = urljoin(self.base_url, "administrator/")
            response = requests.get(joomla_admin_url, timeout=5, verify=False, allow_redirects=False)
            if response.status_code == 200 and ("Joomla" in response.text or "joomla" in response.text):
                return True
        except requests.RequestException:
            pass
        
        return False
    
    def _is_drupal(self, html, headers):
        """
        التحقق مما إذا كان الموقع يستخدم دروبال
        """
        # التحقق من وجود علامات دروبال في HTML
        drupal_signs = [
            "Drupal",
            "drupal",
            "sites/all",
            "sites/default"
        ]
        
        for sign in drupal_signs:
            if sign in html:
                return True
        
        # التحقق من وجود ملفات دروبال
        try:
            drupal_readme_url = urljoin(self.base_url, "CHANGELOG.txt")
            response = requests.get(drupal_readme_url, timeout=5, verify=False, allow_redirects=False)
            if response.status_code == 200 and "Drupal" in response.text:
                return True
        except requests.RequestException:
            pass
        
        return False
    
    def _is_magento(self, html, headers):
        """
        التحقق مما إذا كان الموقع يستخدم ماجنتو
        """
        # التحقق من وجود علامات ماجنتو في HTML
        magento_signs = [
            "Magento",
            "magento",
            "Mage.Cookies",
            "skin/frontend",
            "js/varien",
            "js/mage"
        ]
        
        for sign in magento_signs:
            if sign in html:
                return True
        
        # التحقق من وجود ملفات ماجنتو
        try:
            magento_admin_url = urljoin(self.base_url, "admin/")
            response = requests.get(magento_admin_url, timeout=5, verify=False, allow_redirects=False)
            if response.status_code == 200 and "Magento" in response.text:
                return True
        except requests.RequestException:
            pass
        
        return False
    
    # دوال الحصول على إصدارات أنظمة إدارة المحتوى
    
    def _get_wordpress_version(self, html, headers):
        """
        الحصول على إصدار ووردبريس
        """
        # البحث عن الإصدار في HTML
        version_pattern = r'<meta\s+name=["\']generator["\']\s+content=["\']WordPress\s+([\d\.]+)'
        match = re.search(version_pattern, html)
        if match:
            return match.group(1)
        
        # البحث عن الإصدار في ملف readme.html
        try:
            readme_url = urljoin(self.base_url, "readme.html")
            response = requests.get(readme_url, timeout=5, verify=False)
            if response.status_code == 200:
                version_pattern = r'<br />\s*[Vv]ersion\s+([\d\.]+)'
                match = re.search(version_pattern, response.text)
                if match:
                    return match.group(1)
        except requests.RequestException:
            pass
        
        # البحث عن الإصدار في ملف feed
        try:
            feed_url = urljoin(self.base_url, "feed/")
            response = requests.get(feed_url, timeout=5, verify=False)
            if response.status_code == 200:
                version_pattern = r'<generator>https?://wordpress\.org/\?v=([\d\.]+)</generator>'
                match = re.search(version_pattern, response.text)
                if match:
                    return match.group(1)
        except requests.RequestException:
            pass
        
        return None
    
    def _get_joomla_version(self, html, headers):
        """
        الحصول على إصدار جوملا
        """
        # البحث عن الإصدار في HTML
        version_pattern = r'<meta\s+name=["\']generator["\']\s+content=["\']Joomla!\s+([\d\.]+)'
        match = re.search(version_pattern, html)
        if match:
            return match.group(1)
        
        # البحث عن الإصدار في ملف XML
        try:
            xml_url = urljoin(self.base_url, "administrator/manifests/files/joomla.xml")
            response = requests.get(xml_url, timeout=5, verify=False)
            if response.status_code == 200:
                version_pattern = r'<version>([\d\.]+)</version>'
                match = re.search(version_pattern, response.text)
                if match:
                    return match.group(1)
        except requests.RequestException:
            pass
        
        return None
    
    def _get_drupal_version(self, html, headers):
        """
        الحصول على إصدار دروبال
        """
        # البحث عن الإصدار في ملف CHANGELOG.txt
        try:
            changelog_url = urljoin(self.base_url, "CHANGELOG.txt")
            response = requests.get(changelog_url, timeout=5, verify=False)
            if response.status_code == 200:
                version_pattern = r'Drupal\s+([\d\.]+)'
                match = re.search(version_pattern, response.text)
                if match:
                    return match.group(1)
        except requests.RequestException:
            pass
        
        return None
    
    def _get_magento_version(self, html, headers):
        """
        الحصول على إصدار ماجنتو
        """
        # البحث عن الإصدار في HTML
        version_pattern = r'Magento/([\d\.]+)'
        match = re.search(version_pattern, html)
        if match:
            return match.group(1)
        
        return None
    
    # دوال فحص ووردبريس
    
    def _scan_wordpress_users(self):
        """
        فحص مستخدمي ووردبريس
        """
        users = []
        
        if not self.quiet:
            print_status("فحص مستخدمي ووردبريس...", "info")
        
        # طريقة 1: استخدام WP JSON API
        try:
            api_url = urljoin(self.base_url, "wp-json/wp/v2/users")
            response = requests.get(api_url, timeout=5, verify=False)
            
            if response.status_code == 200:
                try:
                    user_data = response.json()
                    for user in user_data:
                        users.append({
                            "id": user.get("id"),
                            "name": user.get("name"),
                            "slug": user.get("slug"),
                            "link": user.get("link")
                        })
                    
                    if not self.quiet and users:
                        print_status(f"تم العثور على {len(users)} مستخدم عبر WP API", "warning")
                except json.JSONDecodeError:
                    pass
        except requests.RequestException:
            pass
        
        # طريقة 2: استخدام ?author=N
        if not users:
            for i in range(1, 10):  # فحص أول 10 معرفات
                try:
                    author_url = f"{self.base_url}/?author={i}"
                    response = requests.get(author_url, timeout=5, verify=False, allow_redirects=True)
                    
                    if response.status_code == 200:
                        # استخراج اسم المستخدم من العنوان
                        soup = BeautifulSoup(response.text, "html.parser")
                        title = soup.title.string if soup.title else ""
                        
                        # استخراج اسم المستخدم من URL
                        author_pattern = r'/author/([^/]+)'
                        match = re.search(author_pattern, response.url)
                        
                        if match:
                            username = match.group(1)
                            users.append({
                                "id": i,
                                "name": title.split("|")[0].strip() if "|" in title else title.strip(),
                                "slug": username,
                                "link": response.url
                            })
                            
                            if not self.quiet:
                                print_status(f"تم العثور على المستخدم: {username} (ID: {i})", "warning")
                except requests.RequestException:
                    pass
        
        return users
    
    def _scan_wordpress_plugins(self):
        """
        فحص إضافات ووردبريس
        """
        plugins = []
        
        if not self.quiet:
            print_status("فحص إضافات ووردبريس...", "info")
        
        # قائمة الإضافات الشائعة للفحص
        common_plugins = [
            "contact-form-7",
            "woocommerce",
            "jetpack",
            "akismet",
            "wordfence",
            "yoast-seo",
            "elementor",
            "wp-super-cache",
            "all-in-one-seo-pack",
            "updraftplus",
            "really-simple-ssl",
            "wp-optimize",
            "redirection",
            "duplicate-post",
            "classic-editor"
        ]
        
        for plugin in common_plugins:
            try:
                # التحقق من وجود مجلد الإضافة
                plugin_url = urljoin(self.base_url, f"wp-content/plugins/{plugin}/")
                response = requests.get(plugin_url, timeout=5, verify=False, allow_redirects=False)
                
                if response.status_code < 404:
                    # محاولة الحصول على إصدار الإضافة من ملف readme.txt
                    readme_url = urljoin(self.base_url, f"wp-content/plugins/{plugin}/readme.txt")
                    readme_response = requests.get(readme_url, timeout=5, verify=False)
                    
                    version = None
                    if readme_response.status_code == 200:
                        version_pattern = r'Stable tag:\s*([\d\.]+)'
                        match = re.search(version_pattern, readme_response.text)
                        if match:
                            version = match.group(1)
                    
                    plugins.append({
                        "name": plugin,
                        "url": plugin_url,
                        "version": version
                    })
                    
                    if not self.quiet:
                        print_status(f"تم العثور على الإضافة: {plugin}{' (الإصدار: ' + version + ')' if version else ''}", "warning")
            except requests.RequestException:
                pass
        
        return plugins
    
    def _scan_wordpress_themes(self):
        """
        فحص قوالب ووردبريس
        """
        themes = []
        
        if not self.quiet:
            print_status("فحص قوالب ووردبريس...", "info")
        
        # قائمة القوالب الشائعة للفحص
        common_themes = [
            "twentytwentyone",
            "twentytwenty",
            "twentynineteen",
            "twentyseventeen",
            "twentysixteen",
            "astra",
            "divi",
            "avada",
            "oceanwp",
            "generatepress",
            "neve",
            "sydney",
            "hestia",
            "hello-elementor"
        ]
        
        for theme in common_themes:
            try:
                # التحقق من وجود مجلد القالب
                theme_url = urljoin(self.base_url, f"wp-content/themes/{theme}/")
                response = requests.get(theme_url, timeout=5, verify=False, allow_redirects=False)
                
                if response.status_code < 404:
                    # محاولة الحصول على إصدار القالب من ملف style.css
                    style_url = urljoin(self.base_url, f"wp-content/themes/{theme}/style.css")
                    style_response = requests.get(style_url, timeout=5, verify=False)
                    
                    version = None
                    if style_response.status_code == 200:
                        version_pattern = r'Version:\s*([\d\.]+)'
                        match = re.search(version_pattern, style_response.text)
                        if match:
                            version = match.group(1)
                    
                    themes.append({
                        "name": theme,
                        "url": theme_url,
                        "version": version
                    })
                    
                    if not self.quiet:
                        print_status(f"تم العثور على القالب: {theme}{' (الإصدار: ' + version + ')' if version else ''}", "warning")
            except requests.RequestException:
                pass
        
        # محاولة تحديد القالب النشط
        try:
            response = requests.get(self.base_url, timeout=5, verify=False)
            if response.status_code == 200:
                html = response.text
                
                # البحث عن مسار القالب في HTML
                theme_pattern = r'wp-content/themes/([^/]+)'
                matches = re.findall(theme_pattern, html)
                
                if matches:
                    active_theme = matches[0]
                    
                    # التحقق مما إذا كان القالب النشط موجودًا بالفعل في القائمة
                    found = False
                    for theme in themes:
                        if theme["name"] == active_theme:
                            theme["active"] = True
                            found = True
                            break
                    
                    # إذا لم يكن القالب النشط موجودًا في القائمة، أضفه
                    if not found:
                        themes.append({
                            "name": active_theme,
                            "url": urljoin(self.base_url, f"wp-content/themes/{active_theme}/"),
                            "version": None,
                            "active": True
                        })
                        
                        if not self.quiet:
                            print_status(f"تم العثور على القالب النشط: {active_theme}", "warning")
        except requests.RequestException:
            pass
        
        return themes
    
    def _scan_wordpress_vulnerabilities(self, wp_results):
        """
        فحص نقاط ضعف ووردبريس
        """
        vulnerabilities = []
        
        if not self.quiet:
            print_status("فحص نقاط ضعف ووردبريس...", "info")
        
        # فحص نقاط ضعف الإصدار
        version = wp_results.get("version")
        if version:
            # هذه مجرد قائمة بسيطة للتوضيح، في التطبيق الحقيقي يمكن استخدام قاعدة بيانات حقيقية
            vulnerable_versions = {
                "4.7.0": "WordPress 4.7.0 - Content Type Bypass",
                "4.7.1": "WordPress 4.7.1 - REST API Content Injection",
                "4.6": "WordPress 4.6 - Stored XSS",
                "4.5": "WordPress 4.5 - SSRF",
                "4.4": "WordPress 4.4 - CSRF"
            }
            
            for vuln_version, vuln_name in vulnerable_versions.items():
                if version == vuln_version or version.startswith(vuln_version + "."):
                    vulnerabilities.append({
                        "type": "core",
                        "name": vuln_name,
                        "version": version,
                        "severity": "عالية"
                    })
                    
                    if not self.quiet:
                        print_status(f"نقطة ضعف في النواة: {vuln_name} (الإصدار: {version})", "warning")
        
        # فحص نقاط ضعف الإضافات
        plugins = wp_results.get("plugins", [])
        for plugin in plugins:
            plugin_name = plugin.get("name")
            plugin_version = plugin.get("version")
            
            # هذه مجرد قائمة بسيطة للتوضيح، في التطبيق الحقيقي يمكن استخدام قاعدة بيانات حقيقية
            vulnerable_plugins = {
                "contact-form-7": {
                    "5.3.1": "Contact Form 7 5.3.1 - Unrestricted File Upload",
                    "5.2.0": "Contact Form 7 5.2.0 - XSS"
                },
                "woocommerce": {
                    "3.3.0": "WooCommerce 3.3.0 - CSRF",
                    "3.2.0": "WooCommerce 3.2.0 - SQL Injection"
                }
            }
            
            if plugin_name in vulnerable_plugins and plugin_version:
                for vuln_version, vuln_name in vulnerable_plugins[plugin_name].items():
                    if plugin_version == vuln_version or plugin_version.startswith(vuln_version + "."):
                        vulnerabilities.append({
                            "type": "plugin",
                            "name": vuln_name,
                            "plugin": plugin_name,
                            "version": plugin_version,
                            "severity": "متوسطة"
                        })
                        
                        if not self.quiet:
                            print_status(f"نقطة ضعف في الإضافة: {vuln_name} (الإضافة: {plugin_name}, الإصدار: {plugin_version})", "warning")
        
        # فحص نقاط ضعف القوالب
        themes = wp_results.get("themes", [])
        for theme in themes:
            theme_name = theme.get("name")
            theme_version = theme.get("version")
            
            # هذه مجرد قائمة بسيطة للتوضيح، في التطبيق الحقيقي يمكن استخدام قاعدة بيانات حقيقية
            vulnerable_themes = {
                "twentytwenty": {
                    "1.0": "Twenty Twenty 1.0 - XSS",
                    "1.1": "Twenty Twenty 1.1 - CSRF"
                },
                "astra": {
                    "2.0.0": "Astra 2.0.0 - Stored XSS",
                    "2.1.0": "Astra 2.1.0 - CSRF"
                }
            }
            
            if theme_name in vulnerable_themes and theme_version:
                for vuln_version, vuln_name in vulnerable_themes[theme_name].items():
                    if theme_version == vuln_version or theme_version.startswith(vuln_version + "."):
                        vulnerabilities.append({
                            "type": "theme",
                            "name": vuln_name,
                            "theme": theme_name,
                            "version": theme_version,
                            "severity": "منخفضة"
                        })
                        
                        if not self.quiet:
                            print_status(f"نقطة ضعف في القالب: {vuln_name} (القالب: {theme_name}, الإصدار: {theme_version})", "warning")
        
        return vulnerabilities
    
    # دوال فحص جوملا
    
    def _scan_joomla_components(self):
        """
        فحص مكونات جوملا
        """
        components = []
        
        if not self.quiet:
            print_status("فحص مكونات جوملا...", "info")
        
        # قائمة المكونات الشائعة للفحص
        common_components = [
            "com_content",
            "com_users",
            "com_contact",
            "com_banners",
            "com_finder",
            "com_tags",
            "com_newsfeeds",
            "com_search",
            "com_weblinks",
            "com_mailto",
            "com_wrapper",
            "com_admin",
            "com_media",
            "com_config",
            "com_plugins",
            "com_redirect",
            "com_modules"
        ]
        
        for component in common_components:
            try:
                # التحقق من وجود المكون
                component_url = urljoin(self.base_url, f"index.php?option={component}")
                response = requests.get(component_url, timeout=5, verify=False, allow_redirects=True)
                
                if response.status_code < 404:
                    components.append({
                        "name": component,
                        "url": component_url
                    })
                    
                    if not self.quiet:
                        print_status(f"تم العثور على المكون: {component}", "warning")
            except requests.RequestException:
                pass
        
        return components
    
    def _scan_joomla_plugins(self):
        """
        فحص إضافات جوملا
        """
        plugins = []
        
        if not self.quiet:
            print_status("فحص إضافات جوملا...", "info")
        
        # قائمة الإضافات الشائعة للفحص
        common_plugins = [
            "system/debug",
            "system/cache",
            "system/log",
            "system/redirect",
            "system/remember",
            "system/sef",
            "content/emailcloak",
            "content/joomla",
            "content/loadmodule",
            "content/pagebreak",
            "content/pagenavigation",
            "editors/tinymce",
            "editors/codemirror",
            "editors-xtd/article",
            "editors-xtd/image",
            "editors-xtd/pagebreak",
            "editors-xtd/readmore"
        ]
        
        for plugin in common_plugins:
            try:
                # التحقق من وجود الإضافة (هذا مجرد تخمين، لا توجد طريقة مباشرة للتحقق)
                plugin_type, plugin_name = plugin.split("/")
                plugin_url = urljoin(self.base_url, f"plugins/{plugin_type}/{plugin_name}/")
                response = requests.get(plugin_url, timeout=5, verify=False, allow_redirects=False)
                
                if response.status_code < 404:
                    plugins.append({
                        "name": plugin_name,
                        "type": plugin_type,
                        "url": plugin_url
                    })
                    
                    if not self.quiet:
                        print_status(f"تم العثور على الإضافة: {plugin_type}/{plugin_name}", "warning")
            except requests.RequestException:
                pass
        
        return plugins
    
    def _scan_joomla_templates(self):
        """
        فحص قوالب جوملا
        """
        templates = []
        
        if not self.quiet:
            print_status("فحص قوالب جوملا...", "info")
        
        # قائمة القوالب الشائعة للفحص
        common_templates = [
            "protostar",
            "beez3",
            "hathor",
            "isis",
            "system",
            "atomic",
            "beez5",
            "beez_20",
            "cassiopeia",
            "atum"
        ]
        
        for template in common_templates:
            try:
                # التحقق من وجود القالب
                template_url = urljoin(self.base_url, f"templates/{template}/")
                response = requests.get(template_url, timeout=5, verify=False, allow_redirects=False)
                
                if response.status_code < 404:
                    # محاولة الحصول على إصدار القالب من ملف templateDetails.xml
                    xml_url = urljoin(self.base_url, f"templates/{template}/templateDetails.xml")
                    xml_response = requests.get(xml_url, timeout=5, verify=False)
                    
                    version = None
                    if xml_response.status_code == 200:
                        version_pattern = r'<version>([\d\.]+)</version>'
                        match = re.search(version_pattern, xml_response.text)
                        if match:
                            version = match.group(1)
                    
                    templates.append({
                        "name": template,
                        "url": template_url,
                        "version": version
                    })
                    
                    if not self.quiet:
                        print_status(f"تم العثور على القالب: {template}{' (الإصدار: ' + version + ')' if version else ''}", "warning")
            except requests.RequestException:
                pass
        
        # محاولة تحديد القالب النشط
        try:
            response = requests.get(self.base_url, timeout=5, verify=False)
            if response.status_code == 200:
                html = response.text
                
                # البحث عن مسار القالب في HTML
                template_pattern = r'templates/([^/]+)'
                matches = re.findall(template_pattern, html)
                
                if matches:
                    active_template = matches[0]
                    
                    # التحقق مما إذا كان القالب النشط موجودًا بالفعل في القائمة
                    found = False
                    for template in templates:
                        if template["name"] == active_template:
                            template["active"] = True
                            found = True
                            break
                    
                    # إذا لم يكن القالب النشط موجودًا في القائمة، أضفه
                    if not found:
                        templates.append({
                            "name": active_template,
                            "url": urljoin(self.base_url, f"templates/{active_template}/"),
                            "version": None,
                            "active": True
                        })
                        
                        if not self.quiet:
                            print_status(f"تم العثور على القالب النشط: {active_template}", "warning")
        except requests.RequestException:
            pass
        
        return templates
    
    def _scan_joomla_vulnerabilities(self, joomla_results):
        """
        فحص نقاط ضعف جوملا
        """
        vulnerabilities = []
        
        if not self.quiet:
            print_status("فحص نقاط ضعف جوملا...", "info")
        
        # فحص نقاط ضعف الإصدار
        version = joomla_results.get("version")
        if version:
            # هذه مجرد قائمة بسيطة للتوضيح، في التطبيق الحقيقي يمكن استخدام قاعدة بيانات حقيقية
            vulnerable_versions = {
                "3.7.0": "Joomla 3.7.0 - SQL Injection",
                "3.6.0": "Joomla 3.6.0 - Account Creation",
                "3.5.0": "Joomla 3.5.0 - Object Injection",
                "3.4.0": "Joomla 3.4.0 - CSRF",
                "3.3.0": "Joomla 3.3.0 - XSS"
            }
            
            for vuln_version, vuln_name in vulnerable_versions.items():
                if version == vuln_version or version.startswith(vuln_version + "."):
                    vulnerabilities.append({
                        "type": "core",
                        "name": vuln_name,
                        "version": version,
                        "severity": "عالية"
                    })
                    
                    if not self.quiet:
                        print_status(f"نقطة ضعف في النواة: {vuln_name} (الإصدار: {version})", "warning")
        
        # فحص نقاط ضعف المكونات
        components = joomla_results.get("components", [])
        for component in components:
            component_name = component.get("name")
            
            # هذه مجرد قائمة بسيطة للتوضيح، في التطبيق الحقيقي يمكن استخدام قاعدة بيانات حقيقية
            vulnerable_components = {
                "com_content": "Joomla com_content - SQL Injection",
                "com_users": "Joomla com_users - Privilege Escalation",
                "com_contact": "Joomla com_contact - XSS",
                "com_weblinks": "Joomla com_weblinks - CSRF"
            }
            
            if component_name in vulnerable_components:
                vulnerabilities.append({
                    "type": "component",
                    "name": vulnerable_components[component_name],
                    "component": component_name,
                    "severity": "متوسطة"
                })
                
                if not self.quiet:
                    print_status(f"نقطة ضعف في المكون: {vulnerable_components[component_name]} (المكون: {component_name})", "warning")
        
        return vulnerabilities

if __name__ == "__main__":
    # اختبار الوحدة
    import logging
    logger = logging.getLogger("test")
    
    target = "example.com"
    scanner = CMSScanner(target, logger, quiet=False, debug=True)
    
    # اكتشاف نظام إدارة المحتوى
    cms_info = scanner.detect_cms()
    print(json.dumps(cms_info, indent=4))
    
    # فحص ووردبريس
    wp_results = scanner.scan_wordpress()
    print(json.dumps(wp_results, indent=4, default=str))
    
    # فحص جوملا
    joomla_results = scanner.scan_joomla()
    print(json.dumps(joomla_results, indent=4, default=str))