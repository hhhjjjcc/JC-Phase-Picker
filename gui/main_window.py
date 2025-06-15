"""
Main Window
"""

import os
import logging
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from gui.plot_widget import PlotWidget
from gui.settings_dialog import SettingsDialog
from gui.progress_dialog import ProgressDialog
from core.file_manager import FileManager
from core.pick_manager import PickManager
from core.batch_processor import BatchProcessor
from core.command_history import CommandHistory, AddPickCommand, RemovePickCommand, UpdatePickCommand
from config.settings import Settings
from config.constants import (
    FILE_TYPES,
    PICK_QUALITY,
    COLORS,
    DEFAULT_PARAMS,
    DEFAULT_PICK_QUALITY
)
import matplotlib.pyplot as plt

class MainWindow(tk.Tk):
    """Main window class"""
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        
        # Set fonts
        self.setup_fonts()
        
        # Initialize settings
        self.settings = Settings()
        
        # Initialize managers
        self.file_manager = FileManager()
        self.pick_manager = PickManager()
        self.command_history = CommandHistory()
        self.batch_processor = BatchProcessor(self.file_manager, self.pick_manager)
        
        self.selected_pick = None # Initialize selected pick
        self.is_loading_file = False  # Add flag to prevent duplicate loading
        
        # Create UI
        self.title("P-wave Phase Picking System")
        self.geometry("1200x800")
        self.create_widgets()
        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        
        # Bind events
        self.bind_events()
        
        # Center window
        self.center_window()
    
    def setup_fonts(self):
        """Set fonts"""
        # Set default font to Arial
        self.default_font = "Arial"
        default_tk_font = font.nametofont("TkDefaultFont")
        default_tk_font.configure(family=self.default_font, size=12)
        logging.info(f"Font set to: {self.default_font}")
        
        # Set matplotlib font
        try:
            import matplotlib.font_manager as fm
            fm.findfont(self.default_font)
            plt.rcParams['font.family'] = self.default_font
            plt.rcParams['axes.unicode_minus'] = False  # Resolve minus sign display issue
        except Exception as e:
            logging.warning(f"Failed to set matplotlib font: {str(e)}")
    
    def create_widgets(self):
        """Create widgets"""
        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create left panel
        self.left_panel = ttk.Frame(self.main_frame)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Create file list
        self.create_file_list()
        
        # Create right panel
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Create plot area
        self.plot_widget = PlotWidget(self.right_panel, self.file_manager, self.pick_manager)
        self.plot_widget.pack(fill=tk.BOTH, expand=True)
        
        # Create toolbar
        self.toolbar = NavigationToolbar2Tk(self.plot_widget.canvas, self.right_panel)
        self.toolbar.update()
    
    def create_file_list(self):
        """Create file list"""
        # Create file list frame
        self.file_list_frame = ttk.LabelFrame(self.left_panel, text="File List")
        self.file_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create file list
        self.file_list = ttk.Treeview(
            self.file_list_frame,
            columns=("File Name", "Status"),
            show="headings"
        )
        self.file_list.heading("File Name", text="File")
        self.file_list.heading("Status", text="Stat.")
        self.file_list.column("File Name", width=150)
        self.file_list.column("Status", width=50)
        self.file_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create scrollbar
        self.file_scrollbar = ttk.Scrollbar(
            self.file_list_frame,
            orient=tk.VERTICAL,
            command=self.file_list.yview
        )
        self.file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_list.configure(yscrollcommand=self.file_scrollbar.set)
        
        # Bind selection event
        self.file_list.bind("<<TreeviewSelect>>", self.on_file_select)
    
    def create_menu(self):
        """Create menu"""
        # Create menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open File", command=self.open_file)
        self.file_menu.add_command(label="Open Directory", command=self.open_directory)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save Picks", command=self.save_picks)
        self.file_menu.add_command(label="Export Data", command=self.export_data)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Delete Pick", command=self.remove_pick)
        
        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Reset View", command=self.reset_view)
        self.view_menu.add_command(label="Zoom In", command=self.zoom_in)
        self.view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        
        # Settings menu
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Parameter Settings", command=self.show_settings)
        
        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Instructions", command=self.show_help)
        self.help_menu.add_command(label="About", command=self.show_about)
    
    def create_toolbar(self):
        """Create toolbar"""
        # Create toolbar frame
        self.toolbar_frame = ttk.Frame(self)
        self.toolbar_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Create toolbar buttons
        ttk.Button(
            self.toolbar_frame,
            text="Open File",
            command=self.open_file
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            self.toolbar_frame,
            text="Save Picks",
            command=self.save_picks
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            self.toolbar_frame,
            text="Undo",
            command=self.undo
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            self.toolbar_frame,
            text="Redo",
            command=self.redo
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            self.toolbar_frame,
            text="Delete Pick",
            command=self.remove_pick
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            self.toolbar_frame,
            text="Reset View",
            command=self.reset_view
        ).pack(side=tk.LEFT, padx=2)
        
        # Add quality selection dropdown
        self.quality_var = tk.StringVar(value=DEFAULT_PICK_QUALITY)
        quality_label = ttk.Label(self.toolbar_frame, text="Quality:")
        quality_label.pack(side=tk.LEFT, padx=(10, 2), pady=2)
        self.quality_combobox = ttk.Combobox(self.toolbar_frame, textvariable=self.quality_var,
                                             values=list(PICK_QUALITY.keys()), state='readonly', width=3)
        self.quality_combobox.set(DEFAULT_PICK_QUALITY) # Set default value
        self.quality_combobox.pack(side=tk.LEFT, padx=2, pady=2)
        self.quality_combobox.bind("<<ComboboxSelected>>", self.on_quality_change) # Bind quality change event
    
    def create_statusbar(self):
        """Create status bar"""
        # Create status bar frame
        self.statusbar_frame = ttk.Frame(self)
        self.statusbar_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
        
        # Create status label
        self.status_label = ttk.Label(
            self.statusbar_frame,
            text="Ready"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Create progress bar
        self.progress_bar = ttk.Progressbar(
            self.statusbar_frame,
            mode='determinate',
            length=200
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=5)
    
    def bind_events(self):
        """Bind events"""
        # Bind keyboard events
        self.bind("<Control-z>", lambda e: self.undo())
        self.bind("<Control-y>", lambda e: self.redo())
        self.bind("<Delete>", lambda e: self.remove_pick())
        
        # Bind mouse events
        self.plot_widget.canvas.mpl_connect(
            "button_press_event",
            self.on_plot_click
        )
    
    def center_window(self):
        """Center window"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def open_file(self):
        """Open file"""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=FILE_TYPES
        )
        if file_path:
            # Add file to list and select it
            self.update_file_list_with_new_file(file_path)
            self.file_list.selection_set(file_path) # Selects the item with the full path as iid
            self.file_list.focus(file_path) # Focuses on it as well
    
    def open_directory(self):
        """Open directory"""
        dir_path = filedialog.askdirectory(title="Select Directory")
        if dir_path:
            self.update_status("Scanning directory...")
            # Run scan in a separate thread to prevent GUI freeze
            self.after(100, lambda: self._run_scan_directory_thread(dir_path)) # Short delay for status message to appear

    def _run_scan_directory_thread(self, dir_path):
        # This function runs the actual scanning in a thread
        import threading
        thread = threading.Thread(target=self._scan_directory_task, args=(dir_path,))
        thread.start()

    def _scan_directory_task(self, dir_path):
        try:
            self.file_manager.scan_directory(dir_path)
            self.update_file_list()
            self.update_status(f"Scanned {len(self.file_manager.get_files())} files.")
            if self.file_manager.has_files():
                # Automatically load the first file after scanning a directory
                first_file = self.file_manager.get_files()[0]
                self.file_list.selection_set(first_file) # Selects the item with the full path as iid
                self.file_list.focus(first_file) # Focuses on it as well
        except Exception as e:
            self.update_status(f"Error scanning directory: {str(e)}")
            messagebox.showerror("Error", f"Failed to scan directory: {str(e)}")

    def save_picks(self):
        """Save picks"""
        if not self.file_manager.get_current_file():
            messagebox.showwarning("Warning", "No file loaded to save picks for.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Picks",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")]
        )
        if file_path:
            try:
                current_file_path = self.file_manager.get_current_file()
                self.pick_manager.save_picks(current_file_path, file_path)
                self.update_status(f"Picks saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save picks: {str(e)}")
    
    def export_data(self):
        """Export data"""
        if not self.file_manager.get_current_trace():
            messagebox.showwarning("Warning", "No waveform loaded to export data from.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Waveform Data",
            defaultextension=".mseed",
            filetypes=FILE_TYPES
        )
        if file_path:
            try:
                self.file_manager.export_data(file_path)
                self.update_status(f"Waveform data exported to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def undo(self):
        """Undo operation"""
        success, message = self.command_history.undo()
        if success:
            self.update_plot()
            self.update_status(message)
            # Update quality dropdown if the undo operation affected the selected pick
            if self.selected_pick and not self.pick_manager.get_pick(self.selected_pick.time, self.selected_pick.quality, self.file_manager.get_current_file()):
                self.selected_pick = None # The pick was removed by undo, deselect it
                self.quality_var.set(DEFAULT_PICK_QUALITY)
            elif self.selected_pick:
                # If the pick itself was updated, ensure dropdown reflects new quality
                pick_after_undo = self.pick_manager.find_nearest_pick(self.file_manager.get_current_file(), self.selected_pick.time, threshold=0.01)
                if pick_after_undo: # Ensure pick still exists
                    self.quality_var.set(pick_after_undo.quality)
        else:
            self.update_status(message)
    
    def redo(self):
        """Redo operation"""
        success, message = self.command_history.redo()
        if success:
            self.update_plot()
            self.update_status(message)
            # Update quality dropdown if the redo operation affected the selected pick
            if self.selected_pick and not self.pick_manager.get_pick(self.selected_pick.time, self.selected_pick.quality, self.file_manager.get_current_file()):
                # If a new pick was redone, select it (assuming it's the last one added)
                current_file_path = self.file_manager.get_current_file()
                picks_for_file = self.pick_manager.get_picks_for_file(current_file_path)
                if picks_for_file:
                    self.selected_pick = picks_for_file[-1] # Select the last pick (usually the one redone)
                    self.quality_var.set(self.selected_pick.quality)
                else:
                    self.selected_pick = None
                    self.quality_var.set(DEFAULT_PICK_QUALITY)
            elif self.selected_pick:
                # If the pick itself was updated, ensure dropdown reflects new quality
                pick_after_redo = self.pick_manager.find_nearest_pick(self.file_manager.get_current_file(), self.selected_pick.time, threshold=0.01)
                if pick_after_redo: # Ensure pick still exists
                    self.quality_var.set(pick_after_redo.quality)
        else:
            self.update_status(message)
    
    def remove_pick(self):
        """Remove selected pick"""
        if self.selected_pick:
            current_file_path = self.file_manager.get_current_file()
            # Create remove command
            command = RemovePickCommand(self.pick_manager, current_file_path, self.selected_pick)
            # Execute command
            success, message = self.command_history.execute_command(command)
            if success:
                self.selected_pick = None # Deselect the pick after removal
                self.update_plot()
                self.update_status(message)
                self.quality_var.set(DEFAULT_PICK_QUALITY) # Reset quality dropdown to default
                self.update_file_status(current_file_path, "Processed") # Update status to Processed
            else:
                messagebox.showerror("Error", message)
        else:
            self.update_status("No pick selected to remove.")
    
    def reset_view(self):
        """Reset view"""
        self.plot_widget.reset_view()
    
    def zoom_in(self):
        """Zoom in"""
        self.plot_widget.zoom_in()
    
    def zoom_out(self):
        """Zoom out"""
        self.plot_widget.zoom_out()
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self)
        self.wait_window(dialog)
    
    def show_help(self):
        """Show help"""
        messagebox.showinfo(
            "Instructions",
            "1. Use left mouse button to click waveform to add pick\n"
            "2. Use Delete key to delete the last pick\n"
            "3. Use Ctrl+Z to undo operation\n"
            "4. Use Ctrl+Y to redo operation"
        )
    
    def show_about(self):
        """Show about"""
        messagebox.showinfo(
            "About",
            "P-wave Phase Picking System\n"
            "Version: 1.0.0\n"
            "Author: Jiachen Hu, ZJU"
        )
    
    def on_file_select(self, event):
        """File selection event handler"""
        if self.is_loading_file:  # Skip if already loading a file
            return
            
        selection = self.file_list.selection()
        if selection:
            # Get selected file's full path from iid
            file_path_to_load = selection[0]
            print(f"DEBUG: Attempting to load file: {file_path_to_load}")
            try:
                self.is_loading_file = True  # Set loading flag
                # Load file
                self.file_manager.load_file(file_path_to_load)
                # Show trace
                self.show_trace()
                # Update status
                self.update_status("File loaded successfully")

                # Update pick quality selector based on current file's picks
                picks_for_file = self.pick_manager.get_picks_for_file(file_path_to_load)
                if picks_for_file:
                    # Set quality to the last pick's quality
                    self.quality_var.set(picks_for_file[-1].quality)
                else:
                    # No picks for this file, reset to default
                    self.quality_var.set(DEFAULT_PICK_QUALITY)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            finally:
                self.is_loading_file = False  # Reset loading flag
    
    def on_plot_click(self, event):
        """Plot area click event handler"""
        # Ignore click if zoom or pan is active
        if self.toolbar.mode in ['zoom rect', 'pan/zoom']:
            return
        if event.inaxes:
            # Get clicked time and current file path
            time = event.xdata
            current_file_path = self.file_manager.get_current_file()

            if not current_file_path:
                messagebox.showwarning("Warning", "Please load a file first!")
                return

            # Try to find an existing pick near the click
            # Define a threshold for proximity (e.g., 0.5 seconds)
            # This threshold might need adjustment based on typical data sampling rates
            threshold_seconds = 0.5
            nearest_pick = self.pick_manager.find_nearest_pick(current_file_path, time, threshold=threshold_seconds)

            if nearest_pick:
                # Select the existing pick
                self.selected_pick = nearest_pick
                self.quality_var.set(self.selected_pick.quality)
                self.update_status(f"Pick selected with quality: {self.selected_pick.quality}")
                self.update_plot() # Redraw to highlight selected pick
            else:
                # If a pick was previously selected, deselect it when clicking elsewhere
                if self.selected_pick:
                    self.selected_pick = None # Deselect the pick
                    self.update_plot() # Redraw to remove highlight

                # Create new pick
                current_quality = self.quality_var.get()
                print(f"DEBUG: Creating pick with quality: {current_quality}")
                pick = self.pick_manager.create_pick(time, quality=current_quality)
                # Create add command
                command = AddPickCommand(self.pick_manager, current_file_path, pick)
                # Execute command
                success, message = self.command_history.execute_command(command)
                if success:
                    self.update_plot()
                    self.update_status(message)
                    self.update_file_status(current_file_path, "Processed") # Update status to Processed
                    # After adding a new pick, automatically select it
                    self.selected_pick = pick
                    self.quality_var.set(pick.quality) # Update dropdown to match new pick's quality
                    # Verify the pick was created with the correct quality
                    picks = self.pick_manager.get_picks_for_file(current_file_path)
                    if picks:
                        print(f"DEBUG: Last pick quality: {picks[-1].quality}")
                else:
                    messagebox.showerror("Error", message)
    
    def show_trace(self):
        """Show trace"""
        trace = self.file_manager.get_current_trace()
        current_file_path = self.file_manager.get_current_file()
        if trace:
            self.plot_widget.clear_picks() # Clear old picks
            # Pass the selected pick for highlighting
            self.plot_widget.plot_trace(trace, current_file_path, self.selected_pick)
            # Show existing picks for the current file
            # for pick in self.pick_manager.get_picks_for_file(current_file_path):
            #     # We need to ensure add_pick can handle highlighting
            #     # For now, just add all, plot_trace will handle the highlight
            #     if pick != self.selected_pick: # Avoid drawing selected pick twice if it's already passed as selected_pick
            #         self.plot_widget.add_pick(pick)
    
    def update_plot(self):
        """Update plot"""
        # No need to clear picks here, show_trace will handle it
        self.show_trace()
    
    def update_file_list(self):
        """Update file list"""
        # Clear list
        for item in self.file_list.get_children():
            self.file_list.delete(item)
        
        # Add files
        for file in self.file_manager.get_files():
            file_name_only = os.path.basename(file)
            self.file_list.insert(
                "",
                tk.END,
                iid=file,
                values=(file_name_only, "Unprocessed")
            )
    
    def update_status(self, message):
        """Update status"""
        self.status_label.config(text=message)
    
    def update_progress(self, current, total, status):
        """Update progress"""
        # Update progress bar
        self.progress_bar["value"] = (current / total) * 100
        # Update status
        self.update_status(status)
    
    def update_file_status(self, file_path, status):
        """Update the status of a file in the file list treeview"""
        print(f"DEBUG: update_file_status called for file_path: {file_path}, status: {status}")
        for item_id in self.file_list.get_children():
            current_item_file_path = item_id # item_id itself is the iid (full file path)
            print(f"DEBUG: Checking item_id: {item_id}, iid (file_path): {current_item_file_path}")
            if current_item_file_path == file_path:
                file_name_only = os.path.basename(file_path)
                self.file_list.item(item_id, values=(file_name_only, status))
                print(f"DEBUG: Status updated for {file_name_only} to {status}")
                break
    
    def on_quality_change(self, event):
        """Handle quality combobox selection change"""
        if self.selected_pick:
            current_file_path = self.file_manager.get_current_file()
            new_quality = self.quality_var.get()
            
            # Create update command
            # Pass old pick and new quality to the command for undo/redo context
            command = UpdatePickCommand(self.pick_manager, current_file_path, self.selected_pick, new_quality)
            
            # Execute command
            success, message = self.command_history.execute_command(command)
            if success:
                self.update_plot() # Redraw plot to reflect new quality color
                self.update_status(message)
            else:
                messagebox.showerror("Error", message)
        else:
            self.update_status("No pick selected to update quality.")
    
    def run(self):
        """Run main loop"""
        self.mainloop() 