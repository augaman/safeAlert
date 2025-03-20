import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Alert, AlertFilters, Location, LoginCredentials, StatusUpdate, Team, User } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await AsyncStorage.removeItem('token');
      // Handle unauthorized access (e.g., redirect to login)
    }
    return Promise.reject(error);
  }
);

class ApiService {
  // Auth methods
  async login(email: string, password: string): Promise<{ user: User; token: string }> {
    const response = await api.post('/auth/login', { email, password });
    await AsyncStorage.setItem('token', response.data.token);
    return response.data;
  }

  async logout(): Promise<void> {
    await AsyncStorage.removeItem('token');
  }

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/auth/me');
    return response.data;
  }

  // Alert methods
  async getAlerts(filters?: AlertFilters): Promise<Alert[]> {
    const response = await api.get('/alerts', { params: filters });
    return response.data;
  }

  async getAlertById(id: string): Promise<Alert> {
    const response = await api.get(`/alerts/${id}`);
    return response.data;
  }

  async updateAlertStatus(update: StatusUpdate): Promise<Alert> {
    const response = await api.post(`/alerts/${update.alertId}/status`, update);
    return response.data;
  }

  // Team methods
  async getTeams(): Promise<Team[]> {
    const response = await api.get('/teams');
    return response.data;
  }

  async getTeamById(id: string): Promise<Team> {
    const response = await api.get(`/teams/${id}`);
    return response.data;
  }

  async updateTeamLocation(teamId: string, location: { latitude: number; longitude: number }): Promise<Team> {
    const response = await api.put(`/teams/${teamId}/location`, location);
    return response.data;
  }

  // User methods
  async createUser(userData: Omit<User, 'id'>): Promise<User> {
    const response = await api.post('/users', userData);
    return response.data;
  }

  async updateUser(id: string, userData: Partial<User>): Promise<User> {
    const response = await api.put(`/users/${id}`, userData);
    return response.data;
  }

  async deleteUser(id: string): Promise<void> {
    await api.delete(`/users/${id}`);
  }

  async updateUserSettings(userId: string, settings: { deviceToken?: string }): Promise<User> {
    const response = await api.put(`/users/${userId}/settings`, settings);
    return response.data;
  }
}

export const apiService = new ApiService(); 