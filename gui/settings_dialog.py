"""
Settings Dialog
"""

import tkinter as tk
from tkinter import ttk, filedialog
from config.settings import Settings
from config.constants import DEFAULT_PARAMS

class SettingsDialog(tk.Toplevel):
    """Settings Dialog"""
    
    def __init__(self, parent):
        """Initialize the dialog"""
        super().__init__(parent)
        
        # Set window properties
        self.title("Settings")
        self.geometry("600x400")
        self.resizable(False, False)
        
        # Initialize settings
        self.settings = Settings()
        
        # Create UI
        self.create_widgets()
        
        # Load current settings
        self.load_settings()
        
        # Set modal
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.center_window()
    
    def create_widgets(self):
        """Create widgets"""
        # Create tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create individual setting pages
        self.create_ui_page()
        self.create_plot_page()
        self.create_process_page()
        self.create_path_page()
        self.create_filter_page()
        
        # Create buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="OK", command=self.on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.on_cancel).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Apply", command=self.on_apply).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.on_reset).pack(side=tk.RIGHT, padx=5)
    
    def create_ui_page(self):
        """Create UI settings page"""
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text="UI")
        
        # Window Size
        ttk.Label(page, text="Window Size:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.window_size_var = tk.StringVar()
        ttk.Entry(page, textvariable=self.window_size_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        # Theme
        ttk.Label(page, text="Theme:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.theme_var = tk.StringVar()
        ttk.Combobox(page, textvariable=self.theme_var, values=['default', 'dark', 'light'], width=20).grid(row=1, column=1, padx=5, pady=5)
        
        # Show Grid
        self.show_grid_var = tk.BooleanVar()
        ttk.Checkbutton(page, text="Show Grid", variable=self.show_grid_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
    
    def create_plot_page(self):
        """Create plot settings page"""
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text="Plot")
        
        # Line Width
        ttk.Label(page, text="Line Width:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.line_width_var = tk.DoubleVar()
        ttk.Entry(page, textvariable=self.line_width_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        # Background Color
        ttk.Label(page, text="Background Color:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.bg_color_var = tk.StringVar()
        ttk.Entry(page, textvariable=self.bg_color_var, width=20).grid(row=1, column=1, padx=5, pady=5)
        
        # Auto Scale
        self.auto_scale_var = tk.BooleanVar()
        ttk.Checkbutton(page, text="Auto Scale", variable=self.auto_scale_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
    
    def create_process_page(self):
        """Create processing settings page"""
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text="Process")
        
        # Sampling Rate
        ttk.Label(page, text="Sampling Rate:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.sampling_rate_var = tk.DoubleVar()
        ttk.Entry(page, textvariable=self.sampling_rate_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        # Preprocess
        self.preprocess_var = tk.BooleanVar()
        ttk.Checkbutton(page, text="Preprocess", variable=self.preprocess_var).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Auto Pick
        self.auto_pick_var = tk.BooleanVar()
        ttk.Checkbutton(page, text="Auto Pick", variable=self.auto_pick_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
    
    def create_path_page(self):
        """Create path settings page"""
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text="Paths")
        
        # Data Directory
        ttk.Label(page, text="Data Directory:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_dir_var = tk.StringVar()
        ttk.Entry(page, textvariable=self.data_dir_var, width=40).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(page, text="Browse", command=lambda: self.browse_directory(self.data_dir_var)).grid(row=0, column=2, padx=5, pady=5)
        
        # Output Directory
        ttk.Label(page, text="Output Directory:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.output_dir_var = tk.StringVar()
        ttk.Entry(page, textvariable=self.output_dir_var, width=40).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(page, text="Browse", command=lambda: self.browse_directory(self.output_dir_var)).grid(row=1, column=2, padx=5, pady=5)
    
    def create_filter_page(self):
        """Create filter settings page"""
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text="Filter")
        
        # Filter Type
        ttk.Label(page, text="Filter Type:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.filter_type_var = tk.StringVar()
        ttk.Combobox(page, textvariable=self.filter_type_var, values=['bandpass', 'highpass', 'lowpass'], width=20).grid(row=0, column=1, padx=5, pady=5)
        
        # Frequency Range
        ttk.Label(page, text="Frequency Range:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.freq_range_var = tk.StringVar()
        ttk.Entry(page, textvariable=self.freq_range_var, width=20).grid(row=1, column=1, padx=5, pady=5)
    
    def load_settings(self):
        """Load settings"""
        # UI settings
        window_size = self.settings.get('ui', 'window_size')
        self.window_size_var.set(f"{window_size[0]}x{window_size[1]}")
        self.theme_var.set(self.settings.get('ui', 'theme'))
        self.show_grid_var.set(self.settings.get('ui', 'show_grid'))
        
        # Plot settings
        self.line_width_var.set(self.settings.get('plot', 'line_width'))
        self.bg_color_var.set(self.settings.get('plot', 'background_color'))
        self.auto_scale_var.set(self.settings.get('plot', 'auto_scale'))
        
        # Processing settings
        self.sampling_rate_var.set(self.settings.get('process', 'sampling_rate'))
        self.preprocess_var.set(self.settings.get('process', 'preprocess'))
        self.auto_pick_var.set(self.settings.get('process', 'auto_pick'))
        
        # Path settings
        self.data_dir_var.set(self.settings.get('paths', 'data_dir'))
        self.output_dir_var.set(self.settings.get('paths', 'output_dir'))
        
        # Filter settings
        self.filter_type_var.set(self.settings.get('filter', 'type'))
        freq_range = self.settings.get('filter', 'freq_range')
        self.freq_range_var.set(f"{freq_range[0]}-{freq_range[1]}")
    
    def save_settings(self):
        """Save settings"""
        # UI settings
        window_size = [int(x) for x in self.window_size_var.get().split('x')]
        self.settings.set('ui', 'window_size', window_size)
        self.settings.set('ui', 'theme', self.theme_var.get())
        self.settings.set('ui', 'show_grid', self.show_grid_var.get())
        
        # Plot settings
        self.settings.set('plot', 'line_width', self.line_width_var.get())
        self.settings.set('plot', 'background_color', self.bg_color_var.get())
        self.settings.set('plot', 'auto_scale', self.auto_scale_var.get())
        
        # Processing settings
        self.settings.set('process', 'sampling_rate', self.sampling_rate_var.get())
        self.settings.set('process', 'preprocess', self.preprocess_var.get())
        self.settings.set('process', 'auto_pick', self.auto_pick_var.get())
        
        # Path settings
        self.settings.set('paths', 'data_dir', self.data_dir_var.get())
        self.settings.set('paths', 'output_dir', self.output_dir_var.get())
        
        # Filter settings
        self.settings.set('filter', 'type', self.filter_type_var.get())
        freq_range = [float(x) for x in self.freq_range_var.get().split('-')]
        self.settings.set('filter', 'freq_range', freq_range)
        
        # Save to file
        self.settings.save()
    
    def on_ok(self):
        """OK button event"""
        self.save_settings()
        self.destroy()
    
    def on_cancel(self):
        """Cancel button event"""
        self.destroy()
    
    def on_apply(self):
        """Apply button event"""
        self.save_settings()
    
    def on_reset(self):
        """Reset button event"""
        self.settings.reset_to_defaults()
        self.load_settings()
    
    def browse_directory(self, var):
        """Browse directory"""
        directory = filedialog.askdirectory()
        if directory:
            var.set(directory)
    
    def center_window(self):
        """Center window"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}') 