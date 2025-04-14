import AsyncStorage from '@react-native-async-storage/async-storage';
import { router } from 'expo-router';
import React, { useState } from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { Appbar, Menu, PaperProvider } from 'react-native-paper';
import FontAwesome6 from 'react-native-vector-icons/FontAwesome6';

const handleLogout = async () => {
    await AsyncStorage.removeItem('accessToken');
    router.replace('/login');
  };

const NavigationBar = ({coins}: {coins: number}) => {
  const [menuVisible, setMenuVisible] = useState(false);

  const openMenu = () => setMenuVisible(true);
  const closeMenu = () => setMenuVisible(false);

  return (
    <PaperProvider>
      <Appbar.Header style={styles.header}>
        <Appbar.Content title="Tasks Manager" titleStyle={styles.title} />
        <View style={styles.coins}>
          <FontAwesome6 name="coins" size={24} color="orange" />
          <Text style={styles.coinsText}>{coins}</Text>
        </View>
        <Menu
          visible={menuVisible}
          onDismiss={closeMenu}
          style={{ zIndex: 100, position: 'absolute' }}
          anchor={
            <Appbar.Action
              icon="dots-vertical"
              color="white"
              onPress={openMenu}
            />
          }
          contentStyle={styles.menuContent}
        >
          <Menu.Item
            onPress={() => console.log('Action 1')}
            title="Action 1"
            titleStyle={styles.menuItem}
          />
          <Menu.Item
            onPress={() => console.log('Action 2')}
            title="Action 2"
            titleStyle={styles.menuItem}
          />
          <Menu.Item
            onPress={handleLogout}
            title="Se déconnecter"
            titleStyle={styles.menuItem}
          />
        </Menu>
      </Appbar.Header>
    </PaperProvider>
  );
};

const styles = StyleSheet.create({
  header: {
    backgroundColor: '#6200EE', // Couleur de la barre
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  title: {
    color: 'white', // Couleur du texte
    fontSize: 20,
    fontWeight: 'bold',
  },
  coins: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 10,
  },
  coinsText: {
    color: 'white',
    fontSize: 16,
    marginLeft: 5,
  },
  menuContent: {
    backgroundColor: '#6200EE', // Même couleur que la barre
  },
  menuItem: {
    color: 'white', // Couleur des textes du menu
  },
});

export default NavigationBar;
