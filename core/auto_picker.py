"""
Automatic Picking Algorithm Module
Provides functionality for automatic P-wave first arrival picking and signal quality evaluation.
"""

import numpy as np
from obspy import Trace
from obspy.signal.trigger import classic_sta_lta, recursive_sta_lta
from scipy import signal
from typing import Optional, Tuple, List, Dict

from config.constants import (
    DEFAULT_STA_LTA_WINDOW,
    DEFAULT_STA_LTA_THRESHOLD,
    DEFAULT_SNR_WINDOW,
    DEFAULT_SNR_THRESHOLD,
    PICK_QUALITY_LEVELS
)

class AutoPicker:
    """Automatic Picker Class"""
    
    def __init__(self):
        """Initialize the automatic picker"""
        self.sta_window = DEFAULT_STA_LTA_WINDOW[0]
        self.lta_window = DEFAULT_STA_LTA_WINDOW[1]
        self.sta_lta_threshold = DEFAULT_STA_LTA_THRESHOLD
        self.snr_window = DEFAULT_SNR_WINDOW
        self.snr_threshold = DEFAULT_SNR_THRESHOLD
    
    def pick_sta_lta(self, tr: Trace,
                     threshold: Optional[float] = None,
                     algorithm: str = 'classic') -> Optional[float]:
        """
        Picks P-wave first arrival using STA/LTA algorithm
        
        Args:
            tr: Input waveform data
            threshold: STA/LTA threshold
            algorithm: Algorithm type ('classic' or 'recursive')
            
        Returns:
            Pick time (time relative to waveform start, in seconds)
        """
        if threshold is None:
            threshold = self.sta_lta_threshold
        
        # Choose algorithm
        if algorithm == 'classic':
            cft = classic_sta_lta(tr.data,
                                int(self.sta_window * tr.stats.sampling_rate),
                                int(self.lta_window * tr.stats.sampling_rate))
        else:
            cft = recursive_sta_lta(tr.data,
                                  int(self.sta_window * tr.stats.sampling_rate),
                                  int(self.lta_window * tr.stats.sampling_rate))
        
        # Find points exceeding the threshold
        trigger_points = np.where(cft > threshold)[0]
        
        if len(trigger_points) > 0:
            # Return the time of the first trigger point
            return trigger_points[0] / tr.stats.sampling_rate
        
        return None
    
    def pick_energy_ratio(self, tr: Trace,
                         window_length: int = 100) -> Optional[float]:
        """
        Picks P-wave first arrival using energy ratio algorithm
        
        Args:
            tr: Input waveform data
            window_length: Window length for calculation
            
        Returns:
            Pick time (time relative to waveform start, in seconds)
        """
        # Calculate signal energy
        energy = tr.data**2
        
        # Calculate sliding window energy ratio
        ratios = []
        for i in range(len(energy) - window_length):
            pre_energy = np.mean(energy[i:i+window_length])
            post_energy = np.mean(energy[i+window_length:i+2*window_length])
            if pre_energy > 0:
                ratios.append(post_energy / pre_energy)
            else:
                ratios.append(0)
        
        # Find maximum energy ratio
        if len(ratios) > 0:
            max_ratio_idx = np.argmax(ratios)
            return max_ratio_idx / tr.stats.sampling_rate
        
        return None
    
    def pick_ar_aic(self, tr: Trace,
                    order: int = 5) -> Optional[float]:
        """
        Picks P-wave first arrival using AR-AIC algorithm
        
        Args:
            tr: Input waveform data
            order: Order of the AR model
            
        Returns:
            Pick time (time relative to waveform start, in seconds)
        """
        # Calculate AIC values
        aic = np.zeros(len(tr.data))
        
        for i in range(order, len(tr.data) - order):
            # Forward AR model
            x1 = tr.data[i-order:i]
            a1 = np.polyfit(np.arange(len(x1)), x1, order)
            e1 = np.sum((x1 - np.polyval(a1, np.arange(len(x1))))**2)
            
            # Backward AR model
            x2 = tr.data[i:i+order]
            a2 = np.polyfit(np.arange(len(x2)), x2, order)
            e2 = np.sum((x2 - np.polyval(a2, np.arange(len(x2))))**2)
            
            # Calculate AIC value
            aic[i] = i * np.log(e1) + (len(tr.data) - i) * np.log(e2)
        
        # Find minimum AIC
        if len(aic) > 0:
            min_aic_idx = np.argmin(aic)
            return min_aic_idx / tr.stats.sampling_rate
        
        return None
    
    def evaluate_signal_quality(self, tr: Trace) -> Tuple[int, float]:
        """
        Evaluates signal quality
        
        Args:
            tr: Input waveform data
            
        Returns:
            (Quality level, Signal-to-noise ratio)
        """
        # Calculate signal-to-noise ratio
        snr = self._calculate_snr(tr)
        
        # Determine quality level based on SNR
        if snr >= self.snr_threshold * 2:
            quality = 0  # High quality
        elif snr >= self.snr_threshold:
            quality = 1  # Medium quality
        else:
            quality = 2  # Low quality
        
        return quality, snr
    
    def _calculate_snr(self, tr: Trace) -> float:
        """
        Calculates signal-to-noise ratio
        
        Args:
            tr: Input waveform data
            
        Returns:
            Signal-to-noise ratio value
        """
        # Get data
        data = tr.data
        
        # Calculate signal power
        signal_power = np.mean(data**2)
        
        # Calculate noise power (using the first window_length points)
        noise_power = np.mean(data[:self.snr_window]**2)
        
        # Calculate SNR
        snr = 10 * np.log10(signal_power / noise_power)
        
        return snr
    
    def get_pick_quality_description(self, quality: int) -> str:
        """
        Gets pick quality description
        
        Args:
            quality: Quality level
            
        Returns:
            Quality description
        """
        return PICK_QUALITY_LEVELS.get(quality, "Unknown")
    
    def get_pick_statistics(self, picks: List[Tuple[float, int]]) -> Dict:
        """
        Gets pick statistics
        
        Args:
            picks: List of picking results, each element is (time, quality level)
            
        Returns:
            Dictionary of statistics
        """
        if not picks:
            return {
                'total_picks': 0,
                'quality_distribution': {},
                'mean_time': 0,
                'std_time': 0
            }
        
        # Calculate total picks
        total_picks = len(picks)
        
        # Calculate quality distribution
        quality_distribution = {}
        for _, quality in picks:
            quality_distribution[quality] = quality_distribution.get(quality, 0) + 1
        
        # Calculate time statistics
        times = [time for time, _ in picks]
        mean_time = np.mean(times)
        std_time = np.std(times)
        
        return {
            'total_picks': total_picks,
            'quality_distribution': quality_distribution,
            'mean_time': mean_time,
            'std_time': std_time
        } 