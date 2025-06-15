# P-wave Phase Picking System API Documentation

## 1. Core Modules (core)

### 1.1 File Manager (FileManager)

```python
class FileManager:
    def __init__(self):
        """Initializes the file manager"""
    
    def load_file(self, file_path: str) -> Stream:
        """
        Loads a MiniSEED file.
        
        Args:
            file_path: The path to the file.
            
        Returns:
            The waveform data stream.
        """
    
    def save_picks(self, st: Stream, picks: List[Dict[str, Any]]) -> bool:
        """
        Saves pick results to the file header.
        
        Args:
            st: The waveform data stream.
            picks: A list of pick results.
            
        Returns:
            True if saving was successful, False otherwise.
        """
    
    def check_format(self, file_path: str) -> bool:
        """
        Checks the file format.
        
        Args:
            file_path: The path to the file.
            
        Returns:
            True if the format is supported, False otherwise.
        """
    
    def scan_directory(self, directory: str) -> List[str]:
        """
        Scans a directory for supported files.
        
        Args:
            directory: The path to the directory.
            
        Returns:
            A list of file paths.
        """
```

### 1.2 Pick Manager (PickManager)

```python
class PickManager:
    def __init__(self):
        """Initializes the pick manager"""
    
    def add_pick(self, time: float, quality: int = 0) -> bool:
        """
        Adds a pick point.
        
        Args:
            time: The pick time.
            quality: The quality level.
            
        Returns:
            True if adding was successful, False otherwise.
        """
    
    def remove_pick(self, time: float) -> bool:
        """
        Removes a pick point.
        
        Args:
            time: The pick time.
            
        Returns:
            True if removal was successful, False otherwise.
        """
    
    def update_quality(self, time: float, quality: int) -> bool:
        """
        Updates the pick quality.
        
        Args:
            time: The pick time.
            quality: The quality level.
            
        Returns:
            True if updating was successful, False otherwise.
        """
    
    def get_picks(self) -> List[Dict[str, Any]]:
        """
        Gets all pick points.
        
        Returns:
            A list of pick points.
        """
```

### 1.3 Command History Manager (CommandHistory)

```python
class CommandHistory:
    def __init__(self):
        """Initializes the command history manager"""
    
    def execute(self, command: Command) -> bool:
        """
        Executes a command.
        
        Args:
            command: The command object.
            
        Returns:
            True if execution was successful, False otherwise.
        """
    
    def undo(self) -> bool:
        """
        Undoes the last operation.
        
        Returns:
            True if undo was successful, False otherwise.
        """
    
    def redo(self) -> bool:
        """
        Redoes the last operation.
        
        Returns:
            True if redo was successful, False otherwise.
        """
    
    def can_undo(self) -> bool:
        """
        Checks if undo is possible.
        
        Returns:
            True if undo is possible, False otherwise.
        """
    
    def can_redo(self) -> bool:
        """
        Checks if redo is possible.
        
        Returns:
            True if redo is possible, False otherwise.
        """
```

### 1.4 Batch Processor (BatchProcessor)

```python
class BatchProcessor:
    def __init__(self):
        """Initializes the batch processor"""
    
    def start(self, input_dir: str, output_dir: str) -> None:
        """
        Starts batch processing.
        
        Args:
            input_dir: The input directory.
            output_dir: The output directory.
        """
    
    def pause(self) -> None:
        """Pauses processing"""
    
    def resume(self) -> None:
        """Resumes processing"""
    
    def stop(self) -> None:
        """Stops processing"""
    
    def skip_file(self) -> None:
        """Skips the current file"""
    
    def get_progress(self) -> Dict[str, Any]:
        """
        Gets processing progress.
        
        Returns:
            A dictionary containing progress information.
        """
```

### 1.5 Waveform Processor (WaveformProcessor)

```python
class WaveformProcessor:
    def __init__(self):
        """Initializes the waveform processor"""
    
    def preprocess(self, st: Stream) -> Stream:
        """
        Preprocesses waveform data.
        
        Args:
            st: The input waveform data stream.
            
        Returns:
            The processed waveform data stream.
        """
    
    def apply_filter(self, st: Stream, filter_type: str = 'bandpass', **kwargs) -> Stream:
        """
        Applies a filter to the waveform data.
        
        Args:
            st: The input waveform data stream.
            filter_type: The type of filter.
            **kwargs: Filter parameters.
            
        Returns:
            The filtered waveform data stream.
        """
    
    def calculate_snr(self, tr: Trace, window_length: Optional[int] = None) -> float:
        """
        Calculates the signal-to-noise ratio.
        
        Args:
            tr: The input waveform trace.
            window_length: The window length for calculation.
            
        Returns:
            The SNR value.
        """
```

### 1.6 Auto Picker (AutoPicker)

```python
class AutoPicker:
    def __init__(self):
        """Initializes the auto picker"""
    
    def pick_sta_lta(self, tr: Trace, threshold: Optional[float] = None,
                     algorithm: str = 'classic') -> Optional[float]:
        """
        Picks P-wave arrival times using STA/LTA algorithm.
        
        Args:
            tr: The input waveform trace.
            threshold: The picking threshold.
            algorithm: The STA/LTA algorithm type (e.g., 'classic').
            
        Returns:
            The picked time if successful, None otherwise.
        """
    
    def pick_energy_ratio(self, tr: Trace, window_length: int = 100) -> Optional[float]:
        """
        使用能量比算法拾取P波初至
        
        Args:
            tr: 输入波形数据
            window_length: 计算窗口长度
            
        Returns:
            拾取时间
        """
    
    def evaluate_signal_quality(self, tr: Trace) -> Tuple[int, float]:
        """
        评估信号质量
        
        Args:
            tr: 输入波形数据
            
        Returns:
            (质量等级, 信噪比)
        """
```

### 1.7 Data Exporter (DataExporter)

```python
class DataExporter:
    def __init__(self):
        """Initializes the data exporter"""
    
    def export_picks_to_csv(self, picks: List[Dict[str, Any]], file_path: str) -> bool:
        """
        Exports pick data to a CSV file.
        
        Args:
            picks: A list of pick data.
            file_path: The path to the output CSV file.
            
        Returns:
            True if export was successful, False otherwise.
        """
    
    def export_waveform_to_sac(self, st: Stream, file_path: str) -> bool:
        """
        Exports waveform data to SAC format.
        
        Args:
            st: The waveform data stream.
            file_path: The path to the output SAC file.
            
        Returns:
            True if export was successful, False otherwise.
        """
```

## 2. GUI Modules (gui)

### 2.1 Main Window (MainWindow)

```python
class MainWindow:
    def __init__(self):
        """Initializes the main window"""
    
    def show(self) -> None:
        """
        Displays the main window and starts the event loop.
        """
    
    def update_status(self, message: str) -> None:
        """
        Updates the status bar message.
        
        Args:
            message: The status message.
        """
    
    def show_error_message(self, title: str, message: str) -> None:
        """
        Displays an error message box.
        
        Args:
            title: The title of the error box.
            message: The error message.
        """
```

### 2.2 Plot Widget (PlotWidget)

```python
class PlotWidget:
    def __init__(self, parent: Any):
        """Initializes the plot widget"""
    
    def plot_trace(self, trace: Trace) -> None:
        """
        Plots a seismic trace.
        
        Args:
            trace: The seismic trace to plot.
        """
    
    def add_pick(self, pick_time: float, quality: str) -> None:
        """
        Adds a pick line to the plot.
        
        Args:
            pick_time: The time of the pick.
            quality: The quality of the pick (e.g., 'A', 'B', 'C').
        """
    
    def remove_pick(self, pick_time: float) -> None:
        """
        Removes a pick line from the plot.
        
        Args:
            pick_time: The time of the pick to remove.
        """
    
    def clear_plot(self) -> None:
        """
        Clears all content from the plot.
        """
```

### 2.3 Settings Dialog (SettingsDialog)

```python
class SettingsDialog:
    def __init__(self, parent: Any):
        """Initializes the settings dialog"""
    
    def show(self) -> None:
        """
        Displays the settings dialog.
        """
    
    def apply_settings(self) -> None:
        """
        Applies the settings from the dialog.
        """
    
    def reset_settings(self) -> None:
        """
        Resets settings to default values.
        """
```

### 2.4 Progress Dialog (ProgressDialog)

```python
class ProgressDialog:
    def __init__(self, parent: Any, title: str, message: str, allow_cancel: bool = True):
        """
        Initializes the progress dialog.
        
        Args:
            parent: The parent Tkinter window.
            title: The title of the dialog.
            message: The initial message displayed.
            allow_cancel: Whether to show a cancel button.
        """
    
    def update_progress(self, value: int) -> None:
        """
        Updates the progress bar value.
        
        Args:
            value: The progress value (0-100).
        """
    
    def update_message(self, message: str) -> None:
        """
        Updates the message displayed in the dialog.
        
        Args:
            message: The new message.
        """
    
    def close(self) -> None:
        """
        Closes the progress dialog.
        """
    
    def is_cancelled(self) -> bool:
        """
        Checks if the dialog was cancelled by the user.
        
        Returns:
            True if cancelled, False otherwise.
        """
```

## 3. Utility Modules (utils)

### 3.1 mseed_utils

```python
def validate_mseed_file(file_path: str) -> bool:
    """
    Validates if a file is a valid MiniSEED file.
    
    Args:
        file_path: The path to the file.
        
    Returns:
        True if valid, False otherwise.
    """

def get_mseed_info(file_path: str) -> Dict[str, Any]:
    """
    Gets information from a MiniSEED file (e.g., station, channel, start time).
    
    Args:
        file_path: The path to the file.
        
    Returns:
        A dictionary containing file information.
    """

def extract_picks_from_header(trace: Trace) -> List[Dict[str, Any]]:
    """
    Extracts pick information from trace headers.
    
    Args:
        trace: The seismic trace.
        
    Returns:
        A list of pick information.
    """
```

### 3.2 time_utils

```python
def format_utc_time(utcdatetime: UTCDateTime, format_str: str = "%Y-%m-%d %H:%M:%S.%f") -> str:
    """
    Formats an ObsPy UTCDateTime object into a string.
    
    Args:
        utcdatetime: The UTCDateTime object.
        format_str: The desired string format.
        
    Returns:
        The formatted time string.
    """

def parse_time_string(time_str: str) -> UTCDateTime:
    """
    Parses a time string into an ObsPy UTCDateTime object.
    
    Args:
        time_str: The time string.
        
    Returns:
        The UTCDateTime object.
    """

def time_offset_to_sample(time_offset: float, sampling_rate: float) -> int:
    """
    Converts a time offset (in seconds) to a sample number.
    
    Args:
        time_offset: The time offset in seconds.
        sampling_rate: The sampling rate of the data.
        
    Returns:
        The corresponding sample number.
    """
```

## 4. Configuration Modules (config)

### 4.1 Settings (Settings)

```python
class Settings:
    def __init__(self):
        """Initializes the settings manager"""
    
    def load_settings(self) -> Dict[str, Any]:
        """
        Loads application settings from a JSON file.
        
        Returns:
            A dictionary of settings.
        """
    
    def save_settings(self, settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        Saves application settings to a JSON file.
        
        Args:
            settings: The settings dictionary to save. If None, saves current settings.
            
        Returns:
            True if saving was successful, False otherwise.
        """
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Gets a setting value from a specific section and key.
        
        Args:
            section: The section name.
            key: The key name.
            default: The default value if the key is not found.
            
        Returns:
            The setting value.
        """
    
    def set(self, section: str, key: str, value: Any) -> bool:
        """
        Sets a setting value.
        
        Args:
            section: The section name.
            key: The key name.
            value: The value to set.
            
        Returns:
            True if setting and saving were successful, False otherwise.
        """
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Gets an entire section of settings.
        
        Args:
            section: The section name.
            
        Returns:
            A dictionary representing the section.
        """
    
    def reset_to_defaults(self) -> bool:
        """
        Resets all settings to their default values.
        
        Returns:
            True if reset and saving were successful, False otherwise.
        """
    
    def update(self, new_settings: Dict[str, Any]) -> bool:
        """
        Updates existing settings with new values.
        
        Args:
            new_settings: A dictionary of new settings to apply.
            
        Returns:
            True if update and saving were successful, False otherwise.
        """
```

### 4.2 Constants (Constants)

```python
# Application Information
APP_NAME: str
APP_VERSION: str
APP_AUTHOR: str

# File Related
SUPPORTED_EXTENSIONS: Dict[str, str]
MAX_FILES_PER_BATCH: int
PROGRESS_FILE: str

# Processing Modes
PROCESSING_MODES: Dict[str, str]

# CSV Column Definitions
CSV_COLUMNS: Dict[str, str]

# File Types
FILE_TYPES: List[Tuple[str, str]]

# Pick Quality
PICK_QUALITY: Dict[str, str]

# Color Definitions
COLORS: Dict[str, str]

# Default Parameters
DEFAULT_PARAMS: Dict[str, Any]

# Error Messages
ERROR_MESSAGES: Dict[str, str]

# Status Messages
STATUS_MESSAGES: Dict[str, str]

# Keyboard Shortcuts
KEYBOARD_SHORTCUTS: Dict[str, str]

# Command Types
COMMAND_TYPES: Dict[str, str]
``` 