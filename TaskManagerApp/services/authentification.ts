import AsyncStorage from '@react-native-async-storage/async-storage';

export const TMDB_CONFIG = {
    BASE_URL: 'https://api.themoviedb.org/3',
    API_KEY: process.env.EXPO_PUBLIC_MOVIE_API_KEY,
    headers: {
        accept: 'application/json',
        Authorization: `Bearer ${process.env.EXPO_PUBLIC_MOVIE_API_KEY}`,
    }
}

export const fetchQuery = async (token: string, query: string, useBearer: boolean = true, method: string = 'GET', body: any = null) => {
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
        const response = await fetch(`http://127.0.0.1:8000/api/${query}/`, fetchOptions);
        if (response.ok) {
          const data = await response.json();
          return data;
        } else if (response.status === 401) {
            console.error('Token is invalid:', response.status);
        } else {
          console.error('Failed to fetch submanagers:', response.status);
        }
      } catch (error) {
        console.error('Error fetching submanagers:', error);
      }
}


export const getToken = async () => {
  return await AsyncStorage.getItem('accessToken');
};

export const verifyToken = async (parsedToken: string) => {
  return await fetchQuery(parsedToken, 'token/verify', false, 'POST', { token: parsedToken });
};

export const refreshToken = async () => {
  try {
    const refreshTokenValue = await AsyncStorage.getItem('refreshToken');
    if (refreshTokenValue) {
      const refreshResponse = await fetchQuery(JSON.parse(refreshTokenValue), 'login/refresh', false, 'POST', { refresh: JSON.parse(refreshTokenValue) });
      if (refreshResponse.access) {
        const newAccessToken = refreshResponse.access;
        await AsyncStorage.setItem('accessToken', JSON.stringify(newAccessToken));
        return newAccessToken;
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
