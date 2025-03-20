import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiService } from '../../services/api';
import { Alert, AlertFilters, AlertState, StatusUpdate } from '../../types';

const initialState: AlertState = {
  alerts: [],
  selectedAlert: null,
  loading: false,
  error: null,
};

export const fetchAlerts = createAsyncThunk(
  'alerts/fetchAlerts',
  async (filters?: AlertFilters) => {
    const response = await apiService.getAlerts(filters);
    return response;
  }
);

export const fetchAlertById = createAsyncThunk(
  'alerts/fetchAlertById',
  async (id: string) => {
    const response = await apiService.getAlertById(id);
    return response;
  }
);

export const updateAlertStatus = createAsyncThunk(
  'alerts/updateStatus',
  async (update: StatusUpdate) => {
    const response = await apiService.updateAlertStatus(update);
    return response;
  }
);

const alertsSlice = createSlice({
  name: 'alerts',
  initialState,
  reducers: {
    setSelectedAlert: (state, action) => {
      state.selectedAlert = action.payload;
    },
    clearSelectedAlert: (state) => {
      state.selectedAlert = null;
    },
    clearError: (state) => {
      state.error = null;
    },
    updateAlertInList: (state, action) => {
      const index = state.alerts.findIndex(alert => alert.id === action.payload.id);
      if (index !== -1) {
        state.alerts[index] = action.payload;
      }
      if (state.selectedAlert?.id === action.payload.id) {
        state.selectedAlert = action.payload;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Alerts
      .addCase(fetchAlerts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAlerts.fulfilled, (state, action) => {
        state.loading = false;
        state.alerts = action.payload;
      })
      .addCase(fetchAlerts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch alerts';
      })
      // Fetch Alert by ID
      .addCase(fetchAlertById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAlertById.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedAlert = action.payload;
      })
      .addCase(fetchAlertById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch alert details';
      })
      // Update Alert Status
      .addCase(updateAlertStatus.fulfilled, (state, action) => {
        state.updateAlertInList(action.payload);
      });
  },
});

export const {
  setSelectedAlert,
  clearSelectedAlert,
  clearError,
  updateAlertInList,
} = alertsSlice.actions;

export default alertsSlice.reducer; 