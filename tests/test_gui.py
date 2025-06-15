"""
GUI组件测试
"""

import unittest
import tkinter as tk
from gui import MainWindow, PlotWidget, SettingsDialog, ProgressDialog
from config.settings import Settings
from config.constants import STATUS_MESSAGES

class TestMainWindow(unittest.TestCase):
    """主窗口测试"""
    
    def setUp(self):
        """测试前准备"""
        self.root = tk.Tk()
        self.window = MainWindow()
    
    def tearDown(self):
        """测试后清理"""
        self.window.destroy()
        self.root.destroy()
    
    def test_window_title(self):
        """测试窗口标题"""
        self.assertIn("P波初至震相拾取系统", self.window.title())
    
    def test_file_operations(self):
        """测试文件操作"""
        # 测试添加文件
        self.window.add_files()
        self.assertEqual(len(self.window.file_manager.get_files()), 0)
        
        # 测试添加目录
        self.window.add_directory()
        self.assertEqual(len(self.window.file_manager.get_files()), 0)
        
        # 测试清空文件列表
        self.window.clear_files()
        self.assertEqual(len(self.window.file_manager.get_files()), 0)
    
    def test_pick_operations(self):
        """测试拾取操作"""
        # 测试自动拾取
        self.window.auto_pick()
        self.assertEqual(self.window.statusbar.cget('text'), STATUS_MESSAGES['auto_pick_failed'])
        
        # 测试撤销/重做
        self.window.undo()
        self.window.redo()
    
    def test_batch_operations(self):
        """测试批处理操作"""
        # 测试开始批处理
        self.window.start_batch()
        self.assertEqual(self.window.statusbar.cget('text'), STATUS_MESSAGES['batch_failed'])
        
        # 测试暂停/继续
        self.window.pause_batch()
        self.window.resume_batch()
        
        # 测试停止
        self.window.stop_batch()
    
    def test_view_operations(self):
        """测试视图操作"""
        # 测试重置视图
        self.window.reset_view()
        
        # 测试缩放
        self.window.zoom_in()
        self.window.zoom_out()

class TestPlotWidget(unittest.TestCase):
    """绘图组件测试"""
    
    def setUp(self):
        """测试前准备"""
        self.root = tk.Tk()
        self.widget = PlotWidget(self.root)
    
    def tearDown(self):
        """测试后清理"""
        self.widget.destroy()
        self.root.destroy()
    
    def test_plot_trace(self):
        """测试绘制波形"""
        # 创建测试数据
        import numpy as np
        from obspy import Trace
        data = np.random.randn(1000)
        trace = Trace(data=data)
        
        # 测试绘制
        self.widget.plot_trace(trace)
    
    def test_add_picks(self):
        """测试添加拾取"""
        # 创建测试数据
        picks = [
            {'time': 0.5, 'quality': 'A'},
            {'time': 1.0, 'quality': 'B'}
        ]
        
        # 测试添加
        self.widget.add_picks(picks)
    
    def test_zoom_operations(self):
        """测试缩放操作"""
        # 测试放大
        self.widget.zoom_in()
        
        # 测试缩小
        self.widget.zoom_out()
        
        # 测试重置
        self.widget.reset_view()

class TestSettingsDialog(unittest.TestCase):
    """设置对话框测试"""
    
    def setUp(self):
        """测试前准备"""
        self.root = tk.Tk()
        self.dialog = SettingsDialog(self.root)
    
    def tearDown(self):
        """测试后清理"""
        self.dialog.destroy()
        self.root.destroy()
    
    def test_load_settings(self):
        """测试加载设置"""
        self.dialog.load_settings()
    
    def test_save_settings(self):
        """测试保存设置"""
        # 修改设置
        self.dialog.window_size.delete(0, tk.END)
        self.dialog.window_size.insert(0, "800x600")
        
        # 保存设置
        self.dialog.save_settings()
    
    def test_reset_settings(self):
        """测试重置设置"""
        self.dialog.reset_settings()

class TestProgressDialog(unittest.TestCase):
    """进度对话框测试"""
    
    def setUp(self):
        """测试前准备"""
        self.root = tk.Tk()
        self.dialog = ProgressDialog(self.root)
    
    def tearDown(self):
        """测试后清理"""
        self.dialog.destroy()
        self.root.destroy()
    
    def test_update_progress(self):
        """测试更新进度"""
        # 测试确定模式
        self.dialog.update_progress(50)
        
        # 测试不确定模式
        self.dialog.set_indeterminate(True)
        self.dialog.update_progress(0, "处理中...")
    
    def test_cancel(self):
        """测试取消操作"""
        self.dialog.cancel()
        self.assertTrue(self.dialog.cancelled)

if __name__ == '__main__':
    unittest.main() 