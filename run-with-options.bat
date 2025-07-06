@echo off
REM SaudiAttacks Runner with Options
REM هذا الملف يسهل تشغيل أداة SaudiAttacks مع خيارات محددة مسبقًا

setlocal EnableDelayedExpansion

REM التحقق من صلاحيات المسؤول
powershell -Command "&{[bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match 'S-1-5-32-544')}" > %TEMP%\isadmin.txt
set /p isadmin=<%TEMP%\isadmin.txt
del %TEMP%\isadmin.txt

if "%isadmin%"=="False" (
    echo [!] يجب تشغيل هذا السكريبت بصلاحيات المسؤول.
    echo [i] الرجاء النقر بزر الماوس الأيمن على الملف واختيار "Run as administrator".
    pause
    exit /b 1
)

REM التحقق من وجود البيئة الافتراضية
if not exist "%~dp0venv\Scripts\python.exe" (
    echo [!] لم يتم العثور على البيئة الافتراضية. هل قمت بتثبيت الأداة؟
    echo [i] الرجاء تشغيل سكريبت التثبيت أولاً: install.bat
    pause
    exit /b 1
)

REM عرض القائمة الرئيسية
:MENU
cls
echo =================================================
echo         قائمة تشغيل أداة SaudiAttacks        
echo =================================================
echo.
echo 1. فحص هدف محدد (IP أو اسم نطاق)
echo 2. فحص قائمة من الأهداف من ملف
echo 3. فحص شامل لهدف محدد
echo 4. فحص منافذ لهدف محدد
echo 5. فحص خادم الويب لهدف محدد
echo 6. فحص ثغرات ووردبريس لهدف محدد
echo 7. فحص ثغرات جوملا لهدف محدد
echo 8. عرض المساعدة
echo 9. خروج
echo.
echo =================================================
echo.

set /p choice=اختر رقم العملية: 

if "%choice%"=="1" goto TARGET_SCAN
if "%choice%"=="2" goto FILE_SCAN
if "%choice%"=="3" goto FULL_SCAN
if "%choice%"=="4" goto PORT_SCAN
if "%choice%"=="5" goto WEB_SCAN
if "%choice%"=="6" goto WP_SCAN
if "%choice%"=="7" goto JOOMLA_SCAN
if "%choice%"=="8" goto HELP
if "%choice%"=="9" goto EXIT

echo.
echo [!] اختيار غير صحيح. الرجاء المحاولة مرة أخرى.
echo.
pause
goto MENU

:TARGET_SCAN
cls
echo =================================================
echo         فحص هدف محدد        
echo =================================================
echo.
set /p target=أدخل الهدف (IP أو اسم نطاق): 
echo.
echo اختر نوع الفحص:
echo 1. فحص المنافذ
echo 2. فحص خادم الويب
echo 3. فحص الثغرات الأمنية
echo 4. فحص المنافذ وخادم الويب
echo 5. فحص شامل
echo.
set /p scan_type=اختر رقم نوع الفحص: 

if "%scan_type%"=="1" (
    echo.
    echo جاري تنفيذ فحص المنافذ للهدف !target!...
    echo.
    call "%~dp0saudi-attacks.bat" -t !target! -p
)
if "%scan_type%"=="2" (
    echo.
    echo جاري تنفيذ فحص خادم الويب للهدف !target!...
    echo.
    call "%~dp0saudi-attacks.bat" -t !target! -w
)
if "%scan_type%"=="3" (
    echo.
    echo جاري تنفيذ فحص الثغرات الأمنية للهدف !target!...
    echo.
    call "%~dp0saudi-attacks.bat" -t !target! -v
)
if "%scan_type%"=="4" (
    echo.
    echo جاري تنفيذ فحص المنافذ وخادم الويب للهدف !target!...
    echo.
    call "%~dp0saudi-attacks.bat" -t !target! -p -w
)
if "%scan_type%"=="5" (
    echo.
    echo جاري تنفيذ فحص شامل للهدف !target!...
    echo.
    call "%~dp0saudi-attacks.bat" -t !target! -a
)

echo.
pause
goto MENU

:FILE_SCAN
cls
echo =================================================
echo         فحص قائمة من الأهداف من ملف        
echo =================================================
echo.
set /p file_path=أدخل مسار الملف الذي يحتوي على قائمة الأهداف: 

if not exist "!file_path!" (
    echo.
    echo [!] الملف غير موجود. الرجاء التحقق من المسار.
    echo.
    pause
    goto MENU
)

echo.
echo اختر نوع الفحص:
echo 1. فحص المنافذ
echo 2. فحص خادم الويب
echo 3. فحص الثغرات الأمنية
echo 4. فحص المنافذ وخادم الويب
echo 5. فحص شامل
echo.
set /p scan_type=اختر رقم نوع الفحص: 

if "%scan_type%"=="1" (
    echo.
    echo جاري تنفيذ فحص المنافذ للأهداف في الملف !file_path!...
    echo.
    call "%~dp0saudi-attacks.bat" -f "!file_path!" -p
)
if "%scan_type%"=="2" (
    echo.
    echo جاري تنفيذ فحص خادم الويب للأهداف في الملف !file_path!...
    echo.
    call "%~dp0saudi-attacks.bat" -f "!file_path!" -w
)
if "%scan_type%"=="3" (
    echo.
    echo جاري تنفيذ فحص الثغرات الأمنية للأهداف في الملف !file_path!...
    echo.
    call "%~dp0saudi-attacks.bat" -f "!file_path!" -v
)
if "%scan_type%"=="4" (
    echo.
    echo جاري تنفيذ فحص المنافذ وخادم الويب للأهداف في الملف !file_path!...
    echo.
    call "%~dp0saudi-attacks.bat" -f "!file_path!" -p -w
)
if "%scan_type%"=="5" (
    echo.
    echo جاري تنفيذ فحص شامل للأهداف في الملف !file_path!...
    echo.
    call "%~dp0saudi-attacks.bat" -f "!file_path!" -a
)

echo.
pause
goto MENU

:FULL_SCAN
cls
echo =================================================
echo         فحص شامل لهدف محدد        
echo =================================================
echo.
set /p target=أدخل الهدف (IP أو اسم نطاق): 

echo.
echo جاري تنفيذ فحص شامل للهدف !target!...
echo.
call "%~dp0saudi-attacks.bat" -t !target! -a

echo.
pause
goto MENU

:PORT_SCAN
cls
echo =================================================
echo         فحص منافذ لهدف محدد        
echo =================================================
echo.
set /p target=أدخل الهدف (IP أو اسم نطاق): 

echo.
echo جاري تنفيذ فحص المنافذ للهدف !target!...
echo.
call "%~dp0saudi-attacks.bat" -t !target! -p

echo.
pause
goto MENU

:WEB_SCAN
cls
echo =================================================
echo         فحص خادم الويب لهدف محدد        
echo =================================================
echo.
set /p target=أدخل الهدف (IP أو اسم نطاق): 

echo.
echo جاري تنفيذ فحص خادم الويب للهدف !target!...
echo.
call "%~dp0saudi-attacks.bat" -t !target! -w

echo.
pause
goto MENU

:WP_SCAN
cls
echo =================================================
echo         فحص ثغرات ووردبريس لهدف محدد        
echo =================================================
echo.
set /p target=أدخل الهدف (IP أو اسم نطاق): 

echo.
echo جاري تنفيذ فحص ثغرات ووردبريس للهدف !target!...
echo.
call "%~dp0saudi-attacks.bat" -t !target! -wp

echo.
pause
goto MENU

:JOOMLA_SCAN
cls
echo =================================================
echo         فحص ثغرات جوملا لهدف محدد        
echo =================================================
echo.
set /p target=أدخل الهدف (IP أو اسم نطاق): 

echo.
echo جاري تنفيذ فحص ثغرات جوملا للهدف !target!...
echo.
call "%~dp0saudi-attacks.bat" -t !target! -j

echo.
pause
goto MENU

:HELP
cls
echo =================================================
echo         مساعدة أداة SaudiAttacks        
echo =================================================
echo.
call "%~dp0saudi-attacks.bat" --help

echo.
pause
goto MENU

:EXIT
cls
echo =================================================
echo         شكرًا لاستخدام أداة SaudiAttacks        
echo =================================================
echo.
echo تم تطويرها بواسطة: Saudi Linux
echo البريد الإلكتروني: SaudiLinux7@gmail.com
echo.
echo =================================================

endlocal
exit /b 0