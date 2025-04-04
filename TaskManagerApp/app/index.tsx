import { Text, View, Button, StyleSheet, FlatList } from "react-native";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';
import { useState, useEffect } from 'react';
import { getToken, verifyToken, fetchSubmanagersData, refreshToken, fetchUserId } from "@/services/authentification";
import MenuItem from "@/components/MenuItem";

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

  useEffect(() => {
    const fetchSubmanagers = async () => {
      const token = await getToken();
      if (token) {
        try {
          let parsedToken = JSON.parse(token);
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

    fetchSubmanagers();
  }, []);

  const handleLogout = async () => {
    await AsyncStorage.removeItem('accessToken');
    router.replace('/login');
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={submanagers}
        renderItem={({ item }) => (
          <MenuItem name={item.name} link={`/submanager/${item.id}`} />
        )}
        keyExtractor={item => item.id.toString()}
        ListHeaderComponent={() => 
        <View>
          <Text style={styles.name}>Bienvenue {userId}</Text>
          <Text style={{ fontSize: 20, fontWeight: 'bold' }}>Objectifs</Text>
          <MenuItem name="Objectif hebdomadaire" link="/weekly" />
          <MenuItem name="Objectif mensuel" link="/monthly" />
          <MenuItem name="Objectif annuel" link="/yearly" />
          <Text style={{ fontSize: 20, fontWeight: 'bold' }}>Liste des sous-managers</Text>
        </View>}
        ListEmptyComponent={() => <Text>No submanagers found.</Text>}
      />
      <Button title="Logout" onPress={handleLogout} />
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
    marginBottom: 10,
    textAlign: 'center',
  }
});
