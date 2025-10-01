/**
 * API Client Configuration
 */

import axios from 'axios';
import { API_CONFIG, ENDPOINTS, HEADERS } from '../constants/api';
import { secureStorage } from '../utils/secureStorage';

// Create axios instance
const apiClient = axios.create({
  baseURL: `${API_CONFIG.BASE_URL}/api/${API_CONFIG.API_VERSION}`,
  timeout: API_CONFIG.TIMEOUT,
  headers: HEADERS,
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  async (config) => {
    try {
      const tokens = await secureStorage.getTokens();
      if (tokens?.accessToken) {
        config.headers.Authorization = `Bearer ${tokens.accessToken}`;
      }
    } catch (error) {
      console.warn('Failed to get tokens for request:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 error and we haven't already tried to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const tokens = await secureStorage.getTokens();
        if (tokens?.refreshToken) {
          // Try to refresh the token
          const refreshResponse = await axios.post(
            `${API_CONFIG.BASE_URL}/api/${API_CONFIG.API_VERSION}${ENDPOINTS.AUTH.REFRESH}`,
            { refresh_token: tokens.refreshToken }
          );

          const newAccessToken = refreshResponse.data.access_token;

          // Update stored tokens
          await secureStorage.storeTokens({
            ...tokens,
            accessToken: newAccessToken,
          });

          // Update the authorization header and retry the request
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, clear tokens and redirect to login
        await secureStorage.clearTokens();

        // You can dispatch a logout action here if needed
        // store.dispatch(logoutUser());

        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;