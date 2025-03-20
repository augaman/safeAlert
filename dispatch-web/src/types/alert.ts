export type AlertStatus = 'pending' | 'active' | 'resolved' | 'cancelled';
export type AlertPriority = 'low' | 'medium' | 'high' | 'critical';

export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  teamId?: string;
  notifications?: {
    email: boolean;
    push: boolean;
    sms: boolean;
  };
  theme?: 'light' | 'dark';
  language?: string;
}

export interface Team {
  id: string;
  name: string;
  description: string;
  members: User[];
}

export interface Alert {
  id: string;
  title: string;
  description: string;
  status: AlertStatus;
  priority: AlertPriority;
  location: {
    latitude: number;
    longitude: number;
    address?: string;
  };
  createdAt: string;
  updatedAt: string;
  createdBy: User;
  assignedTo?: Team;
  resolvedBy?: User;
  resolvedAt?: string;
  attachments?: string[];
  comments?: AlertComment[];
}

export interface AlertComment {
  id: string;
  content: string;
  createdAt: string;
  createdBy: User;
}

export interface ReportData {
  totalAlerts: number;
  activeAlerts: number;
  resolvedAlerts: number;
  averageResponseTime: number;
  alertsByStatus: {
    status: string;
    count: number;
  }[];
  alertsByPriority: {
    priority: string;
    count: number;
  }[];
  alertsByTeam: {
    teamName: string;
    count: number;
  }[];
}

export interface ReportParams {
  startDate: string;
  endDate: string;
  type: 'daily' | 'weekly' | 'monthly';
}

export interface UserSettings {
  name: string;
  email: string;
  notifications: {
    email: boolean;
    push: boolean;
    sms: boolean;
  };
  theme: 'light' | 'dark';
  language: string;
} 