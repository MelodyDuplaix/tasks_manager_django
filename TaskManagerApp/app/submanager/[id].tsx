import { Text, View, StyleSheet, ScrollView, FlatList, TouchableOpacity } from "react-native";
import { useRouter, useLocalSearchParams } from 'expo-router';
import { useState, useEffect, useCallback } from 'react';
import NavigationBar from "@/components/NavigationBar";
import ProgressBar from "@/components/ProgressBar";
import MenuItem from "@/components/MenuItem";
import { fetchSubmanagerData, fetchTotalCoins, fetchSubmanagers } from "@/services/fetchApiInfos";
import { validateReward } from "@/services/rewardService";
import { markTaskDone } from "@/services/taskService";
import TaskItem from "@/components/TaskItem";
import FontAwesome6 from 'react-native-vector-icons/FontAwesome6';
import SubmanagerNavigation from "@/components/SubmanagerNavigation";

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
  const [submanagers, setSubmanagers] = useState<any[]>([]);

  const loadData = useCallback(async () => {
    const data = await fetchSubmanagerData(submanagerId);
    if (data) {
      setTasks(data.tasks);
      setPonctualTasks(data.ponctual_tasks);
      setRewards(data.rewards);
      setDailyObjective(data.daily_objective);
      setTotalCoinsToday(data.daily_coins);
      setSubmanagerName(data.submanager.name);
    }
  }, [submanagerId]);

  const loadTotalCoins = useCallback(async () => {
    try {
      const coins = await fetchTotalCoins(submanagerId);
      if (coins) {
        setTotalCoins(coins);
      } else if (coins === 0) {
        setTotalCoins(0);
      }
    } catch (error) {
      console.error("Failed to fetch total coins:", error);
    }
  }, []);

  const loadSubmanagers = useCallback(async () => {
    try {
      const submanagersData = await fetchSubmanagers();
      if (submanagersData) {
        setSubmanagers(submanagersData);
      }
    } catch (error) {
      console.error("Failed to fetch submanagers:", error);
    }
  }, []);

  useEffect(() => {
    loadData();
    loadTotalCoins();
    loadSubmanagers();
  }, [loadData, loadTotalCoins, loadSubmanagers]);

  const getPreviousSubmanager = () => {
    const currentIndex = submanagers.findIndex(sm => sm.id === submanagerId);
    if (currentIndex > 0) {
      return submanagers[currentIndex - 1];
    } else if (submanagers.length > 1) {
      return submanagers[submanagers.length - 1];
    }
    return null;
  };

  const getNextSubmanager = () => {
    const currentIndex = submanagers.findIndex(sm => sm.id === submanagerId);
    if (currentIndex < submanagers.length - 1) {
      return submanagers[currentIndex + 1];
    } else if (submanagers.length > 1) {
      return submanagers[0];
    }
    return null;
  };


  const handleTaskDone = async (taskId: number, isPonctual: boolean) => {
    await markTaskDone(taskId, isPonctual, () => {
      if (isPonctual) {
        setPonctualTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
      }
    });
    await loadData();
    await loadTotalCoins();
  };

  const handleRewardValidated = async (rewardId: number) => {
    const reward = rewards.find(reward => reward.id === rewardId);
    if (reward) {
      await loadData();
      await loadTotalCoins();
    }
  };

  const renderPonctualTaskItem = ({ item }: { item: any }) => (
    <TaskItem
      id={item.id}
      name={item.name}
      coins_number={item.coins_number}
      type={item.type}
      date={item.date}
      isPonctual={true}
      onTaskDone={handleTaskDone}
      done_today_count={0}
    />
  );

  const renderFooter = (type: string) => {
    const route = type === 'une tâche ponctuelle' ? `/createPonctualTask?submanagerId=${submanagerId}` : type === 'une tâche' ? `/createTask?submanagerId=${submanagerId}` : '/createReward';
    return (
      <TouchableOpacity style={styles.addButton} onPress={() => router.push(route as any)}>
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
        <SubmanagerNavigation
          submanagers={submanagers}
          submanagerId={submanagerId}
          submanagerName={submanagerName}
        />

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
                renderItem={({ item }) => renderPonctualTaskItem({ item })}
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
                renderItem={({ item }) => (
                  <TaskItem
                    id={item.id}
                    name={item.name}
                    coins_number={item.coins_number}
                    type={item.type}
                    date={item.date}
                    isPonctual={false}
                    onTaskDone={handleTaskDone}
                    done_today_count={item.done_today_count}
                    isReward={false}
                  />
                )}
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
                renderItem={({ item }) => (
                  <TaskItem
                    id={item.id}
                    name={item.name}
                    coins_number={item.coins_number}
                    type={item.type}
                    date={item.date}
                    onTaskDone={() => validateReward(item.id, handleRewardValidated)}
                    done_today_count={0}
                    isReward={true}
                  />
                )}
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
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  navButton: {
    backgroundColor: '#ddd',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  },
  navButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
});
