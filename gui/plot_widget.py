"""
Plotting Widget
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from config.settings import Settings
from config.constants import COLORS
import logging
import os

class PlotWidget(ttk.Frame):
    """Plotting widget class"""
    
    def __init__(self, parent, file_manager, pick_manager):
        """Initialize the widget"""
        super().__init__(parent)
        
        # Store managers instance
        self.file_manager = file_manager
        self.pick_manager = pick_manager # Store pick manager
        
        # Initialize settings
        self.settings = Settings()
        
        # Create plot area
        self.create_widgets()
        
        # Initialize variables
        self.trace = None
        self.pick_line_artists = []
        self.zoom_level = 1.0
        self.pan_offset = 0.0
    
    def create_widgets(self):
        """Create widgets"""
        # Create figure
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.axes = self.figure.add_subplot(111)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Set grid
        self.axes.grid(True, alpha=0.3)
        
        # Set title and labels
        self.axes.set_title("Waveform Display")
        self.axes.set_xlabel("Time (s)")
        self.axes.set_ylabel("Amplitude")
    
    def plot_trace(self, trace, file_path=None, selected_pick=None):
        """Plot waveform"""
        # Save waveform data
        self.trace = trace
        
        # Clear figure
        self.axes.clear()
        
        # Plot waveform
        self.axes.plot(trace.times(), trace.data, color=COLORS['waveform'])
        
        # Add logging for trace data range in plot_trace
        logging.info(f"plot_trace: Trace data min: {trace.data.min()}, max: {trace.data.max()}, shape: {trace.data.shape}")
        
        # Clear all current pick lines
        self.clear_pick_line_artists()

        # Draw existing picks for the current file
        if file_path:
            picks_for_file = self.pick_manager.get_picks_for_file(file_path)
            for pick in picks_for_file:
                line_color = COLORS['selected_pick'] if pick == selected_pick else COLORS[pick.quality]
                self._draw_pick_line(pick, line_color)

        # Set grid
        self.axes.grid(True, alpha=0.3)
        
        # Set title and labels
        title_text = "Waveform Display"
        if file_path:
            file_name = os.path.basename(file_path)
            title_text += f": {file_name}"
        self.axes.set_title(title_text)
        self.axes.set_xlabel("Time (s)")
        self.axes.set_ylabel("Amplitude")
        
        # Autoscale X and Y axes tightly after plotting
        self.axes.autoscale_view(tight=True)
        
        # Update canvas
        self.canvas.draw()
    
    def _draw_pick_line(self, pick, color, linestyle='--', alpha=0.8):
        """Helper to draw a single pick line"""
        if self.trace is not None:
            line = self.axes.axvline(
                x=pick.time,
                color=color,
                linestyle=linestyle,
                alpha=alpha
            )
            self.pick_line_artists.append(line)
    
    def clear_pick_line_artists(self):
        """Clear all pick lines from the plot"""
        for line in self.pick_line_artists:
            line.remove()
        self.pick_line_artists = []
        self.canvas.draw()
    
    def clear_picks(self):
        """Clear all picks from the plot.
        This method is called from MainWindow to clear existing picks before replotting.
        """
        self.clear_pick_line_artists()
        
    def add_pick(self, pick, is_selected=False):
        """Add a single pick to the plot and redraw. If is_selected is True, it will be drawn as a selected pick.
        """
        line_color = COLORS['selected_pick'] if is_selected else COLORS[pick.quality]
        self._draw_pick_line(pick, line_color)
        self.canvas.draw()
    
    def zoom_in(self):
        """Zoom in"""
        if self.trace is not None:
            # Increase zoom level
            self.zoom_level *= 1.2
            
            # Update display range
            self.update_view()
    
    def zoom_out(self):
        """Zoom out"""
        if self.trace is not None:
            # Decrease zoom level
            self.zoom_level /= 1.2
            
            # Update display range
            self.update_view()
    
    def pan(self, event):
        """Pan"""
        if self.trace is not None:
            # Calculate pan distance
            dx = event.xdata - event.x
            self.pan_offset += dx
            
            # Update display range
            self.update_view()
    
    def update_view(self):
        """Update view"""
        if self.trace is not None:
            # Calculate display range
            times = self.trace.times()
            center = (times[0] + times[-1]) / 2 + self.pan_offset
            width = (times[-1] - times[0]) / self.zoom_level
            
            # Set display range for X-axis
            self.axes.set_xlim(center - width/2, center + width/2)
            
            # Recompute data limits and autoscale both X and Y axes
            self.axes.relim()
            self.axes.autoscale_view(tight=True)
            
            # Update canvas
            self.canvas.draw()
    
    def clear(self):
        """Clear figure (data and all pick lines)"""
        self.trace = None
        self.clear_pick_line_artists()
        self.axes.clear()
        self.canvas.draw()

    def reset_view(self):
        """Reset view"""
        if self.trace is not None:
            # Reset zoom and pan parameters
            self.zoom_level = 1.0
            self.pan_offset = 0.0
            
            current_file_path = self.file_manager.get_current_file()
            self.plot_trace(self.trace, current_file_path, None) # Clear any selection on reset
            self.update_view() # Apply the reset zoom/pan to the view