# دليل استكشاف الأخطاء وإصلاحها

يوفر هذا الدليل حلولاً للمشكلات الشائعة التي قد تواجهها أثناء تثبيت أو استخدام أداة SaudiAttacks.

## جدول المحتويات

- [مشكلات التثبيت](#مشكلات-التثبيت)
- [مشكلات التشغيل](#مشكلات-التشغيل)
- [مشكلات الفحص](#مشكلات-الفحص)
- [مشكلات التقارير](#مشكلات-التقارير)
- [مشكلات متعلقة بنظام التشغيل](#مشكلات-متعلقة-بنظام-التشغيل)
- [الأسئلة الشائعة](#الأسئلة-الشائعة)

## مشكلات التثبيت

### خطأ في تثبيت المتطلبات

**المشكلة**: فشل في تثبيت المتطلبات من ملف requirements.txt.

**الحل**:
1. تأكد من تثبيت Python 3.6 أو أحدث:
   ```bash
   python --version
   ```

2. حاول تحديث pip:
   ```bash
   python -m pip install --upgrade pip
   ```

3. قم بتثبيت كل حزمة على حدة للتعرف على الحزمة التي تسبب المشكلة:
   ```bash
   pip install <اسم_الحزمة>
   ```

4. إذا كنت تواجه مشكلة مع حزمة معينة تتطلب مكتبات تطوير، قم بتثبيتها:
   - على Ubuntu/Debian:
     ```bash
     sudo apt-get install python3-dev libxml2-dev libxslt1-dev
     ```
   - على CentOS/RHEL:
     ```bash
     sudo yum install python3-devel libxml2-devel libxslt-devel
     ```
   - على Windows:
     تأكد من تثبيت Visual C++ Build Tools.

### خطأ "Command 'pip' not found"

**المشكلة**: عدم العثور على أمر pip.

**الحل**:
1. تثبيت pip:
   - على Linux:
     ```bash
     sudo apt-get install python3-pip  # Ubuntu/Debian
     sudo yum install python3-pip      # CentOS/RHEL
     ```
   - على Windows:
     قم بتنزيل وتثبيت Python من [الموقع الرسمي](https://www.python.org/downloads/) مع تحديد خيار تثبيت pip.

2. أو استخدم الطريقة البديلة:
   ```bash
   python -m ensurepip --default-pip
   ```

### خطأ في تثبيت Nmap

**المشكلة**: عدم القدرة على تثبيت Nmap أو عدم العثور عليه بعد التثبيت.

**الحل**:
1. تثبيت Nmap:
   - على Linux:
     ```bash
     sudo apt-get install nmap  # Ubuntu/Debian
     sudo yum install nmap      # CentOS/RHEL
     ```
   - على Windows:
     قم بتنزيل وتثبيت Nmap من [الموقع الرسمي](https://nmap.org/download.html).

2. تأكد من إضافة Nmap إلى متغير PATH:
   - على Windows:
     أضف مسار تثبيت Nmap (مثل `C:\Program Files (x86)\Nmap`) إلى متغير البيئة PATH.

3. تحقق من تثبيت Nmap:
   ```bash
   nmap --version
   ```

## مشكلات التشغيل

### خطأ "Permission denied"

**المشكلة**: رسالة خطأ "Permission denied" عند تشغيل الأداة.

**الحل**:
1. تشغيل الأداة بصلاحيات المستخدم الجذر (على Linux):
   ```bash
   sudo python saudi_attacks.py <الهدف>
   ```

2. تشغيل موجه الأوامر بصلاحيات المسؤول (على Windows).

3. التأكد من أن الملف قابل للتنفيذ (على Linux):
   ```bash
   chmod +x saudi_attacks.py
   ```

### خطأ "ModuleNotFoundError"

**المشكلة**: رسالة خطأ "ModuleNotFoundError: No module named 'xxx'" عند تشغيل الأداة.

**الحل**:
1. تأكد من تثبيت جميع المتطلبات:
   ```bash
   pip install -r requirements.txt
   ```

2. تثبيت الوحدة المفقودة مباشرة:
   ```bash
   pip install <اسم_الوحدة>
   ```

3. تأكد من استخدام بيئة Python الصحيحة إذا كنت تستخدم بيئات افتراضية.

### خطأ في تشغيل الأداة على Windows

**المشكلة**: مشكلات متنوعة عند تشغيل الأداة على Windows.

**الحل**:
1. تأكد من تثبيت جميع المتطلبات بشكل صحيح.

2. تشغيل موجه الأوامر بصلاحيات المسؤول.

3. استخدام PowerShell بدلاً من موجه الأوامر التقليدي (CMD).

4. تعطيل برنامج مكافحة الفيروسات مؤقتاً إذا كان يعترض على عمليات الفحص.

5. تأكد من إضافة Python ومسار تثبيت Nmap إلى متغير البيئة PATH.

## مشكلات الفحص

### فشل فحص المنافذ

**المشكلة**: فشل في إجراء فحص المنافذ أو عدم ظهور نتائج.

**الحل**:
1. تأكد من تثبيت Nmap بشكل صحيح:
   ```bash
   nmap --version
   ```

2. تأكد من أن الهدف متاح ويمكن الوصول إليه:
   ```bash
   ping <الهدف>
   ```

3. تشغيل الأداة بصلاحيات المستخدم الجذر (على Linux) أو بصلاحيات المسؤول (على Windows).

4. تحديد نطاق منافذ أصغر للفحص:
   ```bash
   python saudi_attacks.py <الهدف> --ports 1-1000
   ```

5. تأكد من عدم حظر عمليات فحص المنافذ من قبل جدار الحماية أو مزود خدمة الإنترنت.

### بطء عمليات الفحص

**المشكلة**: استغراق وقت طويل لإكمال عمليات الفحص.

**الحل**:
1. تحديد نطاق منافذ أصغر للفحص.

2. استخدام وضع الفحص السريع:
   ```bash
   python saudi_attacks.py <الهدف> --fast
   ```

3. تحديد نوع فحص محدد بدلاً من الفحص الشامل:
   ```bash
   python saudi_attacks.py <الهدف> --scan-type port
   ```

4. تأكد من جودة اتصال الإنترنت.

### خطأ في فحص تطبيقات الويب

**المشكلة**: فشل في فحص تطبيقات الويب أو ظهور أخطاء.

**الحل**:
1. تأكد من أن الهدف يستضيف خدمة ويب:
   ```bash
   curl -I http://<الهدف>
   ```

2. تحديد المنفذ الصحيح لخدمة الويب:
   ```bash
   python saudi_attacks.py <الهدف> --web-port 8080
   ```

3. تأكد من عدم وجود آليات حماية تمنع عمليات الفحص مثل Web Application Firewall (WAF).

### خطأ في فحص أنظمة إدارة المحتوى

**المشكلة**: فشل في اكتشاف أو فحص نظام إدارة المحتوى (CMS).

**الحل**:
1. تأكد من أن الهدف يستخدم نظام إدارة المحتوى المحدد:
   ```bash
   python saudi_attacks.py <الهدف> --scan-type web
   ```

2. تحديد نوع نظام إدارة المحتوى يدوياً:
   ```bash
   python saudi_attacks.py <الهدف> --scan-type wordpress
   # أو
   python saudi_attacks.py <الهدف> --scan-type joomla
   ```

3. تأكد من إمكانية الوصول إلى المسارات الشائعة لنظام إدارة المحتوى:
   ```bash
   curl -I http://<الهدف>/wp-login.php  # WordPress
   curl -I http://<الهدف>/administrator  # Joomla
   ```

## مشكلات التقارير

### فشل في إنشاء التقرير

**المشكلة**: فشل في إنشاء ملف التقرير أو ظهور أخطاء أثناء توليد التقرير.

**الحل**:
1. تأكد من وجود صلاحيات كتابة في المجلد الحالي:
   - على Linux:
     ```bash
     chmod 755 .
     ```
   - على Windows:
     تأكد من تشغيل الأداة بصلاحيات المسؤول.

2. تحديد مسار مختلف لملف التقرير:
   ```bash
   python saudi_attacks.py <الهدف> --output /tmp/report.html
   # أو
   python saudi_attacks.py <الهدف> --output C:\Temp\report.html
   ```

3. تغيير تنسيق التقرير:
   ```bash
   python saudi_attacks.py <الهدف> --output report.json --format json
   ```

### مشكلات في عرض التقرير

**المشكلة**: مشكلات في عرض محتوى التقرير أو تنسيقه.

**الحل**:
1. تأكد من فتح ملف التقرير HTML باستخدام متصفح ويب حديث.

2. إذا كان التقرير بتنسيق JSON، استخدم أداة لتنسيق JSON مثل `jq` أو محرر نصوص يدعم تنسيق JSON.

3. تحقق من وجود أخطاء في ملف التقرير:
   ```bash
   cat report.html  # على Linux
   type report.html  # على Windows
   ```

## مشكلات متعلقة بنظام التشغيل

### مشكلات على Linux

**المشكلة**: مشكلات متنوعة عند تشغيل الأداة على Linux.

**الحل**:
1. تأكد من تثبيت جميع حزم التطوير المطلوبة:
   ```bash
   sudo apt-get install python3-dev libxml2-dev libxslt1-dev  # Ubuntu/Debian
   sudo yum install python3-devel libxml2-devel libxslt-devel  # CentOS/RHEL
   ```

2. تأكد من تثبيت Nmap:
   ```bash
   sudo apt-get install nmap  # Ubuntu/Debian
   sudo yum install nmap      # CentOS/RHEL
   ```

3. تشغيل الأداة بصلاحيات المستخدم الجذر:
   ```bash
   sudo python saudi_attacks.py <الهدف>
   ```

### مشكلات على Windows

**المشكلة**: مشكلات متنوعة عند تشغيل الأداة على Windows.

**الحل**:
1. تأكد من تثبيت Python بشكل صحيح وإضافته إلى متغير البيئة PATH.

2. تأكد من تثبيت Nmap وإضافته إلى متغير البيئة PATH.

3. تشغيل موجه الأوامر أو PowerShell بصلاحيات المسؤول.

4. تعطيل برنامج مكافحة الفيروسات مؤقتاً إذا كان يعترض على عمليات الفحص.

5. استخدام WSL (Windows Subsystem for Linux) لتشغيل الأداة في بيئة Linux على Windows.

## الأسئلة الشائعة

### هل يمكن استخدام الأداة بدون صلاحيات المستخدم الجذر/المسؤول؟

**الجواب**: بعض وظائف الأداة، خاصة فحص المنافذ باستخدام Nmap، تتطلب صلاحيات المستخدم الجذر على Linux أو صلاحيات المسؤول على Windows. يمكنك تشغيل بعض الوظائف الأخرى بدون هذه الصلاحيات، لكن قد تكون النتائج محدودة.

### هل يمكن استخدام الأداة على نظام macOS؟

**الجواب**: نعم، يمكن استخدام الأداة على نظام macOS. تأكد من تثبيت Python 3.6 أو أحدث وNmap. يمكنك استخدام Homebrew لتثبيت المتطلبات:
```bash
brew install python3 nmap
pip3 install -r requirements.txt
```

### هل يمكن استخدام الأداة عبر بروكسي؟

**الجواب**: نعم، يمكنك استخدام الأداة عبر بروكسي عن طريق تعيين متغيرات البيئة HTTP_PROXY وHTTPS_PROXY:
```bash
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"
python saudi_attacks.py <الهدف>
```
على Windows:
```cmd
set HTTP_PROXY=http://proxy:port
set HTTPS_PROXY=http://proxy:port
python saudi_attacks.py <الهدف>
```

### كيف يمكنني الإبلاغ عن مشكلة أو خطأ؟

**الجواب**: يمكنك الإبلاغ عن المشكلات والأخطاء عن طريق فتح issue في مستودع GitHub للمشروع. تأكد من تضمين المعلومات التالية:
- وصف المشكلة
- خطوات إعادة إنتاج المشكلة
- رسائل الخطأ (إن وجدت)
- نظام التشغيل وإصدار Python
- أي معلومات إضافية قد تساعد في تشخيص المشكلة

### هل يمكن استخدام الأداة لفحص شبكة داخلية؟

**الجواب**: نعم، يمكن استخدام الأداة لفحص أهداف في شبكة داخلية. يمكنك تحديد عنوان IP أو نطاق عناوين IP:
```bash
python saudi_attacks.py 192.168.1.1
# أو
python saudi_attacks.py 192.168.1.0/24
```

### كيف يمكنني تسريع عمليات الفحص؟

**الجواب**: يمكنك تسريع عمليات الفحص عن طريق:
- تحديد نطاق منافذ أصغر
- استخدام وضع الفحص السريع
- تحديد نوع فحص محدد بدلاً من الفحص الشامل
- تحديد عدد أقل من الأهداف

```bash
python saudi_attacks.py <الهدف> --ports 1-1000 --fast --scan-type port
```

### هل يمكن استخدام الأداة في بيئة افتراضية؟

**الجواب**: نعم، يمكن استخدام الأداة في بيئة افتراضية مثل virtualenv أو conda:
```bash
# باستخدام virtualenv
python -m venv venv
source venv/bin/activate  # على Linux
venv\Scripts\activate  # على Windows
pip install -r requirements.txt
python saudi_attacks.py <الهدف>

# باستخدام conda
conda create -n saudi-attacks python=3.8
conda activate saudi-attacks
pip install -r requirements.txt
python saudi_attacks.py <الهدف>
```