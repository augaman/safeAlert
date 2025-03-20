import { ALERT_STATUS, ALERT_TYPES, ROLES } from '../config/environment';

export interface User {
  id: string;
  email: string;
  name: string;
  role: typeof ROLES[keyof typeof ROLES];
  createdAt: string;
  updatedAt: string;
}

export interface Location {
  latitude: number;
  longitude: number;
  address?: string;
  timestamp: string;
}

export interface Alert {
  id: string;
  type: typeof ALERT_TYPES[keyof typeof ALERT_TYPES];
  status: typeof ALERT_STATUS[keyof typeof ALERT_STATUS];
  clientId: string;
  clientName: string;
  location: Location;
  details?: Record<string, any>;
  assignedTo?: string;
  assignedTeam?: string;
  createdAt: string;
  updatedAt: string;
  resolvedAt?: string;
}

export interface InterventionTeam {
  id: string;
  name: string;
  members: string[];
  status: 'available' | 'busy' | 'offline';
  currentLocation?: Location;
  createdAt: string;
  updatedAt: string;
}

export interface PaginationParams {
  page: number;
  pageSize: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface AlertFilters {
  type?: typeof ALERT_TYPES[keyof typeof ALERT_TYPES];
  status?: typeof ALERT_STATUS[keyof typeof ALERT_STATUS];
  startDate?: string;
  endDate?: string;
  assignedTo?: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface AlertState {
  alerts: Alert[];
  selectedAlert: Alert | null;
  filters: AlertFilters;
  pagination: PaginationParams;
  total: number;
  isLoading: boolean;
  error: string | null;
}

export interface RootState {
  auth: AuthState;
  alerts: AlertState;
} 