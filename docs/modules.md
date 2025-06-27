# توثيق وحدات أداة SaudiAttacks

هذا المستند يوفر شرحاً مفصلاً لوحدات أداة SaudiAttacks المختلفة ووظائفها.

## جدول المحتويات

- [نظرة عامة على البنية](#نظرة-عامة-على-البنية)
- [الوحدة الرئيسية (saudi_attacks.py)](#الوحدة-الرئيسية-saudi_attackspy)
- [وحدة جمع المعلومات (info_gathering.py)](#وحدة-جمع-المعلومات-info_gatheringpy)
- [وحدة فحص المنافذ (port_scanner.py)](#وحدة-فحص-المنافذ-port_scannerpy)
- [وحدة فحص الثغرات (vulnerability_scanner.py)](#وحدة-فحص-الثغرات-vulnerability_scannerpy)
- [وحدة فحص الويب (web_scanner.py)](#وحدة-فحص-الويب-web_scannerpy)
- [وحدة فحص أنظمة إدارة المحتوى (cms_scanner.py)](#وحدة-فحص-أنظمة-إدارة-المحتوى-cms_scannerpy)
- [وحدة توليد التقارير (report_generator.py)](#وحدة-توليد-التقارير-report_generatorpy)
- [وحدة الأدوات المساعدة (utils.py)](#وحدة-الأدوات-المساعدة-utilspy)
- [وحدة العرض (banner.py)](#وحدة-العرض-bannerpy)

## نظرة عامة على البنية

تتكون أداة SaudiAttacks من عدة وحدات متخصصة تعمل معاً لتوفير حل شامل للاختبار الأمني. تم تصميم البنية بطريقة معيارية تسمح بإضافة وظائف جديدة بسهولة وتحسين الوظائف الحالية.

المخطط التالي يوضح العلاقات بين الوحدات المختلفة:

```
saudi_attacks.py (الوحدة الرئيسية)
  ├── info_gathering.py (جمع المعلومات)
  ├── port_scanner.py (فحص المنافذ)
  ├── vulnerability_scanner.py (فحص الثغرات)
  ├── web_scanner.py (فحص الويب)
  ├── cms_scanner.py (فحص أنظمة إدارة المحتوى)
  ├── report_generator.py (توليد التقارير)
  ├── utils.py (الأدوات المساعدة)
  └── banner.py (العرض)
```

## الوحدة الرئيسية (saudi_attacks.py)

هذه هي نقطة الدخول الرئيسية للأداة. تقوم بمعالجة وسائط سطر الأوامر، وتنسيق عمليات الفحص المختلفة، وإدارة تدفق العمل العام.

### الوظائف الرئيسية

- `main()`: الدالة الرئيسية التي تبدأ تنفيذ الأداة
- `parse_arguments()`: تحليل وسائط سطر الأوامر
- `process_targets()`: معالجة الأهداف المحددة (IP واحد، نطاق، أو قائمة)
- `run_scans()`: تنفيذ عمليات الفحص المطلوبة على الأهداف

## وحدة جمع المعلومات (info_gathering.py)

تقوم هذه الوحدة بجمع معلومات أساسية عن الهدف قبل بدء عمليات الفحص المتخصصة.

### الفئة الرئيسية: `InfoGathering`

#### الطرق الرئيسية

- `gather_all()`: جمع جميع المعلومات المتاحة عن الهدف
- `gather_dns_info()`: جمع معلومات DNS (سجلات A، MX، NS، TXT)
- `gather_whois_info()`: جمع معلومات WHOIS للنطاقات وعناوين IP
- `gather_network_info()`: جمع معلومات الشبكة
- `gather_web_info()`: جمع معلومات أساسية عن خدمات الويب
- `gather_additional_info()`: جمع معلومات إضافية عن الهدف

## وحدة فحص المنافذ (port_scanner.py)

تقوم هذه الوحدة بفحص المنافذ المفتوحة على الهدف واكتشاف الخدمات التي تعمل عليها.

### الفئة الرئيسية: `PortScanner`

#### الطرق الرئيسية

- `scan()`: إجراء فحص المنافذ باستخدام Nmap
- `scan_top_ports()`: فحص المنافذ الأكثر شيوعاً
- `scan_all_ports()`: فحص جميع المنافذ
- `scan_specific_ports()`: فحص منافذ محددة
- `get_service_info()`: الحصول على معلومات الخدمات المكتشفة

## وحدة فحص الثغرات (vulnerability_scanner.py)

تقوم هذه الوحدة بفحص الثغرات الأمنية العامة في الهدف.

### الفئة الرئيسية: `VulnerabilityScanner`

#### الطرق الرئيسية

- `scan()`: إجراء فحص شامل للثغرات
- `check_heartbleed()`: فحص ثغرة Heartbleed
- `check_shellshock()`: فحص ثغرة Shellshock
- `check_ssl_tls()`: فحص إعدادات SSL/TLS
- `check_exposed_services()`: فحص الخدمات المعرضة
- `check_misconfigurations()`: فحص الإعدادات الخاطئة

## وحدة فحص الويب (web_scanner.py)

تقوم هذه الوحدة بفحص خوادم الويب والتطبيقات للكشف عن الثغرات والمشكلات الأمنية.

### الفئة الرئيسية: `WebScanner`

#### الطرق الرئيسية

- `scan()`: إجراء فحص شامل لخادم الويب
- `scan_server_info()`: فحص معلومات خادم الويب
- `check_security_headers()`: فحص رؤوس الأمان
- `check_sensitive_files()`: فحص الملفات الحساسة
- `check_cors()`: فحص إعدادات CORS

## وحدة فحص أنظمة إدارة المحتوى (cms_scanner.py)

تقوم هذه الوحدة بفحص أنظمة إدارة المحتوى مثل WordPress و Joomla للكشف عن الثغرات والمشكلات الأمنية.

### الفئة الرئيسية: `CMSScanner`

#### الطرق الرئيسية

- `detect_cms()`: اكتشاف نوع نظام إدارة المحتوى
- `scan_wordpress()`: فحص مواقع WordPress
- `scan_joomla()`: فحص مواقع Joomla
- `check_wp_version()`: فحص إصدار WordPress
- `check_wp_plugins()`: فحص إضافات WordPress
- `check_wp_themes()`: فحص قوالب WordPress
- `check_joomla_version()`: فحص إصدار Joomla
- `check_joomla_extensions()`: فحص إضافات Joomla

## وحدة توليد التقارير (report_generator.py)

تقوم هذه الوحدة بتجميع نتائج جميع عمليات الفحص وتوليد تقارير شاملة بتنسيقات مختلفة.

### الفئة الرئيسية: `ReportGenerator`

#### الطرق الرئيسية

- `add_info_gathering_results()`: إضافة نتائج جمع المعلومات
- `add_port_scan_results()`: إضافة نتائج فحص المنافذ
- `add_vulnerability_scan_results()`: إضافة نتائج فحص الثغرات
- `add_web_scan_results()`: إضافة نتائج فحص الويب
- `add_cms_scan_results()`: إضافة نتائج فحص أنظمة إدارة المحتوى
- `generate_report()`: توليد التقرير النهائي
- `_generate_html_report()`: توليد تقرير بتنسيق HTML
- `_generate_json_report()`: توليد تقرير بتنسيق JSON
- `_generate_charts()`: توليد الرسوم البيانية للتقرير

## وحدة الأدوات المساعدة (utils.py)

توفر هذه الوحدة مجموعة من الدوال المساعدة التي تستخدمها الوحدات الأخرى.

### الدوال الرئيسية

- `check_root()`: التحقق من صلاحيات الجذر (root)
- `check_dependencies()`: التحقق من وجود التبعيات المطلوبة
- `setup_logging()`: إعداد نظام التسجيل
- `is_valid_ip()`: التحقق من صحة عنوان IP
- `is_valid_domain()`: التحقق من صحة اسم النطاق
- `resolve_host()`: تحليل اسم المضيف إلى عنوان IP
- `check_http_https()`: التحقق من توفر خدمات HTTP و HTTPS
- `run_command()`: تنفيذ أمر في نظام التشغيل
- `print_status()`: طباعة رسائل الحالة بتنسيق موحد

## وحدة العرض (banner.py)

تقوم هذه الوحدة بعرض شعار الأداة ومعلومات أساسية عند بدء التشغيل.

### الدوال الرئيسية

- `display_banner()`: عرض شعار الأداة ومعلومات النظام
- `display_target_info()`: عرض معلومات الهدف وبدء الفحص