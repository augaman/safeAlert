import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { API_CONFIG, AUTH_CONFIG } from '../config/environment';
import { Alert, AlertFilters, InterventionTeam, PaginatedResponse, User, Team, ReportData, ReportParams, UserSettings } from '../types';

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
        const token = localStorage.getItem(AUTH_CONFIG.TOKEN_KEY);
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
            const refreshToken = localStorage.getItem(AUTH_CONFIG.REFRESH_TOKEN_KEY);
            const response = await this.refreshToken(refreshToken);
            const { token } = response.data;
            localStorage.setItem(AUTH_CONFIG.TOKEN_KEY, token);
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
    localStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
    localStorage.removeItem(AUTH_CONFIG.REFRESH_TOKEN_KEY);
    window.location.href = '/login';
  }

  // Auth methods
  async login(email: string, password: string): Promise<{ user: User; token: string; refreshToken: string }> {
    const response = await this.api.post('/auth/login', { email, password });
    const { user, token, refreshToken } = response.data;
    localStorage.setItem(AUTH_CONFIG.TOKEN_KEY, token);
    localStorage.setItem(AUTH_CONFIG.REFRESH_TOKEN_KEY, refreshToken);
    return response.data;
  }

  async logout(): Promise<void> {
    await this.api.post('/auth/logout');
    localStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
    localStorage.removeItem(AUTH_CONFIG.REFRESH_TOKEN_KEY);
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.api.get('/auth/me');
    return response.data;
  }

  // Alert methods
  async getAlerts(
    page: number,
    pageSize: number,
    filters?: AlertFilters
  ): Promise<PaginatedResponse<Alert>> {
    const response = await this.api.get('/alerts', {
      params: { page, pageSize, ...filters },
    });
    return response.data;
  }

  async getAlertById(id: string): Promise<Alert> {
    const response = await this.api.get(`/alerts/${id}`);
    return response.data;
  }

  async updateAlertStatus(id: string, status: string): Promise<Alert> {
    const response = await this.api.patch(`/alerts/${id}/status`, { status });
    return response.data;
  }

  async assignAlert(id: string, teamId: string): Promise<Alert> {
    const response = await this.api.post(`/alerts/${id}/assign`, { teamId });
    return response.data;
  }

  // Intervention Team methods
  async getTeams(): Promise<InterventionTeam[]> {
    const response = await this.api.get('/teams');
    return response.data;
  }

  async getTeamById(id: string): Promise<InterventionTeam> {
    const response = await this.api.get(`/teams/${id}`);
    return response.data;
  }

  async updateTeamStatus(id: string, status: string): Promise<InterventionTeam> {
    const response = await this.api.patch(`/teams/${id}/status`, { status });
    return response.data;
  }

  // User management methods (Admin only)
  async getUsers(page: number, pageSize: number): Promise<PaginatedResponse<User>> {
    const response = await this.api.get('/users', { params: { page, pageSize } });
    return response.data;
  }

  async createUser(userData: Partial<User>): Promise<User> {
    const response = await this.api.post('/users', userData);
    return response.data;
  }

  async updateUser(id: string, userData: Partial<User>): Promise<User> {
    const response = await this.api.put(`/users/${id}`, userData);
    return response.data;
  }

  async deleteUser(id: string): Promise<void> {
    await this.api.delete(`/users/${id}`);
  }

  // Teams
  async getTeams(): Promise<Team[]> {
    const response = await this.api.get('/teams');
    return response.data;
  }

  async getTeam(id: string): Promise<Team> {
    const response = await this.api.get(`/teams/${id}`);
    return response.data;
  }

  async createTeam(data: Partial<Team>): Promise<Team> {
    const response = await this.api.post('/teams', data);
    return response.data;
  }

  async updateTeam(id: string, data: Partial<Team>): Promise<Team> {
    const response = await this.api.put(`/teams/${id}`, data);
    return response.data;
  }

  async deleteTeam(id: string): Promise<void> {
    await this.api.delete(`/teams/${id}`);
  }

  // Reports
  async getReportData(params: ReportParams): Promise<ReportData> {
    const response = await this.api.get('/reports', { params });
    return response.data;
  }

  // User Settings
  async updateUserSettings(settings: UserSettings): Promise<User> {
    const response = await this.api.put('/users/settings', settings);
    return response.data;
  }
}

export const apiService = new ApiService(); 