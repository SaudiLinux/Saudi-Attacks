#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات وحدة جمع المعلومات
"""

import unittest
import sys
import os
import logging

# إضافة المجلد الرئيسي إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.info_gathering import InfoGathering

class TestInfoGathering(unittest.TestCase):
    """
    اختبارات لوحدة جمع المعلومات
    """
    
    def setUp(self):
        """
        إعداد بيئة الاختبار
        """
        # إنشاء مسجل اختبار
        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.DEBUG)
        # إنشاء معالج للطباعة على وحدة التحكم
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        # إضافة المعالج إلى المسجل
        self.logger.addHandler(handler)
        
        # إنشاء كائن InfoGathering للاختبار
        self.info_gatherer_domain = InfoGathering('example.com', self.logger, quiet=True, debug=True)
        self.info_gatherer_ip = InfoGathering('8.8.8.8', self.logger, quiet=True, debug=True)
    
    def test_initialization(self):
        """
        اختبار تهيئة الكائن
        """
        self.assertEqual(self.info_gatherer_domain.target, 'example.com')
        self.assertEqual(self.info_gatherer_ip.target, '8.8.8.8')
        self.assertTrue(self.info_gatherer_domain.quiet)
        self.assertTrue(self.info_gatherer_domain.debug)
    
    def test_is_valid_domain(self):
        """
        اختبار التحقق من صحة اسم النطاق
        """
        self.assertTrue(self.info_gatherer_domain.is_valid_domain('example.com'))
        self.assertTrue(self.info_gatherer_domain.is_valid_domain('sub.example.com'))
        self.assertFalse(self.info_gatherer_domain.is_valid_domain('invalid'))
        self.assertFalse(self.info_gatherer_domain.is_valid_domain('8.8.8.8'))
    
    def test_is_valid_ip(self):
        """
        اختبار التحقق من صحة عنوان IP
        """
        self.assertTrue(self.info_gatherer_ip.is_valid_ip('8.8.8.8'))
        self.assertTrue(self.info_gatherer_ip.is_valid_ip('192.168.1.1'))
        self.assertFalse(self.info_gatherer_ip.is_valid_ip('256.256.256.256'))
        self.assertFalse(self.info_gatherer_ip.is_valid_ip('example.com'))
    
    def test_resolve_host(self):
        """
        اختبار تحليل اسم المضيف
        """
        # هذا الاختبار يتطلب اتصالاً بالإنترنت
        # قد يفشل إذا كان هناك مشكلة في الاتصال
        try:
            ip = self.info_gatherer_domain.resolve_host('example.com')
            self.assertIsNotNone(ip)
            self.assertTrue(self.info_gatherer_domain.is_valid_ip(ip))
        except Exception as e:
            self.skipTest(f"تخطي اختبار تحليل اسم المضيف بسبب: {str(e)}")
    
    def test_check_http_https(self):
        """
        اختبار التحقق من توفر HTTP/HTTPS
        """
        # هذا الاختبار يتطلب اتصالاً بالإنترنت
        # قد يفشل إذا كان هناك مشكلة في الاتصال
        try:
            http_info, https_info = self.info_gatherer_domain.check_http_https('example.com')
            self.assertIsNotNone(http_info)
            self.assertIsNotNone(https_info)
            self.assertIn('status_code', http_info)
            self.assertIn('status_code', https_info)
        except Exception as e:
            self.skipTest(f"تخطي اختبار التحقق من HTTP/HTTPS بسبب: {str(e)}")

if __name__ == '__main__':
    unittest.main()