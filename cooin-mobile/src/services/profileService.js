/**
 * Profile Service
 */

import apiClient from './apiClient';
import { ENDPOINTS } from '../constants/api';

class ProfileService {
  // Get current user's profile
  async getMyProfile() {
    try {
      const response = await apiClient.get(ENDPOINTS.PROFILES.ME);
      return response.data;
    } catch (error) {
      console.error('Get profile error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Create user profile
  async createProfile(profileData) {
    try {
      const response = await apiClient.post(ENDPOINTS.PROFILES.ME, profileData);
      return response.data;
    } catch (error) {
      console.error('Create profile error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Update user profile
  async updateProfile(profileData) {
    try {
      const response = await apiClient.put(ENDPOINTS.PROFILES.ME, profileData);
      return response.data;
    } catch (error) {
      console.error('Update profile error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Update financial information
  async updateFinancialInfo(financialData) {
    try {
      const response = await apiClient.put(ENDPOINTS.PROFILES.FINANCIAL, financialData);
      return response.data;
    } catch (error) {
      console.error('Update financial info error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Update lending preferences
  async updateLendingPreferences(lendingData) {
    try {
      const response = await apiClient.put(ENDPOINTS.PROFILES.LENDING, lendingData);
      return response.data;
    } catch (error) {
      console.error('Update lending preferences error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Update borrowing preferences
  async updateBorrowingPreferences(borrowingData) {
    try {
      const response = await apiClient.put(ENDPOINTS.PROFILES.BORROWING, borrowingData);
      return response.data;
    } catch (error) {
      console.error('Update borrowing preferences error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get profile completion status
  async getProfileCompletion() {
    try {
      const response = await apiClient.get(ENDPOINTS.PROFILES.COMPLETION);
      return response.data;
    } catch (error) {
      console.error('Get profile completion error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get public profile by user ID
  async getPublicProfile(userId) {
    try {
      const response = await apiClient.get(ENDPOINTS.PROFILES.BY_ID(userId));
      return response.data;
    } catch (error) {
      console.error('Get public profile error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Search profiles
  async searchProfiles(params = {}) {
    try {
      const response = await apiClient.get(ENDPOINTS.PROFILES.SEARCH, { params });
      return response.data;
    } catch (error) {
      console.error('Search profiles error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get profile statistics
  async getProfileStats() {
    try {
      const response = await apiClient.get(ENDPOINTS.PROFILES.STATS);
      return response.data;
    } catch (error) {
      console.error('Get profile stats error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Delete profile
  async deleteProfile() {
    try {
      const response = await apiClient.delete(ENDPOINTS.PROFILES.ME);
      return response.data;
    } catch (error) {
      console.error('Delete profile error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Upload profile picture (if implemented)
  async uploadProfilePicture(imageData) {
    try {
      const formData = new FormData();
      formData.append('file', {
        uri: imageData.uri,
        type: imageData.type || 'image/jpeg',
        name: imageData.fileName || 'profile.jpg',
      });

      const response = await apiClient.post('/profiles/me/avatar', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      console.error('Upload profile picture error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Upload banner image (if implemented)
  async uploadBannerImage(imageData) {
    try {
      const formData = new FormData();
      formData.append('file', {
        uri: imageData.uri,
        type: imageData.type || 'image/jpeg',
        name: imageData.fileName || 'banner.jpg',
      });

      const response = await apiClient.post('/profiles/me/banner', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      console.error('Upload banner image error:', error.response?.data || error.message);
      throw error;
    }
  }
}

export const profileService = new ProfileService();