import { Alert } from 'react-native';
import { fetchQuery, getToken } from './authentification';

export const validateReward = async (id: number, onRewardValidated: (rewardId: number) => void) => {
  try {
    const token = await getToken();
    if (!token) {
      Alert.alert('Error', 'Not authenticated');
      return;
    }
    const response = await fetchQuery(token, `reward/validate/${id}`, true, 'POST');
    if (response && response.message) {
      Alert.alert('Success', response.message);
      onRewardValidated(id);
    } else {
      Alert.alert('Error', 'Failed to validate reward');
    }
  } catch (error: any) {
    console.error('Error validating reward:', error);
    Alert.alert('Error', 'Error validating reward');
  }
};

export const deleteReward = async (id: number, onRewardDeleted: (rewardId: number) => void) => {
  try {
    const token = await getToken();
    if (!token) {
      Alert.alert('Error', 'Not authenticated');
      return;
    }
    const response = await fetchQuery(token, `reward/delete/${id}`, true, 'DELETE');
    if (response && response.message) {
      Alert.alert('Success', response.message);
      onRewardDeleted(id);
    } else {
      Alert.alert('Error', 'Failed to delete reward');
    }
  } catch (error: any) {
    console.error('Error deleting reward:', error);
    Alert.alert('Error', 'Error deleting reward');
  }
};
