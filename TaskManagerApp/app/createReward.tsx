import { useState } from 'react';
import { Text, View, StyleSheet, TextInput, Button, ScrollView } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { fetchQuery, getToken } from '../services/authentification';

const CreateReward = () => {
  const params = useLocalSearchParams();
  const submanagerId = Array.isArray(params.id) ? params.id[0] : params.id;
  const router = useRouter();
  const [name, setName] = useState('');
  const [coinsNumber, setCoinsNumber] = useState('');

  const handleSubmit = async () => {
    const token = await getToken();
    if (token) {
      const data = {
        name,
        coins_number: parseInt(coinsNumber, 10),
        sub_manager_id: parseInt(submanagerId?.toString() || '', 10),
      };
      const response = await fetchQuery(token, 'reward/add', true, 'POST', data);
      if (response) {
        router.back();
      }
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.label}>Nom de la récompense:</Text>
      <TextInput
        style={styles.input}
        value={name}
        onChangeText={setName}
      />
      <Text style={styles.label}>Nombre de pièces:</Text>
      <TextInput
        style={styles.input}
        value={coinsNumber}
        onChangeText={setCoinsNumber}
        keyboardType="number-pad"
      />
      <Button title="Créer la récompense" onPress={handleSubmit} />
    </ScrollView>
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

export default CreateReward;
