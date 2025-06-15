"""
Constants Definition
"""

# Application Information
APP_NAME = "P-wave Phase Picking System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Seismic Data Processing Team"

# File Related
SUPPORTED_EXTENSIONS = {
    '.mseed': 'MiniSEED Format',
    '.seed': 'SEED Format',
    '.sac': 'SAC Format'
}
MAX_FILES_PER_BATCH = 1000
PROGRESS_FILE = 'progress.json'

# Processing Modes
PROCESSING_MODES = {
    'manual': 'Manual Picking',
    'auto': 'Automatic Picking',
    'batch': 'Batch Processing'
}

# CSV Column Definitions
CSV_COLUMNS = {
    'filename': 'File Name',
    'network': 'Network',
    'station': 'Station',
    'location': 'Location',
    'channel': 'Channel',
    'pick_time': 'Pick Time',
    'pick_quality': 'Pick Quality',
    'snr': 'SNR',
    'offset': 'Offset'
}

# File Types
FILE_TYPES = [
    ("MiniSEED Files", "*.mseed"),
    ("All Files", "*.*")
]

# Pick Quality
PICK_QUALITY = {
    'A': 'Excellent',
    'B': 'Good',
    'C': 'Fair'
}

DEFAULT_PICK_QUALITY = 'A' # Define the default pick quality

# Color Definitions
COLORS = {
    'waveform': '#1f77b4',  # Waveform color
    'A': '#2ecc71',         # A-quality pick color
    'B': '#f1c40f',         # B-quality pick color
    'C': '#e74c3c',         # C-quality pick color
    'pick_line': '#ff0000',     # Pick line color
    'selected_pick': '#8e44ad', # A new color for selected picks (purple)
    'grid': '#cccccc',          # Grid color
    'background': '#ffffff',    # Background color
    'text': '#000000'          # Text color
}

# Default Parameters
DEFAULT_PARAMS = {
    'ui': {
        'window_size': [1200, 800],
        'theme': 'default',
        'font_size': 10,
        'show_grid': True
    },
    'plot': {
        'line_width': 1.0,
        'grid_alpha': 0.3,
        'pick_line_width': 2.0,
        'background_color': '#ffffff',
        'auto_scale': True
    },
    'process': {
        'sampling_rate': 100.0,
        'preprocess': True,
        'auto_pick': False
    },
    'paths': {
        'data_dir': '',
        'output_dir': ''
    },
    'filter': {
        'type': 'bandpass',
        'freq_range': [1.0, 10.0]
    }
}

# Error Messages
ERROR_MESSAGES = {
    'file_not_found': 'File not found',
    'invalid_format': 'Unsupported file format',
    'read_error': 'File read error',
    'write_error': 'File write error',
    'invalid_pick': 'Invalid pick location',
    'processing_error': 'Processing error'
}

# Status Messages
STATUS_MESSAGES = {
    'ready': 'Ready',
    'processing': 'Processing',
    'completed': 'Completed',
    'error': 'Error'
}

# Keyboard Shortcuts
KEYBOARD_SHORTCUTS = {
    'open_file': 'Ctrl+O',
    'save': 'Ctrl+S',
    'export': 'Ctrl+E',
    'undo': 'Ctrl+Z',
    'redo': 'Ctrl+Y',
    'delete': 'Delete',
    'help': 'F1',
    'quit': 'Ctrl+Q'
}

# Command Types
COMMAND_TYPES = {
    'add_pick': 'Add Pick',
    'remove_pick': 'Remove Pick',
    'update_pick': 'Update Pick',
    'batch_process': 'Batch Process'
} 