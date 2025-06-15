"""
Batch Processing Module
"""

import os
import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from obspy import read, UTCDateTime
from config.settings import Settings
from config.constants import MAX_FILES_PER_BATCH, PROGRESS_FILE, PROCESSING_MODES
from core.file_manager import FileManager
from core.pick_manager import PickManager
import numpy as np # Import numpy

class BatchProcessor:
    """Batch Processor"""
    
    def __init__(self, file_manager, pick_manager):
        """Initialize the batch processor"""
        self.settings = Settings()
        self.file_manager = file_manager
        self.pick_manager = pick_manager
        self.files = []
        self.current_index = 0
        self.is_processing = False
        self.is_paused = False
        self.progress_callback = None
        self.status_callback = None
        self.command_history = [] # This attribute is not used in this class, it's in MainWindow
        self.processing = False
        self.current_batch = 0
        self.total_batches = 0
        self.cancel_flag = False
    
    def scan_folder(self, folder_path):
        """Scan folder"""
        success, result = self.file_manager.scan_directory(folder_path)
        if not success:
            return False, result
        
        self.files = result[:MAX_FILES_PER_BATCH]
        self.current_index = 0
        return True, f"Found {len(self.files)} files"
    
    def start_processing(self, mode='manual'):
        """Start processing"""
        if not self.files:
            return False, "No files to process"
        
        if mode not in PROCESSING_MODES:
            return False, "Invalid processing mode"
        
        self.is_processing = True
        self.is_paused = False
        self.mode = mode
        
        # Start processing
        while self.is_processing and self.current_index < len(self.files):
            if self.is_paused:
                import time
                time.sleep(0.1)
                continue
            
            # Process current file
            success, message = self._process_file(self.files[self.current_index])
            
            # Update progress
            if self.progress_callback:
                progress = (self.current_index + 1) / len(self.files) * 100
                self.progress_callback(progress, message)
            
            # Update status
            if self.status_callback:
                self.status_callback(f"Processing: {os.path.basename(self.files[self.current_index])}")
            
            # Save progress
            self._save_progress()
            
            self.current_index += 1
        
        self.is_processing = False
        return True, "Processing complete"
    
    def pause_processing(self):
        """Pause processing"""
        self.is_paused = True
        if self.status_callback:
            self.status_callback("Processing paused")
    
    def resume_processing(self):
        """Resume processing"""
        self.is_paused = False
        if self.status_callback:
            self.status_callback("Processing resumed")
    
    def stop_processing(self):
        """Stop processing"""
        self.is_processing = False
        if self.status_callback:
            self.status_callback("Processing stopped")
    
    def skip_current_file(self):
        """Skip current file"""
        if self.current_index < len(self.files):
            self.current_index += 1
            if self.status_callback:
                self.status_callback(f"Skipped: {os.path.basename(self.files[self.current_index-1])}")
    
    def _process_file(self, filename):
        """Process a single file"""
        try:
            # Load file
            trace = self.file_manager.load_file(filename)
            if trace is None:
                return False, "Failed to load file"
            
            # Process based on mode
            if self.mode == 'auto':
                # Automatic picking
                pick_time = self._auto_pick(trace)
                if pick_time:
                    self.pick_manager.add_pick(filename, self.pick_manager.create_pick(pick_time))
                    return True, "Automatic pick successful"
                return False, "Automatic pick failed"
            
            elif self.mode == 'manual':
                # Manual picking mode, just load the file
                return True, "File loaded, waiting for manual picking"
            
            return False, "Unknown processing mode"
            
        except Exception as e:
            logging.error(f"Error processing file: {str(e)}")
            return False, f"Error processing file: {str(e)}"
    
    def _auto_pick(self, trace):
        """Automatic picking algorithm (STA/LTA method)"""
        try:
            # Calculate STA/LTA
            data = trace.data
            sampling_rate = trace.stats.sampling_rate
            
            # Set STA and LTA window lengths
            sta_window = int(0.5 * sampling_rate)  # 0.5 seconds
            lta_window = int(5.0 * sampling_rate)  # 5 seconds
            
            # Calculate STA and LTA
            sta = np.zeros_like(data)
            lta = np.zeros_like(data)
            
            # Calculate STA
            for i in range(len(data)):
                if i < sta_window:
                    sta[i] = np.mean(data[:i+1]**2)
                else:
                    sta[i] = np.mean(data[i-sta_window:i]**2)
            
            # Calculate LTA
            for i in range(len(data)):
                if i < lta_window:
                    lta[i] = np.mean(data[:i+1]**2)
                else:
                    lta[i] = np.mean(data[i-lta_window:i]**2)
            
            # Calculate STA/LTA ratio
            ratio = sta / (lta + 1e-10)  # Avoid division by zero
            
            # Set trigger threshold
            threshold = 3.0
            
            # Find trigger points
            trigger_points = np.where(ratio > threshold)[0]
            if len(trigger_points) > 0:
                # Take the first trigger point
                pick_sample = trigger_points[0]
                pick_time = trace.stats.starttime + pick_sample / sampling_rate
                return pick_time
            
            return None
            
        except Exception as e:
            logging.error(f"Automatic picking failed: {str(e)}")
            return None
    
    def _save_progress(self):
        """Save progress"""
        try:
            progress = {
                'current_index': self.current_index,
                'total_files': len(self.files),
                'mode': self.mode,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Use datetime for consistency
            }
            
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=4, ensure_ascii=False) # Pretty print and ensure_ascii for readability
                
        except Exception as e:
            logging.error(f"Failed to save progress: {str(e)}")
            pass # Suppress error to avoid crashing the batch processor
    
    def load_progress(self):
        """Load progress"""
        try:
            if os.path.exists(PROGRESS_FILE):
                with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                
                self.current_index = progress.get('current_index', 0)
                self.mode = progress.get('mode', 'manual')
                return True, "Progress loaded successfully"
            
            return False, "No progress file found"
            
        except Exception as e:
            logging.error(f"Failed to load progress: {str(e)}")
            return False, f"Failed to load progress: {str(e)}"
    
    def set_callbacks(self, progress_callback=None, status_callback=None):
        """Set callbacks"""
        self.progress_callback = progress_callback
        self.status_callback = status_callback
    
    def process_batch(self, files, mode='manual', callback=None):
        """Process a batch of files"""
        if self.processing:
            return False, "Another processing task is already running"
        
        self.processing = True
        self.cancel_flag = False
        self.progress_callback = callback
        
        # Calculate total batches
        self.total_batches = (len(files) + MAX_FILES_PER_BATCH - 1) // MAX_FILES_PER_BATCH
        
        # Create progress file
        self._create_progress_file()
        
        # Start processing thread
        thread = threading.Thread(
            target=self._process_files,
            args=(files, mode)
        )
        thread.start()
        
        return True, "Batch processing started"
    
    def cancel_processing(self):
        """Cancel processing"""
        self.cancel_flag = True
        if self.status_callback:
            self.status_callback("Processing cancelled")

    def _process_files(self, files, mode):
        """Process files in a separate thread"""
        for i, file_path in enumerate(files):
            if self.cancel_flag:
                break

            # Update status
            if self.status_callback:
                self.status_callback(f"Processing file: {os.path.basename(file_path)}")

            # Process single file
            success, message = self._process_single_file(file_path, mode)
            if not success:
                logging.error(f"Failed to process {os.path.basename(file_path)}: {message}")
                # Continue to next file on error, but log it

            # Update progress
            if self.progress_callback:
                progress = (i + 1) / len(files) * 100
                self.progress_callback(progress, f"Processed {os.path.basename(file_path)}")

        self.processing = False
        if self.status_callback:
            self.status_callback("Batch processing finished.")

    def _process_single_file(self, file_path, mode):
        """Process a single file (for batch processing)"""
        try:
            trace = self.file_manager.load_file(file_path)
            if trace is None:
                return False, "Failed to load file"

            if mode == 'auto':
                pick_time = self._auto_pick(trace)
                if pick_time:
                    self.pick_manager.add_pick(file_path, self.pick_manager.create_pick(pick_time))
                    return True, "Automatic pick successful"
                return False, "Automatic pick failed"
            elif mode == 'manual':
                # For manual mode in batch, just load and make sure it's in file list
                return True, "File loaded for manual picking"
            
            return False, "Unknown processing mode"

        except Exception as e:
            logging.error(f"Error processing file {os.path.basename(file_path)}: {str(e)}")
            return False, str(e)

    def _create_progress_file(self):
        """Create a progress file to track batch processing state"""
        progress = {
            'current_batch': 0,
            'total_batches': self.total_batches,
            'files_processed_in_current_batch': 0,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        try:
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Failed to create progress file: {str(e)}")

    def _update_progress_file(self, file, success):
        """Update the progress file after processing a single file"""
        try:
            if os.path.exists(PROGRESS_FILE):
                with open(PROGRESS_FILE, 'r+', encoding='utf-8') as f:
                    progress = json.load(f)
                    progress['files_processed_in_current_batch'] += 1
                    # if progress['files_processed_in_current_batch'] >= MAX_FILES_PER_BATCH:
                    #     progress['current_batch'] += 1
                    #     progress['files_processed_in_current_batch'] = 0
                    progress['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    f.seek(0)
                    json.dump(progress, f, indent=4, ensure_ascii=False)
                    f.truncate()
        except Exception as e:
            logging.error(f"Failed to update progress file: {str(e)}")

    def _update_progress(self, current, total, status):
        """Update progress for the GUI (dummy function, actual update is in MainWindow)"""
        # This function is usually set by MainWindow to its own update_progress method.
        # No direct GUI update here.
        pass 