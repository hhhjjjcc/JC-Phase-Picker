"""
文件管理
"""

import os
import logging
from obspy import read
from config.settings import Settings

class FileManager:
    """文件管理类"""
    
    def __init__(self):
        """初始化文件管理器"""
        self.settings = Settings()
        self.files = []
        self.current_file = None
        self.current_trace = None
    
    def load_file(self, file_path):
        """加载文件"""
        try:
            # 读取文件
            st = read(file_path)
            if len(st) > 0:
                # 保存文件信息
                self.current_file = file_path
                self.current_trace = st[0]
                
                # 预处理
                if self.settings.get('process', 'preprocess'):
                    self.preprocess_trace()
                
                return self.current_trace
            else:
                raise ValueError("文件为空")
                
        except Exception as e:
            logging.error(f"加载文件失败: {str(e)}")
            raise
    
    def scan_directory(self, dir_path):
        """扫描目录"""
        try:
            # 清空文件列表
            self.files = []
            
            # 扫描目录
            for root, _, files in os.walk(dir_path):
                for file in files:
                    if file.endswith('.mseed'):
                        self.files.append(os.path.join(root, file))
            
            # 更新设置
            self.settings.set('paths', 'data_dir', dir_path)
            self.settings.save()
            
            return self.files
            
        except Exception as e:
            logging.error(f"扫描目录失败: {str(e)}")
            raise
    
    def get_files(self):
        """获取文件列表"""
        return self.files
    
    def get_current_file(self):
        """获取当前文件"""
        return self.current_file
    
    def get_current_trace(self):
        """获取当前波形"""
        return self.current_trace
    
    def has_files(self):
        """是否有文件"""
        return len(self.files) > 0
    
    def preprocess_trace(self):
        """预处理波形"""
        if self.current_trace:
            try:
                # 去趋势
                self.current_trace.detrend('demean')
                
                # 重采样
                sampling_rate = self.settings.get('process', 'sampling_rate')
                if sampling_rate:
                    self.current_trace.resample(sampling_rate)
                
                # 滤波
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
                logging.error(f"预处理波形失败: {str(e)}")
                raise
    
    def export_data(self, file_path):
        """导出数据"""
        try:
            # 导出波形数据
            if self.current_trace:
                self.current_trace.write(file_path, format='MSEED')
            
        except Exception as e:
            logging.error(f"导出数据失败: {str(e)}")
            raise 