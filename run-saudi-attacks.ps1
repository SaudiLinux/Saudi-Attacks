# SaudiAttacks Runner Script
# هذا السكريبت يسهل تشغيل أداة SaudiAttacks على نظام Windows

# تحقق من صلاحيات المسؤول
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[!] يجب تشغيل هذا السكريبت بصلاحيات المسؤول" -ForegroundColor Red
    Write-Host "[i] الرجاء تشغيله كمسؤول (Run as Administrator)" -ForegroundColor Yellow
    exit 1
}

# تحقق من وجود البيئة الافتراضية
if (-not (Test-Path "$PSScriptRoot\venv\Scripts\python.exe")) {
    Write-Host "[!] لم يتم العثور على البيئة الافتراضية. هل قمت بتثبيت الأداة؟" -ForegroundColor Red
    Write-Host "[i] الرجاء تشغيل سكريبت التثبيت أولاً: install.bat" -ForegroundColor Yellow
    exit 1
}

# تحقق من وجود ملف saudi_attacks.py
if (-not (Test-Path "$PSScriptRoot\saudi_attacks.py")) {
    Write-Host "[!] لم يتم العثور على ملف saudi_attacks.py" -ForegroundColor Red
    exit 1
}

# عرض شعار الأداة
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "        تشغيل أداة SaudiAttacks        " -ForegroundColor Green
Write-Host "        المطور: Saudi Linux        " -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan

# إذا لم يتم تمرير أي وسيطات، عرض المساعدة
if ($args.Count -eq 0) {
    Write-Host "[i] لم يتم تحديد أي وسيطات. عرض المساعدة..." -ForegroundColor Yellow
    & "$PSScriptRoot\venv\Scripts\python.exe" "$PSScriptRoot\saudi_attacks.py" --help
    exit 0
}

# تشغيل الأداة مع تمرير الوسيطات
Write-Host "[+] جاري تشغيل الأداة..." -ForegroundColor Green
& "$PSScriptRoot\venv\Scripts\python.exe" "$PSScriptRoot\saudi_attacks.py" $args

# عرض رسالة الانتهاء
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "        تم الانتهاء من تنفيذ الأداة        " -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan