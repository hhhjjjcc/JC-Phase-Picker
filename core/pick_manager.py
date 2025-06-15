"""
Pick Management
"""

import os
import csv
import logging
from datetime import datetime
from config.settings import Settings
from config.constants import PICK_QUALITY
import re # Import re module for regex operations

class Pick:
    """Pick Class"""
    
    def __init__(self, time, quality='A'):
        """Initialize the pick"""
        self.time = time
        self.quality = quality
        self.created_at = datetime.now()

class PickManager:
    """Pick Management Class"""
    
    def __init__(self):
        """Initialize the pick manager"""
        self.settings = Settings()
        self.picks_by_file = {}  # Stores picks for each file {file_path: [pick1, pick2, ...]}
    
    def add_pick(self, file_path, pick):
        """Add a pick"""
        if file_path not in self.picks_by_file:
            self.picks_by_file[file_path] = []
        self.picks_by_file[file_path].append(pick)
    
    def remove_pick(self, file_path, pick):
        """Remove a pick"""
        if file_path in self.picks_by_file and pick in self.picks_by_file[file_path]:
            self.picks_by_file[file_path].remove(pick)
    
    def remove_last_pick(self, file_path):
        """Remove the last pick"""
        if file_path in self.picks_by_file and self.picks_by_file[file_path]:
            return self.picks_by_file[file_path].pop()
        return None
    
    def update_pick_quality(self, file_path, pick, new_quality):
        """Update pick quality"""
        if file_path in self.picks_by_file and pick in self.picks_by_file[file_path]:
            pick.quality = new_quality
            logging.info(f"Updated pick quality for {file_path} to {new_quality}")
        else:
            logging.warning(f"Failed to update pick quality for pick: {pick.time} in {file_path}. Pick not found.")
    
    def find_nearest_pick(self, file_path, time, threshold=0.1):
        """Find the nearest pick"""
        if file_path not in self.picks_by_file or not self.picks_by_file[file_path]:
            return None
        
        picks_for_file = self.picks_by_file[file_path]
        # Calculate time differences
        time_diffs = [abs(pick.time - time) for pick in picks_for_file]
        min_diff = min(time_diffs)
        
        # If time difference is less than threshold, return the corresponding pick
        if min_diff <= threshold:
            return picks_for_file[time_diffs.index(min_diff)]
        return None
    
    def get_picks_for_file(self, file_path):
        """Get picks for a specific file"""
        return self.picks_by_file.get(file_path, [])

    def get_all_picks(self):
        """Get all picks from all files (for saving, etc.)"""
        all_picks = []
        for file_path, picks_list in self.picks_by_file.items():
            all_picks.extend([(file_path, pick) for pick in picks_list])
        return all_picks
    
    def has_picks(self):
        """Check if there are any picks"""
        return any(self.picks_by_file.values())
    
    def create_pick(self, time, quality='A'):
        """Create a pick instance"""
        return Pick(time, quality)
    
    def save_picks(self, current_file_path, output_file_path):
        """Save picks for the current file to a JSON file or all picks to CSV (depending on output_file_path extension)
        If output_file_path ends with .json, it saves picks for the current file.
        Otherwise, it saves all picks to a CSV file.
        """
        if output_file_path.endswith('.json'):
            try:
                # Ensure output directory exists
                output_dir = os.path.dirname(output_file_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)

                picks_for_current_file = self.get_picks_for_file(current_file_path)
                pick_data = {
                    "file_path": current_file_path,
                    "picks": []
                }
                for pick in picks_for_current_file:
                    pick_data["picks"].append({
                        "time": pick.time,
                        "quality": pick.quality,
                        "created_at": pick.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    })

                with open(output_file_path, 'w', encoding='utf-8') as f:
                    json.dump(pick_data, f, indent=4, ensure_ascii=False)
                logging.info(f"Picks for {current_file_path} saved successfully to {output_file_path}")
            except Exception as e:
                logging.error(f"Failed to save picks for {current_file_path}: {str(e)}")
                raise
        else: # Assume CSV export for all picks if not JSON
            try:
                # Ensure output directory exists
                output_dir = os.path.dirname(output_file_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                
                with open(output_file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['File Path', 'File Name', 'Event ID', 'Pick Time', 'Pick Quality', 'Created At'])
                    
                    for file_path, picks_list in self.picks_by_file.items():
                        if not picks_list:
                            continue # Skip if no picks for this file

                        file_name = os.path.basename(file_path)
                        evid_match = re.search(r'evid\.(\d+)', file_name)
                        event_id = evid_match.group(1) if evid_match else 'N/A'
                        
                        for pick in picks_list:
                            writer.writerow([
                                file_path,
                                file_name,
                                event_id,
                                pick.time,
                                pick.quality,
                                pick.created_at.strftime('%Y-%m-%d %H:%M:%S')
                            ])
                logging.info(f"All picks successfully saved to file: {output_file_path}")
            except Exception as e:
                logging.error(f"Failed to save all picks: {str(e)}")
                raise # Re-raise the exception after logging 

    def get_pick(self, time, quality, file_path):
        """Get a specific pick based on time, quality, and file path"""
        if file_path in self.picks_by_file:
            for pick in self.picks_by_file[file_path]:
                if pick.time == time and pick.quality == quality:
                    return pick
        return None 