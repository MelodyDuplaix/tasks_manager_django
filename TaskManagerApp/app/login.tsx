import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { fetchToken } from '@/services/authentification';

const LoginScreen = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

 const handleLogin = async () => {
    try {
      setErrorMessage('');
      if (!username) {
        setErrorMessage("Veuillez fournir un nom d'utilisateur");
        return;
      }
      if (!password) {
        setErrorMessage("Veuillez fournir un mot de passe");
        return;
      }
      const error = await fetchToken(username, password);
      if (error) {
        setErrorMessage(error);
        return;
      }
    } catch (error) {
      console.error('Login error:', error);
      setErrorMessage('Une erreur est survenue lors de la connexion');
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
