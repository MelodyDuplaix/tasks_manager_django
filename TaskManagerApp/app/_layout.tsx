import { Stack, useRouter } from "expo-router";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useEffect } from 'react';

export default function RootLayout() {
  const router = useRouter();

  useEffect(() => {
    const checkToken = async () => {
      try {
        const token = await AsyncStorage.getItem('authToken');
        if (token && typeof token === 'string') {
          try {
            JSON.parse(token);
            router.replace('/');
          } catch (parseError: any) {
            console.error('Error parsing token:', parseError);
            console.log('Token value:', token);
            router.replace('/login');
          }
        } else {
          console.log('Token is not a string or is null/undefined:', token);
          router.replace('/login');
        }
      } catch (error: any) {
        console.error('Error checking token:', error);
        console.log('Error details:', error.message, error.stack);
        router.replace('/login');
      }
    };

    checkToken();
  }, []);

  return (
    <Stack>
      <Stack.Screen name="login" options={{ headerShown: false }} />
      <Stack.Screen name="index" options={{ headerShown: false }} />
    </Stack>
  );
}
