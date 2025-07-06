# دليل تثبيت أداة SaudiAttacks

هذا الدليل يوضح خطوات تثبيت أداة SaudiAttacks على أنظمة Linux و Windows.

## المتطلبات الأساسية

- Python 3.6 أو أحدث
- Nmap
- حزم Python المطلوبة (مذكورة في ملف requirements.txt)

## تثبيت المتطلبات الأساسية

### على نظام Linux

#### تثبيت Python

```bash
# على توزيعات Debian/Ubuntu
sudo apt update
sudo apt install python3 python3-pip python3-venv

# على توزيعات Fedora
sudo dnf install python3 python3-pip

# على توزيعات Arch Linux
sudo pacman -S python python-pip
```

#### تثبيت Nmap

```bash
# على توزيعات Debian/Ubuntu
sudo apt install nmap

# على توزيعات Fedora
sudo dnf install nmap

# على توزيعات Arch Linux
sudo pacman -S nmap
```

### على نظام Windows

#### الطريقة السريعة: استخدام سكريبت التثبيت التلقائي

1. قم بتنزيل أو استنساخ المستودع
2. انقر بزر الماوس الأيمن على ملف `install.bat` واختر "Run as administrator" (تشغيل كمسؤول)
3. سيقوم السكريبت تلقائيًا بتثبيت جميع المتطلبات بما في ذلك:
   - تثبيت Chocolatey (مدير حزم لنظام Windows)
   - تثبيت Python 3
   - تثبيت Nmap
   - إنشاء بيئة Python افتراضية
   - تثبيت جميع مكتبات Python المطلوبة
   - إنشاء ملف تشغيل سهل الاستخدام

#### الطريقة اليدوية: تثبيت المتطلبات يدويًا

##### تثبيت Python

1. قم بتنزيل أحدث إصدار من Python من [الموقع الرسمي](https://www.python.org/downloads/windows/)
2. قم بتشغيل المثبت وتأكد من تحديد خيار "Add Python to PATH"
3. اتبع تعليمات المثبت لإكمال عملية التثبيت

##### تثبيت Nmap

1. قم بتنزيل أحدث إصدار من Nmap من [الموقع الرسمي](https://nmap.org/download.html)
2. قم بتشغيل المثبت واتبع التعليمات لإكمال عملية التثبيت
3. تأكد من إضافة Nmap إلى متغير PATH في نظام Windows

## طرق تثبيت أداة SaudiAttacks

### الطريقة 1: التثبيت من مستودع GitHub

```bash
# استنساخ المستودع
git clone https://github.com/SaudiLinux/Saudi-Attacks.git
cd Saudi-Attacks

# إنشاء بيئة افتراضية (اختياري ولكن موصى به)
python3 -m venv venv
source venv/bin/activate  # على Linux
# أو
venv\Scripts\activate  # على Windows

# تثبيت المتطلبات
pip install -r requirements.txt
```

### الطريقة 2: التثبيت باستخدام pip

```bash
pip install saudi-attacks
```

### الطريقة 3: التثبيت من الكود المصدري

```bash
# استنساخ المستودع
git clone https://github.com/SaudiLinux/Saudi-Attacks.git
cd Saudi-Attacks

# تثبيت الحزمة
pip install -e .
```

## التحقق من التثبيت

### على نظام Linux

بعد الانتهاء من التثبيت، يمكنك التحقق من نجاح العملية بتنفيذ الأمر التالي:

```bash
saudi-attacks --help
```

أو إذا قمت بالتثبيت من المستودع مباشرة:

```bash
python saudi_attacks.py --help
```

### على نظام Windows

إذا قمت بالتثبيت باستخدام سكريبت التثبيت التلقائي:

```cmd
saudi-attacks.bat --help
```

أو إذا قمت بإضافة المجلد إلى متغير PATH أثناء التثبيت:

```cmd
saudi-attacks --help
```

أو يمكنك تشغيل الأداة مباشرة من المجلد:

```cmd
cd C:\path\to\Saudi-Attacks
.\saudi-attacks.bat --help
```

يجب أن ترى قائمة بالخيارات المتاحة والتعليمات الخاصة باستخدام الأداة.

## استكشاف الأخطاء وإصلاحها

### مشكلات شائعة على Linux

- **خطأ في الصلاحيات**: تأكد من تشغيل الأداة بصلاحيات الجذر (root) عند الحاجة لذلك.
  ```bash
  sudo saudi-attacks [الخيارات]
  ```

- **مشكلات في تثبيت المكتبات**: قد تحتاج إلى تثبيت بعض حزم التطوير.
  ```bash
  sudo apt install python3-dev libssl-dev libffi-dev  # على Debian/Ubuntu
  ```

### مشكلات شائعة على Windows

- **مشكلات في تشغيل سكريبت التثبيت**: تأكد من تشغيل ملف `install.bat` بصلاحيات المسؤول (Run as administrator).

- **مشكلات في تفعيل البيئة الافتراضية**: إذا واجهت خطأ عند تفعيل البيئة الافتراضية، قم بتنفيذ الأمر التالي في PowerShell بصلاحيات المسؤول:
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- **مشكلات في تشغيل Nmap**: تأكد من إضافة Nmap إلى متغير PATH في نظام Windows.

- **مشكلات في تثبيت المكتبات**: قد تحتاج إلى تثبيت أدوات البناء لبعض المكتبات.
  ```powershell
  python -m pip install --upgrade setuptools wheel
  ```

- **مشكلات في تثبيت Chocolatey**: إذا فشل تثبيت Chocolatey، يمكنك تثبيته يدويًا باتباع التعليمات في [الموقع الرسمي](https://chocolatey.org/install).

- **مشكلات في تنفيذ الأداة**: إذا واجهت مشكلة في تنفيذ الأداة بعد التثبيت، جرب تشغيلها مباشرة من خلال Python:
  ```cmd
  cd C:\path\to\Saudi-Attacks
  .\venv\Scripts\python.exe saudi_attacks.py --help
  ```

## الخطوات التالية

بعد التثبيت بنجاح، يمكنك الرجوع إلى [README.md](README.md) للحصول على معلومات حول كيفية استخدام الأداة والخيارات المتاحة.