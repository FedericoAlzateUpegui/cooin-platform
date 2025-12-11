import { apiClient } from './api';
import { secureStorage } from '../utils/secureStorage';
import {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  User
} from '../types/api';
import { STORAGE_KEYS } from '../constants/config';
import { logger } from '../utils/logger';
import { hasMessage, hasDetail } from '../utils/errorUtils';

class AuthService {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<any>('/auth/login', credentials);
      logger.debug('Login response received', response);

      // Backend returns tokens nested in {user, tokens, message}
      // Extract tokens from nested structure
      const tokens = response.tokens || response;
      const access_token = tokens.access_token;
      const refresh_token = tokens.refresh_token;

      logger.debug('Extracted tokens', { hasAccessToken: !!access_token, hasRefreshToken: !!refresh_token });

      if (!access_token || !refresh_token) {
        const debugInfo = `Response keys: ${Object.keys(response).join(', ')}\nTokens keys: ${Object.keys(tokens).join(', ')}`;
        logger.error('Missing tokens', { debugInfo });
        throw new Error(`Missing tokens. ${debugInfo}`);
      }

      // Store tokens securely
      await apiClient.storeTokens(access_token, refresh_token);

      // Store user data (only if user object exists and is valid)
      if (response.user && typeof response.user === 'object') {
        await secureStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(response.user));
      }

      // Return in expected format
      return {
        access_token,
        refresh_token,
        token_type: tokens.token_type || 'bearer',
        expires_in: tokens.expires_in,
        user: response.user
      };
    } catch (error: unknown) {
      logger.error('Login error in authService', error);
      throw error;
    }
  }

  async register(userData: RegisterRequest): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<any>('/auth/register', userData);

      // Backend returns tokens nested in {user, tokens, message}
      // Extract tokens from nested structure
      const tokens = response.tokens || response;
      const access_token = tokens.access_token;
      const refresh_token = tokens.refresh_token;

      if (!access_token || !refresh_token) {
        throw new Error('Registration failed: No tokens received');
      }

      // Store tokens securely
      await apiClient.storeTokens(access_token, refresh_token);

      // Store user data (only if user object exists and is valid)
      if (response.user && typeof response.user === 'object') {
        await secureStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(response.user));
      }

      // Return in expected format
      return {
        access_token,
        refresh_token,
        token_type: tokens.token_type || 'bearer',
        expires_in: tokens.expires_in,
        user: response.user
      };
    } catch (error: unknown) {
      logger.error('Registration error in authService', error);
      throw error;
    }
  }

  async logout(): Promise<void> {
    try {
      // Call logout endpoint to invalidate tokens on server
      await apiClient.post('/auth/logout');
    } catch (error) {
      // Continue with logout even if server call fails
      logger.warn('Server logout failed', error);
    } finally {
      // Clear local storage
      await apiClient.clearTokens();
    }
  }

  async getCurrentUser(): Promise<User | null> {
    try {
      const userData = await secureStorage.getItem(STORAGE_KEYS.USER_DATA);
      if (userData) {
        try {
          return JSON.parse(userData);
        } catch (parseError) {
          logger.error('Failed to parse user data, clearing corrupted data', parseError);
          await secureStorage.deleteItem(STORAGE_KEYS.USER_DATA);
        }
      }

      // If no cached user data, fetch from server
      const user = await apiClient.get<User>('/auth/me');
      if (user && typeof user === 'object') {
        await secureStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(user));
      }
      return user;
    } catch (error) {
      logger.error('Error getting current user', error);
      return null;
    }
  }

  async isAuthenticated(): Promise<boolean> {
    return await apiClient.isAuthenticated();
  }

  async refreshTokens(): Promise<void> {
    try {
      const refreshToken = await secureStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await apiClient.post<AuthResponse>('/auth/refresh', {
        refresh_token: refreshToken,
      });

      await apiClient.storeTokens(response.access_token, response.refresh_token);
    } catch (error) {
      logger.error('Token refresh failed', error);
      await this.logout();
      throw error;
    }
  }

  async forgotPassword(email: string): Promise<{ message: string }> {
    return await apiClient.post('/auth/forgot-password', { email });
  }

  async resetPassword(token: string, newPassword: string): Promise<{ message: string }> {
    return await apiClient.post('/auth/reset-password', {
      token,
      new_password: newPassword,
    });
  }

  async verifyEmail(token: string): Promise<{ message: string }> {
    return await apiClient.post('/auth/verify-email', { token });
  }

  async resendVerificationEmail(): Promise<{ message: string }> {
    return await apiClient.post('/auth/resend-verification');
  }

  async changePassword(data: {
    current_password: string;
    new_password: string;
    confirm_new_password: string;
  }): Promise<{ message: string }> {
    return await apiClient.put('/auth/change-password', data);
  }
}

export const authService = new AuthService();