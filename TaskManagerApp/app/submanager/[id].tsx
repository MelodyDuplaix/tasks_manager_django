import { Text, View, StyleSheet, ScrollView, FlatList, TouchableOpacity } from "react-native";
import { useRouter, useLocalSearchParams } from 'expo-router';
import { useState, useEffect } from 'react';
import NavigationBar from "@/components/NavigationBar";
import ProgressBar from "@/components/ProgressBar";
import MenuItem from "@/components/MenuItem";
import { fetchSubmanagerData, fetchTotalCoins } from "@/services/fetchApiInfos";
import TaskItem from "@/components/TaskItem";
import FontAwesome6 from 'react-native-vector-icons/FontAwesome6';

export default function SubmanagerPage() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const submanagerId = Number(id);
  const [submanagerName, setSubmanagerName] = useState<string>("Nom du sous-manager");
  const [dailyObjective, setDailyObjective] = useState<number>(50);
  const [totalCoinsToday, setTotalCoinsToday] = useState<number>(25);
  const [tasks, setTasks] = useState<any[]>([]);
  const [ponctualTasks, setPonctualTasks] = useState<any[]>([]);
  const [rewards, setRewards] = useState<any[]>([]);
  const [showTasks, setShowTasks] = useState(true);
  const [totalCoins, setTotalCoins] = useState<number>(100);

  useEffect(() => {
    const loadData = async () => {
      const data = await fetchSubmanagerData(submanagerId);
      if (data) {
        setTasks(data.tasks);
        setPonctualTasks(data.ponctual_tasks);
        setRewards(data.rewards);
        setDailyObjective(data.daily_objective);
        setTotalCoinsToday(data.daily_coins);
        setSubmanagerName(data.submanager.name);
      }
    };

    const loadTotalCoins = async () => {
      try {
        const coins = await fetchTotalCoins();
        if (coins) {
          setTotalCoins(coins);
        }
      } catch (error) {
        console.error("Failed to fetch total coins:", error);
      }
    };

    loadData();
    loadTotalCoins();
  }, [submanagerId]);

  const dailyObjectivePercentage = (totalCoinsToday / dailyObjective) * 100;

  const renderItem = ({ item }: { item: any }) => (
    <TaskItem name={item.name} coins_number={item.coins_number} type={item.type} date={item.date} />
  );

  const renderFooter = (type: string) => {
    return (
      <TouchableOpacity style={styles.addButton} onPress={() => console.log(`Add ${type}`)}>
        <Text style={styles.addButtonText}>Ajouter {type}</Text>
      </TouchableOpacity>
    );
  };

  return (
    <View>
      <View style={{ zIndex: 10 }}>
        <NavigationBar coins={totalCoins} />
      </View>
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.title}>{submanagerName}</Text>

        <Text style={styles.heading}>Objectif quotidien</Text>
        <ProgressBar current={totalCoinsToday} total={dailyObjective} />
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={[styles.button, showTasks ? styles.activeButton : {}]}
            onPress={() => setShowTasks(true)}
          >
            <Text style={[styles.buttonText, showTasks ? styles.activeButtonText : {}]}>Tâches</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.button, !showTasks ? styles.activeButton : {}]}
            onPress={() => setShowTasks(false)}
          >
            <Text style={[styles.buttonText, !showTasks ? styles.activeButtonText : {}]}>Récompenses</Text>
          </TouchableOpacity>
        </View>

        {showTasks ? (
          <>
            <Text style={styles.heading}>Tâches ponctuelles</Text>
            {ponctualTasks.length > 0 ? (
              <FlatList
                data={ponctualTasks}
                renderItem={renderItem}
                keyExtractor={(item) => item.id.toString()}
                style={styles.listContainer}
                ListFooterComponent={() => renderFooter("une tâche ponctuelle")}
              />
            ) : (
              <View style={styles.emptyListContainer}>
                <Text>Pas de tâches ponctuelles</Text>
                {renderFooter("une tâche ponctuelle")}
              </View>
            )}

            <Text style={styles.heading}>Tâches</Text>
            {tasks.length > 0 ? (
              <FlatList
                data={tasks}
                renderItem={renderItem}
                keyExtractor={(item) => item.id.toString()}
                style={styles.tasksContainer}
                ListFooterComponent={() => renderFooter("une tâche")}
              />
            ) : (
              <View style={styles.emptyListContainer}>
                <Text>Pas de tâches</Text>
                {renderFooter("une tâche")}
              </View>
            )}
          </>
        ) : (
          <>
            <Text style={styles.heading}>Récompenses</Text>
            {rewards.length > 0 ? (
              <FlatList
                data={rewards}
                renderItem={renderItem}
                keyExtractor={(item) => item.id.toString()}
                style={styles.listContainer}
                ListFooterComponent={() => renderFooter("une récompense")}
              />
            ) : (
              <View style={styles.emptyListContainer}>
                <Text>Pas de récompenses</Text>
                {renderFooter("une récompense")}
              </View>
            )}
          </>
        )}

        <MenuItem name="Historique du manager" link={`/submanager/${submanagerId}/history`} />
        <MenuItem name="Statistiques des tâches" link={`/submanager/${submanagerId}/statistics`} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    alignItems: "stretch",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
    textAlign: "center",
  },
  heading: {
    fontSize: 20,
    fontWeight: "bold",
    marginTop: 30,
    marginBottom: 10,
  },
  progressText: {
    textAlign: "center",
    marginTop: 5,
  },
  listContainer: {
    marginTop: 10,
    backgroundColor: "#f0f0f0",
    borderRadius: 5,
  },
  tasksContainer: {
    marginTop: 10,
  },
  optionsContainer: {
    marginTop: 30,
    alignItems: "center",
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 10,
  },
  button: {
    backgroundColor: '#ddd',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  },
  activeButton: {
    backgroundColor: '#4CAF50',
  },
  buttonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  activeButtonText: {
    color: '#fff',
  },
  addButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
    alignSelf: 'center',
    marginTop: 10,
  },
  addButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  emptyListContainer: {
    marginTop: 10,
    padding: 10,
  }
});
