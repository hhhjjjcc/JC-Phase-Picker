"""
命令历史测试
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
    """命令基类测试"""
    
    def test_command_execute(self):
        """测试命令执行"""
        class TestCommand(Command):
            def __init__(self):
                self.executed = False
            
            def execute(self):
                self.executed = True
            
            def undo(self):
                self.executed = False
        
        # 创建命令
        command = TestCommand()
        
        # 执行命令
        command.execute()
        self.assertTrue(command.executed)
        
        # 撤销命令
        command.undo()
        self.assertFalse(command.executed)

class TestAddPickCommand(unittest.TestCase):
    """添加拾取命令测试"""
    
    def setUp(self):
        """测试前准备"""
        self.pick_manager = type('PickManager', (), {
            'add_pick': lambda file, time, quality: None,
            'remove_pick': lambda file, time: None
        })()
    
    def test_add_pick_command(self):
        """测试添加拾取命令"""
        # 创建命令
        command = AddPickCommand(
            self.pick_manager,
            'test.mseed',
            0.5,
            'A'
        )
        
        # 执行命令
        command.execute()
        
        # 撤销命令
        command.undo()

class TestRemovePickCommand(unittest.TestCase):
    """移除拾取命令测试"""
    
    def setUp(self):
        """测试前准备"""
        self.pick_manager = type('PickManager', (), {
            'add_pick': lambda file, time, quality: None,
            'remove_pick': lambda file, time: None
        })()
    
    def test_remove_pick_command(self):
        """测试移除拾取命令"""
        # 创建命令
        command = RemovePickCommand(
            self.pick_manager,
            'test.mseed',
            0.5,
            'A'
        )
        
        # 执行命令
        command.execute()
        
        # 撤销命令
        command.undo()

class TestUpdatePickCommand(unittest.TestCase):
    """更新拾取命令测试"""
    
    def setUp(self):
        """测试前准备"""
        self.pick_manager = type('PickManager', (), {
            'update_pick': lambda file, old_time, new_time, quality: None
        })()
    
    def test_update_pick_command(self):
        """测试更新拾取命令"""
        # 创建命令
        command = UpdatePickCommand(
            self.pick_manager,
            'test.mseed',
            0.5,
            0.6,
            'A'
        )
        
        # 执行命令
        command.execute()
        
        # 撤销命令
        command.undo()

class TestCommandHistory(unittest.TestCase):
    """命令历史测试"""
    
    def setUp(self):
        """测试前准备"""
        self.history = CommandHistory()
    
    def test_execute_command(self):
        """测试执行命令"""
        # 创建测试命令
        class TestCommand(Command):
            def __init__(self):
                self.executed = False
                self.undone = False
            
            def execute(self):
                self.executed = True
            
            def undo(self):
                self.undone = True
        
        # 执行命令
        command = TestCommand()
        self.history.execute(command)
        
        # 验证结果
        self.assertTrue(command.executed)
        self.assertFalse(command.undone)
    
    def test_undo_command(self):
        """测试撤销命令"""
        # 创建测试命令
        class TestCommand(Command):
            def __init__(self):
                self.executed = False
                self.undone = False
            
            def execute(self):
                self.executed = True
            
            def undo(self):
                self.undone = True
        
        # 执行命令
        command = TestCommand()
        self.history.execute(command)
        
        # 撤销命令
        self.history.undo()
        
        # 验证结果
        self.assertTrue(command.executed)
        self.assertTrue(command.undone)
    
    def test_redo_command(self):
        """测试重做命令"""
        # 创建测试命令
        class TestCommand(Command):
            def __init__(self):
                self.executed = False
                self.undone = False
            
            def execute(self):
                self.executed = True
            
            def undo(self):
                self.undone = True
        
        # 执行命令
        command = TestCommand()
        self.history.execute(command)
        
        # 撤销命令
        self.history.undo()
        
        # 重做命令
        self.history.redo()
        
        # 验证结果
        self.assertTrue(command.executed)
        self.assertTrue(command.undone)
    
    def test_can_undo_redo(self):
        """测试撤销/重做状态"""
        # 创建测试命令
        class TestCommand(Command):
            def execute(self):
                pass
            
            def undo(self):
                pass
        
        # 初始状态
        self.assertFalse(self.history.can_undo())
        self.assertFalse(self.history.can_redo())
        
        # 执行命令
        command = TestCommand()
        self.history.execute(command)
        
        # 验证状态
        self.assertTrue(self.history.can_undo())
        self.assertFalse(self.history.can_redo())
        
        # 撤销命令
        self.history.undo()
        
        # 验证状态
        self.assertFalse(self.history.can_undo())
        self.assertTrue(self.history.can_redo())
    
    def test_clear_history(self):
        """测试清空历史"""
        # 创建测试命令
        class TestCommand(Command):
            def execute(self):
                pass
            
            def undo(self):
                pass
        
        # 执行命令
        command = TestCommand()
        self.history.execute(command)
        
        # 清空历史
        self.history.clear()
        
        # 验证状态
        self.assertFalse(self.history.can_undo())
        self.assertFalse(self.history.can_redo())

if __name__ == '__main__':
    unittest.main() 