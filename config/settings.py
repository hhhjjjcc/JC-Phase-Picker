"""
Settings Management Module
"""

import json
import os
from pathlib import Path
from .constants import DEFAULT_PARAMS

class Settings:
    """Settings Management Class"""
    
    def __init__(self):
        """Initialize settings"""
        self.settings_file = Path.home() / '.p_wave_picker' / 'settings.json'
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return self._create_default_settings()
        else:
            return self._create_default_settings()
    
    def _create_default_settings(self):
        """Create default settings"""
        # Ensure directory exists
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create default settings
        settings = DEFAULT_PARAMS.copy()
        
        # Save default settings
        self.save_settings(settings)
        
        return settings
    
    def save_settings(self, settings=None):
        """Save settings"""
        if settings is None:
            settings = self.settings
        
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def get(self, section, key, default=None):
        """Get setting value"""
        try:
            return self.settings[section][key]
        except KeyError:
            return default
    
    def set(self, section, key, value):
        """Set value"""
        if section not in self.settings:
            self.settings[section] = {}
        self.settings[section][key] = value
        return self.save_settings()
    
    def get_section(self, section):
        """Get entire section"""
        return self.settings.get(section, {})
    
    def reset_to_defaults(self):
        """Reset to default settings"""
        self.settings = self._create_default_settings()
        return self.save_settings()
    
    def update(self, new_settings):
        """Update settings"""
        self._update_dict(self.settings, new_settings)
        return self.save_settings()
    
    def _update_dict(self, d, u):
        """Recursively update dictionary"""
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = self._update_dict(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    def save(self):
        """Save current settings"""
        return self.save_settings() 