# دليل التطوير لأداة SaudiAttacks

هذا الدليل موجه للمطورين الذين يرغبون في المساهمة في تطوير أداة SaudiAttacks أو فهم بنيتها الداخلية.

## جدول المحتويات

- [بيئة التطوير](#بيئة-التطوير)
- [بنية المشروع](#بنية-المشروع)
- [إرشادات كتابة الكود](#إرشادات-كتابة-الكود)
- [إضافة وحدات جديدة](#إضافة-وحدات-جديدة)
- [الاختبارات](#الاختبارات)
- [التوثيق](#التوثيق)
- [عملية الإصدار](#عملية-الإصدار)

## بيئة التطوير

### المتطلبات

- Python 3.6 أو أحدث
- Git
- IDE مناسب (مثل PyCharm، VS Code، إلخ)
- Nmap
- حزم Python المطلوبة (مذكورة في ملف requirements.txt)

### إعداد بيئة التطوير

1. استنساخ المستودع:
   ```bash
   git clone https://github.com/SaudiLinux/Saudi-Attacks.git
   cd Saudi-Attacks
   ```

2. إنشاء بيئة افتراضية:
   ```bash
   python -m venv venv
   source venv/bin/activate  # على Linux
   # أو
   venv\Scripts\activate  # على Windows
   ```

3. تثبيت التبعيات للتطوير:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov flake8 black
   ```

## بنية المشروع

```
Saudi-Attacks/
├── assets/                  # الموارد (الشعار، الصور، إلخ)
├── docs/                    # الوثائق
├── modules/                 # وحدات الأداة
│   ├── __init__.py
│   ├── banner.py            # عرض الشعار والمعلومات
│   ├── cms_scanner.py       # فحص أنظمة إدارة المحتوى
│   ├── info_gathering.py    # جمع المعلومات
│   ├── port_scanner.py      # فحص المنافذ
│   ├── report_generator.py  # توليد التقارير
│   ├── utils.py             # أدوات مساعدة
│   ├── vulnerability_scanner.py  # فحص الثغرات
│   └── web_scanner.py       # فحص الويب
├── tests/                   # اختبارات الوحدة
│   ├── __init__.py
│   ├── test_banner.py
│   ├── test_cms_scanner.py
│   ├── test_info_gathering.py
│   ├── test_port_scanner.py
│   ├── test_report_generator.py
│   ├── test_saudi_attacks.py
│   ├── test_utils.py
│   ├── test_vulnerability_scanner.py
│   └── test_web_scanner.py
├── .gitignore               # ملفات ومجلدات مستثناة من Git
├── CHANGELOG.md             # سجل التغييرات
├── CODE_OF_CONDUCT.md       # مدونة قواعد السلوك
├── CONTRIBUTING.md          # إرشادات المساهمة
├── INSTALL.md               # تعليمات التثبيت
├── LICENSE                  # رخصة المشروع
├── README.md                # الوصف العام للمشروع
├── SECURITY.md              # سياسة الأمان
├── requirements.txt         # التبعيات المطلوبة
├── saudi_attacks.py         # نقطة الدخول الرئيسية
└── setup.py                 # ملف إعداد حزمة Python
```

## إرشادات كتابة الكود

### أسلوب الكود

- اتبع معيار PEP 8 لكتابة كود Python.
- استخدم أداة `black` لتنسيق الكود تلقائياً.
- استخدم أداة `flake8` للتحقق من جودة الكود.

### التعليقات والتوثيق

- استخدم docstrings لتوثيق الفئات والدوال باستخدام تنسيق Google أو NumPy.
- اكتب تعليقات واضحة للأجزاء المعقدة من الكود.
- حافظ على تحديث الوثائق عند إجراء تغييرات على الكود.

### رسائل Commit

- اكتب رسائل commit واضحة وموجزة.
- استخدم صيغة الأمر الحاضر (مثل "إضافة ميزة" بدلاً من "تمت إضافة ميزة").
- اشرح سبب التغيير وليس فقط ما تم تغييره.

## إضافة وحدات جديدة

### خطوات إضافة وحدة جديدة

1. أنشئ ملف Python جديد في مجلد `modules/`.
2. اتبع نمط التصميم المستخدم في الوحدات الأخرى.
3. أضف اختبارات للوحدة الجديدة في مجلد `tests/`.
4. قم بتحديث الوثائق لتشمل الوحدة الجديدة.
5. قم بتحديث `saudi_attacks.py` لدمج الوحدة الجديدة في تدفق العمل العام.

### مثال على بنية وحدة جديدة

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""وصف الوحدة الجديدة."""

import logging
from modules import utils

class NewModule:
    """وصف الفئة الجديدة."""

    def __init__(self, target, logger=None, quiet=False, debug=False):
        """تهيئة الفئة الجديدة.

        Args:
            target (str): الهدف المراد فحصه.
            logger (logging.Logger, optional): كائن التسجيل.
            quiet (bool, optional): وضع الصمت.
            debug (bool, optional): وضع التصحيح.
        """
        self.target = target
        self.logger = logger or logging.getLogger(__name__)
        self.quiet = quiet
        self.debug = debug
        self.results = {}

    def scan(self):
        """إجراء الفحص الرئيسي.

        Returns:
            dict: نتائج الفحص.
        """
        try:
            # تنفيذ عملية الفحص
            utils.print_status(f"بدء الفحص على {self.target}", self.quiet)
            
            # إضافة النتائج
            self.results["example"] = "نتيجة مثال"
            
            return self.results
        except Exception as e:
            self.logger.error(f"خطأ أثناء الفحص: {str(e)}")
            if self.debug:
                self.logger.exception("تفاصيل الخطأ:")
            return {"error": str(e)}

# اختبار ذاتي
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scanner = NewModule("example.com")
    results = scanner.scan()
    print(results)
```

## الاختبارات

### إطار الاختبار

نستخدم `pytest` لكتابة وتشغيل اختبارات الوحدة.

### كتابة الاختبارات

- اكتب اختبارات لكل وحدة جديدة أو ميزة جديدة.
- استخدم `unittest.mock` لعزل الاختبارات عن الخدمات الخارجية.
- حاول تحقيق تغطية اختبار عالية (أكثر من 80%).

### تشغيل الاختبارات

```bash
# تشغيل جميع الاختبارات
pytest

# تشغيل اختبارات مع تقرير التغطية
pytest --cov=modules tests/

# تشغيل اختبارات محددة
pytest tests/test_utils.py
```

## التوثيق

### توثيق الكود

- استخدم docstrings لتوثيق الفئات والدوال.
- اتبع تنسيق Google أو NumPy للـ docstrings.

### توثيق المستخدم

- حافظ على تحديث ملف README.md بالمعلومات الأساسية.
- أضف وثائق مفصلة في مجلد `docs/`.
- قم بتوثيق التغييرات في ملف CHANGELOG.md.

## عملية الإصدار

### الإصدار الدلالي

نتبع [الإصدار الدلالي](https://semver.org/) لترقيم الإصدارات:

- **MAJOR**: تغييرات غير متوافقة مع الإصدارات السابقة
- **MINOR**: إضافة وظائف جديدة بطريقة متوافقة مع الإصدارات السابقة
- **PATCH**: إصلاحات للأخطاء بطريقة متوافقة مع الإصدارات السابقة

### خطوات الإصدار

1. تحديث رقم الإصدار في `setup.py`
2. تحديث ملف CHANGELOG.md بالتغييرات الجديدة
3. إنشاء علامة Git جديدة للإصدار
4. بناء ونشر الحزمة على PyPI (إذا كان ذلك مناسباً)

```bash
# مثال على إنشاء علامة إصدار جديدة
git tag -a v1.1.0 -m "الإصدار 1.1.0"
git push origin v1.1.0
```