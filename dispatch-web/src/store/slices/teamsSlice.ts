import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiService } from '../../services/api';
import { TeamState, Team, PaginationParams } from '../../types';
import { PAGINATION } from '../../config/environment';

const initialState: TeamState = {
  teams: [],
  selectedTeam: null,
  pagination: {
    page: 1,
    pageSize: PAGINATION.DEFAULT_PAGE_SIZE,
    sortBy: 'name',
    sortOrder: 'asc',
  },
  total: 0,
  isLoading: false,
  error: null,
};

export const fetchTeams = createAsyncThunk(
  'teams/fetchTeams',
  async ({ page, pageSize }: { page: number; pageSize: number }) => {
    const response = await apiService.getTeams(page, pageSize);
    return response;
  }
);

export const fetchTeamById = createAsyncThunk(
  'teams/fetchTeamById',
  async (id: string) => {
    const response = await apiService.getTeamById(id);
    return response;
  }
);

export const createTeam = createAsyncThunk(
  'teams/createTeam',
  async (teamData: Partial<Team>) => {
    const response = await apiService.createTeam(teamData);
    return response;
  }
);

export const updateTeam = createAsyncThunk(
  'teams/updateTeam',
  async ({ id, teamData }: { id: string; teamData: Partial<Team> }) => {
    const response = await apiService.updateTeam(id, teamData);
    return response;
  }
);

export const deleteTeam = createAsyncThunk(
  'teams/deleteTeam',
  async (id: string) => {
    await apiService.deleteTeam(id);
    return id;
  }
);

const teamsSlice = createSlice({
  name: 'teams',
  initialState,
  reducers: {
    setSelectedTeam: (state, action) => {
      state.selectedTeam = action.payload;
    },
    clearSelectedTeam: (state) => {
      state.selectedTeam = null;
    },
    setPagination: (state, action) => {
      state.pagination = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    updateTeamInList: (state, action) => {
      const index = state.teams.findIndex(team => team.id === action.payload.id);
      if (index !== -1) {
        state.teams[index] = action.payload;
      }
      if (state.selectedTeam?.id === action.payload.id) {
        state.selectedTeam = action.payload;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Teams
      .addCase(fetchTeams.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchTeams.fulfilled, (state, action) => {
        state.isLoading = false;
        state.teams = action.payload.data;
        state.total = action.payload.total;
      })
      .addCase(fetchTeams.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch teams';
      })
      // Fetch Team by ID
      .addCase(fetchTeamById.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchTeamById.fulfilled, (state, action) => {
        state.isLoading = false;
        state.selectedTeam = action.payload;
      })
      .addCase(fetchTeamById.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch team details';
      })
      // Create Team
      .addCase(createTeam.fulfilled, (state, action) => {
        state.teams.push(action.payload);
      })
      // Update Team
      .addCase(updateTeam.fulfilled, (state, action) => {
        state.updateTeamInList(action.payload);
      })
      // Delete Team
      .addCase(deleteTeam.fulfilled, (state, action) => {
        state.teams = state.teams.filter(team => team.id !== action.payload);
        if (state.selectedTeam?.id === action.payload) {
          state.selectedTeam = null;
        }
      });
  },
});

export const {
  setSelectedTeam,
  clearSelectedTeam,
  setPagination,
  clearError,
  updateTeamInList,
} = teamsSlice.actions;

export default teamsSlice.reducer; 