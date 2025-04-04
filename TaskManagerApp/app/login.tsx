import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';

const LoginScreen = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const router = useRouter();

 const handleLogin = async () => {
    try {
      setErrorMessage('');
      console.log('handleLogin called', username, password);
      const response = await axios.post('http://127.0.0.1:8000/api/login/', {
        username: username,
        password: password,
      });

      if (response.status === 200) {
        const { access, refresh } = response.data;
        await AsyncStorage.setItem('authToken', access);
        await AsyncStorage.setItem('refreshToken', refresh);
        router.replace('/');
      } else if (response.status === 401) {
        setErrorMessage('Mauvais identifiants');
        Alert.alert('Mauvais identifiants', 'Veuillez vérifier votre nom d\'utilisateur et votre mot de passe.');
      } else {
        console.log(response.status)
        setErrorMessage('Erreur de connexion');
        Alert.alert('Erreur de connexion', 'Une erreur s\'est produite lors de la connexion.');
      }
    } catch (error: any) {
      if (error.response && error.response.status === 401) {
        setErrorMessage('Mauvais identifiants');
        Alert.alert('Mauvais identifiants', 'Veuillez vérifier votre nom d\'utilisateur et votre mot de passe.');
        return;
      }
      setErrorMessage('Erreur de connexion');
      Alert.alert('Erreur de connexion', error.message);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>
      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      <Button title="Login" onPress={handleLogin} />
      {errorMessage ? <Text style={styles.error}>{errorMessage}</Text> : null}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    marginBottom: 10,
    borderRadius: 5,
  },
  error: {
    color: 'red',
    marginTop: 10,
  },
});

export default LoginScreen;
