#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة عرض شعار البرنامج
"""

from colorama import Fore, Style
import random
import platform
import datetime

def display_banner():
    """
    عرض شعار البرنامج
    """
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    selected_color = random.choice(colors)
    
    banner = f"""
{selected_color}
  ██████  ▄▄▄       █    ██ ▓█████▄  ██▓    ▄▄▄     ▄▄▄█████▓▄▄▄█████▓ ▄▄▄       ▄████▄   ██ ▄█▀  ██████ 
▒██    ▒ ▒████▄     ██  ▓██▒▒██▀ ██▌▓██▒   ▒████▄   ▓  ██▒ ▓▒▓  ██▒ ▓▒▒████▄    ▒██▀ ▀█   ██▄█▒ ▒██    ▒ 
░ ▓██▄   ▒██  ▀█▄  ▓██  ▒██░░██   █▌▒██░   ▒██  ▀█▄ ▒ ▓██░ ▒░▒ ▓██░ ▒░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ░ ▓██▄   
  ▒   ██▒░██▄▄▄▄██ ▓▓█  ░██░░▓█▄   ▌▒██░   ░██▄▄▄▄██░ ▓██▓ ░ ░ ▓██▓ ░ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄   ▒   ██▒
▒██████▒▒ ▓█   ▓██▒▒█████▓ ░▒████▓ ░██████▒▓█   ▓██▒ ▒██▒ ░   ▒██▒ ░  ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄▒██████▒▒
▒ ▒▓▒ ▒ ░ ▒▒   ▓▒█░▒▓▒ ▒ ▒  ▒▒▓  ▒ ░ ▒░▓  ░▒▒   ▓▒█░ ▒ ░░     ▒ ░░    ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒▒ ▒▓▒ ▒ ░
░ ░▒  ░ ░  ▒   ▒▒ ░░▒░ ░ ░  ░ ▒  ▒ ░ ░ ▒  ░ ▒   ▒▒ ░   ░        ░      ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░░ ░▒  ░ ░
░  ░  ░    ░   ▒   ░░░ ░ ░  ░ ░  ░   ░ ░    ░   ▒    ░        ░        ░   ▒   ░        ░ ░░ ░ ░  ░  ░  
      ░        ░  ░  ░        ░        ░  ░     ░  ░                       ░  ░░ ░      ░  ░         ░  
                            ░                                                   ░                        
{Style.RESET_ALL}"""
    
    print(banner)
    print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  SaudiAttacks - أداة اختبار اختراق آلي{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  المطور: Saudi Linux | البريد الإلكتروني: SaudiLinux7@gmail.com{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  النظام: {platform.system()} {platform.release()} | التاريخ: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")

def display_target_info(target):
    """
    عرض معلومات الهدف
    """
    print(f"{Fore.YELLOW}[*] الهدف: {target}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] وقت البدء: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] نوع الفحص: اختبار اختراق آلي{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    # اختبار الوحدة
    display_banner()
    display_target_info("example.com")