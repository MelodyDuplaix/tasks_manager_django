import { Alert } from 'react-native';
import { fetchQuery, getToken } from './authentification';

export const markTaskDone = async (id: number, isPonctual: boolean, onTaskDone: (id: number, isPonctual: boolean) => void) => {
  try {
    const token = await getToken();
    if (!token) {
      Alert.alert('Error', 'Not authenticated');
      return;
    }
    const response = await fetchQuery(token, `task/done/${id}`, true, 'POST', { is_ponctual: isPonctual });
    if (response && response.message) {
      Alert.alert('Success', response.message);
      onTaskDone(id, isPonctual);
    } else {
      Alert.alert('Error', 'Failed to mark task as done');
    }
  } catch (error: any) {
    console.error('Error marking task as done:', error);
    Alert.alert('Error', 'Error marking task as done');
  }
};

export const updateTask = async (id: number, updates: any, onTaskUpdated: (id: number) => void) => {
  try {
    const token = await getToken();
    if (!token) {
      Alert.alert('Error', 'Not authenticated');
      return;
    }
    const response = await fetchQuery(token, `task/update/${id}`, true, 'PUT', updates);
    if (response && response.message) {
      Alert.alert('Success', response.message);
      onTaskUpdated(id);
    } else {
      Alert.alert('Error', 'Failed to update task');
    }
  } catch (error: any) {
    console.error('Error updating task:', error);
    Alert.alert('Error', 'Error updating task');
  }
};

export const deleteTask = async (id: number, onTaskDeleted: (id: number) => void, isPonctual?: boolean) => {
  try {
    const token = await getToken();
    if (!token) {
      Alert.alert('Error', 'Not authenticated');
      return;
    }
    
    const endpoint = isPonctual !== undefined 
      ? `task/delete/${id}?is_ponctual=${isPonctual}` 
      : `task/delete/${id}`;
    
    const response = await fetchQuery(token, endpoint, true, 'DELETE');
    
    if (response && response.message) {
      Alert.alert('Success', response.message);
      onTaskDeleted(id);
    } else {
      Alert.alert('Error', 'Failed to delete task');
    }
  } catch (error: any) {
    console.error('Error deleting task:', error);
    Alert.alert('Error', 'Error deleting task');
  }
};

export const fetchTaskDetails = async (id: number) => {
  try {
    const token = await getToken();
    if (!token) {
      throw new Error('Not authenticated');
    }
    const response = await fetchQuery(token, `task/${id}`);
    if (!response) {
      throw new Error('Task not found');
    }
    return response;
  } catch (error: any) {
    console.error('Error fetching task details:', error);
    throw error; 
  }
};
