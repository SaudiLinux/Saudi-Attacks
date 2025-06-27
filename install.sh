#!/bin/bash

# SaudiAttacks Installation Script
# Author: Saudi Linux (SaudiLinux7@gmail.com)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo -e "${RED}[!] يجب تشغيل هذا السكربت بصلاحيات الجذر (root)${NC}"
    echo -e "${YELLOW}[i] الرجاء تشغيله باستخدام sudo${NC}"
    exit 1
fi

# Check if running on Linux
if [ "$(uname)" != "Linux" ]; then
    echo -e "${RED}[!] هذه الأداة مصممة للعمل على نظام لينكس فقط${NC}"
    exit 1
fi

echo -e "${BLUE}==================================================${NC}"
echo -e "${CYAN}        تثبيت أداة SaudiAttacks        ${NC}"
echo -e "${CYAN}        المطور: Saudi Linux        ${NC}"
echo -e "${CYAN}        البريد: SaudiLinux7@gmail.com        ${NC}"
echo -e "${BLUE}==================================================${NC}"

# Create directories
echo -e "${YELLOW}[+] إنشاء المجلدات اللازمة...${NC}"
mkdir -p logs reports
chmod 755 logs reports

# Install system dependencies
echo -e "${YELLOW}[+] تثبيت متطلبات النظام...${NC}"

# Detect package manager
if [ -x "$(command -v apt-get)" ]; then
    # Debian/Ubuntu
    echo -e "${GREEN}[i] تم اكتشاف نظام Debian/Ubuntu${NC}"
    apt-get update
    apt-get install -y python3 python3-pip python3-venv nmap whois host dnsutils libssl-dev libffi-dev build-essential
elif [ -x "$(command -v dnf)" ]; then
    # Fedora/RHEL/CentOS 8+
    echo -e "${GREEN}[i] تم اكتشاف نظام Fedora/RHEL/CentOS${NC}"
    dnf install -y python3 python3-pip python3-devel nmap whois bind-utils openssl-devel libffi-devel gcc
elif [ -x "$(command -v yum)" ]; then
    # CentOS/RHEL
    echo -e "${GREEN}[i] تم اكتشاف نظام CentOS/RHEL${NC}"
    yum install -y python3 python3-pip python3-devel nmap whois bind-utils openssl-devel libffi-devel gcc
elif [ -x "$(command -v pacman)" ]; then
    # Arch Linux
    echo -e "${GREEN}[i] تم اكتشاف نظام Arch Linux${NC}"
    pacman -Sy --noconfirm python python-pip nmap whois bind openssl libffi
elif [ -x "$(command -v zypper)" ]; then
    # openSUSE
    echo -e "${GREEN}[i] تم اكتشاف نظام openSUSE${NC}"
    zypper install -y python3 python3-pip python3-devel nmap whois bind-utils libopenssl-devel libffi-devel gcc
else
    echo -e "${RED}[!] لم يتم التعرف على مدير الحزم. الرجاء تثبيت المتطلبات يدويًا:${NC}"
    echo -e "${YELLOW}python3, python3-pip, nmap, whois, host/dig utilities${NC}"
fi

# Set up Python virtual environment
echo -e "${YELLOW}[+] إعداد بيئة Python الافتراضية...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}[+] تثبيت متطلبات Python...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Make the main script executable
echo -e "${YELLOW}[+] جعل السكربت الرئيسي قابل للتنفيذ...${NC}"
chmod +x saudi_attacks.py

# Create symbolic link to /usr/local/bin
echo -e "${YELLOW}[+] إنشاء رابط رمزي في /usr/local/bin...${NC}"
ln -sf "$(pwd)/saudi_attacks.py" /usr/local/bin/saudi-attacks

echo -e "${GREEN}[✓] تم تثبيت أداة SaudiAttacks بنجاح!${NC}"
echo -e "${BLUE}==================================================${NC}"
echo -e "${CYAN}للاستخدام، قم بتشغيل:${NC}"
echo -e "${YELLOW}saudi-attacks --help${NC}"
echo -e "${BLUE}==================================================${NC}"