#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات وحدة الأدوات المساعدة
"""

import unittest
import sys
import os
import logging
from unittest.mock import patch, MagicMock

# إضافة المجلد الرئيسي إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.utils import check_root, check_dependencies, setup_logging, is_valid_ip, is_valid_domain, resolve_host, check_http_https, run_command, print_status

class TestUtils(unittest.TestCase):
    """
    اختبارات للأدوات المساعدة
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
    
    @patch('os.geteuid')
    def test_check_root(self, mock_geteuid):
        """
        اختبار التحقق من صلاحيات الجذر
        """
        # اختبار حالة المستخدم الجذر
        mock_geteuid.return_value = 0
        self.assertTrue(check_root())
        
        # اختبار حالة المستخدم العادي
        mock_geteuid.return_value = 1000
        self.assertFalse(check_root())
    
    @patch('shutil.which')
    @patch('importlib.util.find_spec')
    def test_check_dependencies(self, mock_find_spec, mock_which):
        """
        اختبار التحقق من المتطلبات
        """
        # إعداد السلوك المتوقع للدوال الوهمية
        mock_which.side_effect = lambda x: '/usr/bin/' + x if x in ['nmap', 'python3'] else None
        mock_find_spec.side_effect = lambda x: MagicMock() if x in ['requests', 'colorama', 'argparse', 'bs4', 'tqdm'] else None
        
        # اختبار حالة توفر جميع المتطلبات
        result = check_dependencies(self.logger)
        self.assertTrue(result)
        
        # اختبار حالة عدم توفر أحد البرامج
        mock_which.side_effect = lambda x: None if x == 'nmap' else '/usr/bin/' + x
        result = check_dependencies(self.logger)
        self.assertFalse(result)
        
        # اختبار حالة عدم توفر أحد المكتبات
        mock_which.side_effect = lambda x: '/usr/bin/' + x if x in ['nmap', 'python3'] else None
        mock_find_spec.side_effect = lambda x: None if x == 'requests' else MagicMock()
        result = check_dependencies(self.logger)
        self.assertFalse(result)
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_setup_logging(self, mock_makedirs, mock_exists):
        """
        اختبار إعداد التسجيل
        """
        # إعداد السلوك المتوقع للدوال الوهمية
        mock_exists.return_value = False
        
        # اختبار إعداد التسجيل
        logger = setup_logging('test', debug=True)
        self.assertIsNotNone(logger)
        self.assertEqual(logger.level, logging.DEBUG)
        mock_exists.assert_called_once()
        mock_makedirs.assert_called_once()
        
        # اختبار إعداد التسجيل بدون وضع التصحيح
        mock_exists.reset_mock()
        mock_makedirs.reset_mock()
        logger = setup_logging('test', debug=False)
        self.assertIsNotNone(logger)
        self.assertEqual(logger.level, logging.INFO)
    
    def test_is_valid_ip(self):
        """
        اختبار التحقق من صحة عنوان IP
        """
        # اختبار عناوين IP صحيحة
        self.assertTrue(is_valid_ip('192.168.1.1'))
        self.assertTrue(is_valid_ip('8.8.8.8'))
        self.assertTrue(is_valid_ip('127.0.0.1'))
        self.assertTrue(is_valid_ip('255.255.255.255'))
        
        # اختبار عناوين IP غير صحيحة
        self.assertFalse(is_valid_ip('256.256.256.256'))
        self.assertFalse(is_valid_ip('192.168.1'))
        self.assertFalse(is_valid_ip('192.168.1.1.1'))
        self.assertFalse(is_valid_ip('example.com'))
        self.assertFalse(is_valid_ip('not-an-ip'))
    
    def test_is_valid_domain(self):
        """
        اختبار التحقق من صحة اسم النطاق
        """
        # اختبار أسماء نطاقات صحيحة
        self.assertTrue(is_valid_domain('example.com'))
        self.assertTrue(is_valid_domain('sub.example.com'))
        self.assertTrue(is_valid_domain('sub.sub.example.com'))
        self.assertTrue(is_valid_domain('example-domain.com'))
        self.assertTrue(is_valid_domain('example123.com'))
        
        # اختبار أسماء نطاقات غير صحيحة
        self.assertFalse(is_valid_domain('example'))
        self.assertFalse(is_valid_domain('192.168.1.1'))
        self.assertFalse(is_valid_domain('-example.com'))
        self.assertFalse(is_valid_domain('example-.com'))
        self.assertFalse(is_valid_domain('exam ple.com'))
    
    @patch('socket.gethostbyname')
    def test_resolve_host(self, mock_gethostbyname):
        """
        اختبار تحليل اسم المضيف
        """
        # إعداد السلوك المتوقع للدالة الوهمية
        mock_gethostbyname.return_value = '93.184.216.34'
        
        # اختبار تحليل اسم نطاق
        result = resolve_host('example.com')
        self.assertEqual(result, '93.184.216.34')
        mock_gethostbyname.assert_called_once_with('example.com')
        
        # اختبار تحليل عنوان IP
        mock_gethostbyname.reset_mock()
        result = resolve_host('8.8.8.8')
        self.assertEqual(result, '8.8.8.8')
        mock_gethostbyname.assert_not_called()
    
    @patch('requests.get')
    def test_check_http_https(self, mock_get):
        """
        اختبار التحقق من توفر HTTP/HTTPS
        """
        # إعداد الاستجابات الوهمية
        mock_http_response = MagicMock()
        mock_http_response.status_code = 200
        mock_http_response.headers = {'Server': 'nginx/1.18.0'}
        mock_http_response.text = '<html><head><title>Example Domain</title></head><body></body></html>'
        
        mock_https_response = MagicMock()
        mock_https_response.status_code = 200
        mock_https_response.headers = {'Server': 'nginx/1.18.0'}
        mock_https_response.text = '<html><head><title>Example Domain</title></head><body></body></html>'
        
        # تكوين السلوك المتوقع للدالة الوهمية
        mock_get.side_effect = [mock_http_response, mock_https_response]
        
        # اختبار التحقق من توفر HTTP/HTTPS
        http_info, https_info = check_http_https('example.com')
        
        # التحقق من النتائج
        self.assertIsNotNone(http_info)
        self.assertIsNotNone(https_info)
        self.assertEqual(http_info['status_code'], 200)
        self.assertEqual(https_info['status_code'], 200)
        self.assertEqual(http_info['server'], 'nginx/1.18.0')
        self.assertEqual(https_info['server'], 'nginx/1.18.0')
        self.assertEqual(http_info['title'], 'Example Domain')
        self.assertEqual(https_info['title'], 'Example Domain')
        
        # التحقق من عدد مرات استدعاء الدالة الوهمية
        self.assertEqual(mock_get.call_count, 2)
    
    @patch('subprocess.run')
    def test_run_command(self, mock_run):
        """
        اختبار تنفيذ الأوامر
        """
        # إعداد السلوك المتوقع للدالة الوهمية
        mock_process = MagicMock()
        mock_process.stdout = b'Command output'
        mock_process.stderr = b''
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        # اختبار تنفيذ أمر ناجح
        output, error, status = run_command('echo "test"')
        self.assertEqual(output, 'Command output')
        self.assertEqual(error, '')
        self.assertEqual(status, 0)
        mock_run.assert_called_once()
        
        # اختبار تنفيذ أمر فاشل
        mock_run.reset_mock()
        mock_process.stdout = b''
        mock_process.stderr = b'Command error'
        mock_process.returncode = 1
        mock_run.return_value = mock_process
        
        output, error, status = run_command('invalid_command')
        self.assertEqual(output, '')
        self.assertEqual(error, 'Command error')
        self.assertEqual(status, 1)
        mock_run.assert_called_once()
    
    @patch('builtins.print')
    def test_print_status(self, mock_print):
        """
        اختبار طباعة الحالة
        """
        # اختبار طباعة رسائل بمختلف الأنواع
        print_status('معلومات', 'info')
        print_status('نجاح', 'success')
        print_status('تحذير', 'warning')
        print_status('خطأ', 'error')
        print_status('تصحيح', 'debug')
        print_status('رسالة عادية', 'normal')
        
        # التحقق من عدد مرات استدعاء الدالة الوهمية
        self.assertEqual(mock_print.call_count, 6)

if __name__ == '__main__':
    unittest.main()