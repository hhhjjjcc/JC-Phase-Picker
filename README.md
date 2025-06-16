# P-wave First Arrival Phase Picking System: JC-Phase-Picker

## Project Overview
JC-Phase-Picker is a seismic data processing tool primarily designed to pick P-wave first arrival phases from MiniSEED format seismic waveform data.

## Key Features
- Supports reading and processing MiniSEED file format
- Interactive Waveform Display and P-wave first arrival picking
- Saving and exporting picking results
- Undo/Redo operations
- Automatic Picking algorithm

## System Requirements
- Python 3.7+
- Operating System: Windows/Linux/macOS

## Installation Guide
1. Clone the project:
```bash
git clone https://github.com/hhhjjjcc/JC-Phase-Picker.git
cd path/p-wave-picker
```

2. Create and activate environment:
```bash
conda create -n p_wave_picker python=3.8
conda activate p_wave_picker

# Install main dependencies
conda install -c conda-forge obspy matplotlib numpy pandas scipy tk

# Install other potentially needed dependencies
conda install -c conda-forge setuptools
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage Instructions
1. Start the program:
```bash
python main.py
```

2. Basic Operations:
- Open File: Click "File" → "Open File"
- Pick P-wave: Left-click on the P-wave first arrival location on the waveform plot
- Save Results: Click "File" → "Save"

## Project Structure
```
p_wave_picker/
├── main.py                 # Main program entry point
├── requirements.txt        # List of dependencies
├── config/                # Configuration files
├── core/                  # Core functionality modules
├── gui/                   # Graphical user interface modules
├── utils/                 # Utility functions
├── tests/                 # Test files
└── examples/              # Example files
```

## Developer
- Jiachen Hu, Zhejiang University

## License
MIT License

## Quick Start Tutorial

### 1. Environment Setup

1. Create and activate conda environment:
```bash
conda create -n p_wave_picker python=3.8
conda activate p_wave_picker
```

2. Install dependencies:
```bash
conda install -c conda-forge obspy matplotlib numpy pandas scipy tk
```

3. Run the program:
```bash
python main.py
```

### 2. Basic Operation Flow

#### 2.1 Loading Data

1. **Single File Loading**:
   - Click the "Open" button on the toolbar
   - Or select "File" -> "Open File" from the menu bar
   - Select a MiniSEED format seismic waveform file

2. **Batch Loading**:
   - Click the "Add Directory" button
   - Or select "File" -> "Open Directory" from the menu bar
   - Select a folder containing multiple MiniSEED files

#### 2.1.1 Preprocessing Workflow

When MiniSEED files are loaded, waveform data will undergo the following preprocessing steps based on the settings in `config/settings.py`:

1.  **Detrending**: Remove the mean value of the waveform data (`demean`) to eliminate DC offset or baseline drift.
2.  **Resampling**: Waveform data will be resampled to the target sampling rate specified in `sampling_rate` in the settings.
3.  **Filtering**: Waveform data will be filtered according to the `filter_type` (supports `bandpass`, `highpass`, `lowpass`) and `freq_range` defined in the settings.

#### 2.2 Waveform Display and Operations

1. **Basic View**:
   - Waveform is displayed in the right panel of the main window, i.e., Waveform Display
   - The left panel displays the loaded "File List"

2. **Waveform Operations**:
   - Zoom: Use the mouse scroll wheel or the "Zoom In"/"Zoom Out" buttons on the toolbar
   - Reset View: Click the "Reset View" button on the toolbar

#### 2.3 Picking Operations

1. **Manual Picking**:
   - Click on the waveform at the desired picking location
   - Use the "Quality" dropdown menu to select picking quality (A/B/C)
   - Or use hotkeys:
     - `A`: Set to A-quality
     - `B`: Set to B-quality
     - `C`: Set to C-quality

2. **Editing Picks**:
   - Undo: Click "Undo" button or use `Ctrl+Z`
   - Redo: Click "Redo" button or use `Ctrl+Y`
   - Delete: Press `Delete` key after selecting a pick

#### 2.4 Saving Results

1. **Save Picks**:
   - Click the "Save" button on the toolbar
   - Select the save location and filename

2. **Export CSV**:
   - Select "File" -> "Export CSV" from the menu bar
   - Select the export location and filename
   - The CSV file will contain information for all picks

### 3. Important Notes

1. **File Format**:
   - Supports MiniSEED format seismic waveform files
   - Ensure the file contains correct header information

2. **Picking Quality**:
   - A-quality: High quality pick, clear waveform
   - B-quality: Medium quality, waveform identifiable
   - C-quality: Low quality, for reference only

3. **Data Backup**:
   - Regularly save picking results
   - Export CSV files for backup
   - Record processing logs

### 4. Getting Help

- Check "Help" menu for "Shortcuts" and "About"
- Check log file: `~/.p_wave_picker/logs/app.log`
- Refer to full documentation: `docs/user_manual.md`

### Note:

- Features listed in README.md have been developed, but some functionalities in the user manual are still under development. The author is working hard to complete them 💪
- Demo data is available in the `example_data` folder
- 
<div style="text-align: center;">
  <img src="https://github.com/hhhjjjcc/JC-Phase-Picker/blob/main/example.png" width="70%">
  <p><b>Figure: Example GUI Interface</p>
</div>
