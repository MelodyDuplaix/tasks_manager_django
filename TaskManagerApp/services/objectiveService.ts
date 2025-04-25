import { fetchQuery, getToken } from './authentification';

export const decomposeObjective = async (objective: string, nb_tasks: number = 7): Promise<any> => {
  try {
    const token = await getToken();
    if (!token) {
      throw new Error('No token found');
    }

    const response = await fetchQuery(token, 'objectif/decompose', true, 'POST', {
      objectif: objective,
      nb_tasks: nb_tasks
    });

    return response;
  } catch (error: any) {
    console.error('Error decomposing objective:', error);
    throw error;
  }
};

export const saveTasks = async (submanagerId: number, tasks: any[]): Promise<any> => {
  try {
    const token = await getToken();
    if (!token) {
      throw new Error('No token found');
    }

    const response = await fetchQuery(token, `submanager/${submanagerId}/add_tasks`, true, 'POST', {
      tasks: tasks
    });

    return response;
  } catch (error: any) {
    console.error('Error saving tasks:', error);
    throw error;
  }
};
