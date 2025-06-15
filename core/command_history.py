"""
Command History Management
"""

import logging
from datetime import datetime
from config.constants import COMMAND_TYPES

class Command:
    """Base class for commands"""
    
    def __init__(self, command_type):
        """Initialize the command"""
        self.type = command_type
        self.timestamp = datetime.now()
    
    def execute(self):
        """Execute the command"""
        raise NotImplementedError
    
    def undo(self):
        """Undo the command"""
        raise NotImplementedError

class AddPickCommand(Command):
    """Command to add a pick"""
    
    def __init__(self, pick_manager, file_path, pick):
        """Initialize the command"""
        super().__init__(COMMAND_TYPES['add_pick'])
        self.pick_manager = pick_manager
        self.file_path = file_path
        self.pick = pick
    
    def execute(self):
        """Execute the command"""
        try:
            self.pick_manager.add_pick(self.file_path, self.pick)
            return True, "Pick added successfully"
        except Exception as e:
            logging.error(f"Failed to add pick: {str(e)}")
            return False, str(e)
    
    def undo(self):
        """Undo the command"""
        try:
            self.pick_manager.remove_pick(self.file_path, self.pick)
            return True, "Undo add pick successful"
        except Exception as e:
            logging.error(f"Failed to undo add pick: {str(e)}")
            return False, str(e)

class RemovePickCommand(Command):
    """Command to remove a pick"""
    
    def __init__(self, pick_manager, file_path, pick):
        """Initialize the command"""
        super().__init__(COMMAND_TYPES['remove_pick'])
        self.pick_manager = pick_manager
        self.file_path = file_path
        self.pick = pick
    
    def execute(self):
        """Execute the command"""
        try:
            self.pick_manager.remove_pick(self.file_path, self.pick)
            return True, "Pick removed successfully"
        except Exception as e:
            logging.error(f"Failed to remove pick: {str(e)}")
            return False, str(e)
    
    def undo(self):
        """Undo the command"""
        try:
            self.pick_manager.add_pick(self.file_path, self.pick)
            return True, "Undo remove pick successful"
        except Exception as e:
            logging.error(f"Failed to undo remove pick: {str(e)}")
            return False, str(e)

class UpdatePickCommand(Command):
    """Command to update a pick"""
    
    def __init__(self, pick_manager, file_path, pick, new_quality):
        """Initialize the command"""
        super().__init__(COMMAND_TYPES['update_pick'])
        self.pick_manager = pick_manager
        self.file_path = file_path
        self.pick = pick
        self.old_quality = pick.quality
        self.new_quality = new_quality
    
    def execute(self):
        """Execute the command"""
        try:
            self.pick_manager.update_pick_quality(self.file_path, self.pick, self.new_quality)
            self.pick.quality = self.new_quality
            return True, "Pick updated successfully"
        except Exception as e:
            logging.error(f"Failed to update pick: {str(e)}")
            return False, str(e)
    
    def undo(self):
        """Undo the command"""
        try:
            self.pick_manager.update_pick_quality(self.file_path, self.pick, self.old_quality)
            self.pick.quality = self.old_quality
            return True, "Undo update pick successful"
        except Exception as e:
            logging.error(f"Failed to undo update pick: {str(e)}")
            return False, str(e)

class CommandHistory:
    """Command History Class"""
    
    def __init__(self):
        """Initialize command history"""
        self.undo_stack = []
        self.redo_stack = []
    
    def execute_command(self, command):
        """Execute command"""
        success, message = command.execute()
        if success:
            self.undo_stack.append(command)
            self.redo_stack.clear()
        return success, message
    
    def undo(self):
        """Undo command"""
        if not self.undo_stack:
            return False, "No commands to undo"
        
        command = self.undo_stack.pop()
        success, message = command.undo()
        if success:
            self.redo_stack.append(command)
        return success, message
    
    def redo(self):
        """Redo command"""
        if not self.redo_stack:
            return False, "No commands to redo"
        
        command = self.redo_stack.pop()
        success, message = command.execute()
        if success:
            self.undo_stack.append(command)
        return success, message
    
    def clear(self):
        """Clear history"""
        self.undo_stack.clear()
        self.redo_stack.clear()
    
    def can_undo(self):
        """Can undo?"""
        return len(self.undo_stack) > 0
    
    def can_redo(self):
        """Can redo?"""
        return len(self.redo_stack) > 0 