"""
Command History Tests
"""

import unittest
from core.command_history import (
    Command,
    AddPickCommand,
    RemovePickCommand,
    UpdatePickCommand,
    CommandHistory
)

class TestCommand(unittest.TestCase):
    """Base Command Class Tests"""
    
    def test_command_execute(self):
        """Test command execution"""
        class TestCommand(Command):
            def __init__(self):
                self.executed = False
            
            def execute(self):
                self.executed = True
            
            def undo(self):
                self.executed = False
        
        # Create command
        command = TestCommand()
        
        # Execute command
        command.execute()
        self.assertTrue(command.executed)
        
        # Undo command
        command.undo()
        self.assertFalse(command.executed)

class TestAddPickCommand(unittest.TestCase):
    """Add Pick Command Tests"""
    
    def setUp(self):
        """Setup before test"""
        self.pick_manager = type('PickManager', (), {
            'add_pick': lambda file, time, quality: None,
            'remove_pick': lambda file, time: None
        })()
    
    def test_add_pick_command(self):
        """Test add pick command"""
        # Create command
        command = AddPickCommand(
            self.pick_manager,
            'test.mseed',
            0.5,
            'A'
        )
        
        # Execute command
        command.execute()
        
        # Undo command
        command.undo()

class TestRemovePickCommand(unittest.TestCase):
    """Remove Pick Command Tests"""
    
    def setUp(self):
        """Setup before test"""
        self.pick_manager = type('PickManager', (), {
            'add_pick': lambda file, time, quality: None,
            'remove_pick': lambda file, time: None
        })()
    
    def test_remove_pick_command(self):
        """Test remove pick command"""
        # Create command
        command = RemovePickCommand(
            self.pick_manager,
            'test.mseed',
            0.5,
            'A'
        )
        
        # Execute command
        command.execute()
        
        # Undo command
        command.undo()

class TestUpdatePickCommand(unittest.TestCase):
    """Update Pick Command Tests"""
    
    def setUp(self):
        """Setup before test"""
        self.pick_manager = type('PickManager', (), {
            'update_pick': lambda file, old_time, new_time, quality: None
        })()
    
    def test_update_pick_command(self):
        """Test update pick command"""
        # Create command
        command = UpdatePickCommand(
            self.pick_manager,
            'test.mseed',
            0.5,
            0.6,
            'A'
        )
        
        # Execute command
        command.execute()
        
        # Undo command
        command.undo()

class TestCommandHistory(unittest.TestCase):
    """Command History Tests"""
    
    def setUp(self):
        """Setup before test"""
        self.history = CommandHistory()
    
    def test_execute_command(self):
        """Test execute command"""
        # Create test command
        class TestCommand(Command):
            def __init__(self):
                self.executed = False
                self.undone = False
            
            def execute(self):
                self.executed = True
            
            def undo(self):
                self.undone = True
        
        # Execute command
        command = TestCommand()
        self.history.execute(command)
        
        # Verify result
        self.assertTrue(command.executed)
        self.assertFalse(command.undone)
    
    def test_undo_command(self):
        """Test undo command"""
        # Create test command
        class TestCommand(Command):
            def __init__(self):
                self.executed = False
                self.undone = False
            
            def execute(self):
                self.executed = True
            
            def undo(self):
                self.undone = True
        
        # Execute command
        command = TestCommand()
        self.history.execute(command)
        
        # Undo command
        self.history.undo()
        
        # Verify result
        self.assertTrue(command.executed)
        self.assertTrue(command.undone)
    
    def test_redo_command(self):
        """Test redo command"""
        # Create test command
        class TestCommand(Command):
            def __init__(self):
                self.executed = False
                self.undone = False
            
            def execute(self):
                self.executed = True
            
            def undo(self):
                self.undone = True
        
        # Execute command
        command = TestCommand()
        self.history.execute(command)
        
        # Undo command
        self.history.undo()
        
        # Redo command
        self.history.redo()
        
        # Verify result
        self.assertTrue(command.executed)
        self.assertTrue(command.undone)

if __name__ == '__main__':
    unittest.main() 