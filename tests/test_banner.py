#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات وحدة عرض الشعار
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# إضافة المجلد الرئيسي إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.banner import display_banner, display_target_info

class TestBanner(unittest.TestCase):
    """
    اختبارات لوحدة عرض الشعار
    """
    
    @patch('platform.system')
    @patch('platform.release')
    @patch('platform.version')
    @patch('platform.machine')
    @patch('datetime.datetime')
    @patch('builtins.print')
    def test_display_banner(self, mock_print, mock_datetime, mock_machine, mock_version, mock_release, mock_system):
        """
        اختبار عرض الشعار
        """
        # إعداد السلوك المتوقع للدوال الوهمية
        mock_system.return_value = 'Linux'
        mock_release.return_value = '5.15.0'
        mock_version.return_value = '#1 SMP PREEMPT_DYNAMIC'
        mock_machine.return_value = 'x86_64'
        
        mock_datetime_instance = MagicMock()
        mock_datetime_instance.strftime.return_value = '2023-12-01 12:00:00'
        mock_datetime.now.return_value = mock_datetime_instance
        
        # تنفيذ عرض الشعار
        display_banner()
        
        # التحقق من استدعاء الدوال الوهمية
        mock_system.assert_called_once()
        mock_release.assert_called_once()
        mock_version.assert_called_once()
        mock_machine.assert_called_once()
        mock_datetime.now.assert_called_once()
        mock_datetime_instance.strftime.assert_called_once()
        
        # التحقق من عدد مرات استدعاء دالة الطباعة (يجب أن تكون أكثر من مرة واحدة)
        self.assertGreater(mock_print.call_count, 1)
    
    @patch('builtins.print')
    def test_display_target_info(self, mock_print):
        """
        اختبار عرض معلومات الهدف
        """
        # تنفيذ عرض معلومات الهدف
        display_target_info('example.com', ['192.168.1.1', '10.0.0.1'])
        
        # التحقق من عدد مرات استدعاء دالة الطباعة (يجب أن تكون أكثر من مرة واحدة)
        self.assertGreater(mock_print.call_count, 1)
        
        # اختبار عرض معلومات الهدف بدون أهداف متعددة
        mock_print.reset_mock()
        display_target_info('example.com')
        
        # التحقق من عدد مرات استدعاء دالة الطباعة (يجب أن تكون أكثر من مرة واحدة)
        self.assertGreater(mock_print.call_count, 1)

if __name__ == '__main__':
    unittest.main()