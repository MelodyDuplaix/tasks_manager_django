import { Text, View, StyleSheet, ScrollView, FlatList, TouchableOpacity, Alert, Platform, SectionList, StyleProp, TextStyle } from "react-native";
import { useRouter, useLocalSearchParams } from 'expo-router';
import { useState, useEffect, useCallback } from 'react';
import NavigationBar from "@/components/NavigationBar";
import ProgressBar from "@/components/ProgressBar";
import MenuItem from "@/components/MenuItem";
import { fetchSubmanagerData, fetchTotalCoins, fetchSubmanagers } from "@/services/fetchApiInfos";
import { validateReward } from "@/services/rewardService";
import { deleteTask, markTaskDone } from "@/services/taskService";
import TaskItem, { TaskItemProps } from "@/components/TaskItem";
import FontAwesome6 from 'react-native-vector-icons/FontAwesome6';
import SubmanagerNavigation from "@/components/SubmanagerNavigation";
import { Dialog, Portal, Button } from 'react-native-paper';

// New component for tabbed punctual tasks
const PonctualTasksTabs = ({ tasks, onTaskDone, onDeleteTask, renderFooter }: { tasks: { [key: string]: TaskItemProps[] }; onTaskDone: (id: number, isPonctual: boolean) => void; onDeleteTask: (id: number, isPonctual: boolean) => void; renderFooter: (type: string) => JSX.Element }) => {
  const [selectedTab, setSelectedTab] = useState('pastToday');

  const footerElement = renderFooter("une tâche ponctuelle");

  return (
    <>
      <View style={styles.tabContainer}>
        <TouchableOpacity
          style={[styles.tabButton, selectedTab === 'pastToday' ? styles.activeTabButton : {}]}
          onPress={() => setSelectedTab('pastToday')}
        >
          <Text style={styles.tabButtonText}>Passées et Aujourd'hui</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tabButton, selectedTab === 'tomorrow' ? styles.activeTabButton : {}]}
          onPress={() => setSelectedTab('tomorrow')}
        >
          <Text style={styles.tabButtonText}>Demain</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tabButton, selectedTab === 'dayAfterTomorrow' ? styles.activeTabButton : {}]}
          onPress={() => setSelectedTab('dayAfterTomorrow')}
        >
          <Text style={styles.tabButtonText}>Après-demain</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tabButton, selectedTab === 'future' ? styles.activeTabButton : {}]}
          onPress={() => setSelectedTab('future')}
        >
          <Text style={styles.tabButtonText}>Futures</Text>
        </TouchableOpacity>
      </View>
      {tasks && tasks[selectedTab] && Array.isArray(tasks[selectedTab]) ? (
        tasks[selectedTab].length > 0 ? (
          <FlatList
            data={tasks[selectedTab]}
            renderItem={({ item }) => (
              <TaskItem
                {...item}
                isPonctual={true}
                onTaskDone={onTaskDone}
                onDeleteTask={onDeleteTask}
                done_today_count={0}
                style={item.date && new Date(item.date) < new Date() ? (new Date(item.date).getDate() === new Date().getDate() ? styles.pastDueTodayTaskText : styles.pastDueTaskText) : null}
              />
            )}
            keyExtractor={(item) => item.id.toString()}
            style={styles.listContainer}
            ListFooterComponent={footerElement} // Use the pre-rendered element
          />
        ) : (
          <View style={styles.emptyListContainer}>
            <Text>Pas de tâches ponctuelles</Text>
            {footerElement} {/* Use the pre-rendered element */}
          </View>
        )
      ) : (
        <View style={styles.emptyListContainer}>
          <Text>Erreur de chargement des tâches</Text>
          {footerElement} {/* Use the pre-rendered element */}
        </View>
      )}
    </>
  );
};


export default function SubmanagerPage() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const submanagerId = Number(id);
  const [submanagerName, setSubmanagerName] = useState<string>("Nom du sous-manager");
  const [dailyObjective, setDailyObjective] = useState<number>(50);
  const [totalCoinsToday, setTotalCoinsToday] = useState<number>(25);
  const [tasks, setTasks] = useState<any[]>([]);
  const [ponctualTasks, setPonctualTasks] = useState<TaskItemProps[]>([]);
  const [rewards, setRewards] = useState<any[]>([]);
  const [showTasks, setShowTasks] = useState(true);
  const [totalCoins, setTotalCoins] = useState<number>(100);
  const [submanagers, setSubmanagers] = useState<any[]>([]);
  const [deleteDialogVisible, setDeleteDialogVisible] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState<{id: number, isPonctual: boolean} | null>(null);

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

  const handleDeleteTask = async (taskId: number, isPonctual: boolean) => {
    setTaskToDelete({id: taskId, isPonctual});
    setDeleteDialogVisible(true);
  };
  
  const confirmDeleteTask = () => {
    if (taskToDelete) {
      deleteTask(taskToDelete.id, (deletedId) => {
        if (taskToDelete.isPonctual) {
          setPonctualTasks(prevTasks => prevTasks.filter(task => task.id !== deletedId));
        } else {
          setTasks(prevTasks => prevTasks.filter(task => task.id !== deletedId));
        }
        loadData();
      });
    }
    setDeleteDialogVisible(false);
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

  const categorizeTasksByDate = (tasks: TaskItemProps[]): { [key: string]: TaskItemProps[] } => {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    const dayAfterTomorrow = new Date(tomorrow);
    dayAfterTomorrow.setDate(tomorrow.getDate() + 1);
    const futureDate = new Date(dayAfterTomorrow);
    futureDate.setDate(futureDate.getDate()+1);

    return {
      pastToday: tasks.filter(task => task.date ? new Date(task.date) <= today : false),
      tomorrow: tasks.filter(task => task.date ? new Date(task.date).getTime() === tomorrow.getTime() : false),
      dayAfterTomorrow: tasks.filter(task => task.date ? new Date(task.date).getTime() === dayAfterTomorrow.getTime() : false),
      future: tasks.filter(task => task.date ? new Date(task.date) > dayAfterTomorrow : false),
    };
  };

  const categorizedPonctualTasks = categorizeTasksByDate(ponctualTasks);

  const renderFooter = (type: string) => {
    const route = type === 'une tâche ponctuelle' ? `/createPonctualTask?submanagerId=${submanagerId}` : type === 'une tâche' ? `/createTask?submanagerId=${submanagerId}` : `/createReward?id=${submanagerId}`;
    return (
      <TouchableOpacity style={styles.addButton} onPress={() => router.push(route as any)}>
        <Text style={styles.addButtonText}>Ajouter {type}</Text>
      </TouchableOpacity>
    );
  };
  

  return (
    <ScrollView>
      <View style={{ zIndex: 200 }}>
        <NavigationBar coins={totalCoins} />
      </View>
      <View style={styles.container}>
        <SubmanagerNavigation
          submanagers={submanagers}
          submanagerId={submanagerId}
          submanagerName={submanagerName}
        />
        <TouchableOpacity
          style={styles.decomposeButton}
          onPress={() => router.push(`/decomposeObjective?submanagerId=${submanagerId}`)}
        >
          <Text style={styles.decomposeButtonText}>Décomposer l'objectif</Text>
        </TouchableOpacity>

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
            <PonctualTasksTabs tasks={categorizedPonctualTasks} onTaskDone={handleTaskDone} onDeleteTask={handleDeleteTask} renderFooter={renderFooter} />
            <Text style={styles.heading}>Tâches</Text>
            {tasks.length > 0 ? (
              <FlatList
                data={tasks}
                renderItem={({ item }) => (
                  <View style={{ paddingHorizontal: 10 }}> {/* Added padding */}
                    <TaskItem
                      id={item.id}
                      name={item.name}
                      coins_number={item.coins_number}
                      type={item.type}
                      date={item.date}
                      isPonctual={false}
                      onTaskDone={handleTaskDone}
                      onDeleteTask={handleDeleteTask}
                      done_today_count={item.done_today_count}
                      isReward={false}
                      style={item.date && new Date(item.date) < new Date() ? styles.pastDueTaskText : null}
                    />
                  </View>
                )}
                keyExtractor={(item) => item.id.toString()}
                style={styles.tasksContainer}
                ListFooterComponent={() => renderFooter("une tâche")}
              />
            ) : (
              <View style={styles.emptyListContainer}>
                <Text>Pas de tâches</Text>
                {renderFooter("une tâche")}
                <TouchableOpacity
                  style={styles.decomposeButton}
                  onPress={() => router.push('/decomposeObjective')}
                >
                  <Text style={styles.decomposeButtonText}>Décomposer l'objectif</Text>
                </TouchableOpacity>
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
                    style={item.date && new Date(item.date) < new Date() ? styles.pastDueTaskText : null}
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
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 20,
    paddingHorizontal: 20,
    paddingBottom: 20,
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
  tabContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 10,
  },
  tabButton: {
    backgroundColor: '#ddd',
    paddingVertical: 5,
    paddingHorizontal: 10,
    borderRadius: 5,
    flex: 1,
  },
  activeTabButton: {
    backgroundColor: '#4CAF50',
  },
  tabButtonText: {
    color: '#333',
    textAlign: 'center',
  },
  pastDueTaskText: {
    color: 'red',
  },
  pastDueTodayTaskText: {
    color: 'orange',
  },
  decomposeButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
    marginTop: 20,
  },
  decomposeButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
