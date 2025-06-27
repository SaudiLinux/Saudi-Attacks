#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات وحدة توليد التقارير
"""

import unittest
import sys
import os
import logging
import json
from unittest.mock import patch, MagicMock, mock_open

# إضافة المجلد الرئيسي إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    """
    اختبارات لوحدة توليد التقارير
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
        
        # إنشاء كائن ReportGenerator للاختبار
        self.report_generator = ReportGenerator('example.com', 'test_report.html', self.logger, quiet=True, debug=True)
        
        # بيانات اختبار لإضافتها إلى التقرير
        self.test_info_gathering_data = {
            'ip': '93.184.216.34',
            'dns_records': {
                'A': ['93.184.216.34'],
                'MX': ['0 example.com'],
                'NS': ['a.iana-servers.net', 'b.iana-servers.net'],
                'TXT': ['v=spf1 -all']
            },
            'whois': 'Domain Name: EXAMPLE.COM\nRegistry Domain ID: 2336799_DOMAIN_COM-VRSN',
            'geolocation': {
                'country': 'United States',
                'city': 'Los Angeles',
                'region': 'California',
                'lat': 34.0544,
                'lon': -118.2441
            },
            'web_info': {
                'http': {
                    'status_code': 200,
                    'server': 'ECS (dcb/7F84)',
                    'title': 'Example Domain'
                },
                'https': {
                    'status_code': 200,
                    'server': 'ECS (dcb/7F84)',
                    'title': 'Example Domain'
                }
            }
        }
        
        self.test_port_scan_data = {
            'scan': {
                'example.com': {
                    'tcp': {
                        80: {
                            'state': 'open',
                            'reason': 'syn-ack',
                            'name': 'http',
                            'product': 'nginx',
                            'version': '1.18.0'
                        },
                        443: {
                            'state': 'open',
                            'reason': 'syn-ack',
                            'name': 'https',
                            'product': 'nginx',
                            'version': '1.18.0'
                        },
                        22: {
                            'state': 'filtered',
                            'reason': 'no-response',
                            'name': 'ssh'
                        }
                    }
                }
            }
        }
        
        self.test_vulnerability_scan_data = {
            'known_vulnerabilities': [
                {
                    'name': 'Heartbleed',
                    'vulnerable': False,
                    'details': 'Not vulnerable to Heartbleed'
                },
                {
                    'name': 'Shellshock',
                    'vulnerable': False,
                    'details': 'Not vulnerable to Shellshock'
                }
            ],
            'ssl_tls': {
                'hsts': {
                    'enabled': True,
                    'details': 'HSTS is properly configured'
                },
                'tls_versions': {
                    'TLSv1.0': False,
                    'TLSv1.1': False,
                    'TLSv1.2': True,
                    'TLSv1.3': True
                }
            },
            'exposed_services': [],
            'misconfigurations': [
                {
                    'name': 'Directory Listing',
                    'url': 'https://example.com/images/',
                    'details': 'Directory listing is enabled'
                }
            ]
        }
        
        self.test_web_scan_data = {
            'server_info': {
                'http': {
                    'status_code': 200,
                    'server': 'nginx/1.18.0',
                    'title': 'Example Domain'
                },
                'https': {
                    'status_code': 200,
                    'server': 'nginx/1.18.0',
                    'title': 'Example Domain'
                }
            },
            'security_headers': {
                'hsts': {
                    'present': True,
                    'value': 'max-age=31536000'
                },
                'csp': {
                    'present': False
                },
                'x_content_type_options': {
                    'present': True,
                    'value': 'nosniff'
                },
                'x_frame_options': {
                    'present': True,
                    'value': 'DENY'
                },
                'x_xss_protection': {
                    'present': True,
                    'value': '1; mode=block'
                }
            },
            'sensitive_files': [
                {
                    'url': 'https://example.com/robots.txt',
                    'status_code': 200,
                    'content_length': 42
                }
            ],
            'web_vulnerabilities': [
                {
                    'name': 'Missing Security Headers',
                    'details': 'Content-Security-Policy header is missing',
                    'severity': 'Medium'
                }
            ]
        }
        
        self.test_cms_scan_data = {
            'cms_type': 'WordPress',
            'version': '5.9.3',
            'wordpress_users': [
                {
                    'id': 1,
                    'name': 'admin',
                    'slug': 'admin'
                }
            ],
            'wordpress_plugins': [
                {
                    'name': 'contact-form-7',
                    'version': '5.5.6',
                    'vulnerabilities': []
                },
                {
                    'name': 'woocommerce',
                    'version': '6.3.1',
                    'vulnerabilities': [
                        {
                            'name': 'SQL Injection',
                            'severity': 'High',
                            'fixed_in': '6.4.0'
                        }
                    ]
                }
            ],
            'wordpress_themes': [
                {
                    'name': 'twentytwentytwo',
                    'version': '1.1',
                    'vulnerabilities': []
                }
            ],
            'wordpress_vulnerabilities': [
                {
                    'name': 'Outdated WordPress Version',
                    'details': 'Current version 5.9.3 is outdated. Latest version is 6.0.0',
                    'severity': 'Medium'
                }
            ]
        }
    
    def test_initialization(self):
        """
        اختبار تهيئة الكائن
        """
        self.assertEqual(self.report_generator.target, 'example.com')
        self.assertEqual(self.report_generator.output_file, 'test_report.html')
        self.assertTrue(self.report_generator.quiet)
        self.assertTrue(self.report_generator.debug)
    
    def test_add_info_gathering_results(self):
        """
        اختبار إضافة نتائج جمع المعلومات
        """
        self.report_generator.add_info_gathering_results(self.test_info_gathering_data)
        self.assertEqual(self.report_generator.info_gathering_results, self.test_info_gathering_data)
    
    def test_add_port_scan_results(self):
        """
        اختبار إضافة نتائج فحص المنافذ
        """
        self.report_generator.add_port_scan_results(self.test_port_scan_data)
        self.assertEqual(self.report_generator.port_scan_results, self.test_port_scan_data)
    
    def test_add_vulnerability_scan_results(self):
        """
        اختبار إضافة نتائج فحص الثغرات
        """
        self.report_generator.add_vulnerability_scan_results(self.test_vulnerability_scan_data)
        self.assertEqual(self.report_generator.vulnerability_scan_results, self.test_vulnerability_scan_data)
    
    def test_add_web_scan_results(self):
        """
        اختبار إضافة نتائج فحص الويب
        """
        self.report_generator.add_web_scan_results(self.test_web_scan_data)
        self.assertEqual(self.report_generator.web_scan_results, self.test_web_scan_data)
    
    def test_add_cms_scan_results(self):
        """
        اختبار إضافة نتائج فحص CMS
        """
        self.report_generator.add_cms_scan_results(self.test_cms_scan_data)
        self.assertEqual(self.report_generator.cms_scan_results, self.test_cms_scan_data)
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_generate_json_report(self, mock_json_dump, mock_file_open, mock_makedirs, mock_exists):
        """
        اختبار توليد تقرير JSON
        """
        # إعداد السلوك المتوقع للدوال الوهمية
        mock_exists.return_value = False
        
        # إضافة بيانات الاختبار
        self.report_generator.add_info_gathering_results(self.test_info_gathering_data)
        self.report_generator.add_port_scan_results(self.test_port_scan_data)
        self.report_generator.add_vulnerability_scan_results(self.test_vulnerability_scan_data)
        self.report_generator.add_web_scan_results(self.test_web_scan_data)
        self.report_generator.add_cms_scan_results(self.test_cms_scan_data)
        
        # تنفيذ توليد تقرير JSON
        self.report_generator._generate_json_report()
        
        # التحقق من النتائج
        mock_exists.assert_called_once()
        mock_makedirs.assert_called_once()
        mock_file_open.assert_called_once()
        mock_json_dump.assert_called_once()
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('modules.report_generator.ReportGenerator._generate_ports_chart')
    @patch('modules.report_generator.ReportGenerator._generate_vulnerabilities_chart')
    @patch('modules.report_generator.ReportGenerator._generate_json_report')
    def test_generate_report(self, mock_json_report, mock_vuln_chart, mock_ports_chart, mock_file_open, mock_makedirs, mock_exists):
        """
        اختبار توليد التقرير الكامل
        """
        # إعداد السلوك المتوقع للدوال الوهمية
        mock_exists.return_value = False
        mock_ports_chart.return_value = 'ports_chart.png'
        mock_vuln_chart.return_value = 'vulnerabilities_chart.png'
        
        # إضافة بيانات الاختبار
        self.report_generator.add_info_gathering_results(self.test_info_gathering_data)
        self.report_generator.add_port_scan_results(self.test_port_scan_data)
        self.report_generator.add_vulnerability_scan_results(self.test_vulnerability_scan_data)
        self.report_generator.add_web_scan_results(self.test_web_scan_data)
        self.report_generator.add_cms_scan_results(self.test_cms_scan_data)
        
        # تنفيذ توليد التقرير
        self.report_generator.generate_report()
        
        # التحقق من النتائج
        mock_exists.assert_called()
        mock_makedirs.assert_called_once()
        mock_ports_chart.assert_called_once()
        mock_vuln_chart.assert_called_once()
        mock_json_report.assert_called_once()
        mock_file_open.assert_called()

if __name__ == '__main__':
    unittest.main()