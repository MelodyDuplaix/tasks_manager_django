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
