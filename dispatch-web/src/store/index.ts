import { configureStore } from '@reduxjs/toolkit';
import rootReducer from './rootReducer';
import { websocketService } from '../services/websocket';

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types
        ignoredActions: ['websocket/connected', 'websocket/disconnected'],
        // Ignore these field paths in all actions
        ignoredActionPaths: ['payload.socket'],
      },
    }),
});

// Initialize WebSocket connection when store is created
websocketService.connect();

export type AppDispatch = typeof store.dispatch;
export default store; 