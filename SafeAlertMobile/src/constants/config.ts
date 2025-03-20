export const API_CONFIG = {
  BASE_URL: process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000',
  TIMEOUT: 10000,
  HEADERS: {
    'Content-Type': 'application/json',
  },
};

export const AUTH_CONFIG = {
  TOKEN_KEY: 'auth_token',
  REFRESH_TOKEN_KEY: 'refresh_token',
  BIOMETRIC_KEY: 'biometric_enabled',
};

export const ALERT_CONFIG = {
  PANIC_BUTTON_COOLDOWN: 30000, // 30 seconds
  LOCATION_UPDATE_INTERVAL: 5000, // 5 seconds
  MAX_RETRY_ATTEMPTS: 3,
};

export const NOTIFICATION_CONFIG = {
  PROJECT_ID: 'your-expo-project-id', // Replace with your actual Expo project ID
  CHANNEL_ID: 'default',
  CHANNEL_NAME: 'Default Channel',
  CHANNEL_DESCRIPTION: 'Default notification channel for SafeAlert',
};

export const WEBSOCKET_CONFIG = {
  URL: 'ws://localhost:8000/ws', // WebSocket server URL
  RECONNECT_INTERVAL: 5000, // Time between reconnection attempts in ms
  MAX_RECONNECT_ATTEMPTS: 5, // Maximum number of reconnection attempts
}; 