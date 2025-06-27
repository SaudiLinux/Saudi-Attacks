#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات الملف الرئيسي للأداة
"""

import unittest
import sys
import os
import argparse
from unittest.mock import patch, MagicMock

# إضافة المجلد الرئيسي إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import saudi_attacks

class TestSaudiAttacks(unittest.TestCase):
    """
    اختبارات للملف الرئيسي للأداة
    """
    
    @patch('saudi_attacks.platform.system')
    def test_check_os(self, mock_system):
        """
        اختبار التحقق من نظام التشغيل
        """
        # اختبار نظام Linux
        mock_system.return_value = 'Linux'
        self.assertTrue(saudi_attacks.check_os())
        
        # اختبار نظام Windows
        mock_system.return_value = 'Windows'
        self.assertFalse(saudi_attacks.check_os())
        
        # اختبار نظام macOS
        mock_system.return_value = 'Darwin'
        self.assertFalse(saudi_attacks.check_os())
    
    @patch('saudi_attacks.argparse.ArgumentParser.parse_args')
    def test_parse_arguments(self, mock_parse_args):
        """
        اختبار تحليل المعاملات
        """
        # إعداد الوسيطات الوهمية
        mock_args = MagicMock()
        mock_args.target = 'example.com'
        mock_args.file = None
        mock_args.port_scan = True
        mock_args.web_scan = True
        mock_args.wordpress = False
        mock_args.joomla = False
        mock_args.vuln_scan = False
        mock_args.all = False
        mock_args.output = 'report.html'
        mock_args.quiet = False
        mock_args.debug = True
        mock_parse_args.return_value = mock_args
        
        # تنفيذ تحليل المعاملات
        args = saudi_attacks.parse_arguments()
        
        # التحقق من النتائج
        self.assertEqual(args.target, 'example.com')
        self.assertIsNone(args.file)
        self.assertTrue(args.port_scan)
        self.assertTrue(args.web_scan)
        self.assertFalse(args.wordpress)
        self.assertFalse(args.joomla)
        self.assertFalse(args.vuln_scan)
        self.assertFalse(args.all)
        self.assertEqual(args.output, 'report.html')
        self.assertFalse(args.quiet)
        self.assertTrue(args.debug)
    
    @patch('saudi_attacks.is_valid_ip')
    @patch('saudi_attacks.is_valid_domain')
    def test_process_targets(self, mock_is_valid_domain, mock_is_valid_ip):
        """
        اختبار معالجة الأهداف
        """
        # إعداد السلوك المتوقع للدوال الوهمية
        mock_is_valid_ip.side_effect = lambda x: x == '192.168.1.1'
        mock_is_valid_domain.side_effect = lambda x: x == 'example.com'
        
        # اختبار هدف واحد صالح (عنوان IP)
        targets = saudi_attacks.process_targets('192.168.1.1', None)
        self.assertEqual(targets, ['192.168.1.1'])
        
        # اختبار هدف واحد صالح (اسم نطاق)
        targets = saudi_attacks.process_targets('example.com', None)
        self.assertEqual(targets, ['example.com'])
        
        # اختبار هدف غير صالح
        with self.assertRaises(ValueError):
            saudi_attacks.process_targets('invalid-target', None)
        
        # اختبار ملف أهداف
        with patch('builtins.open', unittest.mock.mock_open(read_data='192.168.1.1\nexample.com\ninvalid-target')):
            targets = saudi_attacks.process_targets(None, 'targets.txt')
            self.assertEqual(targets, ['192.168.1.1', 'example.com'])
    
    @patch('saudi_attacks.check_os')
    @patch('saudi_attacks.check_root')
    @patch('saudi_attacks.check_dependencies')
    @patch('saudi_attacks.setup_logging')
    @patch('saudi_attacks.parse_arguments')
    @patch('saudi_attacks.process_targets')
    @patch('saudi_attacks.display_banner')
    @patch('saudi_attacks.display_target_info')
    @patch('saudi_attacks.InfoGathering')
    @patch('saudi_attacks.PortScanner')
    @patch('saudi_attacks.VulnerabilityScanner')
    @patch('saudi_attacks.WebScanner')
    @patch('saudi_attacks.CMSScanner')
    @patch('saudi_attacks.ReportGenerator')
    def test_main(self, mock_report_generator, mock_cms_scanner, mock_web_scanner, mock_vuln_scanner, mock_port_scanner, mock_info_gathering, mock_display_target_info, mock_display_banner, mock_process_targets, mock_parse_arguments, mock_setup_logging, mock_check_dependencies, mock_check_root, mock_check_os):
        """
        اختبار الدالة الرئيسية
        """
        # إعداد السلوك المتوقع للدوال الوهمية
        mock_check_os.return_value = True
        mock_check_root.return_value = True
        mock_check_dependencies.return_value = True
        
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        mock_args = MagicMock()
        mock_args.target = 'example.com'
        mock_args.file = None
        mock_args.port_scan = True
        mock_args.web_scan = True
        mock_args.wordpress = False
        mock_args.joomla = False
        mock_args.vuln_scan = True
        mock_args.all = False
        mock_args.output = 'report.html'
        mock_args.quiet = False
        mock_args.debug = True
        mock_parse_arguments.return_value = mock_args
        
        mock_process_targets.return_value = ['example.com']
        
        # إعداد كائنات وهمية للفاحصات
        mock_info_gathering_instance = MagicMock()
        mock_info_gathering_instance.gather.return_value = {'ip': '93.184.216.34'}
        mock_info_gathering.return_value = mock_info_gathering_instance
        
        mock_port_scanner_instance = MagicMock()
        mock_port_scanner_instance.scan_common_ports.return_value = {'scan': {}}
        mock_port_scanner.return_value = mock_port_scanner_instance
        
        mock_vuln_scanner_instance = MagicMock()
        mock_vuln_scanner_instance.scan.return_value = {'vulnerabilities': []}
        mock_vuln_scanner.return_value = mock_vuln_scanner_instance
        
        mock_web_scanner_instance = MagicMock()
        mock_web_scanner_instance.scan.return_value = {'server_info': {}}
        mock_web_scanner.return_value = mock_web_scanner_instance
        
        mock_cms_scanner_instance = MagicMock()
        mock_cms_scanner_instance.scan.return_value = {'cms_type': 'Unknown'}
        mock_cms_scanner.return_value = mock_cms_scanner_instance
        
        mock_report_generator_instance = MagicMock()
        mock_report_generator.return_value = mock_report_generator_instance
        
        # تنفيذ الدالة الرئيسية
        saudi_attacks.main()
        
        # التحقق من استدعاء الدوال الوهمية
        mock_check_os.assert_called_once()
        mock_check_root.assert_called_once()
        mock_check_dependencies.assert_called_once()
        mock_setup_logging.assert_called_once()
        mock_parse_arguments.assert_called_once()
        mock_process_targets.assert_called_once()
        mock_display_banner.assert_called_once()
        mock_display_target_info.assert_called_once()
        
        # التحقق من استدعاء الفاحصات
        mock_info_gathering.assert_called_once()
        mock_info_gathering_instance.gather.assert_called_once()
        
        mock_port_scanner.assert_called_once()
        mock_port_scanner_instance.scan_common_ports.assert_called_once()
        
        mock_vuln_scanner.assert_called_once()
        mock_vuln_scanner_instance.scan.assert_called_once()
        
        mock_web_scanner.assert_called_once()
        mock_web_scanner_instance.scan.assert_called_once()
        
        # التحقق من استدعاء مولد التقارير
        mock_report_generator.assert_called_once()
        mock_report_generator_instance.add_info_gathering_results.assert_called_once()
        mock_report_generator_instance.add_port_scan_results.assert_called_once()
        mock_report_generator_instance.add_vulnerability_scan_results.assert_called_once()
        mock_report_generator_instance.add_web_scan_results.assert_called_once()
        mock_report_generator_instance.generate_report.assert_called_once()

if __name__ == '__main__':
    unittest.main()