"""
Progress Dialog
"""

import tkinter as tk
from tkinter import ttk
from config.settings import Settings

class ProgressDialog(tk.Toplevel):
    """Progress Dialog"""
    
    def __init__(self, parent, title="Processing Progress"):
        """Initialize the dialog"""
        super().__init__(parent)
        
        # Set window properties
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)
        
        # Create UI
        self.create_widgets()
        
        # Set modal
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.center_window()
    
    def create_widgets(self):
        """Create widgets"""
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            self,
            variable=self.progress_var,
            maximum=100
        )
        self.progress.pack(fill=tk.X, padx=10, pady=10)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready...")
        self.status = ttk.Label(
            self,
            textvariable=self.status_var
        )
        self.status.pack(fill=tk.X, padx=10, pady=5)
        
        # Cancel button
        self.cancel_button = ttk.Button(
            self,
            text="Cancel",
            command=self.on_cancel
        )
        self.cancel_button.pack(pady=10)
    
    def update_progress(self, value, status=None):
        """Update progress"""
        self.progress_var.set(value)
        if status:
            self.status_var.set(status)
        self.update()
    
    def on_cancel(self):
        """Cancel button event"""
        self.destroy()
    
    def center_window(self):
        """Center window"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}') 