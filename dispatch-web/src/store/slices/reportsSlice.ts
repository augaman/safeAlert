import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiService } from '../../services/api';
import { ReportState, Report, ReportFilters, PaginationParams } from '../../types';
import { PAGINATION } from '../../config/environment';

const initialState: ReportState = {
  reports: [],
  selectedReport: null,
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

export const fetchReports = createAsyncThunk(
  'reports/fetchReports',
  async ({ page, pageSize, filters }: { page: number; pageSize: number; filters?: ReportFilters }) => {
    const response = await apiService.getReports(page, pageSize, filters);
    return response;
  }
);

export const fetchReportById = createAsyncThunk(
  'reports/fetchReportById',
  async (id: string) => {
    const response = await apiService.getReportById(id);
    return response;
  }
);

export const generateReport = createAsyncThunk(
  'reports/generateReport',
  async (filters: ReportFilters) => {
    const response = await apiService.generateReport(filters);
    return response;
  }
);

export const deleteReport = createAsyncThunk(
  'reports/deleteReport',
  async (id: string) => {
    await apiService.deleteReport(id);
    return id;
  }
);

const reportsSlice = createSlice({
  name: 'reports',
  initialState,
  reducers: {
    setSelectedReport: (state, action) => {
      state.selectedReport = action.payload;
    },
    clearSelectedReport: (state) => {
      state.selectedReport = null;
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
    updateReportInList: (state, action) => {
      const index = state.reports.findIndex(report => report.id === action.payload.id);
      if (index !== -1) {
        state.reports[index] = action.payload;
      }
      if (state.selectedReport?.id === action.payload.id) {
        state.selectedReport = action.payload;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Reports
      .addCase(fetchReports.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchReports.fulfilled, (state, action) => {
        state.isLoading = false;
        state.reports = action.payload.data;
        state.total = action.payload.total;
      })
      .addCase(fetchReports.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch reports';
      })
      // Fetch Report by ID
      .addCase(fetchReportById.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchReportById.fulfilled, (state, action) => {
        state.isLoading = false;
        state.selectedReport = action.payload;
      })
      .addCase(fetchReportById.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch report details';
      })
      // Generate Report
      .addCase(generateReport.fulfilled, (state, action) => {
        state.reports.unshift(action.payload);
      })
      // Delete Report
      .addCase(deleteReport.fulfilled, (state, action) => {
        state.reports = state.reports.filter(report => report.id !== action.payload);
        if (state.selectedReport?.id === action.payload) {
          state.selectedReport = null;
        }
      });
  },
});

export const {
  setSelectedReport,
  clearSelectedReport,
  setFilters,
  setPagination,
  clearError,
  updateReportInList,
} = reportsSlice.actions;

export default reportsSlice.reducer; 