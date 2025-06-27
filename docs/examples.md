# أمثلة عملية لاستخدام أداة SaudiAttacks

يوفر هذا المستند أمثلة عملية لاستخدام أداة SaudiAttacks في سيناريوهات مختلفة. ستساعدك هذه الأمثلة على فهم كيفية استخدام الأداة بشكل فعال لمختلف أنواع الفحوصات الأمنية.

## جدول المحتويات

- [الفحص الأساسي](#الفحص-الأساسي)
- [فحص المنافذ](#فحص-المنافذ)
- [فحص تطبيقات الويب](#فحص-تطبيقات-الويب)
- [فحص أنظمة إدارة المحتوى](#فحص-أنظمة-إدارة-المحتوى)
- [فحص عدة أهداف](#فحص-عدة-أهداف)
- [توليد تقارير مخصصة](#توليد-تقارير-مخصصة)
- [سيناريوهات متقدمة](#سيناريوهات-متقدمة)

## الفحص الأساسي

### مثال 1: فحص شامل لهدف واحد

هذا المثال يوضح كيفية إجراء فحص شامل لهدف واحد، وهو الاستخدام الأساسي للأداة.

```bash
python saudi_attacks.py example.com
```

هذا الأمر سيقوم بما يلي:
1. جمع معلومات أساسية عن الهدف (عناوين IP، معلومات النطاق، سجلات DNS)
2. فحص المنافذ الشائعة
3. فحص الثغرات العامة
4. فحص خوادم الويب وتطبيقات الويب (إذا تم اكتشافها)
5. فحص أنظمة إدارة المحتوى (إذا تم اكتشافها)
6. توليد تقرير HTML في المجلد الحالي

### مثال 2: فحص شامل مع حفظ التقرير

```bash
python saudi_attacks.py example.com --output example_report.html
```

هذا الأمر سيقوم بإجراء فحص شامل وحفظ التقرير في ملف `example_report.html`.

## فحص المنافذ

### مثال 3: فحص المنافذ فقط

```bash
python saudi_attacks.py example.com --scan-type port
```

هذا الأمر سيقوم بفحص المنافذ الشائعة فقط دون إجراء فحوصات أخرى.

### مثال 4: فحص منافذ محددة

```bash
python saudi_attacks.py example.com --scan-type port --ports 80,443,8080,3306
```

هذا الأمر سيقوم بفحص المنافذ المحددة فقط (80, 443, 8080, 3306).

### مثال 5: فحص نطاق من المنافذ

```bash
python saudi_attacks.py example.com --scan-type port --ports 1-1000
```

هذا الأمر سيقوم بفحص المنافذ من 1 إلى 1000.

### مثال 6: فحص المنافذ بشكل سريع

```bash
python saudi_attacks.py example.com --scan-type port --fast
```

هذا الأمر سيقوم بفحص المنافذ بشكل سريع باستخدام خيارات Nmap المناسبة للفحص السريع.

## فحص تطبيقات الويب

### مثال 7: فحص تطبيقات الويب فقط

```bash
python saudi_attacks.py example.com --scan-type web
```

هذا الأمر سيقوم بفحص خوادم الويب وتطبيقات الويب فقط.

### مثال 8: فحص تطبيقات الويب على منفذ محدد

```bash
python saudi_attacks.py example.com --scan-type web --web-port 8080
```

هذا الأمر سيقوم بفحص تطبيقات الويب على المنفذ 8080.

### مثال 9: فحص تطبيقات الويب مع فحص SSL/TLS

```bash
python saudi_attacks.py example.com --scan-type web --check-ssl
```

هذا الأمر سيقوم بفحص تطبيقات الويب مع إجراء فحص مفصل لإعدادات SSL/TLS.

## فحص أنظمة إدارة المحتوى

### مثال 10: فحص نظام WordPress

```bash
python saudi_attacks.py example.com --scan-type wordpress
```

هذا الأمر سيقوم بفحص نظام WordPress على الهدف، بما في ذلك:
- إصدار WordPress
- الإضافات المثبتة
- القوالب المثبتة
- الثغرات المعروفة

### مثال 11: فحص نظام Joomla

```bash
python saudi_attacks.py example.com --scan-type joomla
```

هذا الأمر سيقوم بفحص نظام Joomla على الهدف، بما في ذلك:
- إصدار Joomla
- الإضافات المثبتة
- القوالب المثبتة
- الثغرات المعروفة

### مثال 12: اكتشاف نظام إدارة المحتوى تلقائيًا

```bash
python saudi_attacks.py example.com --scan-type cms
```

هذا الأمر سيحاول اكتشاف نظام إدارة المحتوى المستخدم تلقائيًا ثم إجراء الفحص المناسب.

## فحص عدة أهداف

### مثال 13: فحص عدة أهداف محددة

```bash
python saudi_attacks.py example.com,example.org,192.168.1.1
```

هذا الأمر سيقوم بفحص الأهداف المحددة بشكل متتالي.

### مثال 14: فحص أهداف من ملف

```bash
python saudi_attacks.py --targets-file targets.txt
```

حيث يحتوي ملف `targets.txt` على قائمة الأهداف، هدف واحد في كل سطر:

```
example.com
example.org
192.168.1.1
```

### مثال 15: فحص نطاق من عناوين IP

```bash
python saudi_attacks.py 192.168.1.0/24 --scan-type port --ports 80,443
```

هذا الأمر سيقوم بفحص المنافذ 80 و443 على جميع عناوين IP في النطاق 192.168.1.0/24.

## توليد تقارير مخصصة

### مثال 16: توليد تقرير HTML

```bash
python saudi_attacks.py example.com --output report.html --format html
```

هذا الأمر سيقوم بتوليد تقرير بتنسيق HTML.

### مثال 17: توليد تقرير JSON

```bash
python saudi_attacks.py example.com --output report.json --format json
```

هذا الأمر سيقوم بتوليد تقرير بتنسيق JSON، وهو مفيد للمعالجة الآلية للنتائج.

### مثال 18: توليد تقرير مع معلومات مفصلة

```bash
python saudi_attacks.py example.com --output report.html --verbose-report
```

هذا الأمر سيقوم بتوليد تقرير HTML مع معلومات مفصلة عن نتائج الفحص.

## سيناريوهات متقدمة

### مثال 19: فحص شامل مع خيارات متقدمة

```bash
python saudi_attacks.py example.com --ports 1-65535 --timeout 120 --threads 10 --output report.html --verbose-report
```

هذا الأمر سيقوم بإجراء فحص شامل مع الخيارات التالية:
- فحص جميع المنافذ (1-65535)
- زيادة مهلة الانتظار إلى 120 ثانية
- استخدام 10 مسارات متوازية
- توليد تقرير HTML مفصل

### مثال 20: فحص في وضع الصمت

```bash
python saudi_attacks.py example.com --quiet --output report.json --format json
```

هذا الأمر سيقوم بإجراء فحص بدون طباعة أي رسائل على الشاشة، وحفظ النتائج في ملف JSON.

### مثال 21: فحص مع تسجيل التصحيح

```bash
python saudi_attacks.py example.com --debug --log-file debug.log
```

هذا الأمر سيقوم بإجراء فحص مع تسجيل رسائل التصحيح في ملف `debug.log`.

### مثال 22: استخدام الأداة كمكتبة Python

يمكنك أيضًا استخدام الأداة كمكتبة Python في سكريبت خاص بك:

```python
from saudi_attacks import SaudiAttacks
from modules.port_scanner import PortScanner
from modules.web_scanner import WebScanner

# إنشاء كائن SaudiAttacks
scanner = SaudiAttacks(target="example.com", output="report.html", scan_type="all")

# تشغيل الفحص
results = scanner.run()

# أو استخدام وحدات محددة مباشرة
port_scanner = PortScanner(target="example.com")
port_results = port_scanner.scan(ports="80,443")

web_scanner = WebScanner(target="example.com", port_results=port_results)
web_results = web_scanner.scan()

# معالجة النتائج
print(f"تم اكتشاف {len(port_results['open_ports'])} منفذ مفتوح")
for port in port_results['open_ports']:
    print(f"المنفذ {port}: {port_results['services'][port]}")
```

للحصول على مزيد من المعلومات حول استخدام الأداة كمكتبة، راجع [وثائق API](api.md).

## ملاحظات هامة

- تأكد من أن لديك إذن صريح لفحص الأهداف قبل استخدام الأداة.
- بعض الفحوصات قد تستغرق وقتًا طويلاً، خاصة عند فحص نطاقات واسعة من المنافذ أو عدة أهداف.
- استخدم الخيار `--fast` لتسريع الفحص إذا كنت بحاجة إلى نتائج سريعة.
- استخدم الخيار `--timeout` لضبط مهلة الانتظار إذا كانت الاتصالات بطيئة.
- تأكد من تشغيل الأداة بصلاحيات المستخدم الجذر على Linux أو بصلاحيات المسؤول على Windows للحصول على نتائج دقيقة.