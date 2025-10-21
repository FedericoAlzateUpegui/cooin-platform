import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import { secureStorage } from '../utils/secureStorage';
import { API_CONFIG, STORAGE_KEYS } from '../constants/config';
import { ApiError } from '../types/api';

class ApiClient {
  private client: AxiosInstance;
  private isRefreshing = false;
  private refreshSubscribers: Array<(token: string) => void> = [];

  constructor() {
    this.client = axios.create({
      baseURL: API_CONFIG.BASE_URL,
      timeout: API_CONFIG.TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      async (config) => {
        const token = await this.getAccessToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor to handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;

        // Don't try to refresh token for auth endpoints (login, register, refresh)
        const isAuthEndpoint = originalRequest.url?.includes('/auth/login') ||
                               originalRequest.url?.includes('/auth/register') ||
                               originalRequest.url?.includes('/auth/refresh');

        if (error.response?.status === 401 && !originalRequest._retry && !isAuthEndpoint) {
          if (this.isRefreshing) {
            // If already refreshing, queue the request
            return new Promise((resolve) => {
              this.refreshSubscribers.push((token: string) => {
                originalRequest.headers.Authorization = `Bearer ${token}`;
                resolve(this.client(originalRequest));
              });
            });
          }

          originalRequest._retry = true;
          this.isRefreshing = true;

          try {
            const newToken = await this.refreshToken();
            this.isRefreshing = false;

            // Process queued requests
            this.refreshSubscribers.forEach((callback) => callback(newToken));
            this.refreshSubscribers = [];

            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            return this.client(originalRequest);
          } catch (refreshError) {
            this.isRefreshing = false;
            this.refreshSubscribers = [];
            await this.clearTokens();
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(this.handleError(error));
      }
    );
  }

  private async getAccessToken(): Promise<string | null> {
    try {
      return await secureStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
    } catch (error) {
      console.error('Error getting access token:', error);
      return null;
    }
  }

  private async getRefreshToken(): Promise<string | null> {
    try {
      return await secureStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
    } catch (error) {
      console.error('Error getting refresh token:', error);
      return null;
    }
  }

  private async refreshToken(): Promise<string> {
    const refreshToken = await this.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await axios.post(`${API_CONFIG.BASE_URL}/auth/refresh`, {
      refresh_token: refreshToken,
    });

    const { access_token, refresh_token: newRefreshToken } = response.data;

    await this.storeTokens(access_token, newRefreshToken);
    return access_token;
  }

  async storeTokens(accessToken: string, refreshToken: string): Promise<void> {
    try {
      await secureStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, accessToken);
      await secureStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refreshToken);
    } catch (error) {
      console.error('Error storing tokens:', error);
      throw error;
    }
  }

  async clearTokens(): Promise<void> {
    try {
      await secureStorage.deleteItem(STORAGE_KEYS.ACCESS_TOKEN);
      await secureStorage.deleteItem(STORAGE_KEYS.REFRESH_TOKEN);
      await secureStorage.deleteItem(STORAGE_KEYS.USER_DATA);
    } catch (error) {
      console.error('Error clearing tokens:', error);
    }
  }

  private handleError(error: AxiosError): ApiError {
    const apiError: ApiError = {
      detail: 'An unexpected error occurred',
      status_code: error.response?.status || 500,
    };

    if (error.response?.data) {
      const responseData = error.response.data as any;

      // Extract error message from various possible formats
      if (responseData.detail) {
        // FastAPI standard error format
        apiError.detail = responseData.detail;
      } else if (responseData.message) {
        // Alternative message field
        apiError.detail = responseData.message;
      } else if (responseData.field_errors) {
        // Validation errors (422)
        const fieldErrors = responseData.field_errors as any[];
        if (fieldErrors.length > 0) {
          // Show first field error
          apiError.detail = fieldErrors[0].message || fieldErrors[0].msg || 'Validation error';
        }
      } else if (responseData.error) {
        // Another possible error format
        if (typeof responseData.error === 'string') {
          apiError.detail = responseData.error;
        } else if (responseData.error.message) {
          apiError.detail = responseData.error.message;
        }
      }
    } else if (error.message) {
      // Network or request setup error
      if (error.message === 'Network Error') {
        apiError.detail = 'Cannot connect to server. Please check your internet connection.';
      } else {
        apiError.detail = error.message;
      }
    }

    return apiError;
  }

  // HTTP methods
  async get<T>(url: string, params?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.client.post(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.client.put(url, data);
    return response.data;
  }

  async patch<T>(url: string, data?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.client.patch(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response: AxiosResponse<T> = await this.client.delete(url);
    return response.data;
  }

  // Check if user is authenticated
  async isAuthenticated(): Promise<boolean> {
    const token = await this.getAccessToken();
    return !!token;
  }
}

// Export singleton instance
export const apiClient = new ApiClient();