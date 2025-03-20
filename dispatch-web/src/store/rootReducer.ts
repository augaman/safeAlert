import { combineReducers } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import alertsReducer from './slices/alertsSlice';
import teamsReducer from './slices/teamsSlice';
import usersReducer from './slices/usersSlice';
import reportsReducer from './slices/reportsSlice';

const rootReducer = combineReducers({
  auth: authReducer,
  alerts: alertsReducer,
  teams: teamsReducer,
  users: usersReducer,
  reports: reportsReducer,
});

export type RootState = ReturnType<typeof rootReducer>;
export default rootReducer; 