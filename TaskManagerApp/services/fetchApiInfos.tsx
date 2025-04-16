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

export const fetchTotalCoins = async (submanager_id?: number | null): Promise<number | undefined> => {    const token = await getToken();
    if (!token) {
        router.replace('/login');
        return;
    }
    const response = await fetchQuery(token, `user/total_coins${submanager_id ? `/${submanager_id}`: ""}`, true);
    if (response) {
        return response.total_coins;
    } else {
        return 0;
    }
}

export const fetchSubmanagerData = async (submanagerId: number): Promise<any | undefined> => {
    const token = await getToken();
    if (!token) {
        router.replace('/login');
        return;
    }
    const response = await fetchQuery(token, `submanager/${submanagerId}/data`, true);
    return response;
}
