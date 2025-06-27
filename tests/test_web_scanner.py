#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات وحدة فحص خوادم الويب
"""

import unittest
import sys
import os
import logging
from unittest.mock import patch, MagicMock

# إضافة المجلد الرئيسي إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.web_scanner import WebScanner

class TestWebScanner(unittest.TestCase):
    """
    اختبارات لوحدة فحص خوادم الويب
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
        
        # إنشاء كائن WebScanner للاختبار
        self.web_scanner = WebScanner('example.com', self.logger, quiet=True, debug=True)
    
    def test_initialization(self):
        """
        اختبار تهيئة الكائن
        """
        self.assertEqual(self.web_scanner.target, 'example.com')
        self.assertTrue(self.web_scanner.quiet)
        self.assertTrue(self.web_scanner.debug)
    
    @patch('modules.web_scanner.requests.get')
    def test_scan_web_server(self, mock_get):
        """
        اختبار فحص خادم الويب
        """
        # إعداد الاستجابة الوهمية لـ HTTP
        mock_http_response = MagicMock()
        mock_http_response.status_code = 200
        mock_http_response.headers = {
            'Server': 'nginx/1.18.0',
            'Content-Type': 'text/html',
            'Date': 'Wed, 01 Dec 2023 12:00:00 GMT'
        }
        mock_http_response.text = '<html><head><title>Example Domain</title></head><body></body></html>'
        
        # إعداد الاستجابة الوهمية لـ HTTPS
        mock_https_response = MagicMock()
        mock_https_response.status_code = 200
        mock_https_response.headers = {
            'Server': 'nginx/1.18.0',
            'Content-Type': 'text/html',
            'Date': 'Wed, 01 Dec 2023 12:00:00 GMT',
            'Strict-Transport-Security': 'max-age=31536000'
        }
        mock_https_response.text = '<html><head><title>Example Domain</title></head><body></body></html>'
        
        # تكوين السلوك المتوقع للدالة الوهمية
        mock_get.side_effect = [mock_http_response, mock_https_response]
        
        # تنفيذ فحص خادم الويب
        result = self.web_scanner.scan_web_server()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertEqual(result['http']['status_code'], 200)
        self.assertEqual(result['https']['status_code'], 200)
        self.assertEqual(result['http']['server'], 'nginx/1.18.0')
        self.assertEqual(result['http']['title'], 'Example Domain')
        self.assertEqual(result['https']['title'], 'Example Domain')
        
        # التحقق من عدد مرات استدعاء الدالة الوهمية
        self.assertEqual(mock_get.call_count, 2)
    
    @patch('modules.web_scanner.requests.get')
    def test_check_security_headers(self, mock_get):
        """
        اختبار فحص رؤوس الأمان
        """
        # إعداد الاستجابة الوهمية
        mock_response = MagicMock()
        mock_response.headers = {
            'Strict-Transport-Security': 'max-age=31536000',
            'Content-Security-Policy': "default-src 'self'",
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'no-referrer',
            'Feature-Policy': "microphone 'none'; camera 'none'",
            'Permissions-Policy': "microphone=(), camera=()"
        }
        mock_get.return_value = mock_response
        
        # تنفيذ فحص رؤوس الأمان
        result = self.web_scanner.check_security_headers()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertTrue(result['hsts']['present'])
        self.assertTrue(result['csp']['present'])
        self.assertTrue(result['x_content_type_options']['present'])
        self.assertTrue(result['x_frame_options']['present'])
        self.assertTrue(result['x_xss_protection']['present'])
        self.assertTrue(result['referrer_policy']['present'])
        self.assertTrue(result['feature_policy']['present'])
        self.assertTrue(result['permissions_policy']['present'])
        
        # التحقق من استدعاء الدالة الوهمية
        mock_get.assert_called_once()
    
    @patch('modules.web_scanner.requests.get')
    def test_check_sensitive_files(self, mock_get):
        """
        اختبار فحص الملفات الحساسة
        """
        # إعداد الاستجابات الوهمية
        mock_responses = []
        
        # إنشاء استجابة لكل ملف حساس (200 للموجود، 404 لغير الموجود)
        for i in range(len(self.web_scanner.sensitive_files)):
            mock_response = MagicMock()
            # جعل بعض الملفات موجودة وبعضها غير موجود للاختبار
            if i % 3 == 0:  # كل ثالث ملف سيكون "موجودًا"
                mock_response.status_code = 200
                mock_response.text = f"Content of sensitive file {i}"
            else:
                mock_response.status_code = 404
                mock_response.text = "Not Found"
            mock_responses.append(mock_response)
        
        # تكوين السلوك المتوقع للدالة الوهمية
        mock_get.side_effect = mock_responses
        
        # تنفيذ فحص الملفات الحساسة
        result = self.web_scanner.check_sensitive_files()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        
        # عدد الملفات "الموجودة" يجب أن يكون ثلث العدد الإجمالي تقريبًا
        found_files = [f for f in result if f['status_code'] == 200]
        expected_found_count = len(self.web_scanner.sensitive_files) // 3 + (1 if len(self.web_scanner.sensitive_files) % 3 > 0 else 0)
        self.assertEqual(len(found_files), expected_found_count)
        
        # التحقق من عدد مرات استدعاء الدالة الوهمية
        self.assertEqual(mock_get.call_count, len(self.web_scanner.sensitive_files))
    
    @patch('modules.web_scanner.requests.get')
    def test_check_cors_config(self, mock_get):
        """
        اختبار فحص إعدادات CORS
        """
        # إعداد الاستجابة الوهمية
        mock_response = MagicMock()
        mock_response.headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
        mock_get.return_value = mock_response
        
        # تنفيذ فحص إعدادات CORS
        result = self.web_scanner.check_cors_config()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertTrue(result['allow_origin']['present'])
        self.assertEqual(result['allow_origin']['value'], '*')
        self.assertTrue(result['allow_methods']['present'])
        self.assertTrue(result['allow_headers']['present'])
        
        # التحقق من استدعاء الدالة الوهمية
        mock_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()