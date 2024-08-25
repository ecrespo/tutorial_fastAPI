import unittest
from unittest.mock import patch, MagicMock

from app.controllers import TasksController
from app.repositories.TaskRepository import TaskRepository
from app.models.TasksModel import Task


class TestTasks(unittest.TestCase):

    @patch('app.repositories.TaskRepository.TaskRepository')
    def test_createTask(self, mock_repository):
        sample_task = Task(title="Test Task", is_complete=False)
        mock_repository.create_task.return_value = sample_task

        task_data = {'title': 'Test Task'}
        response = Tasks.createTask(task_data)

        mock_repository.create_task.assert_called_once_with(task_data)
        self.assertEqual(response, {"message": "Task has been saved"})
        self.assertEqual(mock_repository.create_task.call_count, 1)
    #
    # ###
    # @patch('app.controllers.Tasks.TaskRepository')
    # def createTask_saves_task_and_returns_message(self, mock_repository):
    #     sample_task = Task(title="Test Task")
    #     mock_repository.create_task.return_value = sample_task
    #
    #     task_data = {'title': 'Test Task'}
    #     response = Tasks.createTask(task_data)
    #
    #     mock_repository.create_task.assert_called_once_with(task_data)
    #     self.assertEqual(response, {"message": "Task has been saved", "task": sample_task})
    #     self.assertEqual(mock_repository.create_task.call_count, 1)
    #
    # @patch('app.controllers.Tasks.TaskRepository')
    # def getalltasks_returns_list_of_tasks(self, mock_repository):
    #     sample_tasks = [Task(title="Task 1"), Task(title="Task 2")]
    #     mock_repository.get_all_tasks.return_value = sample_tasks
    #
    #     response = Tasks.getalltasks()
    #
    #     self.assertEqual(response, sample_tasks)
    #     self.assertEqual(mock_repository.get_all_tasks.call_count, 1)
    #
    # @patch('app.controllers.Tasks.TaskRepository')
    # def retrieveTask_returns_task_if_exists(self, mock_repository):
    #     sample_task = Task(title="Test Task")
    #     mock_repository.get_task_by_id.return_value = sample_task
    #
    #     task_id = PydanticObjectId()
    #     response = Tasks.retrieveTask(task_id)
    #
    #     self.assertEqual(response, sample_task)
    #     self.assertEqual(mock_repository.get_task_by_id.call_count, 1)
    #
    # @patch('app.controllers.Tasks.TaskRepository')
    # def retrieveTask_raises_exception_if_not_found(self, mock_repository):
    #     mock_repository.get_task_by_id.return_value = None
    #
    #     task_id = PydanticObjectId()
    #     with self.assertRaises(HTTPException) as context:
    #         Tasks.retrieveTask(task_id)
    #
    #     self.assertEqual(context.exception.status_code, 404)
    #     self.assertEqual(mock_repository.get_task_by_id.call_count, 1)
    #
    # @patch('app.controllers.Tasks.TaskRepository')
    # def updateTask_updates_task_if_exists(self, mock_repository):
    #     sample_task = Task(title="Updated Task")
    #     mock_repository.update_task.return_value = sample_task
    #
    #     task_id = PydanticObjectId()
    #     task_data = Task(title="Updated Task")
    #     response = Tasks.updateTask(task_data, task_id)
    #
    #     self.assertEqual(response, sample_task)
    #     self.assertEqual(mock_repository.update_task.call_count, 1)
    #
    # @patch('app.controllers.Tasks.TaskRepository')
    # def updateTask_raises_exception_if_not_found(self, mock_repository):
    #     mock_repository.update_task.return_value = None
    #
    #     task_id = PydanticObjectId()
    #     task_data = Task(title="Updated Task")
    #     with self.assertRaises(HTTPException) as context:
    #         Tasks.updateTask(task_data, task_id)
    #
    #     self.assertEqual(context.exception.status_code, 404)
    #     self.assertEqual(mock_repository.update_task.call_count, 1)
    #
    # @patch('app.controllers.Tasks.TaskRepository')
    # def deleteTask_deletes_task_if_exists(self, mock_repository):
    #     mock_repository.delete_task.return_value = True
    #
    #     task_id = PydanticObjectId()
    #     response = Tasks.deleteTask(task_id)
    #
    #     self.assertEqual(response, {"message": "Task deleted"})
    #     self.assertEqual(mock_repository.delete_task.call_count, 1)
    #
    # @patch('app.controllers.Tasks.TaskRepository')
    # def deleteTask_raises_exception_if_not_found(self, mock_repository):
    #     mock_repository.delete_task.return_value = None
    #
    #     task_id = PydanticObjectId()
    #     with self.assertRaises(HTTPException) as context:
    #         Tasks.deleteTask(task_id)
    #
    #     self.assertEqual(context.exception.status_code, 404)
    #     self.assertEqual(mock_repository.delete_task.call_count, 1)

if __name__ == '__main__':
    unittest.main()
