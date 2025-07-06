#!/usr/bin/env pwsh

# SaudiAttacks Installation Script
# Author: Saudi Linux (SaudiLinux7@gmail.com)

# Colors
$RED = "\e[31m"
$GREEN = "\e[32m"
$YELLOW = "\e[33m"
$BLUE = "\e[34m"
$MAGENTA = "\e[35m"
$CYAN = "\e[36m"
$NC = "\e[0m" # No Color

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "${RED}[!] يجب تشغيل هذا السكربت بصلاحيات المسؤول${NC}"
    Write-Host "${YELLOW}[i] الرجاء تشغيله كمسؤول (Run as Administrator)${NC}"
    exit 1
}

Write-Host "${BLUE}==================================================${NC}"
Write-Host "${CYAN}        تثبيت أداة SaudiAttacks        ${NC}"
Write-Host "${CYAN}        المطور: Saudi Linux        ${NC}"
Write-Host "${CYAN}        البريد: SaudiLinux7@gmail.com        ${NC}"
Write-Host "${BLUE}==================================================${NC}"

# Create directories
Write-Host "${YELLOW}[+] إنشاء المجلدات اللازمة...${NC}"
New-Item -ItemType Directory -Force -Path logs, reports | Out-Null

# Install system dependencies
Write-Host "${YELLOW}[+] تثبيت متطلبات النظام...${NC}"
Write-Host "${GREEN}[i] تم اكتشاف نظام Windows${NC}"

# Check if Chocolatey is installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "${YELLOW}[+] تثبيت Chocolatey...${NC}"
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    # Refresh environment variables
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Install required packages using Chocolatey
Write-Host "${YELLOW}[+] تثبيت البرامج المطلوبة...${NC}"
choco install -y python3 nmap

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Set up Python virtual environment
Write-Host "${YELLOW}[+] إعداد بيئة Python الافتراضية...${NC}"
python -m venv venv

# Activate virtual environment
Write-Host "${YELLOW}[+] تفعيل البيئة الافتراضية...${NC}"
.\venv\Scripts\Activate.ps1

# Install Python dependencies
Write-Host "${YELLOW}[+] تثبيت متطلبات Python...${NC}"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Create a batch file for easy execution
Write-Host "${YELLOW}[+] إنشاء ملف تشغيل للأداة...${NC}"
$batchContent = @"
@echo off
@REM SaudiAttacks Launcher
cd /d "%~dp0"
.\venv\Scripts\python.exe saudi_attacks.py %*
"@

Set-Content -Path "saudi-attacks.bat" -Value $batchContent

# Add to PATH (optional)
$addToPath = Read-Host "${YELLOW}هل تريد إضافة الأداة إلى متغير PATH لتتمكن من تشغيلها من أي مكان؟ (y/n)${NC}"
if ($addToPath -eq "y") {
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $scriptDir = (Get-Location).Path
    if (-not $currentPath.Contains($scriptDir)) {
        [Environment]::SetEnvironmentVariable("Path", $currentPath + ";" + $scriptDir, "User")
        Write-Host "${GREEN}[✓] تمت إضافة المجلد إلى متغير PATH${NC}"
    } else {
        Write-Host "${YELLOW}[i] المجلد موجود بالفعل في متغير PATH${NC}"
    }
}

Write-Host "${GREEN}[✓] تم تثبيت أداة SaudiAttacks بنجاح!${NC}"
Write-Host "${BLUE}==================================================${NC}"
Write-Host "${CYAN}للاستخدام، قم بتشغيل:${NC}"
Write-Host "${YELLOW}.\saudi-attacks.bat --help${NC}"
Write-Host "${BLUE}==================================================${NC}"