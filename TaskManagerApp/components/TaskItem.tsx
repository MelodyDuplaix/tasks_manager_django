import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import FontAwesome6 from 'react-native-vector-icons/FontAwesome6';
import { Menu, IconButton, MD3Colors } from 'react-native-paper';

interface TaskItemProps {
  name: string;
  coins_number: number;
  type?: {
    id: number;
    name: string;
  };
  date: string;
}

const TaskItem: React.FC<TaskItemProps> = ({ name, coins_number, type, date }) => {
  const [visible, setVisible] = useState(false);

  const openMenu = () => setVisible(true);
  const closeMenu = () => setVisible(false);

  return (
    <View style={styles.item}>
      <TouchableOpacity style={styles.checkbox}>
        <View style={styles.innerCheckbox} />
      </TouchableOpacity>
      <View style={{flex: 1}}>
        <Text style={styles.text}>{name}</Text>
        {type && (
          <Text style={styles.typeText}>
            ({type.name})
          </Text>
        )}
      </View>
      <View>

        <Text style={styles.dateText}>{date ? date.replace("T", " ").replace("Z", " ") : ""}</Text>
      </View>
      <View style={styles.coins}>
        <Text style={styles.coinsText}>{coins_number}</Text>
        <FontAwesome6 name="coins" size={16} color="orange" />
      </View>
      <Menu
        visible={visible}
        onDismiss={closeMenu}
        anchor={
          <IconButton
            icon="dots-vertical"
            size={20}
            onPress={openMenu}
          />
        }
      >
        <Menu.Item onPress={() => { closeMenu(); console.log('Edit')}} title="Modifier" />
        <Menu.Item onPress={() => { closeMenu(); console.log('Delete')}} title="Supprimer" />
      </Menu>
    </View>
  );
};

const styles = StyleSheet.create({
  item: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    paddingHorizontal: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  checkbox: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#ccc',
    marginRight: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  innerCheckbox: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#fff',
  },
  text: {
    flex: 1,
    fontSize: 16,
  },
  typeText: {
    fontSize: 12,
    fontStyle: 'italic',
    color: 'gray',
  },
  coins: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  coinsText: {
    fontSize: 16,
    marginRight: 5,
  },
  dateText: {
    fontSize: 12,
    color: 'gray',
    marginRight: 10,
  }
});

export default TaskItem;
