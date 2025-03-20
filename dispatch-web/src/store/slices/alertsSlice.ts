import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiService } from '../../services/api';
import { AlertState, Alert, AlertFilters, PaginationParams } from '../../types';
import { PAGINATION } from '../../config/environment';

const initialState: AlertState = {
  alerts: [],
  selectedAlert: null,
  filters: {},
  pagination: {
    page: 1,
    pageSize: PAGINATION.DEFAULT_PAGE_SIZE,
    sortBy: 'createdAt',
    sortOrder: 'desc',
  },
  total: 0,
  isLoading: false,
  error: null,
};

export const fetchAlerts = createAsyncThunk(
  'alerts/fetchAlerts',
  async ({ page, pageSize, filters }: { page: number; pageSize: number; filters?: AlertFilters }) => {
    const response = await apiService.getAlerts(page, pageSize, filters);
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
  async ({ id, status }: { id: string; status: string }) => {
    const response = await apiService.updateAlertStatus(id, status);
    return response;
  }
);

export const assignAlert = createAsyncThunk(
  'alerts/assign',
  async ({ id, teamId }: { id: string; teamId: string }) => {
    const response = await apiService.assignAlert(id, teamId);
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
    setFilters: (state, action) => {
      state.filters = action.payload;
    },
    setPagination: (state, action) => {
      state.pagination = action.payload;
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
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchAlerts.fulfilled, (state, action) => {
        state.isLoading = false;
        state.alerts = action.payload.data;
        state.total = action.payload.total;
      })
      .addCase(fetchAlerts.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch alerts';
      })
      // Fetch Alert by ID
      .addCase(fetchAlertById.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchAlertById.fulfilled, (state, action) => {
        state.isLoading = false;
        state.selectedAlert = action.payload;
      })
      .addCase(fetchAlertById.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch alert details';
      })
      // Update Alert Status
      .addCase(updateAlertStatus.fulfilled, (state, action) => {
        state.updateAlertInList(action.payload);
      })
      // Assign Alert
      .addCase(assignAlert.fulfilled, (state, action) => {
        state.updateAlertInList(action.payload);
      });
  },
});

export const {
  setSelectedAlert,
  clearSelectedAlert,
  setFilters,
  setPagination,
  clearError,
  updateAlertInList,
} = alertsSlice.actions;

export default alertsSlice.reducer; 