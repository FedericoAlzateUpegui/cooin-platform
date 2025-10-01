/**
 * Authentication Service
 */

import apiClient from './apiClient';
import { ENDPOINTS } from '../constants/api';

class AuthService {
  // User registration
  async register(userData) {
    try {
      const response = await apiClient.post(ENDPOINTS.AUTH.REGISTER, userData);
      return response.data;
    } catch (error) {
      console.error('Registration error:', error.response?.data || error.message);
      throw error;
    }
  }

  // User login
  async login(credentials) {
    try {
      const response = await apiClient.post(ENDPOINTS.AUTH.LOGIN, credentials);
      return response.data;
    } catch (error) {
      console.error('Login error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Refresh access token
  async refreshToken(refreshToken) {
    try {
      const response = await apiClient.post(ENDPOINTS.AUTH.REFRESH, {
        refresh_token: refreshToken,
      });
      return response.data;
    } catch (error) {
      console.error('Token refresh error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get current user info
  async getCurrentUser() {
    try {
      const response = await apiClient.get(ENDPOINTS.AUTH.ME);
      return response.data;
    } catch (error) {
      console.error('Get current user error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get user sessions
  async getUserSessions() {
    try {
      const response = await apiClient.get(ENDPOINTS.AUTH.SESSIONS);
      return response.data;
    } catch (error) {
      console.error('Get user sessions error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Logout user
  async logout(refreshToken, logoutAllDevices = false) {
    try {
      const response = await apiClient.post(ENDPOINTS.AUTH.LOGOUT, {
        refresh_token: refreshToken,
        logout_all_devices: logoutAllDevices,
      });
      return response.data;
    } catch (error) {
      console.error('Logout error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Forgot password (if implemented in backend)
  async forgotPassword(email) {
    try {
      // This endpoint might not exist yet in your backend
      const response = await apiClient.post('/auth/forgot-password', { email });
      return response.data;
    } catch (error) {
      console.error('Forgot password error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Reset password (if implemented in backend)
  async resetPassword(token, newPassword) {
    try {
      // This endpoint might not exist yet in your backend
      const response = await apiClient.post('/auth/reset-password', {
        token,
        password: newPassword,
      });
      return response.data;
    } catch (error) {
      console.error('Reset password error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Change password
  async changePassword(currentPassword, newPassword) {
    try {
      // This endpoint might not exist yet in your backend
      const response = await apiClient.post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword,
      });
      return response.data;
    } catch (error) {
      console.error('Change password error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Verify email (if implemented in backend)
  async verifyEmail(token) {
    try {
      // This endpoint might not exist yet in your backend
      const response = await apiClient.post('/auth/verify-email', { token });
      return response.data;
    } catch (error) {
      console.error('Verify email error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Resend verification email
  async resendVerificationEmail(email) {
    try {
      // This endpoint might not exist yet in your backend
      const response = await apiClient.post('/auth/resend-verification', { email });
      return response.data;
    } catch (error) {
      console.error('Resend verification error:', error.response?.data || error.message);
      throw error;
    }
  }
}

export const authService = new AuthService();