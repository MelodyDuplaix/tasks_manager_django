import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, StyleProp, TextStyle } from 'react-native';
import FontAwesome6 from 'react-native-vector-icons/FontAwesome6';
import { Menu, IconButton } from 'react-native-paper';
import { useRouter } from 'expo-router';

interface TaskItemProps {
  id: number;
  name: string;
  coins_number: number;
  type?: any;
  date?: string;
  isPonctual?: boolean;
  onTaskDone: (id: number, isPonctual: boolean) => void;
  onDeleteTask?: (id: number, isPonctual: boolean) => void;
  done_today_count: number;
  isReward?: boolean;
  style?: StyleProp<TextStyle>;
}

const TaskItem: React.FC<TaskItemProps> = (props) => {
  const { id, name, coins_number, type, date, isPonctual, onTaskDone, onDeleteTask, isReward } = props;
  const router = useRouter();
  const [visible, setVisible] = React.useState(false);
  const [showCheck, setShowCheck] = React.useState(false);

  const openMenu = () => setVisible(true);
  const closeMenu = () => setVisible(false);

  const handleCheckboxPress = () => {
    setShowCheck(true);
    props.onTaskDone(id, isPonctual || false);
    setTimeout(() => setShowCheck(false), 500);
  };

  return (
    <View style={styles.item}>
      <TouchableOpacity style={styles.checkbox} onPress={handleCheckboxPress}>
        {showCheck && <View style={styles.innerCheckbox} />}
      </TouchableOpacity>
      <View style={{ flex: 1 }}>
        <Text style={[styles.text, props.style]}>{name}</Text>
        <Text style={styles.dateText}>
          {date ? date.replace("T", " ").replace("Z", " ") : ""}
        </Text>
        {type && (
          <Text style={styles.typeText}>
            ({type.name})
          </Text>
        )}
      </View>
      <View style={styles.coins}>
        {(props.done_today_count || 0) > 0 && (
          <View style={{ flexDirection: 'row', alignItems: 'center', marginRight: 15, gap: 5 }}>
            <Text style={{ color: 'green', fontSize: 14 }}>
              {(props.done_today_count || 0).toString()}
            </Text>
            <FontAwesome6 name="check" size={16} color="green" />
          </View>
        )}
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
        <Menu.Item onPress={() => { closeMenu(); router.push({ pathname: `/editTask`, params: { id: id } }) }} title="Modifier" />
        <Menu.Item onPress={() => {
          closeMenu();
          if (onDeleteTask) {
            onDeleteTask(id, isPonctual || false);
          }
        }} title="Supprimer" />
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
    backgroundColor: 'green',
  },
  text: {
    fontSize: 16,
    marginBottom: 2,
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
    marginTop: 2,
  },
});

export { TaskItemProps };
export default TaskItem;
