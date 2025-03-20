import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Alert, AlertStatus } from '../../types/alert';

interface AlertState {
  alerts: Alert[];
  loading: boolean;
  error: string | null;
  selectedAlert: Alert | null;
}

const initialState: AlertState = {
  alerts: [],
  loading: false,
  error: null,
  selectedAlert: null,
};

const alertSlice = createSlice({
  name: 'alerts',
  initialState,
  reducers: {
    setAlerts: (state, action: PayloadAction<Alert[]>) => {
      state.alerts = action.payload;
    },
    addAlert: (state, action: PayloadAction<Alert>) => {
      state.alerts.unshift(action.payload);
    },
    updateAlert: (state, action: PayloadAction<Alert>) => {
      const index = state.alerts.findIndex((alert) => alert.id === action.payload.id);
      if (index !== -1) {
        state.alerts[index] = action.payload;
      }
    },
    setSelectedAlert: (state, action: PayloadAction<Alert | null>) => {
      state.selectedAlert = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    updateAlertStatus: (
      state,
      action: PayloadAction<{ id: string; status: AlertStatus }>
    ) => {
      const alert = state.alerts.find((a) => a.id === action.payload.id);
      if (alert) {
        alert.status = action.payload.status;
      }
      if (state.selectedAlert?.id === action.payload.id) {
        state.selectedAlert.status = action.payload.status;
      }
    },
  },
});

export const {
  setAlerts,
  addAlert,
  updateAlert,
  setSelectedAlert,
  setLoading,
  setError,
  updateAlertStatus,
} = alertSlice.actions;

export default alertSlice.reducer; 