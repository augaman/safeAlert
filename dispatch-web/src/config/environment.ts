export type Role = 'admin' | 'super_admin' | 'dispatcher' | 'team_leader' | 'team_member';

export const ROLES = {
  ADMIN: 'admin',
  SUPER_ADMIN: 'super_admin',
  DISPATCHER: 'dispatcher',
  TEAM_LEADER: 'team_leader',
  TEAM_MEMBER: 'team_member',
} as const;

export const API = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:3001/api',
  TIMEOUT: 10000,
  HEADERS: {
    'Content-Type': 'application/json',
  },
};

export const APP_CONFIG = {
  APP_NAME: 'SafeAlert',
  APP_VERSION: '1.0.0',
  DEFAULT_LANGUAGE: 'en',
  DEFAULT_THEME: 'light',
  SUPPORTED_LANGUAGES: ['en', 'es', 'fr', 'de'],
  MAP_CENTER: {
    lat: 0,
    lng: 0,
  },
  MAP_ZOOM: 13,
};

export const NOTIFICATION_CONFIG = {
  POSITION: 'top-right',
  AUTO_HIDE_DURATION: 6000,
};

export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [10, 25, 50, 100],
};

export const DATE_FORMAT = {
  DISPLAY: 'MMM DD, YYYY HH:mm',
  API: 'YYYY-MM-DDTHH:mm:ss.SSSZ',
};

export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error occurred. Please check your connection.',
  SERVER_ERROR: 'Server error occurred. Please try again later.',
  UNAUTHORIZED: 'Unauthorized access. Please login again.',
  FORBIDDEN: 'Access forbidden. You do not have permission.',
  NOT_FOUND: 'Resource not found.',
  VALIDATION_ERROR: 'Please check your input and try again.',
};

export const SUCCESS_MESSAGES = {
  LOGIN: 'Successfully logged in.',
  LOGOUT: 'Successfully logged out.',
  CREATE: 'Successfully created.',
  UPDATE: 'Successfully updated.',
  DELETE: 'Successfully deleted.',
  SAVE: 'Successfully saved.',
};

export const WEBSOCKET = {
  URL: process.env.REACT_APP_WEBSOCKET_URL || 'http://localhost:3001',
  RECONNECT_INTERVAL: 5000,
  MAX_RECONNECT_ATTEMPTS: 5,
};

export const AUTH_CONFIG = {
  TOKEN_KEY: 'auth_token',
  REFRESH_TOKEN_KEY: 'refresh_token',
  TOKEN_EXPIRY: 3600, // 1 hour in seconds
};

export const ALERT_TYPES = {
  PANIC: 'panic',
  MEDICAL: 'medical',
  HOME_SECURITY: 'home_security',
  CAR_THEFT: 'car_theft',
} as const;

export const ALERT_STATUS = {
  NEW: 'new',
  ASSIGNED: 'assigned',
  IN_PROGRESS: 'in_progress',
  RESOLVED: 'resolved',
  CANCELLED: 'cancelled',
} as const;

export const MAP = {
  DEFAULT_CENTER: {
    lat: 0,
    lng: 0,
  },
  DEFAULT_ZOOM: 13,
  MAX_ZOOM: 18,
};

export const ALERT = {
  PRIORITIES: {
    HIGH: 'high',
    MEDIUM: 'medium',
    LOW: 'low',
  },
  TYPES: {
    EMERGENCY: 'emergency',
    WARNING: 'warning',
    INFO: 'info',
  },
  STATUSES: {
    NEW: 'new',
    ASSIGNED: 'assigned',
    IN_PROGRESS: 'in_progress',
    RESOLVED: 'resolved',
  },
};

export const REPORT = {
  TYPES: {
    DAILY: 'daily',
    WEEKLY: 'weekly',
    MONTHLY: 'monthly',
    CUSTOM: 'custom',
  },
};

export const USER = {
  ROLES: {
    ADMIN: 'admin',
    DISPATCHER: 'dispatcher',
    RESPONDER: 'responder',
  },
  STATUSES: {
    ACTIVE: 'active',
    INACTIVE: 'inactive',
  },
};

export const TEAM = {
  STATUSES: {
    ACTIVE: 'active',
    INACTIVE: 'inactive',
  },
};

export const DATE_FORMATS = {
  DISPLAY: 'MMM DD, YYYY HH:mm:ss',
  API: 'YYYY-MM-DDTHH:mm:ss.SSSZ',
} as const;

export const ALERT_CONFIG = {
  REFRESH_INTERVAL: 30000, // 30 seconds
  MAX_ALERTS_PER_PAGE: 20,
  PANIC_BUTTON_COOLDOWN: 60000, // 1 minute
}; 