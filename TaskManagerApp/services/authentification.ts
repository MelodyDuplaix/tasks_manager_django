import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { router } from 'expo-router';

export const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:8000/api',
}

export const fetchQuery = async (
          token: string, 
          query: string, 
          useBearer: boolean = true, 
          method: string = 'GET',
          body: any = null
        ): Promise<any> => {
    const headers = {
        'Authorization': `${useBearer ? 'Bearer ' : ''}${token}`,
        'Content-Type': 'application/json',
    };
    const fetchOptions: RequestInit = {
        method: method,
        headers: headers,
    };

    if (body) {
        fetchOptions.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/${query}/`, fetchOptions);
        if (response.ok) {
          const data = await response.json();
          return data;
        } else if (response.status === 401) {
            console.error('Token is invalid:', response.status);
        } else {
          console.error('Failed to fetch query:', response.status);
        }
      } catch (error: any) {
        if (error instanceof SyntaxError) {
          console.error('JSON parsing error:', error);
        } else {
          console.error('Error fetching query:', error);
        }
      }
}


export const getToken = async () => {
  const token = await AsyncStorage.getItem('accessToken');
  return token ? JSON.parse(token as string) : null;
};

export const verifyToken = async (parsedToken: string) => {
  return await fetchQuery(parsedToken, 'token/verify', false, 'POST', { token: parsedToken });
};

export const refreshToken = async () => {
  try {
    const refreshTokenValue = await AsyncStorage.getItem('refreshToken');
    if (refreshTokenValue) {
      const refreshResponse = await fetchQuery(refreshTokenValue, 'login/refresh', false, 'POST', { refresh: refreshTokenValue });
      if (refreshResponse.access) {
        const newAccessToken = refreshResponse.access;
        await AsyncStorage.setItem('accessToken', JSON.stringify(newAccessToken));
        return newAccessToken
      } else {
        console.error("Token refresh failed");
        await AsyncStorage.removeItem('accessToken');
        await AsyncStorage.removeItem('refreshToken');
        return null;
      }
    } else {
      console.error("No refresh token found");
      await AsyncStorage.removeItem('accessToken');
      return null;
    }
  } catch (e) {
    console.error("Error during token refresh", e);
    await AsyncStorage.removeItem('accessToken');
    return null;
  }
};

export const fetchUserId = async (parsedToken: string) => {
  const userIdResponse = await fetchQuery(parsedToken, 'user/id');
  return userIdResponse.username;
};

export const fetchSubmanagersData = async (parsedToken: string) => {
  return await fetchQuery(parsedToken, 'submanagers');
};

export const fetchToken = async (username: string, password: string) => {
  const response = await axios.post(`${API_CONFIG.BASE_URL}/login/`, {
    username: username,
    password: password
  });
  try {
    if (response.status === 200) {
      const { access, refresh } = response.data;
      await AsyncStorage.setItem('accessToken', JSON.stringify(access as string));
      await AsyncStorage.setItem('refreshToken', JSON.stringify(refresh as string));
      router.replace('/');
      return null;
    } else if (response.status === 401) {
      return 'Mauvais identifiants';
    } else {
      console.log(response.status);
      return 'Erreur de connexion';
    }
  } catch (error: any) {
    if (error.response?.status === 401) {
      return 'Mauvais identifiants';
    } else {
      return 'Erreur de connexion';
    }
  }
}
