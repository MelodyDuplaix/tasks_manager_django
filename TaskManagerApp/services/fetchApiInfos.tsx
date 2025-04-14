import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { router } from 'expo-router';
import { fetchQuery, getToken } from './authentification';

export const fetchCoinsNumber = async (): Promise<[number, number] | undefined> =>  {
    const token = await getToken();
    if (!token) {
        router.replace('/login');
        return;
    }
    const response = await fetchQuery(token, 'user/daily_coins', true);
    if (response) {
        return [response.total_coins_today, response.total_daily_objectif];
    } else {
        return [0, 0];
    }
}

export const fetchTotalCoins = async (): Promise<number | undefined> => {
    const token = await getToken();
    if (!token) {
        router.replace('/login');
        return;
    }
    const response = await fetchQuery(token, 'user/total_coins', true);
    if (response) {
        return response.total_coins;
    } else {
        return 0;
    }
}