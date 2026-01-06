/**
 * Task service for API integration
 */
import { Task, CreateTaskRequest, UpdateTaskRequest } from '../types/task';
import { apiClient } from '../lib/api';

export interface TaskService {
  getAllTasks: () => Promise<Task[]>;
  getTaskById: (id: number) => Promise<Task>;
  createTask: (taskData: CreateTaskRequest) => Promise<Task>;
  updateTask: (id: number, taskData: UpdateTaskRequest) => Promise<Task>;
  deleteTask: (id: number) => Promise<void>;
  updateTaskStatus: (id: number, completed: boolean) => Promise<Task>;
}

class TaskServiceImpl implements TaskService {
  async getAllTasks(): Promise<Task[]> {
    const response = await apiClient.tasks.getAll();
    return response.data;
  }

  async getTaskById(id: number): Promise<Task> {
    const response = await apiClient.tasks.getById(id.toString());
    return response.data;
  }

  async createTask(taskData: CreateTaskRequest): Promise<Task> {
    const response = await apiClient.tasks.create(taskData);
    return response.data;
  }

  async updateTask(id: number, taskData: UpdateTaskRequest): Promise<Task> {
    const response = await apiClient.tasks.update(id.toString(), taskData);
    return response.data;
  }

  async deleteTask(id: number): Promise<void> {
    await apiClient.tasks.delete(id.toString());
  }

  async updateTaskStatus(id: number, completed: boolean): Promise<Task> {
    // Use the PATCH endpoint for status updates
    const response = await apiClient.tasks.updateStatus(id.toString(), completed);
    return response.data;
  }
}

// Export singleton instance
export const taskService = new TaskServiceImpl();

// Export the class for potential dependency injection
export default TaskServiceImpl;