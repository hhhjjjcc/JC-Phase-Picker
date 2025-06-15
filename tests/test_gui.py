"""
GUI Component Tests
"""

import unittest
import tkinter as tk
from gui import MainWindow, PlotWidget, SettingsDialog, ProgressDialog
from config.settings import Settings
from config.constants import STATUS_MESSAGES

class TestMainWindow(unittest.TestCase):
    """Main Window Tests"""
    
    def setUp(self):
        """Setup before test"""
        self.root = tk.Tk()
        self.window = MainWindow()
    
    def tearDown(self):
        """Cleanup after test"""
        self.window.destroy()
        self.root.destroy()
    
    def test_window_title(self):
        """Test window title"""
        self.assertIn("P-wave First Arrival Phase Picking System", self.window.title())
    
    def test_file_operations(self):
        """Test file operations"""
        # Test add files
        self.window.add_files()
        self.assertEqual(len(self.window.file_manager.get_files()), 0)
        
        # Test add directory
        self.window.add_directory()
        self.assertEqual(len(self.window.file_manager.get_files()), 0)
        
        # Test clear file list
        self.window.clear_files()
        self.assertEqual(len(self.window.file_manager.get_files()), 0)
    
    def test_pick_operations(self):
        """Test picking operations"""
        # Test auto pick
        self.window.auto_pick()
        self.assertEqual(self.window.statusbar.cget('text'), STATUS_MESSAGES['auto_pick_failed'])
        
        # Test undo/redo
        self.window.undo()
        self.window.redo()
    
    def test_batch_operations(self):
        """Test batch operations"""
        # Test start batch
        self.window.start_batch()
        self.assertEqual(self.window.statusbar.cget('text'), STATUS_MESSAGES['batch_failed'])
        
        # Test pause/resume
        self.window.pause_batch()
        self.window.resume_batch()
        
        # Test stop
        self.window.stop_batch()
    
    def test_view_operations(self):
        """Test view operations"""
        # Test reset view
        self.window.reset_view()
        
        # Test zoom
        self.window.zoom_in()
        self.window.zoom_out()

class TestPlotWidget(unittest.TestCase):
    """Plot Widget Tests"""
    
    def setUp(self):
        """Setup before test"""
        self.root = tk.Tk()
        self.widget = PlotWidget(self.root)
    
    def tearDown(self):
        """Cleanup after test"""
        self.widget.destroy()
        self.root.destroy()
    
    def test_plot_trace(self):
        """Test plot waveform"""
        # Create test data
        import numpy as np
        from obspy import Trace
        data = np.random.randn(1000)
        trace = Trace(data=data)
        
        # Test plot
        self.widget.plot_trace(trace)
    
    def test_add_picks(self):
        """Test add picks"""
        # Create test data
        picks = [
            {'time': 0.5, 'quality': 'A'},
            {'time': 1.0, 'quality': 'B'}
        ]
        
        # Test add
        self.widget.add_picks(picks)
    
    def test_zoom_operations(self):
        """Test zoom operations"""
        # Test zoom in
        self.widget.zoom_in()
        
        # Test zoom out
        self.widget.zoom_out()
        
        # Test reset
        self.widget.reset_view()

class TestSettingsDialog(unittest.TestCase):
    """Settings Dialog Tests"""
    
    def setUp(self):
        """Setup before test"""
        self.root = tk.Tk()
        self.dialog = SettingsDialog(self.root)
    
    def tearDown(self):
        """Cleanup after test"""
        self.dialog.destroy()
        self.root.destroy()
    
    def test_load_settings(self):
        """Test load settings"""
        self.dialog.load_settings()
    
    def test_save_settings(self):
        """Test save settings"""
        # Modify settings
        self.dialog.window_size.delete(0, tk.END)
        self.dialog.window_size.insert(0, "800x600")
        
        # Save settings
        self.dialog.save_settings()
    
    def test_reset_settings(self):
        """Test reset settings"""
        self.dialog.reset_settings()

class TestProgressDialog(unittest.TestCase):
    """Progress Dialog Tests"""
    
    def setUp(self):
        """Setup before test"""
        self.root = tk.Tk()
        self.dialog = ProgressDialog(self.root)
    
    def tearDown(self):
        """Cleanup after test"""
        self.dialog.destroy()
        self.root.destroy()
    
    def test_update_progress(self):
        """Test update progress"""
        # Test determinate mode
        self.dialog.update_progress(50)
        
        # Test indeterminate mode
        self.dialog.set_indeterminate(True)
        self.dialog.update_progress(0, "Processing...")
    
    def test_cancel(self):
        """Test cancel operation"""
        self.dialog.cancel()
        self.assertTrue(self.dialog.cancelled)

if __name__ == '__main__':
    unittest.main() 