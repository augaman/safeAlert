import { useEffect } from 'react';
import { websocketService } from '../services/websocket';
import { useAppDispatch } from './useAppDispatch';
import { updateAlertInList } from '../store/slices/alertsSlice';
import { Alert } from '../types';

export const useWebSocket = () => {
  const dispatch = useAppDispatch();

  useEffect(() => {
    // Subscribe to alert events
    const unsubscribeNewAlert = websocketService.subscribe('alert:new', (alert: Alert) => {
      dispatch(updateAlertInList(alert));
    });

    const unsubscribeUpdateAlert = websocketService.subscribe('alert:update', (alert: Alert) => {
      dispatch(updateAlertInList(alert));
    });

    const unsubscribeStatusAlert = websocketService.subscribe('alert:status', (data: { id: string; status: string }) => {
      dispatch(updateAlertInList({ id: data.id, status: data.status } as Alert));
    });

    // Subscribe to team events
    const unsubscribeTeamStatus = websocketService.subscribe('team:status', (team) => {
      // Handle team status updates
      console.log('Team status updated:', team);
    });

    const unsubscribeTeamLocation = websocketService.subscribe('team:location', (data) => {
      // Handle team location updates
      console.log('Team location updated:', data);
    });

    // Subscribe to connection status
    const unsubscribeConnection = websocketService.onConnectionChange((connected) => {
      console.log('WebSocket connection status:', connected);
    });

    // Cleanup subscriptions
    return () => {
      unsubscribeNewAlert();
      unsubscribeUpdateAlert();
      unsubscribeStatusAlert();
      unsubscribeTeamStatus();
      unsubscribeTeamLocation();
      unsubscribeConnection();
    };
  }, [dispatch]);

  return {
    isConnected: websocketService.isConnected(),
    emit: websocketService.emit.bind(websocketService),
  };
}; 