#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة الدوال المساعدة
"""

import os
import sys
import logging
import platform
import subprocess
import socket
import re
import requests
from colorama import Fore, Style
from datetime import datetime

def check_root():
    """
    التحقق من صلاحيات الجذر (root)
    """
    if platform.system() == "Windows":
        # على نظام ويندوز، نتحقق من صلاحيات المسؤول
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception as e:
            print(f"{Fore.YELLOW}[!] تحذير: فشل التحقق من صلاحيات المسؤول: {str(e)}{Style.RESET_ALL}")
            # نفترض أن المستخدم لديه صلاحيات كافية على نظام ويندوز
            return True
    else:
        # على نظام لينكس، نتحقق من صلاحيات الجذر
        return os.geteuid() == 0

def check_dependencies():
    """
    التحقق من وجود المتطلبات والأدوات اللازمة
    """
    print(f"{Fore.BLUE}[*] التحقق من المتطلبات...{Style.RESET_ALL}")
    
    # التحقق من وجود الأدوات الأساسية
    required_tools = {
        "nmap": "Nmap",
        "python3": "Python 3"
    }
    
    missing_tools = []
    
    for tool, name in required_tools.items():
        try:
            # على نظام ويندوز، نتحقق من وجود nmap بطريقة مختلفة
            if platform.system() == "Windows" and tool == "nmap":
                try:
                    # محاولة تنفيذ الأمر where للبحث عن nmap
                    result = subprocess.run(["where", "nmap"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                    if result.returncode == 0:
                        print(f"{Fore.GREEN}[+] تم العثور على {name}{Style.RESET_ALL}")
                    else:
                        missing_tools.append(name)
                        print(f"{Fore.RED}[!] لم يتم العثور على {name}{Style.RESET_ALL}")
                except Exception:
                    missing_tools.append(name)
                    print(f"{Fore.RED}[!] لم يتم العثور على {name}{Style.RESET_ALL}")
            else:
                subprocess.run([tool, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                print(f"{Fore.GREEN}[+] تم العثور على {name}{Style.RESET_ALL}")
        except FileNotFoundError:
            missing_tools.append(name)
            print(f"{Fore.RED}[!] لم يتم العثور على {name}{Style.RESET_ALL}")
    
    # التحقق من وجود المكتبات الأساسية
    required_modules = [
        "requests", "colorama", "argparse", "bs4", "tqdm"
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"{Fore.GREEN}[+] تم العثور على مكتبة {module}{Style.RESET_ALL}")
        except ImportError:
            missing_modules.append(module)
            print(f"{Fore.RED}[!] لم يتم العثور على مكتبة {module}{Style.RESET_ALL}")
    
    # إذا كانت هناك أدوات أو مكتبات مفقودة، نعرض رسالة تثبيت
    if missing_tools or missing_modules:
        print(f"\n{Fore.YELLOW}[!] يجب تثبيت الأدوات والمكتبات المفقودة:{Style.RESET_ALL}")
        
        if missing_tools:
            print(f"\n{Fore.YELLOW}الأدوات المفقودة:{Style.RESET_ALL}")
            for tool in missing_tools:
                if tool == "Nmap":
                    print(f"  - Nmap: https://nmap.org/download.html")
                elif tool == "Python 3":
                    print(f"  - Python 3: https://www.python.org/downloads/")
        
        if missing_modules:
            print(f"\n{Fore.YELLOW}المكتبات المفقودة:{Style.RESET_ALL}")
            modules_str = " ".join(missing_modules)
            print(f"  pip install {modules_str}")
        
        choice = input(f"\n{Fore.YELLOW}هل ترغب في المتابعة على الرغم من ذلك؟ (y/n): {Style.RESET_ALL}")
        if choice.lower() != 'y':
            sys.exit(1)
    else:
        print(f"{Fore.GREEN}[+] جميع المتطلبات متوفرة{Style.RESET_ALL}")

def setup_logging():
    """
    إعداد نظام السجلات
    """
    # إنشاء مجلد السجلات إذا لم يكن موجودًا
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # تحديد اسم ملف السجل
    log_file = f"logs/saudi_attacks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # إعداد المسجل
    logger = logging.getLogger("SaudiAttacks")
    logger.setLevel(logging.INFO)
    
    # إعداد معالج الملف
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # إعداد تنسيق السجل
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # إضافة المعالج إلى المسجل
    logger.addHandler(file_handler)
    
    print(f"{Fore.GREEN}[+] تم إعداد السجلات في {log_file}{Style.RESET_ALL}")
    
    return logger

def is_valid_ip(ip):
    """
    التحقق من صحة عنوان IP
    """
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, ip))

def is_valid_domain(domain):
    """
    التحقق من صحة اسم المجال
    """
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))

def resolve_host(host):
    """
    تحليل اسم المضيف إلى عنوان IP
    """
    try:
        if is_valid_ip(host):
            return host
        else:
            return socket.gethostbyname(host)
    except socket.gaierror:
        return None

def check_http_https(host):
    """
    التحقق من توفر HTTP و HTTPS للمضيف
    """
    results = {}
    
    # التحقق من HTTP
    try:
        response = requests.get(f"http://{host}", timeout=5, verify=False)
        results["http"] = {
            "available": True,
            "status_code": response.status_code,
            "server": response.headers.get("Server", "Unknown")
        }
    except requests.RequestException:
        results["http"] = {"available": False}
    
    # التحقق من HTTPS
    try:
        response = requests.get(f"https://{host}", timeout=5, verify=False)
        results["https"] = {
            "available": True,
            "status_code": response.status_code,
            "server": response.headers.get("Server", "Unknown")
        }
    except requests.RequestException:
        results["https"] = {"available": False}
    
    return results

def run_command(command):
    """
    تنفيذ أمر وإرجاع النتيجة
    """
    try:
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        return {
            "success": process.returncode == 0,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "returncode": process.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def print_status(message, status="info"):
    """
    طباعة رسالة حالة ملونة
    """
    if status == "info":
        print(f"{Fore.BLUE}[*] {message}{Style.RESET_ALL}")
    elif status == "success":
        print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")
    elif status == "warning":
        print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")
    elif status == "error":
        print(f"{Fore.RED}[!] {message}{Style.RESET_ALL}")
    else:
        print(f"[*] {message}")

if __name__ == "__main__":
    # اختبار الوحدة
    print_status("اختبار الدوال المساعدة", "info")
    print_status("تم تنفيذ العملية بنجاح", "success")
    print_status("تحذير: قد تكون هناك مشكلة", "warning")
    print_status("خطأ: فشلت العملية", "error")