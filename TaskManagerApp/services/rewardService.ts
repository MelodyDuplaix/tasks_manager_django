import { Alert } from 'react-native';
import { fetchQuery, getToken } from './authentification';

export const validateReward = async (rewardId: number, onRewardValidated: (rewardId: number) => void) => {
  try {
    const token = await getToken();
    if (!token) {
      Alert.alert('Error', 'Not authenticated');
      return;
    }
    const response = await fetchQuery(token, `reward/validate/${rewardId}`, true, 'POST');
    if (response && response.message) {
      Alert.alert('Success', response.message);
      onRewardValidated(rewardId);
    } else {
      Alert.alert('Error', 'Failed to validate reward');
    }
  } catch (error: any) {
    console.error('Error validating reward:', error);
    Alert.alert('Error', 'Error validating reward');
  }
};
