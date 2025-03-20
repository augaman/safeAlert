import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import * as SecureStore from 'expo-secure-store';
import { API_CONFIG, AUTH_CONFIG } from '../constants/config';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_CONFIG.BASE_URL,
      timeout: API_CONFIG.TIMEOUT,
      headers: API_CONFIG.HEADERS,
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.api.interceptors.request.use(
      async (config) => {
        const token = await SecureStore.getItemAsync(AUTH_CONFIG.TOKEN_KEY);
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        // Handle token refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          try {
            const refreshToken = await SecureStore.getItemAsync(AUTH_CONFIG.REFRESH_TOKEN_KEY);
            const response = await this.refreshToken(refreshToken);
            const { token } = response.data;
            await SecureStore.setItemAsync(AUTH_CONFIG.TOKEN_KEY, token);
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return this.api(originalRequest);
          } catch (refreshError) {
            // Handle refresh token failure
            await this.handleAuthError();
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  private async refreshToken(refreshToken: string | null): Promise<AxiosResponse> {
    return this.api.post('/auth/refresh', { refreshToken });
  }

  private async handleAuthError(): Promise<void> {
    await SecureStore.deleteItemAsync(AUTH_CONFIG.TOKEN_KEY);
    await SecureStore.deleteItemAsync(AUTH_CONFIG.REFRESH_TOKEN_KEY);
    // Navigate to login screen or handle auth error
  }

  // Generic request methods
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.api.delete<T>(url, config);
    return response.data;
  }

  // Auth methods
  async login(email: string, password: string): Promise<any> {
    return this.post('/auth/login', { email, password });
  }

  async register(userData: any): Promise<any> {
    return this.post('/auth/register', userData);
  }

  async logout(): Promise<void> {
    await SecureStore.deleteItemAsync(AUTH_CONFIG.TOKEN_KEY);
    await SecureStore.deleteItemAsync(AUTH_CONFIG.REFRESH_TOKEN_KEY);
  }

  // Alert methods
  async sendPanicAlert(location: any): Promise<any> {
    return this.post('/alerts/panic', { location });
  }

  async sendMedicalAlert(location: any, details: any): Promise<any> {
    return this.post('/alerts/medical', { location, details });
  }

  async getAlertHistory(): Promise<any> {
    return this.get('/alerts/history');
  }

  // Home Security methods
  async getHomeSecurityStatus(): Promise<any> {
    return this.get('/security/home/status');
  }

  async updateHomeSecurityStatus(status: string): Promise<any> {
    return this.put('/security/home/status', { status });
  }

  // CarSafe methods
  async getCarStatus(): Promise<any> {
    return this.get('/security/car/status');
  }

  async reportCarTheft(location: any): Promise<any> {
    return this.post('/security/car/theft', { location });
  }
}

export const apiService = new ApiService(); 