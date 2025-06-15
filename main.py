"""
Main Program
"""

import os
import sys
import logging
from datetime import datetime
from gui.main_window import MainWindow
from config.settings import Settings

def setup_logging():
    """Setup logging"""
    # Create log directory
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Set log filename
    log_file = os.path.join(
        log_dir,
        f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies():
    """Check dependencies"""
    try:
        import obspy
        import numpy
        import matplotlib
        import tkinter
        return True
    except ImportError as e:
        logging.error(f"Missing required dependencies: {str(e)}")
        return False

def main():
    """Main function"""
    try:
        # Setup logging
        setup_logging()
        
        # Check dependencies
        if not check_dependencies():
            return
        
        # Create main window
        app = MainWindow()
        
        # Run program
        app.run()
        
    except Exception as e:
        logging.error(f"Program error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 