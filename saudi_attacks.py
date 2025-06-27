#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SaudiAttacks - أداة اختبار اختراق آلي

تم تطويرها بواسطة: Saudi Linux
البريد الإلكتروني: SaudiLinux7@gmail.com

وصف: أداة لإدارة سطح الهجوم وتحديد الثغرات الأمنية في أنظمة الكمبيوتر والشبكات والتطبيقات
"""

import os
import sys
import argparse
import datetime
import platform
from colorama import init, Fore, Style
from modules.banner import display_banner, display_target_info
from modules.info_gathering import InfoGathering
from modules.vulnerability_scanner import VulnerabilityScanner
from modules.web_scanner import WebScanner
from modules.cms_scanner import CMSScanner
from modules.port_scanner import PortScanner
from modules.report_generator import ReportGenerator
from modules.utils import check_root, check_dependencies, setup_logging, print_status

# تهيئة colorama للألوان
init(autoreset=True)

def main():
    """
    الدالة الرئيسية للبرنامج
    """
    # التحقق من نظام التشغيل
    if platform.system() != "Linux":
        print(f"{Fore.YELLOW}[!] تحذير: هذه الأداة مصممة للعمل على نظام لينكس فقط.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] قد تواجه مشاكل عند تشغيلها على {platform.system()}.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] سنحاول تشغيل الأداة على {platform.system()} على الرغم من ذلك.{Style.RESET_ALL}")
    
    # عرض الشعار
    display_banner()
    
    # التحقق من صلاحيات الجذر
    if not check_root():
        if platform.system() == "Windows":
            print(f"{Fore.YELLOW}[!] تحذير: يفضل تشغيل هذه الأداة بصلاحيات المسؤول على نظام Windows.{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] سنحاول المتابعة على الرغم من ذلك.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] يجب تشغيل هذه الأداة بصلاحيات الجذر (root).{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] جرب: sudo python3 {os.path.basename(__file__)}{Style.RESET_ALL}")
            sys.exit(1)
    
    # التحقق من المتطلبات
    check_dependencies()
    
    # إعداد السجلات
    logger = setup_logging()
    
    # إعداد محلل الوسيطات
    parser = argparse.ArgumentParser(
        description="SaudiAttacks - أداة اختبار اختراق آلي",
        epilog="مثال: sudo python3 saudi_attacks.py -t 192.168.1.1 -p"
    )
    
    # إضافة الوسيطات
    parser.add_argument("-t", "--target", help="الهدف (IP، نطاق IP، اسم المجال)")
    parser.add_argument("-f", "--file", help="ملف يحتوي على قائمة الأهداف")
    parser.add_argument("-p", "--ports", action="store_true", help="فحص المنافذ")
    parser.add_argument("-w", "--web", action="store_true", help="فحص خادم الويب وتطبيقات الويب")
    parser.add_argument("-wp", "--wordpress", action="store_true", help="فحص ثغرات ووردبريس")
    parser.add_argument("-j", "--joomla", action="store_true", help="فحص ثغرات جوملا")
    parser.add_argument("-v", "--vuln", action="store_true", help="فحص الثغرات الأمنية")
    parser.add_argument("-a", "--all", action="store_true", help="تنفيذ جميع عمليات الفحص")
    parser.add_argument("-o", "--output", help="اسم ملف التقرير (الافتراضي: report_<timestamp>.html)")
    parser.add_argument("-q", "--quiet", action="store_true", help="وضع الصمت (عرض النتائج النهائية فقط)")
    parser.add_argument("-d", "--debug", action="store_true", help="وضع التصحيح (عرض معلومات إضافية)")
    
    args = parser.parse_args()
    
    # التحقق من وجود هدف
    if not args.target and not args.file:
        parser.print_help()
        print(f"\n{Fore.RED}[!] يجب تحديد هدف باستخدام -t أو -f{Style.RESET_ALL}")
        sys.exit(1)
    
    # تحديد الأهداف
    targets = []
    if args.target:
        targets.append(args.target)
    
    if args.file:
        if not os.path.isfile(args.file):
            print(f"{Fore.RED}[!] الملف {args.file} غير موجود{Style.RESET_ALL}")
            sys.exit(1)
        with open(args.file, 'r') as f:
            targets.extend([line.strip() for line in f if line.strip()])
    
    # تحديد اسم ملف التقرير
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = args.output if args.output else f"report_{timestamp}.html"
    
    # إنشاء كائن مولد التقارير
    report_gen = ReportGenerator("multiple_targets", output_file, logger, args.quiet, args.debug)
    
    # تنفيذ عمليات الفحص لكل هدف
    for target in targets:
        print(f"\n{Fore.GREEN}[+] بدء الفحص للهدف: {target}{Style.RESET_ALL}")
        logger.info(f"بدء الفحص للهدف: {target}")
        
        # جمع المعلومات
        info_gatherer = InfoGathering(target, logger, args.quiet, args.debug)
        info_results = info_gatherer.gather_all()
        report_gen.add_results(f"info_{target}", info_results)
        
        # فحص المنافذ
        if args.ports or args.all:
            try:
                port_scanner = PortScanner(target, logger, args.quiet, args.debug)
                port_results = port_scanner.scan()
                if "error" in port_results and "Nmap" in port_results["error"]:
                    if not args.quiet:
                        print_status(f"تخطي فحص المنافذ بسبب عدم توفر Nmap: {port_results['error']}", "warning")
                    logger.warning(f"تخطي فحص المنافذ بسبب عدم توفر Nmap: {port_results['error']}")
                else:
                    report_gen.add_results(f"ports_{target}", port_results)
            except Exception as e:
                if not args.quiet:
                    print_status(f"خطأ أثناء فحص المنافذ: {str(e)}", "error")
                logger.error(f"خطأ أثناء فحص المنافذ: {str(e)}")
        
        # فحص الثغرات
        if args.vuln or args.all:
            vuln_scanner = VulnerabilityScanner(target, logger, args.quiet, args.debug)
            vuln_results = vuln_scanner.scan()
            report_gen.add_results(f"vuln_{target}", vuln_results)
        
        # فحص خادم الويب
        if args.web or args.all:
            web_scanner = WebScanner(target, logger, args.quiet, args.debug)
            web_results = web_scanner.scan()
            report_gen.add_results(f"web_{target}", web_results)
        
        # فحص أنظمة إدارة المحتوى
        cms_scanner = CMSScanner(target, logger, args.quiet, args.debug)
        
        # فحص ووردبريس
        if args.wordpress or args.all:
            wp_results = cms_scanner.scan_wordpress()
            report_gen.add_results(f"wordpress_{target}", wp_results)
        
        # فحص جوملا
        if args.joomla or args.all:
            joomla_results = cms_scanner.scan_joomla()
            report_gen.add_results(f"joomla_{target}", joomla_results)
    
    # إنشاء التقرير النهائي
    report_gen.generate_report()
    print(f"\n{Fore.GREEN}[+] تم إنشاء التقرير: {output_file}{Style.RESET_ALL}")
    logger.info(f"تم إنشاء التقرير: {output_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] تم إيقاف البرنامج بواسطة المستخدم{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] حدث خطأ: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)