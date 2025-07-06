@echo off
REM SaudiAttacks Installation Script Launcher
REM This batch file launches the PowerShell installation script

echo تشغيل سكريبت تثبيت أداة SaudiAttacks...

REM Check if running as administrator
powershell -Command "&{[bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match 'S-1-5-32-544')}" > %TEMP%\isadmin.txt
set /p isadmin=<%TEMP%\isadmin.txt
del %TEMP%\isadmin.txt

if "%isadmin%"=="False" (
    echo يجب تشغيل هذا السكريبت بصلاحيات المسؤول.
    echo الرجاء النقر بزر الماوس الأيمن على الملف واختيار "Run as administrator".
    pause
    exit /b 1
)

REM Run the PowerShell installation script
powershell -ExecutionPolicy Bypass -File "%~dp0install.sh"

pause