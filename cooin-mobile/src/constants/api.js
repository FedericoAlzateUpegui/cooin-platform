/**
 * API Configuration
 */

// Base API configuration
export const API_CONFIG = {
  BASE_URL: __DEV__ ? 'http://localhost:8000' : 'https://api.cooin.com',
  API_VERSION: 'v1',
  TIMEOUT: 10000,
};

// API Endpoints
export const ENDPOINTS = {
  // Authentication
  AUTH: {
    REGISTER: '/auth/register',
    LOGIN: '/auth/login',
    REFRESH: '/auth/refresh',
    LOGOUT: '/auth/logout',
    ME: '/auth/me',
    SESSIONS: '/auth/sessions',
  },

  // Profiles
  PROFILES: {
    ME: '/profiles/me',
    BY_ID: (id) => `/profiles/${id}`,
    SEARCH: '/profiles/',
    COMPLETION: '/profiles/me/completion',
    FINANCIAL: '/profiles/me/financial',
    LENDING: '/profiles/me/lending',
    BORROWING: '/profiles/me/borrowing',
    STATS: '/profiles/stats/overview',
  },

  // Connections
  CONNECTIONS: {
    BASE: '/connections',
    BY_ID: (id) => `/connections/${id}`,
    PENDING: '/connections/pending',
    STATS: '/connections/stats',
    MATCHING: '/connections/matching/search',
    MESSAGES: (id) => `/connections/${id}/messages`,
    MESSAGE_BY_ID: (connId, msgId) => `/connections/${connId}/messages/${msgId}`,
    MESSAGE_READ: (connId, msgId) => `/connections/${connId}/messages/${msgId}/read`,
    BLOCK: (id) => `/connections/${id}/block`,
    REPORT: (id) => `/connections/${id}/report`,
  },

  // Health
  HEALTH: '/health',
};

// Request headers
export const HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
};

// API response status codes
export const STATUS_CODES = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
};