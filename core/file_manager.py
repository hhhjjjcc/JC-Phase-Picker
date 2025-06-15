"""
File Management
"""

import os
import logging
from obspy import read
from config.settings import Settings

class FileManager:
    """File Management Class"""
    
    def __init__(self):
        """Initialize File Manager"""
        self.settings = Settings()
        self.files = []
        self.current_file = None
        self.current_trace = None
    
    def load_file(self, file_path):
        """Load file"""
        try:
            # Read file
            st = read(file_path)
            if len(st) > 0:
                # Save file information
                self.current_file = file_path
                self.current_trace = st[0]
                
                # Preprocess
                if self.settings.get('process', 'preprocess'):
                    self.preprocess_trace()
                
                return self.current_trace
            else:
                raise ValueError("File is empty")
                
        except Exception as e:
            logging.error(f"Failed to load file: {str(e)}")
            raise
    
    def scan_directory(self, dir_path):
        """Scan directory"""
        try:
            # Clear file list
            self.files = []
            
            # Scan directory
            for root, _, files in os.walk(dir_path):
                for file in files:
                    if file.endswith('.mseed'):
                        self.files.append(os.path.join(root, file))
            
            # Update settings
            self.settings.set('paths', 'data_dir', dir_path)
            self.settings.save()
            
            return self.files
            
        except Exception as e:
            logging.error(f"Failed to scan directory: {str(e)}")
            raise
    
    def get_files(self):
        """Get file list"""
        return self.files
    
    def get_current_file(self):
        """Get current file"""
        return self.current_file
    
    def get_current_trace(self):
        """Get current waveform"""
        return self.current_trace
    
    def has_files(self):
        """Check if there are files"""
        return len(self.files) > 0
    
    def preprocess_trace(self):
        """Preprocess waveform"""
        if self.current_trace:
            try:
                # Detrend
                self.current_trace.detrend('demean')
                
                # Resample
                sampling_rate = self.settings.get('process', 'sampling_rate')
                if sampling_rate:
                    self.current_trace.resample(sampling_rate)
                
                # Filter
                filter_type = self.settings.get('filter', 'type')
                freq_range = self.settings.get('filter', 'freq_range')
                if filter_type and freq_range:
                    if filter_type == 'bandpass':
                        self.current_trace.filter('bandpass', freqmin=freq_range[0], freqmax=freq_range[1])
                    elif filter_type == 'highpass':
                        self.current_trace.filter('highpass', freq=freq_range[0])
                    elif filter_type == 'lowpass':
                        self.current_trace.filter('lowpass', freq=freq_range[1])
                
            except Exception as e:
                logging.error(f"Failed to preprocess waveform: {str(e)}")
                raise
    
    def export_data(self, file_path):
        """Export data"""
        try:
            # Export waveform data
            if self.current_trace:
                self.current_trace.write(file_path, format='MSEED')
            
        except Exception as e:
            logging.error(f"Failed to export data: {str(e)}")
            raise 