import { Text, View, StyleSheet, TextInput, Button, ScrollView, Platform } from 'react-native';
import { useState } from 'react';
import { useRouter, useLocalSearchParams } from 'expo-router';
import Slider from '@react-native-community/slider';
import { decomposeObjective, saveTasks } from '../services/objectiveService';
import DateTimePicker, { DateTimePickerEvent } from '@react-native-community/datetimepicker';

export default function DecomposeObjective() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const submanagerId = params.submanagerId as string;

  const [objective, setObjective] = useState('');
  const [number, setNumber] = useState(7);
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const decomposedTasks = await decomposeObjective(objective, number);
      if (decomposedTasks && decomposedTasks.taches) {
        console.log(error)
        console.log(loading)
        const initialTasks = decomposedTasks.taches.map((task: any) => ({
          name: task.name,
          coins_number: 1,
          date: new Date(),
        }));
        setTasks(initialTasks);
      } else {
        setError('Failed to decompose objective');
      }
    } catch (e: any) {
      setError(e.message || 'Failed to decompose objective');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    setError('');
    try {
      if (!submanagerId) {
        setError('Submanager ID is missing');
        return;
      }
      const submanagerIdNumber = parseInt(submanagerId, 10);
      if (isNaN(submanagerIdNumber)) {
        setError('Invalid Submanager ID');
        return;
      }

      const tasksToSave = tasks.map(task => ({
        name: task.name,
        coins_number: task.coins_number,
        date: task.date.toISOString().split('T')[0],
      }));

      const response = await saveTasks(submanagerIdNumber, tasksToSave);
      console.log('Save response:', response);
      if (router.canGoBack()) {
        router.back();
      } else {
        router.replace(`/submanager/${submanagerId}`);
      }
    } catch (e: any) {
      setError(e.message || 'Failed to save tasks');
    } finally {
      setLoading(false);
    }
  };

  const updateTask = (index: number, field: string, value: any) => {
    const newTasks = [...tasks];
    newTasks[index][field] = value;
    setTasks(newTasks);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={{ marginBottom: 20 }}>
      <Text style={styles.label}>Objectif:</Text>
      <TextInput
        style={styles.input}
        value={objective}
        onChangeText={setObjective}
        multiline
      />
      <Text style={styles.label}>Nombre de tâches: {number}</Text>
      <Slider
        style={styles.slider}
        minimumValue={2}
        maximumValue={30}
        step={1}
        value={number}
        onValueChange={(value: number) => setNumber(value)}
      />
      <Button title="Décomposer" onPress={handleSubmit} disabled={loading} />

      {loading ? <Text>Loading...</Text>: null}
      {error ? <Text style={styles.error}>{error}</Text> : null}

      {tasks.map((task, index) => (
        <View key={index} style={styles.taskContainer}>
          <Text style={styles.taskLabel}>Tâche {index + 1}:</Text>
          <TextInput
            style={styles.taskInput}
            value={task.name}
            onChangeText={(text) => updateTask(index, 'name', text)}
          />
          <Text style={styles.taskLabel}>Pièces:</Text>
          <View style={styles.coinsContainer}>
            <Button title="-" onPress={() => updateTask(index, 'coins_number', Math.max(0, task.coins_number - 1))} />
            <TextInput
              style={[styles.taskInput, styles.coinsInput]}
              value={task.coins_number.toString()}
              onChangeText={(text) => updateTask(index, 'coins_number', parseInt(text) || 0)}
              keyboardType="number-pad"
            />
            <Button title="+" onPress={() => updateTask(index, 'coins_number', task.coins_number + 1)} />
          </View>
          <Text style={styles.taskLabel}>Date:</Text>
          {Platform.OS === 'web' ? (
            <View>
              <TextInput
                style={styles.taskInput}
                value={task.date ? task.date.toISOString().slice(0, 16) : ''}
                onChangeText={(text) => {
                  const newDate = new Date(text);
                  if (!isNaN(newDate.getTime())) {
                    updateTask(index, 'date', newDate);
                  }
                }}
                placeholder="YYYY-MM-DDTHH:MM"
              />
            </View>
          ) : (
            <View>
              <DateTimePicker
              style={styles.datePicker}
              value={task.date || new Date()}
              mode="datetime"
              display="default"
              onChange={(event: DateTimePickerEvent, selectedDate?: Date) => {
                if (selectedDate) {
                  updateTask(index, 'date', selectedDate);
                }
              }}
            />
            </View>
          )}
        </View>
      ))}

      {tasks.length > 0 && (
        <Button title="Enregistrer les tâches" onPress={handleSave} disabled={loading} />
      )}
    </View>
    </ScrollView>
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
    height: 100,
    borderColor: '#007bff',
    borderWidth: 2,
    marginBottom: 10,
    paddingHorizontal: 10,
    borderRadius: 5,
  },
  slider: {
    height: 40,
    marginBottom: 10,
  },
  taskContainer: {
    marginBottom: 20,
    padding: 10,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
  },
  taskLabel: {
    fontSize: 14,
    marginBottom: 5,
  },
  taskInput: {
    height: 40,
    borderColor: '#007bff',
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
    borderRadius: 5,
  },
  datePicker: {
    height: 40,
    marginBottom: 10,
  },
  error: {
    color: 'red',
    marginBottom: 10,
  },
  coinsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    width: 150,
  },
  coinsInput: {
    textAlign: 'center',
    width: 50,
    height: 40,
  },
  coinsButton: {
    width: 50,
    height: 60,
  },
});
