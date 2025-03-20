import { io, Socket } from 'socket.io-client';
import { API_CONFIG } from '../config/environment';
import { Alert, Team } from '../types';

class WebSocketService {
  private socket: Socket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout = 1000;

  constructor() {
    this.connect();
  }

  private connect() {
    const token = localStorage.getItem('token');
    if (!token) return;

    this.socket = io(API_CONFIG.WS_URL, {
      auth: { token },
      reconnection: true,
      reconnectionAttempts: this.maxReconnectAttempts,
      reconnectionDelay: this.reconnectTimeout,
    });

    this.setupEventListeners();
  }

  private setupEventListeners() {
    if (!this.socket) return;

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    this.socket.on('reconnect_attempt', (attemptNumber) => {
      console.log(`WebSocket reconnection attempt ${attemptNumber}`);
      this.reconnectAttempts = attemptNumber;
    });

    this.socket.on('reconnect_failed', () => {
      console.error('WebSocket reconnection failed');
    });
  }

  public disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  public isConnected(): boolean {
    return this.socket?.connected || false;
  }

  public emit(event: string, data?: any) {
    if (!this.socket) {
      console.error('WebSocket not connected');
      return;
    }
    this.socket.emit(event, data);
  }

  public on(event: string, callback: (data: any) => void) {
    if (!this.socket) {
      console.error('WebSocket not connected');
      return;
    }
    this.socket.on(event, callback);
  }

  public off(event: string, callback?: (data: any) => void) {
    if (!this.socket) {
      console.error('WebSocket not connected');
      return;
    }
    if (callback) {
      this.socket.off(event, callback);
    } else {
      this.socket.off(event);
    }
  }

  // Alert events
  public subscribeToAlerts(callback: (alert: Alert) => void) {
    this.on('alert:created', callback);
    this.on('alert:updated', callback);
    this.on('alert:deleted', callback);
  }

  public unsubscribeFromAlerts(callback: (alert: Alert) => void) {
    this.off('alert:created', callback);
    this.off('alert:updated', callback);
    this.off('alert:deleted', callback);
  }

  // Team events
  public subscribeToTeamStatus(callback: (team: Team) => void) {
    this.on('team:status', callback);
  }

  public unsubscribeFromTeamStatus(callback: (team: Team) => void) {
    this.off('team:status', callback);
  }

  // Location events
  public subscribeToLocationUpdates(callback: (data: { teamId: string; location: { latitude: number; longitude: number } }) => void) {
    this.on('location:update', callback);
  }

  public unsubscribeFromLocationUpdates(callback: (data: { teamId: string; location: { latitude: number; longitude: number } }) => void) {
    this.off('location:update', callback);
  }
}

export const websocketService = new WebSocketService(); 