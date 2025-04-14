import { Stack, useRouter, usePathname } from "expo-router";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useEffect, useState } from 'react';
import { getToken, verifyToken, refreshToken, fetchUserId } from "@/services/authentification";
import { PaperProvider } from 'react-native-paper';

export default function RootLayout() {
  const router = useRouter();
  const pathname = usePathname();
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    const checkToken = async () => {
      try {
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
                if (pathname !== '/login') {
                  router.replace('/login');
                }
                return;
              }
            }

            const username = await fetchUserId(parsedToken);
            setUserId(username);
          } catch (error) {
            console.error('Error checking token:', error);
            if (pathname !== '/login') {
              router.replace('/login');
            }
          }
        } else {
          if (pathname !== '/login') {
            router.replace('/login');
          }
        }
      } catch (error: any) {
        console.error('Error checking token:', error);
        if (pathname !== '/login') {
          router.replace('/login');
        }
      }
    };

    if (!userId) {
      checkToken();
    }
  }, [pathname, userId]);

  return (
    <PaperProvider>
      <Stack>
        <Stack.Screen name="login" options={{ headerShown: false }} />
        <Stack.Screen name="index" options={{ headerShown: false }} />
        <Stack.Screen name="submanager/[id]" options={{ headerShown: false }} />
      </Stack>
    </PaperProvider>
  );
}
