import { useState } from 'react';
import { Text, View, StyleSheet, TextInput, Button, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import DatePicker from 'react-native-date-picker';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { fetchQuery, getToken } from '../services/authentification';

const CreatePonctualTask = () => {
  const router = useRouter();
  const params = useLocalSearchParams();
  const submanagerId = typeof params.submanagerId === 'string' && !Array.isArray(params.submanagerId) ? parseInt(params.submanagerId, 10) : 0;

  const [taskName, setTaskName] = useState('');
  const [coins, setCoins] = useState('');
  const [date, setDate] = useState(new Date());

  const handleSubmit = async () => {
    const token = await getToken();
    if (token) {
      const dateString = date.getFullYear() + '-' + (date.getMonth() + 1).toString().padStart(2, '0') + '-' + date.getDate().toString().padStart(2, '0') + ' ' + date.getHours().toString().padStart(2, '0') + ':' + date.getMinutes().toString().padStart(2, '0') + ':' + date.getSeconds().toString().padStart(2, '0');
const data = {
        name: taskName,
        coins_number: parseInt(coins, 10),
        sub_manager_id: submanagerId,
        is_ponctual: true,
        type_id: undefined,
        date: dateString,
      };
      const response = await fetchQuery(token, 'task/add', true, 'POST', data);
      if (response) {
        router.back();
      }
    }
  };

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
      <Text style={styles.label}>Date:</Text>
      {Platform.OS === 'web' ? (
        <input type="datetime-local" value={date.toISOString().slice(0, 16)} onChange={(e) => setDate(new Date(e.target.value))} />
      ) : (
        <DatePicker
          date={date}
          onDateChange={setDate}
          mode="datetime"
          locale="fr"
        />
      )}
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
});

export default CreatePonctualTask;
