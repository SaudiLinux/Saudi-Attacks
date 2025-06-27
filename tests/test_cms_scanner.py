#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات وحدة فحص أنظمة إدارة المحتوى
"""

import unittest
import sys
import os
import logging
from unittest.mock import patch, MagicMock

# إضافة المجلد الرئيسي إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.cms_scanner import CMSScanner

class TestCMSScanner(unittest.TestCase):
    """
    اختبارات لوحدة فحص أنظمة إدارة المحتوى
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
        
        # إنشاء كائن CMSScanner للاختبار
        self.cms_scanner = CMSScanner('example.com', self.logger, quiet=True, debug=True)
    
    def test_initialization(self):
        """
        اختبار تهيئة الكائن
        """
        self.assertEqual(self.cms_scanner.target, 'example.com')
        self.assertTrue(self.cms_scanner.quiet)
        self.assertTrue(self.cms_scanner.debug)
    
    @patch('modules.cms_scanner.requests.get')
    def test_detect_cms_wordpress(self, mock_get):
        """
        اختبار اكتشاف نظام WordPress
        """
        # إعداد الاستجابة الوهمية لصفحة WordPress
        mock_response = MagicMock()
        mock_response.text = '''
        <!DOCTYPE html>
        <html lang="en-US">
        <head>
            <meta charset="UTF-8">
            <meta name="generator" content="WordPress 5.9.3">
            <link rel="stylesheet" id="wp-block-library-css" href="https://example.com/wp-includes/css/dist/block-library/style.min.css?ver=5.9.3" type="text/css" media="all">
            <title>Example WordPress Site</title>
        </head>
        <body class="home page-template-default page page-id-1 wp-custom-logo">
            <div id="page" class="site">
                <header id="masthead" class="site-header">
                    <div class="site-branding">
                        <h1 class="site-title"><a href="https://example.com/" rel="home">Example WordPress Site</a></h1>
                    </div>
                </header>
                <div id="content" class="site-content">
                    <div id="primary" class="content-area">
                        <main id="main" class="site-main">
                            <article id="post-1" class="post-1 page type-page status-publish hentry">
                                <div class="entry-content">
                                    <p>Welcome to my WordPress site.</p>
                                </div>
                            </article>
                        </main>
                    </div>
                </div>
                <footer id="colophon" class="site-footer">
                    <div class="site-info">
                        <a href="https://wordpress.org/">Proudly powered by WordPress</a>
                    </div>
                </footer>
            </div>
            <script type='text/javascript' src='https://example.com/wp-includes/js/wp-embed.min.js?ver=5.9.3' id='wp-embed-js'></script>
        </body>
        </html>
        '''
        mock_get.return_value = mock_response
        
        # تنفيذ اكتشاف نظام إدارة المحتوى
        result = self.cms_scanner.detect_cms()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertEqual(result['cms_type'], 'WordPress')
        self.assertEqual(result['version'], '5.9.3')
        
        # التحقق من استدعاء الدالة الوهمية
        mock_get.assert_called_once()
    
    @patch('modules.cms_scanner.requests.get')
    def test_detect_cms_joomla(self, mock_get):
        """
        اختبار اكتشاف نظام Joomla
        """
        # إعداد الاستجابة الوهمية لصفحة Joomla
        mock_response = MagicMock()
        mock_response.text = '''
        <!DOCTYPE html>
        <html lang="en-gb" dir="ltr">
        <head>
            <meta name="generator" content="Joomla! 4.1.2 - Open Source Content Management">
            <title>Example Joomla Site</title>
            <link href="/media/vendor/joomla-custom-elements/css/joomla-alert.min.css?4.1.2" rel="stylesheet">
            <link href="/templates/cassiopeia/css/template.min.css?4.1.2" rel="stylesheet">
        </head>
        <body class="site">
            <div class="body">
                <header class="header container-header full-width">
                    <div class="grid-child">
                        <div class="navbar-brand">
                            <a href="/">Example Joomla Site</a>
                        </div>
                    </div>
                </header>
                <div class="container-component">
                    <div class="grid-child">
                        <main>
                            <div class="com-content-article item-page">
                                <div class="com-content-article__body">
                                    <p>Welcome to my Joomla site.</p>
                                </div>
                            </div>
                        </main>
                    </div>
                </div>
                <footer class="container-footer footer full-width">
                    <div class="grid-child">
                        <div class="copyright">
                            &copy; 2023 Example Joomla Site
                        </div>
                    </div>
                </footer>
            </div>
            <script src="/media/system/js/core.min.js?4.1.2"></script>
        </body>
        </html>
        '''
        mock_get.return_value = mock_response
        
        # تنفيذ اكتشاف نظام إدارة المحتوى
        result = self.cms_scanner.detect_cms()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertEqual(result['cms_type'], 'Joomla')
        self.assertEqual(result['version'], '4.1.2')
        
        # التحقق من استدعاء الدالة الوهمية
        mock_get.assert_called_once()
    
    @patch('modules.cms_scanner.requests.get')
    def test_detect_cms_unknown(self, mock_get):
        """
        اختبار اكتشاف نظام إدارة محتوى غير معروف
        """
        # إعداد الاستجابة الوهمية لصفحة غير معروفة
        mock_response = MagicMock()
        mock_response.text = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Example Website</title>
        </head>
        <body>
            <h1>Welcome to my website</h1>
            <p>This is a custom website without a known CMS.</p>
        </body>
        </html>
        '''
        mock_get.return_value = mock_response
        
        # تنفيذ اكتشاف نظام إدارة المحتوى
        result = self.cms_scanner.detect_cms()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertEqual(result['cms_type'], 'Unknown')
        self.assertIsNone(result['version'])
        
        # التحقق من استدعاء الدالة الوهمية
        mock_get.assert_called_once()
    
    @patch('modules.cms_scanner.CMSScanner.detect_cms')
    @patch('modules.cms_scanner.requests.get')
    def test_scan_wordpress(self, mock_get, mock_detect_cms):
        """
        اختبار فحص WordPress
        """
        # إعداد نتيجة اكتشاف CMS
        mock_detect_cms.return_value = {
            'cms_type': 'WordPress',
            'version': '5.9.3'
        }
        
        # إعداد الاستجابات الوهمية لطلبات WordPress
        mock_responses = []
        
        # استجابة لـ /wp-json/wp/v2/users
        users_response = MagicMock()
        users_response.status_code = 200
        users_response.json.return_value = [
            {
                'id': 1,
                'name': 'admin',
                'slug': 'admin',
                'description': 'Administrator'
            },
            {
                'id': 2,
                'name': 'editor',
                'slug': 'editor',
                'description': 'Editor'
            }
        ]
        mock_responses.append(users_response)
        
        # استجابة لـ /wp-content/plugins/
        plugins_response = MagicMock()
        plugins_response.status_code = 403
        plugins_response.text = 'Forbidden'
        mock_responses.append(plugins_response)
        
        # استجابة لـ /wp-content/themes/
        themes_response = MagicMock()
        themes_response.status_code = 403
        themes_response.text = 'Forbidden'
        mock_responses.append(themes_response)
        
        # تكوين السلوك المتوقع للدالة الوهمية
        mock_get.side_effect = mock_responses
        
        # تنفيذ فحص WordPress
        result = self.cms_scanner.scan()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertEqual(result['cms_type'], 'WordPress')
        self.assertEqual(result['version'], '5.9.3')
        self.assertIn('wordpress_users', result)
        self.assertEqual(len(result['wordpress_users']), 2)
        
        # التحقق من استدعاء الدالة الوهمية
        mock_detect_cms.assert_called_once()
        self.assertEqual(mock_get.call_count, 3)  # 3 طلبات: المستخدمين، الإضافات، القوالب
    
    @patch('modules.cms_scanner.CMSScanner.detect_cms')
    @patch('modules.cms_scanner.requests.get')
    def test_scan_joomla(self, mock_get, mock_detect_cms):
        """
        اختبار فحص Joomla
        """
        # إعداد نتيجة اكتشاف CMS
        mock_detect_cms.return_value = {
            'cms_type': 'Joomla',
            'version': '4.1.2'
        }
        
        # إعداد الاستجابات الوهمية لطلبات Joomla
        mock_responses = []
        
        # استجابة لـ /administrator/
        admin_response = MagicMock()
        admin_response.status_code = 200
        admin_response.text = '<html><body><form id="form-login">Joomla Administrator Login</form></body></html>'
        mock_responses.append(admin_response)
        
        # استجابة لـ /components/
        components_response = MagicMock()
        components_response.status_code = 403
        components_response.text = 'Forbidden'
        mock_responses.append(components_response)
        
        # استجابة لـ /modules/
        modules_response = MagicMock()
        modules_response.status_code = 403
        modules_response.text = 'Forbidden'
        mock_responses.append(modules_response)
        
        # استجابة لـ /templates/
        templates_response = MagicMock()
        templates_response.status_code = 403
        templates_response.text = 'Forbidden'
        mock_responses.append(templates_response)
        
        # تكوين السلوك المتوقع للدالة الوهمية
        mock_get.side_effect = mock_responses
        
        # تنفيذ فحص Joomla
        result = self.cms_scanner.scan()
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertEqual(result['cms_type'], 'Joomla')
        self.assertEqual(result['version'], '4.1.2')
        self.assertIn('joomla_admin_accessible', result)
        self.assertTrue(result['joomla_admin_accessible'])
        
        # التحقق من استدعاء الدالة الوهمية
        mock_detect_cms.assert_called_once()
        self.assertEqual(mock_get.call_count, 4)  # 4 طلبات: المدير، المكونات، الوحدات، القوالب

if __name__ == '__main__':
    unittest.main()