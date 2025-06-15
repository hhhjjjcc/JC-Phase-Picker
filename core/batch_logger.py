"""
Batch Processing Logger Module
Provides logging functionality for the batch processing process
"""

import os
import json
import logging
import datetime
from typing import Dict, Any, Optional, List

from config.constants import (
    LOG_FORMAT,
    LOG_LEVEL,
    PROGRESS_FILE
)

class BatchLogger:
    """Batch Logger Class"""
    
    def __init__(self, log_dir: str):
        """
        Initializes the batch logger
        
        Args:
            log_dir: Log directory
        """
        self.log_dir = log_dir
        self.progress_file = os.path.join(log_dir, PROGRESS_FILE)
        
        # Create log directory
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configure logger
        self.logger = logging.getLogger('batch_processor')
        self.logger.setLevel(LOG_LEVEL)
        
        # Create file handler
        log_file = os.path.join(log_dir, f'batch_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        self.logger.addHandler(file_handler)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        self.logger.addHandler(console_handler)
    
    def log_start(self, total_files: int) -> None:
        """
        Logs the start of batch processing
        
        Args:
            total_files: Total number of files
        """
        self.logger.info(f"Starting batch processing, total files: {total_files}")
        self._save_progress({
            'status': 'running',
            'start_time': datetime.datetime.now().isoformat(),
            'total_files': total_files,
            'processed_files': 0,
            'successful_files': 0,
            'failed_files': 0,
            'current_file': None,
            'results': []
        })
    
    def log_file_start(self, filename: str) -> None:
        """
        Logs the start of file processing
        
        Args:
            filename: Filename
        """
        self.logger.info(f"Starting to process file: {filename}")
        progress = self._load_progress()
        progress['current_file'] = filename
        self._save_progress(progress)
    
    def log_file_complete(self, filename: str,
                         success: bool,
                         picks: Optional[List[Dict[str, Any]]] = None,
                         error: Optional[str] = None) -> None:
        """
        Logs the completion of file processing
        
        Args:
            filename: Filename
            success: Whether successful
            picks: Picking results
            error: Error message
        """
        if success:
            self.logger.info(f"File processed successfully: {filename}")
        else:
            self.logger.error(f"File processing failed: {filename}, Error: {error}")
        
        progress = self._load_progress()
        progress['processed_files'] += 1
        if success:
            progress['successful_files'] += 1
        else:
            progress['failed_files'] += 1
        
        # Add result
        result = {
            'file': filename,
            'success': success,
            'picks': picks if picks else [],
            'error': error,
            'processing_time': datetime.datetime.now().isoformat()
        }
        progress['results'].append(result)
        
        self._save_progress(progress)
    
    def log_complete(self) -> None:
        """
        Logs the completion of batch processing
        """
        progress = self._load_progress()
        end_time = datetime.datetime.now()
        start_time = datetime.datetime.fromisoformat(progress['start_time'])
        duration = (end_time - start_time).total_seconds()
        
        self.logger.info(f"Batch processing complete, total time: {duration:.2f} seconds")
        self.logger.info(f"Successful files: {progress['successful_files']}")
        self.logger.info(f"Failed files: {progress['failed_files']}")
        
        progress['status'] = 'completed'
        progress['end_time'] = end_time.isoformat()
        progress['duration'] = duration
        self._save_progress(progress)
    
    def log_error(self, error: str) -> None:
        """
        Logs an error
        
        Args:
            error: Error message
        """
        self.logger.error(error)
    
    def log_warning(self, warning: str) -> None:
        """
        Logs a warning
        
        Args:
            warning: Warning message
        """
        self.logger.warning(warning)
    
    def log_info(self, info: str) -> None:
        """
        Logs information
        
        Args:
            info: Information message
        """
        self.logger.info(info)
    
    def get_progress(self) -> Dict[str, Any]:
        """
        Gets processing progress
        
        Returns:
            Progress information
        """
        return self._load_progress()
    
    def _save_progress(self, progress: Dict[str, Any]) -> None:
        """
        Saves progress information
        
        Args:
            progress: Progress information
        """
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f, indent=4, ensure_ascii=False)
    
    def _load_progress(self) -> Dict[str, Any]:
        """
        Loads progress information
        
        Returns:
            Progress information
        """
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            'status': 'not_started',
            'start_time': None,
            'total_files': 0,
            'processed_files': 0,
            'successful_files': 0,
            'failed_files': 0,
            'current_file': None,
            'results': []
        } 