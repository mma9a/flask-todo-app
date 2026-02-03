import unittest
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, Task, tasks

class TestTodoApp(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and initialize tasks list"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Clear tasks for testing
        global tasks
        tasks = []
        
    def test_index_page(self):
        """Test that index page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_add_task(self):
        """Test adding a new task"""
        # Test adding a normal task
        response = self.app.post('/add', data={'task': 'Test task'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test task', response.data)
        
        # Test adding empty task (should not add anything)
        initial_task_count = len(tasks)
        response = self.app.post('/add', data={'task': '   '}, follow_redirects=True)
        self.assertEqual(len(tasks), initial_task_count)
        
    def test_complete_task(self):
        """Test marking a task as complete"""
        # Add a task first
        tasks.append(Task(1, 'Test task'))
        
        # Complete the task
        response = self.app.post('/complete/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check that the task is marked as completed
        self.assertTrue(tasks[0].completed)
        
        # Test completing non-existent task (should not raise error)
        response = self.app.post('/complete/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_delete_task(self):
        """Test deleting a task"""
        # Add a task first
        tasks.append(Task(1, 'Test task'))
        
        # Delete the task
        response = self.app.post('/delete/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check that the task is deleted
        self.assertEqual(len(tasks), 0)
        
        # Test deleting non-existent task (should not raise error)
        response = self.app.post('/delete/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_task_persistence(self):
        """Test that tasks persist with unique IDs"""
        # Add multiple tasks
        response1 = self.app.post('/add', data={'task': 'First task'}, follow_redirects=True)
        response2 = self.app.post('/add', data={'task': 'Second task'}, follow_redirects=True)
        
        # Check that both tasks are present
        self.assertIn(b'First task', response2.data)
        self.assertIn(b'Second task', response2.data)
        
        # Check that tasks have different IDs
        self.assertEqual(len(tasks), 2)
        self.assertNotEqual(tasks[0].id, tasks[1].id)

if __name__ == '__main__':
    unittest.main()