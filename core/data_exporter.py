"""
Data Export Module
Provides data export functionality in various formats
"""

import os
import csv
import json
import numpy as np
from obspy import Stream, Trace
from obspy.io.seg2.seg2 import _write_seg2
from obspy.io.segy.segy import _write_segy
from typing import List, Dict, Any, Optional

from config.constants import (
    SUPPORTED_EXPORT_FORMATS,
    CSV_COLUMNS,
    PICK_QUALITY_LEVELS
)

class DataExporter:
    """Data Exporter Class"""
    
    def __init__(self):
        """Initialize the data exporter"""
        self.supported_formats = SUPPORTED_EXPORT_FORMATS
    
    def export_picks(self, picks: List[Dict[str, Any]],
                    output_file: str,
                    format: str = 'csv') -> bool:
        """
        Export picking results
        
        Args:
            picks: List of picking results
            output_file: Output file path
            format: Output format
            
        Returns:
            Whether export was successful
        """
        if format not in self.supported_formats:
            raise ValueError(f"Unsupported export format: {format}")
        
        try:
            if format == 'csv':
                self._export_csv(picks, output_file)
            elif format == 'json':
                self._export_json(picks, output_file)
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            return True
        except Exception as e:
            print(f"Export failed: {str(e)}")
            return False
    
    def export_waveform(self, st: Stream,
                       output_file: str,
                       format: str = 'mseed') -> bool:
        """
        Export waveform data
        
        Args:
            st: Waveform data stream
            output_file: Output file path
            format: Output format
            
        Returns:
            Whether export was successful
        """
        if format not in self.supported_formats:
            raise ValueError(f"Unsupported export format: {format}")
        
        try:
            if format == 'mseed':
                st.write(output_file, format='MSEED')
            elif format == 'sac':
                st.write(output_file, format='SAC')
            elif format == 'segy':
                _write_segy(st, output_file)
            elif format == 'seg2':
                _write_seg2(st, output_file)
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            return True
        except Exception as e:
            print(f"Export failed: {str(e)}")
            return False
    
    def export_batch_results(self, results: List[Dict[str, Any]],
                           output_dir: str,
                           format: str = 'csv') -> bool:
        """
        Export batch results
        
        Args:
            results: List of batch results
            output_dir: Output directory
            format: Output format
            
        Returns:
            Whether export was successful
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        try:
            # Export summary results
            summary_file = os.path.join(output_dir, f'summary.{format}')
            self._export_summary(results, summary_file, format)
            
            # Export detailed results
            for result in results:
                filename = os.path.basename(result['file'])
                base_name = os.path.splitext(filename)[0]
                output_file = os.path.join(output_dir, f'{base_name}_picks.{format}')
                
                if 'picks' in result:
                    self.export_picks(result['picks'], output_file, format)
            
            return True
        except Exception as e:
            print(f"Export failed: {str(e)}")
            return False
    
    def _export_csv(self, picks: List[Dict[str, Any]],
                   output_file: str) -> None:
        """
        Export to CSV format
        
        Args:
            picks: List of picking results
            output_file: Output file path
        """
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            
            for pick in picks:
                # Convert quality level to description
                if 'quality' in pick:
                    pick['quality'] = PICK_QUALITY_LEVELS.get(pick['quality'], "Unknown")
                
                writer.writerow(pick)
    
    def _export_json(self, picks: List[Dict[str, Any]],
                    output_file: str) -> None:
        """
        Export to JSON format
        
        Args:
            picks: List of picking results
            output_file: Output file path
        """
        with open(output_file, 'w') as f:
            json.dump(picks, f, indent=4, ensure_ascii=False)
    
    def _export_summary(self, results: List[Dict[str, Any]],
                       output_file: str,
                       format: str) -> None:
        """
        Export summary results
        
        Args:
            results: List of batch results
            output_file: Output file path
            format: Output format
        """
        summary = {
            'total_files': len(results),
            'successful_files': sum(1 for r in results if r.get('success', False)),
            'failed_files': sum(1 for r in results if not r.get('success', False)),
            'total_picks': sum(len(r.get('picks', [])) for r in results),
            'quality_distribution': self._get_quality_distribution(results),
            'processing_time': sum(r.get('processing_time', 0) for r in results),
            'results': results
        }
        
        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(summary, f, indent=4, ensure_ascii=False)
        else:
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Metric', 'Value'])
                writer.writerow(['Total Files', summary['total_files']])
                writer.writerow(['Successful Files', summary['successful_files']])
                writer.writerow(['Failed Files', summary['failed_files']])
                writer.writerow(['Total Picks', summary['total_picks']])
                writer.writerow(['Total Processing Time', f"{summary['processing_time']:.2f} seconds"])
                
                # Write quality distribution
                writer.writerow([])
                writer.writerow(['Quality Distribution'])
                for quality, count in summary['quality_distribution'].items():
                    writer.writerow([PICK_QUALITY_LEVELS.get(quality, "Unknown"), count])
    
    def _get_quality_distribution(self, results: List[Dict[str, Any]]) -> Dict[int, int]:
        """
        Get quality distribution
        
        Args:
            results: List of batch results
            
        Returns:
            Quality distribution dictionary
        """
        distribution = {}
        
        for result in results:
            if 'picks' in result:
                for pick in result['picks']:
                    if 'quality' in pick:
                        quality = pick['quality']
                        distribution[quality] = distribution.get(quality, 0) + 1
        
        return distribution 