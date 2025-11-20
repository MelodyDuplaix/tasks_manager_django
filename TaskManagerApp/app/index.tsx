import { Text, View, Button, StyleSheet, FlatList, ViewBase } from "react-native";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';
import { useState, useEffect } from 'react';
import FontAwesome6 from '@expo/vector-icons/FontAwesome6';
import { getToken, verifyToken, fetchSubmanagersData, refreshToken, fetchUserId } from "@/services/authentification";
import { fetchCoinsNumber, fetchTotalCoins } from "@/services/fetchApiInfos";
import MenuItem from "@/components/MenuItem";
import NavigationBar from "@/components/NavigationBar";
import ProgressBar from "@/components/ProgressBar";

interface SubManager {
  id: number;
  name: string;
  daily_objectif: number;
  yearly_objectif: number;
  active: boolean;
}

export default function Index() {
  const router = useRouter();
  const [submanagers, setSubmanagers] = useState<SubManager[]>([]);
  const [userId, setUserId] = useState<number | null>(null);
  const [coins, setCoins] = useState<number>(0);
  const [dailyObjective, setDailyObjective] = useState<number>(0);
  const [totalCoins, setTotalCoins] = useState<number>(0);

  useEffect(() => {
    const fetchSubmanagers = async () => {
      const token = await getToken();
      if (token) {
        try {
          let parsedToken = token;
          const verificationResponse = await verifyToken(parsedToken);

          if (verificationResponse && verificationResponse.detail === 'Invalid token.') {
            const newAccessToken = await refreshToken();
            if (newAccessToken) {
              parsedToken = newAccessToken;
            } else {
              router.replace('/login');
              return;
            }
          }

          const username = await fetchUserId(parsedToken);
          setUserId(username);

          const response = await fetchSubmanagersData(parsedToken);
          setSubmanagers(response);
        } catch (error) {
          console.error("Token verification or submanager fetch failed:", error);
          router.replace('/login');
        }
      } else {
        router.replace('/login');
      }
    };

    const fetchDailyCoins = async () => {
      try {
        const coinsData = await fetchCoinsNumber();
        if (coinsData) {
          const [coinsNumber, dailyObj] = coinsData;
          setCoins(coinsNumber || 0);
          setDailyObjective(dailyObj || 0);
        } else {
          setCoins(0);
          setDailyObjective(0);
        }
      } catch (error) {
        console.error("Token verification or submanager fetch failed:", error);
        router.replace('/login');
      }
    };

    const fetchCoins = async () => {
      try {
        const totalCoins = await fetchTotalCoins();
        setTotalCoins(totalCoins || 0);
      } catch (error) {
        console.error("Token verification or submanager fetch failed:", error);
        router.replace('/login');
      }
    };

    fetchSubmanagers();
    fetchDailyCoins();
    fetchCoins();
  }, []);

  return (
      <View style={{ flex: 1 }}>
      <View style={{zIndex: 10 }}>
        <NavigationBar coins={totalCoins} />
      </View>
      <View style={styles.container}>
          <Text style={styles.welcome}>Bienvenue <Text style={styles.name}>{userId}</Text></Text>
          <ProgressBar current={coins} total={dailyObjective} />
          <Text style={{ fontSize: 20, fontWeight: 'bold' }}>Objectifs</Text>
          <MenuItem name="Objectif hebdomadaire" link="/weekly" />
          <MenuItem name="Objectif mensuel" link="/monthly" />
          <MenuItem name="Objectif annuel" link="/yearly" />
      <FlatList
        data={submanagers}
        renderItem={({ item }) => (
          <MenuItem name={item.name} link={`/submanager/${item.id}`}/>
        )}
        keyExtractor={item => item.id.toString()}
        ListHeaderComponent={() => 
        <View style={{ justifyContent: "flex-start"}}>
          <Text style={{ fontSize: 20, fontWeight: 'bold' }}>Liste des sous-managers</Text>
        </View>}
        ListEmptyComponent={() => <Text>No submanagers found.</Text>}
        contentContainerStyle={styles.flatlist}
      />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "flex-start",
    alignItems: "stretch",
    padding: 20,
    width: '100%',
  },
  submanagerItem: {
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  name: {
    fontStyle: 'italic',
  },
  coins: {
    flexDirection: 'row',
    gap: 5,
    justifyContent: "flex-end"
  },
  flatlist: {
    justifyContent: "flex-start",
    alignItems: "stretch",
    zIndex: 1,
  },
  welcome: {
    marginBottom: 10,
    textAlign: 'center',
    fontSize: 20,
  }
});
