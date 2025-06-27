# توثيق واجهة برمجة التطبيقات (API) لأداة SaudiAttacks

يوفر هذا المستند توثيقًا مفصلاً لواجهة برمجة التطبيقات (API) الخاصة بأداة SaudiAttacks، مما يتيح للمطورين استخدام الأداة كمكتبة في مشاريعهم الخاصة.

## جدول المحتويات

- [نظرة عامة](#نظرة-عامة)
- [الفئة الرئيسية: SaudiAttacks](#الفئة-الرئيسية-saudiattacks)
- [وحدة جمع المعلومات: InfoGathering](#وحدة-جمع-المعلومات-infogathering)
- [وحدة فحص المنافذ: PortScanner](#وحدة-فحص-المنافذ-portscanner)
- [وحدة فحص الثغرات: VulnerabilityScanner](#وحدة-فحص-الثغرات-vulnerabilityscanner)
- [وحدة فحص الويب: WebScanner](#وحدة-فحص-الويب-webscanner)
- [وحدة فحص أنظمة إدارة المحتوى: CMSScanner](#وحدة-فحص-أنظمة-إدارة-المحتوى-cmsscanner)
- [وحدة توليد التقارير: ReportGenerator](#وحدة-توليد-التقارير-reportgenerator)
- [وحدة الأدوات المساعدة: Utils](#وحدة-الأدوات-المساعدة-utils)
- [أمثلة استخدام](#أمثلة-استخدام)

## نظرة عامة

يمكن استخدام SaudiAttacks كمكتبة Python في مشاريعك الخاصة. يتيح لك ذلك الاستفادة من وظائف الأداة المختلفة مثل جمع المعلومات، فحص المنافذ، فحص الثغرات، وغيرها.

لاستخدام SaudiAttacks كمكتبة، يمكنك استيراد الوحدات المختلفة كما يلي:

```python
# استيراد الفئة الرئيسية
from saudi_attacks import SaudiAttacks

# استيراد وحدات محددة
from modules.info_gathering import InfoGathering
from modules.port_scanner import PortScanner
from modules.vulnerability_scanner import VulnerabilityScanner
from modules.web_scanner import WebScanner
from modules.cms_scanner import CMSScanner
from modules.report_generator import ReportGenerator
from modules.utils import print_banner, print_status, print_error
```

## الفئة الرئيسية: SaudiAttacks

### الوصف

الفئة الرئيسية التي تدير جميع عمليات الفحص وتنسق بين الوحدات المختلفة.

### التهيئة

```python
SaudiAttacks(target, output=None, scan_type="all", quiet=False, debug=False)
```

#### المعلمات

- `target` (str): الهدف المراد فحصه (اسم النطاق أو عنوان IP).
- `output` (str, optional): مسار ملف الإخراج لحفظ التقرير. الافتراضي هو `None`.
- `scan_type` (str, optional): نوع الفحص المراد إجراؤه. الافتراضي هو `"all"`.
  - القيم المحتملة: `"all"`, `"port"`, `"vuln"`, `"web"`, `"wordpress"`, `"joomla"`.
- `quiet` (bool, optional): وضع الصمت (عدم طباعة الرسائل). الافتراضي هو `False`.
- `debug` (bool, optional): وضع التصحيح (طباعة رسائل التصحيح). الافتراضي هو `False`.

### الطرق

#### run()

تشغيل عملية الفحص الكاملة.

```python
run()
```

**القيمة المرجعة**: `dict` - نتائج الفحص.

#### generate_report(results, output_format="html")

توليد تقرير بنتائج الفحص.

```python
generate_report(results, output_format="html")
```

**المعلمات**:
- `results` (dict): نتائج الفحص.
- `output_format` (str, optional): تنسيق الإخراج. الافتراضي هو `"html"`.
  - القيم المحتملة: `"html"`, `"json"`.

**القيمة المرجعة**: `str` - مسار ملف التقرير.

## وحدة جمع المعلومات: InfoGathering

### الوصف

وحدة مسؤولة عن جمع المعلومات الأساسية عن الهدف مثل عناوين IP، معلومات النطاق، وغيرها.

### التهيئة

```python
InfoGathering(target, logger=None, quiet=False, debug=False)
```

#### المعلمات

- `target` (str): الهدف المراد جمع المعلومات عنه.
- `logger` (logging.Logger, optional): كائن التسجيل. الافتراضي هو `None`.
- `quiet` (bool, optional): وضع الصمت. الافتراضي هو `False`.
- `debug` (bool, optional): وضع التصحيح. الافتراضي هو `False`.

### الطرق

#### gather()

جمع المعلومات عن الهدف.

```python
gather()
```

**القيمة المرجعة**: `dict` - المعلومات التي تم جمعها.

#### get_ip_address()

الحصول على عنوان IP للهدف.

```python
get_ip_address()
```

**القيمة المرجعة**: `str` - عنوان IP للهدف.

#### get_whois_info()

الحصول على معلومات WHOIS للهدف.

```python
get_whois_info()
```

**القيمة المرجعة**: `dict` - معلومات WHOIS.

#### get_dns_records()

الحصول على سجلات DNS للهدف.

```python
get_dns_records()
```

**القيمة المرجعة**: `dict` - سجلات DNS.

## وحدة فحص المنافذ: PortScanner

### الوصف

وحدة مسؤولة عن فحص المنافذ المفتوحة على الهدف باستخدام Nmap.

### التهيئة

```python
PortScanner(target, logger=None, quiet=False, debug=False)
```

#### المعلمات

- `target` (str): الهدف المراد فحص المنافذ عليه.
- `logger` (logging.Logger, optional): كائن التسجيل. الافتراضي هو `None`.
- `quiet` (bool, optional): وضع الصمت. الافتراضي هو `False`.
- `debug` (bool, optional): وضع التصحيح. الافتراضي هو `False`.

### الطرق

#### scan(ports=None)

فحص المنافذ على الهدف.

```python
scan(ports=None)
```

**المعلمات**:
- `ports` (str, optional): المنافذ المراد فحصها. الافتراضي هو `None` (جميع المنافذ الشائعة).

**القيمة المرجعة**: `dict` - نتائج فحص المنافذ.

#### get_open_ports()

الحصول على قائمة المنافذ المفتوحة.

```python
get_open_ports()
```

**القيمة المرجعة**: `list` - قائمة المنافذ المفتوحة.

#### get_service_info(port)

الحصول على معلومات الخدمة على منفذ محدد.

```python
get_service_info(port)
```

**المعلمات**:
- `port` (int): رقم المنفذ.

**القيمة المرجعة**: `dict` - معلومات الخدمة.

## وحدة فحص الثغرات: VulnerabilityScanner

### الوصف

وحدة مسؤولة عن فحص الثغرات الأمنية العامة في الهدف.

### التهيئة

```python
VulnerabilityScanner(target, port_results=None, logger=None, quiet=False, debug=False)
```

#### المعلمات

- `target` (str): الهدف المراد فحص الثغرات فيه.
- `port_results` (dict, optional): نتائج فحص المنافذ. الافتراضي هو `None`.
- `logger` (logging.Logger, optional): كائن التسجيل. الافتراضي هو `None`.
- `quiet` (bool, optional): وضع الصمت. الافتراضي هو `False`.
- `debug` (bool, optional): وضع التصحيح. الافتراضي هو `False`.

### الطرق

#### scan()

فحص الثغرات في الهدف.

```python
scan()
```

**القيمة المرجعة**: `dict` - نتائج فحص الثغرات.

#### scan_service(service, port)

فحص ثغرات خدمة محددة.

```python
scan_service(service, port)
```

**المعلمات**:
- `service` (str): اسم الخدمة.
- `port` (int): رقم المنفذ.

**القيمة المرجعة**: `dict` - نتائج فحص الثغرات للخدمة.

## وحدة فحص الويب: WebScanner

### الوصف

وحدة مسؤولة عن فحص تطبيقات الويب وخوادم الويب.

### التهيئة

```python
WebScanner(target, port_results=None, logger=None, quiet=False, debug=False)
```

#### المعلمات

- `target` (str): الهدف المراد فحص تطبيقات الويب فيه.
- `port_results` (dict, optional): نتائج فحص المنافذ. الافتراضي هو `None`.
- `logger` (logging.Logger, optional): كائن التسجيل. الافتراضي هو `None`.
- `quiet` (bool, optional): وضع الصمت. الافتراضي هو `False`.
- `debug` (bool, optional): وضع التصحيح. الافتراضي هو `False`.

### الطرق

#### scan()

فحص تطبيقات الويب وخوادم الويب.

```python
scan()
```

**القيمة المرجعة**: `dict` - نتائج فحص الويب.

#### get_web_server_info()

الحصول على معلومات خادم الويب.

```python
get_web_server_info()
```

**القيمة المرجعة**: `dict` - معلومات خادم الويب.

#### scan_web_vulnerabilities()

فحص ثغرات تطبيقات الويب.

```python
scan_web_vulnerabilities()
```

**القيمة المرجعة**: `dict` - نتائج فحص ثغرات تطبيقات الويب.

#### check_ssl_tls()

فحص إعدادات SSL/TLS.

```python
check_ssl_tls()
```

**القيمة المرجعة**: `dict` - نتائج فحص SSL/TLS.

## وحدة فحص أنظمة إدارة المحتوى: CMSScanner

### الوصف

وحدة مسؤولة عن فحص أنظمة إدارة المحتوى مثل WordPress وJoomla.

### التهيئة

```python
CMSScanner(target, cms_type="auto", logger=None, quiet=False, debug=False)
```

#### المعلمات

- `target` (str): الهدف المراد فحص نظام إدارة المحتوى فيه.
- `cms_type` (str, optional): نوع نظام إدارة المحتوى. الافتراضي هو `"auto"`.
  - القيم المحتملة: `"auto"`, `"wordpress"`, `"joomla"`.
- `logger` (logging.Logger, optional): كائن التسجيل. الافتراضي هو `None`.
- `quiet` (bool, optional): وضع الصمت. الافتراضي هو `False`.
- `debug` (bool, optional): وضع التصحيح. الافتراضي هو `False`.

### الطرق

#### scan()

فحص نظام إدارة المحتوى.

```python
scan()
```

**القيمة المرجعة**: `dict` - نتائج فحص نظام إدارة المحتوى.

#### detect_cms()

اكتشاف نوع نظام إدارة المحتوى.

```python
detect_cms()
```

**القيمة المرجعة**: `str` - نوع نظام إدارة المحتوى.

#### scan_wordpress()

فحص نظام WordPress.

```python
scan_wordpress()
```

**القيمة المرجعة**: `dict` - نتائج فحص WordPress.

#### scan_joomla()

فحص نظام Joomla.

```python
scan_joomla()
```

**القيمة المرجعة**: `dict` - نتائج فحص Joomla.

## وحدة توليد التقارير: ReportGenerator

### الوصف

وحدة مسؤولة عن توليد تقارير بنتائج الفحص بتنسيقات مختلفة.

### التهيئة

```python
ReportGenerator(results, target, logger=None, quiet=False, debug=False)
```

#### المعلمات

- `results` (dict): نتائج الفحص.
- `target` (str): الهدف الذي تم فحصه.
- `logger` (logging.Logger, optional): كائن التسجيل. الافتراضي هو `None`.
- `quiet` (bool, optional): وضع الصمت. الافتراضي هو `False`.
- `debug` (bool, optional): وضع التصحيح. الافتراضي هو `False`.

### الطرق

#### generate(output_file=None, output_format="html")

توليد تقرير بنتائج الفحص.

```python
generate(output_file=None, output_format="html")
```

**المعلمات**:
- `output_file` (str, optional): مسار ملف الإخراج. الافتراضي هو `None`.
- `output_format` (str, optional): تنسيق الإخراج. الافتراضي هو `"html"`.
  - القيم المحتملة: `"html"`, `"json"`.

**القيمة المرجعة**: `str` - مسار ملف التقرير.

#### generate_html(output_file=None)

توليد تقرير HTML.

```python
generate_html(output_file=None)
```

**المعلمات**:
- `output_file` (str, optional): مسار ملف الإخراج. الافتراضي هو `None`.

**القيمة المرجعة**: `str` - مسار ملف التقرير HTML.

#### generate_json(output_file=None)

توليد تقرير JSON.

```python
generate_json(output_file=None)
```

**المعلمات**:
- `output_file` (str, optional): مسار ملف الإخراج. الافتراضي هو `None`.

**القيمة المرجعة**: `str` - مسار ملف التقرير JSON.

## وحدة الأدوات المساعدة: Utils

### الوصف

وحدة توفر وظائف مساعدة مختلفة للأداة.

### الدوال

#### print_banner()

طباعة شعار الأداة.

```python
print_banner()
```

#### print_status(message, quiet=False)

طباعة رسالة حالة.

```python
print_status(message, quiet=False)
```

**المعلمات**:
- `message` (str): الرسالة المراد طباعتها.
- `quiet` (bool, optional): وضع الصمت. الافتراضي هو `False`.

#### print_error(message, quiet=False)

طباعة رسالة خطأ.

```python
print_error(message, quiet=False)
```

**المعلمات**:
- `message` (str): رسالة الخطأ المراد طباعتها.
- `quiet` (bool, optional): وضع الصمت. الافتراضي هو `False`.

#### is_valid_target(target)

التحقق من صحة الهدف.

```python
is_valid_target(target)
```

**المعلمات**:
- `target` (str): الهدف المراد التحقق منه.

**القيمة المرجعة**: `bool` - `True` إذا كان الهدف صالحًا، `False` خلاف ذلك.

#### is_root()

التحقق مما إذا كان المستخدم الحالي هو المستخدم الجذر (root).

```python
is_root()
```

**القيمة المرجعة**: `bool` - `True` إذا كان المستخدم الحالي هو المستخدم الجذر، `False` خلاف ذلك.

## أمثلة استخدام

### استخدام الفئة الرئيسية

```python
from saudi_attacks import SaudiAttacks

# إنشاء كائن SaudiAttacks
scanner = SaudiAttacks(target="example.com", output="report.html", scan_type="all")

# تشغيل الفحص
results = scanner.run()

# طباعة النتائج
print(results)
```

### استخدام وحدات محددة

```python
from modules.info_gathering import InfoGathering
from modules.port_scanner import PortScanner
from modules.report_generator import ReportGenerator

# جمع المعلومات
info_gatherer = InfoGathering(target="example.com")
info_results = info_gatherer.gather()
print(info_results)

# فحص المنافذ
port_scanner = PortScanner(target="example.com")
port_results = port_scanner.scan()
print(port_results)

# دمج النتائج
results = {
    "info": info_results,
    "ports": port_results
}

# توليد تقرير
report_generator = ReportGenerator(results=results, target="example.com")
report_path = report_generator.generate(output_file="report.html", output_format="html")
print(f"تم إنشاء التقرير في: {report_path}")
```

### فحص نظام WordPress

```python
from modules.cms_scanner import CMSScanner

# فحص WordPress
cms_scanner = CMSScanner(target="example.com", cms_type="wordpress")
cms_results = cms_scanner.scan()
print(cms_results)
```

### فحص تطبيقات الويب

```python
from modules.web_scanner import WebScanner

# فحص تطبيقات الويب
web_scanner = WebScanner(target="example.com")
web_results = web_scanner.scan()
print(web_results)
```