# P波初至震相拾取系统：JC-Phase-Picker

## 项目概述
JC-Phase-Picker是一款地震数据处理工具，主要功能是从MiniSEED格式的地震波形数据中拾取P波初至震相。

## 主要功能
- 支持MiniSEED文件格式的读取和处理
- 交互式Waveform Display和P波初至拾取
- 拾取结果保存和导出
- Undo/Redo操作
- Automatic Picking算法

## 系统要求
- Python 3.7+
- 操作系统：Windows/Linux/macOS

## 安装指南
1. 克隆项目：
```bash
git clone https://github.com/hhhjjjcc/JC-Phase-Picker.git
cd path/p-wave-pickerp-wave-picker
```

2. 创建并激活环境：
```bash
conda create -n p_wave_picker python=3.8
conda activate p_wave_picker

# 安装主要依赖
conda install -c conda-forge obspy matplotlib numpy pandas scipy tk

# 安装其他可能需要的依赖
conda install -c conda-forge setuptools
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用说明
1. 启动程序：
```bash
python main.py
```

2. 基本操作：
- Open File: 点击"File" → "Open File"
- Pick P-wave: 在波形图上用鼠标左键点击P波初至位置
- Save Results: 点击"File" → "Save"

## 项目结构
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

## 开发者
- Jiachen Hu, Zhejiang University

## 许可证
MIT License

## 快速入门教程

### 1. 环境配置

1. 创建并激活conda环境：
```bash
conda create -n p_wave_picker python=3.8
conda activate p_wave_picker
```

2. 安装依赖：
```bash
conda install -c conda-forge obspy matplotlib numpy pandas scipy tk
```

3. 运行程序：
```bash
python main.py
```

### 2. 基本操作流程

#### 2.1 加载数据

1. **单个文件加载**：
   - 点击工具栏的"Open"按钮
   - 或从菜单栏选择"File" -> "Open File"
   - 选择MiniSEED格式的地震波形文件

2. **批量加载**：
   - 点击"Add Directory"按钮
   - 或从菜单栏选择"File" -> "Open Directory"
   - 选择包含多个MiniSEED文件的文件夹

#### 2.1.1 预处理流程

当MiniSEED文件被加载后，波形数据会根据 `config/settings.py` 中的设置进行以下预处理步骤：

1.  **去趋势**：移除波形数据的平均值 (`demean`)，以消除直流偏移或基线漂移。
2.  **重采样**：波形数据会根据设置中指定的 `sampling_rate` 重采样到目标采样率。
3.  **滤波**：根据设置中定义的 `filter_type` (支持 `bandpass`、`highpass`、`lowpass`) 和 `freq_range`，对波形数据进行滤波。

#### 2.2 波形显示与操作

1. **基本查看**：
   - 波形显示在主窗口的右侧面板，即Waveform Display
   - 左侧面板显示已加载的"File List"

2. **波形操作**：
   - 缩放：使用鼠标滚轮或工具栏的"Zoom In"/"Zoom Out"按钮
   - Reset View：点击工具栏的"Reset View"按钮

#### 2.3 拾取操作

1. **手动拾取**：
   - 在波形上点击要拾取的位置
   - 使用下拉菜单"Quality"选择拾取质量（A/B/C）
   - 或使用快捷键：
     - `A`：设置为A-quality
     - `B`：设置为B-quality
     - `C`：设置为C-quality

2. **Editing Picks**：
   - Undo：点击"Undo"按钮或使用 `Ctrl+Z`
   - Redo：点击"Redo"按钮或使用 `Ctrl+Y`
   - Delete：选中拾取点后按 `Delete` 键

#### 2.4 Saving Results

1. **Save Picks**：
   - 点击工具栏的"Save"按钮
   - 选择保存位置和文件名

2. **Export CSV**：
   - 从菜单栏选择"File" -> "Export CSV"
   - 选择导出位置和文件名
   - CSV文件将包含所有拾取点的信息

### 3. 注意事项

1. **文件格式**：
   - 支持MiniSEED格式的地震波形文件
   - 确保文件包含正确的header information

2. **Picking Quality**：
   - A-quality: High quality pick, clear waveform
   - B-quality: Medium quality, waveform identifiable
   - C-quality: Low quality, for reference only

3. **Data Backup**：
   - 定期保存picking results
   - Export CSV files for backup
   - 记录processing logs

### 4. 获取帮助

- 查看"Help"菜单中的"Shortcuts"和"About"
- 检查日志文件：`~/.p_wave_picker/logs/app.log`
- 参考完整文档：`docs/user_manual.md` 

### 注意：

- README.md中列出功能已完成开发，但用户手册上有些功能仍待开发，作者正在努力中💪
- 数据demo可用example_data文件夹

<div style="text-align: center;">
  <img src="https://github.com/hhhjjjcc/JC-Phase-Picker/blob/main/example.png" width="70%">
  <p><b>Figure 1: GUI示例交互界面</p>
</div>
