import { useState, useEffect } from 'react';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Text, View, StyleSheet, TextInput, Button, Alert, Platform } from 'react-native';
import { updateTask, fetchTaskDetails } from '../services/taskService';
import { fetchSubmanagers } from '../services/fetchApiInfos';
import { Picker } from '@react-native-picker/picker';
import DateTimePicker from '@react-native-community/datetimepicker';
import { fetchQuery, getToken } from '../services/authentification';

interface TaskUpdates {
  name: string;
  coins_number: number;
  type_id?: number;
  sub_manager_id?: number;
  date?: Date;
}

interface SubManager {
  id: number;
  name: string;
}

interface TaskType {
  id: number;
  name: string;
}

export default function EditTask() {
  const router = useRouter();
  const { id, submanagerId: submanagerIdParam } = useLocalSearchParams();
  const taskId = Array.isArray(id) ? parseInt(id[0] || '0', 10) : parseInt(id || '0', 10);
  const [taskName, setTaskName] = useState('');
  const [coinsNumber, setCoinsNumber] = useState('');
  const [typeId, setTypeId] = useState('');
  const [error, setError] = useState('');
  const initialSubmanagerId = typeof submanagerIdParam === 'string' ? parseInt(submanagerIdParam, 10) : 0;
  const [submanagerId, setSubmanagerId] = useState(initialSubmanagerId);
  const [isPonctual, setIsPonctual] = useState(false);
  const [date, setDate] = useState<Date | undefined>(undefined);
  const [submanagers, setSubmanagers] = useState<SubManager[]>([]);
  const [taskTypes, setTaskTypes] = useState<TaskType[]>([]);
  const [newTaskTypeName, setNewTaskTypeName] = useState('');
  const [showDatePicker, setShowDatePicker] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const task = await fetchTaskDetails(taskId);
        if (task) {
          if (task.date) {
            // Ponctual task
            setIsPonctual(true);
            setTaskName(task.name);
            setCoinsNumber(task.coins_number.toString());
            setDate(new Date(task.date));
            setSubmanagerId(task.sub_manager?.id || 0);
          } else {
            // Regular task
            setIsPonctual(false);
            if (task.name && task.coins_number && task.type && task.type.id) {
              setTaskName(task.name);
              setCoinsNumber(task.coins_number.toString());
              setTypeId(task.type.id.toString());
              setSubmanagerId(task.type.sub_manager);
            } else {
              setError('Task data incomplete');
            }
          }
        } else {
          setError('Task not found');
        }
      } catch (error: any) {
        setError(`Error fetching task details: ${error.message}`);
        console.error('Error fetching task details:', error);
      }
    };

    const fetchSubmanagersData = async () => {
      try {
        const submanagersData = await fetchSubmanagers();
        setSubmanagers(submanagersData || []);
      } catch (error) {
        console.error("Failed to fetch submanagers:", error);
      }
    };

    const fetchTaskTypesData = async (submanagerId: number) => {
      try {
        const token = await getToken();
        if (token) {
          const response: TaskType[] | null = await fetchQuery(token, `tasktype/${submanagerId}`);
          console.log('Task types:', response);
          setTaskTypes(response || []);
        } else {
          console.error("No token found");
        }
      } catch (error) {
        console.error("Failed to fetch task types:", error);
      }
    };

    const runEffect = async () => {
      await fetchData();
      await fetchSubmanagersData();
      if (submanagerId) {
        console.log("submanagerId:", submanagerId);
        await fetchTaskTypesData(submanagerId);
      }
    };

    runEffect();
  }, [taskId, submanagerId]);

  const handleSubmit = async () => {
    try {
      const updates: TaskUpdates = {
        name: taskName,
        coins_number: parseInt(coinsNumber, 10),
      };

      if (isPonctual) {
        updates.sub_manager_id = submanagerId;
        updates.date = date;
      } else {
        updates.type_id = parseInt(typeId, 10);
        if (newTaskTypeName) {
          const token = await getToken();
          if (token) {
            await fetchQuery(token, 'tasktype/add', true, 'POST', { name: newTaskTypeName, sub_manager_id: submanagerId });
            const response: TaskType[] | null = await fetchQuery(token, `tasktype/${submanagerId}`);
            if (response) {
              setTaskTypes(response || []);
            }
          }
        }
      }

      await updateTask(taskId, updates, () => {
        router.push(`/submanager/${submanagerId}`);
      });
    } catch (error) {
      setError('Error updating task');
      console.error('Error updating task:', error);
      Alert.alert('Error', 'Error updating task');
    }
  };

  const onChange = (event: any, selectedDate: Date | undefined) => {
    setShowDatePicker(Platform.OS === 'ios');
    if (selectedDate) {
      setDate(selectedDate);
    }
  };

  const showMode = () => {
    setShowDatePicker(true);
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

      {isPonctual ? (
        <>
          <Text style={styles.label}>Date:</Text>
          {Platform.OS === 'web' ? (
            <TextInput
              style={styles.input}
              value={date ? date.toISOString() : ''}
              onChangeText={(text) => {
                const newDate = new Date(text);
                if (!isNaN(newDate.getTime())) {
                  setDate(newDate);
                }
              }}
              keyboardType="numbers-and-punctuation"
            />
          ) : (
            <>
              <Button onPress={showMode} title="Show date picker!" />
              {showDatePicker && (
                <DateTimePicker
                  testID="dateTimePicker"
                  value={date || new Date()}
                  mode="datetime"
                  display="default"
                  onChange={onChange}
                />
              )}
              {date && <Text>Date: {date.toLocaleString()}</Text>}
            </>
          )}

          <Text style={styles.label}>Submanager:</Text>
          <Picker
            selectedValue={submanagerId}
            style={styles.picker}
            onValueChange={(itemValue: number) => {
              setSubmanagerId(itemValue);
            }}
          >
            {submanagers.map((submanager) => (
              <Picker.Item key={submanager.id} label={submanager.name} value={submanager.id} />
            ))}
          </Picker>
        </>
      ) : (
        <>
          <Text style={styles.label}>Type ID:</Text>
          <Picker
            selectedValue={typeId}
            style={styles.picker}
            onValueChange={(itemValue: string) => setTypeId(itemValue)}
          >
            {taskTypes.map((taskType) => (
              <Picker.Item key={taskType.id} label={taskType.name} value={taskType.id.toString()} />
            ))}
          </Picker>
          <Text style={styles.label}>New Task Type:</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter new task type"
            value={newTaskTypeName}
            onChangeText={setNewTaskTypeName}
          />
        </>
      )}

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
  picker: {
    height: 40,
    marginBottom: 10,
  },
});
