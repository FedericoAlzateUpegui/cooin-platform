import { apiClient } from './api';
import * as SecureStore from 'expo-secure-store';
import {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  User
} from '../types/api';
import { STORAGE_KEYS } from '../constants/config';

class AuthService {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/login', credentials);

    // Store tokens securely
    await apiClient.storeTokens(response.access_token, response.refresh_token);

    // Store user data
    await SecureStore.setItemAsync(STORAGE_KEYS.USER_DATA, JSON.stringify(response.user));

    return response;
  }

  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/register', userData);

    // Store tokens securely
    await apiClient.storeTokens(response.access_token, response.refresh_token);

    // Store user data
    await SecureStore.setItemAsync(STORAGE_KEYS.USER_DATA, JSON.stringify(response.user));

    return response;
  }

  async logout(): Promise<void> {
    try {
      // Call logout endpoint to invalidate tokens on server
      await apiClient.post('/auth/logout');
    } catch (error) {
      // Continue with logout even if server call fails
      console.warn('Server logout failed:', error);
    } finally {
      // Clear local storage
      await apiClient.clearTokens();
    }
  }

  async getCurrentUser(): Promise<User | null> {
    try {
      const userData = await SecureStore.getItemAsync(STORAGE_KEYS.USER_DATA);
      if (userData) {
        return JSON.parse(userData);
      }

      // If no cached user data, fetch from server
      const user = await apiClient.get<User>('/auth/me');
      await SecureStore.setItemAsync(STORAGE_KEYS.USER_DATA, JSON.stringify(user));
      return user;
    } catch (error) {
      console.error('Error getting current user:', error);
      return null;
    }
  }

  async isAuthenticated(): Promise<boolean> {
    return await apiClient.isAuthenticated();
  }

  async refreshTokens(): Promise<void> {
    try {
      const refreshToken = await SecureStore.getItemAsync(STORAGE_KEYS.REFRESH_TOKEN);
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await apiClient.post<AuthResponse>('/auth/refresh', {
        refresh_token: refreshToken,
      });

      await apiClient.storeTokens(response.access_token, response.refresh_token);
    } catch (error) {
      console.error('Token refresh failed:', error);
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

  async changePassword(currentPassword: string, newPassword: string): Promise<{ message: string }> {
    return await apiClient.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  }
}

export const authService = new AuthService();