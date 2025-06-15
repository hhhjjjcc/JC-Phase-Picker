"""
主程序
"""

import os
import sys
import logging
from datetime import datetime
from gui.main_window import MainWindow
from config.settings import Settings

def setup_logging():
    """设置日志"""
    # 创建日志目录
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志文件名
    log_file = os.path.join(
        log_dir,
        f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies():
    """检查依赖"""
    try:
        import obspy
        import numpy
        import matplotlib
        import tkinter
        return True
    except ImportError as e:
        logging.error(f"缺少必要的依赖: {str(e)}")
        return False

def main():
    """主函数"""
    try:
        # 设置日志
        setup_logging()
        
        # 检查依赖
        if not check_dependencies():
            return
        
        # 创建主窗口
        app = MainWindow()
        
        # 运行程序
        app.run()
        
    except Exception as e:
        logging.error(f"程序运行出错: {str(e)}")
        raise

if __name__ == "__main__":
    main() 