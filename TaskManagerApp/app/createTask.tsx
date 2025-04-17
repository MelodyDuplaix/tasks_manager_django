import { useEffect, useState } from 'react';
import { Text, View, StyleSheet, TextInput, Button, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { fetchQuery, getToken } from '../services/authentification';

interface TaskType {
  id: number;
  name: string;
}

const CreateTask = () => {
  const router = useRouter();
  const params = useLocalSearchParams();
  const submanagerId = typeof params.submanagerId === 'string' && !Array.isArray(params.submanagerId) ? parseInt(params.submanagerId, 10) : 0;

  const [taskName, setTaskName] = useState('');
  const [coins, setCoins] = useState('');
  const [taskType, setTaskType] = useState<string>('');
  const [newTaskTypeName, setNewTaskTypeName] = useState('');
  const [taskTypes, setTaskTypes] = useState<TaskType[]>([]);

  const fetchTaskTypes = async () => {
    const token = await getToken();
    if (token) {
      const response: TaskType[] | null = await fetchQuery(token, `tasktype/${submanagerId}`);
      if (response) {
        setTaskTypes(response || []);
      }
    }
  };

  const handleSubmit = async () => {
    const token = await getToken();
    if (token) {
      console.log("taskType:", taskType);
      const typeId = parseInt(taskType, 10);
      if (isNaN(typeId)) {
        console.error("Invalid task type selected");
        return;
      }
      const data = {
        name: taskName,
        coins_number: parseInt(coins, 10),
        type_id: typeId,
        is_ponctual: false,
        sub_manager_id: submanagerId,
        date: undefined,
      };
      if (newTaskTypeName) {
        await createTaskType(token, newTaskTypeName, submanagerId);
        await fetchTaskTypes();
      }
      const response = await fetchQuery(token, 'task/add', true, 'POST', data);
      if (response) {
        router.back();
      }
    }
  };

  const createTaskType = async (token: string | null, name: string, submanagerId: number) => {
    if (token) {
      const response = await fetchQuery(token, 'tasktype/add', true, 'POST', { name, sub_manager_id: submanagerId });
      if (!response) {
        console.error('Failed to create task type');
      }
    }
  };

  useEffect(() => {
    if (taskTypes.length === 0) {
      fetchTaskTypes();
    }
    if (taskTypes.length > 0) {
      setTaskType(taskTypes[0].id.toString());
    }
  }, [taskTypes]);

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <Text style={styles.label}>Nom de la tâche:</Text>
      <TextInput
        style={styles.input}
        value={taskName}
        onChangeText={setTaskName}
      />
      <Text style={styles.label}>Nombre de pièces:</Text>
      <TextInput
        style={styles.input}
        value={coins}
        onChangeText={setCoins}
        keyboardType="number-pad"
      />
      <Text style={styles.label}>Type de tâche:</Text>
      {taskTypes.length > 0 && (
        <Picker
          selectedValue={taskType}
          style={styles.picker}
          onValueChange={(itemValue: string) => setTaskType(itemValue)}
        >
          {taskTypes.map((type) => (
            <Picker.Item key={type.id} label={type.name} value={type.id.toString()} />
          ))}
        </Picker>
      )}
      <Text style={styles.label}>Nouveau type de tâche:</Text>
      <TextInput
        style={styles.input}
        value={newTaskTypeName}
        onChangeText={setNewTaskTypeName}
      />
      <Button title="Créer la tâche" onPress={handleSubmit} />
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    flexGrow: 1,
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
  picker: {
    height: 40,
    marginBottom: 10,
  },
});

export default CreateTask;
