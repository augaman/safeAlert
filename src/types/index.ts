export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'dispatcher' | 'team_member';
  teamId?: string;
  phoneNumber?: string;
  deviceToken?: string;
}

export interface Location {
  latitude: number;
  longitude: number;
  timestamp: string;
}

export interface Alert {
  id: string;
  type: 'fire' | 'flood' | 'earthquake' | 'other';
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'pending' | 'assigned' | 'in_progress' | 'resolved' | 'cancelled';
  location: {
    latitude: number;
    longitude: number;
    address: string;
  };
  description: string;
  createdAt: string;
  updatedAt: string;
  assignedTeamId?: string;
  assignedTeam?: Team;
  reporterId: string;
  reporter?: User;
  updates: StatusUpdate[];
}

export interface Team {
  id: string;
  name: string;
  members: User[];
  status: 'available' | 'busy' | 'offline';
  currentLocation?: {
    latitude: number;
    longitude: number;
    timestamp: string;
  };
}

export interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

export interface AlertState {
  alerts: Alert[];
  selectedAlert: Alert | null;
  loading: boolean;
  error: string | null;
}

export interface LocationState {
  currentLocation: Location | null;
  isTracking: boolean;
  error: string | null;
}

export interface RootState {
  auth: AuthState;
  alerts: AlertState;
  location: LocationState;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AlertFilters {
  type?: Alert['type'];
  severity?: Alert['severity'];
  status?: Alert['status'];
  startDate?: string;
  endDate?: string;
  teamId?: string;
}

export interface StatusUpdate {
  id: string;
  alertId: string;
  teamId: string;
  status: Alert['status'];
  message: string;
  timestamp: string;
  location?: {
    latitude: number;
    longitude: number;
  };
} 