#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات وحدة فحص المنافذ
"""

import unittest
import sys
import os
import logging
from unittest.mock import patch, MagicMock

# إضافة المجلد الرئيسي إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.port_scanner import PortScanner

class TestPortScanner(unittest.TestCase):
    """
    اختبارات لوحدة فحص المنافذ
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
        
        # إنشاء كائن PortScanner للاختبار
        self.port_scanner = PortScanner('example.com', self.logger, quiet=True, debug=True)
    
    def test_initialization(self):
        """
        اختبار تهيئة الكائن
        """
        self.assertEqual(self.port_scanner.target, 'example.com')
        self.assertTrue(self.port_scanner.quiet)
        self.assertTrue(self.port_scanner.debug)
    
    @patch('modules.port_scanner.nmap.PortScanner')
    def test_scan(self, mock_nmap):
        """
        اختبار وظيفة المسح
        """
        # إنشاء كائن وهمي لنتائج المسح
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.scan.return_value = {
            'scan': {
                'example.com': {
                    'tcp': {
                        80: {
                            'state': 'open',
                            'reason': 'syn-ack',
                            'name': 'http',
                            'product': 'nginx',
                            'version': '1.18.0',
                            'extrainfo': '',
                            'conf': '10',
                            'cpe': 'cpe:/a:nginx:nginx:1.18.0'
                        },
                        443: {
                            'state': 'open',
                            'reason': 'syn-ack',
                            'name': 'https',
                            'product': 'nginx',
                            'version': '1.18.0',
                            'extrainfo': '',
                            'conf': '10',
                            'cpe': 'cpe:/a:nginx:nginx:1.18.0'
                        }
                    }
                }
            }
        }
        mock_nmap.return_value = mock_scanner_instance
        
        # تنفيذ المسح
        result = self.port_scanner.scan(ports="80,443", args="-sV")
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertIn('scan', result)
        mock_scanner_instance.scan.assert_called_once()
    
    @patch('modules.port_scanner.PortScanner.scan')
    def test_scan_common_ports(self, mock_scan):
        """
        اختبار مسح المنافذ الشائعة
        """
        mock_scan.return_value = {'scan': {'example.com': {'tcp': {80: {'state': 'open'}}}}}
        
        # تنفيذ مسح المنافذ الشائعة
        result = self.port_scanner.scan_common_ports()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        mock_scan.assert_called_once()
    
    @patch('modules.port_scanner.PortScanner.scan')
    def test_scan_all_ports(self, mock_scan):
        """
        اختبار مسح جميع المنافذ
        """
        mock_scan.return_value = {'scan': {'example.com': {'tcp': {80: {'state': 'open'}}}}}
        
        # تنفيذ مسح جميع المنافذ
        result = self.port_scanner.scan_all_ports()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        mock_scan.assert_called_once()
    
    @patch('modules.port_scanner.PortScanner.scan')
    def test_scan_web_ports(self, mock_scan):
        """
        اختبار مسح منافذ الويب
        """
        mock_scan.return_value = {'scan': {'example.com': {'tcp': {80: {'state': 'open'}, 443: {'state': 'open'}}}}}
        
        # تنفيذ مسح منافذ الويب
        result = self.port_scanner.scan_web_ports()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        mock_scan.assert_called_once()
    
    @patch('modules.port_scanner.PortScanner.scan')
    def test_os_detection(self, mock_scan):
        """
        اختبار اكتشاف نظام التشغيل
        """
        mock_scan.return_value = {
            'scan': {
                'example.com': {
                    'osmatch': [
                        {
                            'name': 'Linux 4.15',
                            'accuracy': '95',
                            'line': '1',
                            'osclass': [
                                {
                                    'type': 'general purpose',
                                    'vendor': 'Linux',
                                    'osfamily': 'Linux',
                                    'osgen': '4.X',
                                    'accuracy': '95'
                                }
                            ]
                        }
                    ]
                }
            }
        }
        
        # تنفيذ اكتشاف نظام التشغيل
        result = self.port_scanner.os_detection()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        mock_scan.assert_called_once()

if __name__ == '__main__':
    unittest.main()