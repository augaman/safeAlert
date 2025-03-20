import { io, Socket } from 'socket.io-client';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Alert, Team } from '../types';

const WEBSOCKET_URL = process.env.REACT_APP_WEBSOCKET_URL || 'http://localhost:3001';

class WebSocketService {
  private socket: Socket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout = 1000;

  constructor() {
    this.connect();
  }

  private async connect() {
    try {
      const token = await AsyncStorage.getItem('token');
      if (!token) {
        console.error('No authentication token found');
        return;
      }

      this.socket = io(WEBSOCKET_URL, {
        auth: { token },
        reconnection: true,
        reconnectionAttempts: this.maxReconnectAttempts,
        reconnectionDelay: this.reconnectTimeout,
      });

      this.setupEventListeners();
      this.reconnectAttempts = 0;
    } catch (error) {
      console.error('Failed to connect to WebSocket:', error);
      this.handleReconnect();
    }
  }

  private setupEventListeners() {
    if (!this.socket) return;

    this.socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    this.socket.on('reconnect', () => {
      console.log('Reconnected to WebSocket server');
      this.reconnectAttempts = 0;
    });

    this.socket.on('reconnect_error', (error) => {
      console.error('WebSocket reconnection error:', error);
    });

    this.socket.on('reconnect_failed', () => {
      console.error('Failed to reconnect to WebSocket server');
      this.handleReconnect();
    });
  }

  private handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      setTimeout(() => {
        this.connect();
      }, this.reconnectTimeout * this.reconnectAttempts);
    }
  }

  public disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  public subscribeToAlerts(callback: (alert: Alert) => void) {
    if (!this.socket) return;

    this.socket.on('alert:new', callback);
    this.socket.on('alert:update', callback);
    this.socket.on('alert:status', callback);
  }

  public unsubscribeFromAlerts(callback: (alert: Alert) => void) {
    if (!this.socket) return;

    this.socket.off('alert:new', callback);
    this.socket.off('alert:update', callback);
    this.socket.off('alert:status', callback);
  }

  public subscribeToTeamStatus(callback: (team: Team) => void) {
    if (!this.socket) return;

    this.socket.on('team:status', callback);
    this.socket.on('team:location', callback);
  }

  public unsubscribeFromTeamStatus(callback: (team: Team) => void) {
    if (!this.socket) return;

    this.socket.off('team:status', callback);
    this.socket.off('team:location', callback);
  }

  public emit(event: string, data: any) {
    if (!this.socket) return;

    this.socket.emit(event, data);
  }
}

export const websocketService = new WebSocketService(); 