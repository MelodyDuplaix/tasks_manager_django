import { useState, useEffect } from 'react';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Text, View, StyleSheet, TextInput, Button, Alert } from 'react-native';
import { updateTask, fetchTaskDetails } from '../services/taskService';

export default function EditTask() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const taskId = Array.isArray(id) ? parseInt(id[0] || '0', 10) : parseInt(id || '0', 10);
  const [taskName, setTaskName] = useState('');
  const [coinsNumber, setCoinsNumber] = useState('');
  const [typeId, setTypeId] = useState('');
  const [error, setError] = useState('');
  const [submanagerId, setSubmanagerId] = useState(0);

  useEffect(() => {
    const fetchTask = async () => {
      try {
        const task = await fetchTaskDetails(taskId);
        if (task) {
          if (task.name && task.coins_number && task.type && task.type.id) {
            setTaskName(task.name);
            setCoinsNumber(task.coins_number.toString());
            setTypeId(task.type.id.toString());
            setSubmanagerId(task.type.sub_manager);
          } else {
            setError('Task data incomplete');
          }
        } else {
          setError('Task not found');
        }
      } catch (error: any) {
        setError(`Error fetching task details: ${error.message}`);
        console.error('Error fetching task details:', error);
      }
    };
    fetchTask();
  }, [taskId]);

  const handleSubmit = async () => {
    try {
      await updateTask(taskId, { name: taskName, coins_number: parseInt(coinsNumber, 10), type_id: parseInt(typeId, 10) }, () => {
        router.push(`/submanager/${submanagerId}`);
      });
    } catch (error) {
      setError('Error updating task');
      console.error('Error updating task:', error);
      Alert.alert('Error', 'Error updating task');
    }
  };

  if (error) {
    return <View style={styles.container}><Text>{error}</Text></View>;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Task Name:</Text>
      <TextInput
        style={styles.input}
        value={taskName}
        onChangeText={setTaskName}
      />
      <Text style={styles.label}>Coins:</Text>
      <TextInput
        style={styles.input}
        value={coinsNumber}
        onChangeText={setCoinsNumber}
        keyboardType="number-pad"
      />
      <Text style={styles.label}>Type ID:</Text>
      <TextInput
        style={styles.input}
        value={typeId}
        onChangeText={setTypeId}
        keyboardType="number-pad"
      />
      <Button title="Update Task" onPress={handleSubmit} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  label: {
    fontSize: 16,
    marginBottom: 5,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
  },
});
