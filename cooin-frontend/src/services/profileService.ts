import { apiClient } from './api';
import {
  UserProfile,
  ProfileUpdateRequest,
  PaginatedResponse
} from '../types/api';

class ProfileService {
  async getCurrentProfile(): Promise<UserProfile> {
    return await apiClient.get<UserProfile>('/profiles/me');
  }

  async updateProfile(profileData: ProfileUpdateRequest): Promise<UserProfile> {
    return await apiClient.put<UserProfile>('/profiles/me', profileData);
  }

  async uploadProfileImage(imageUri: string): Promise<{ profile_image_url: string }> {
    const formData = new FormData();
    formData.append('file', {
      uri: imageUri,
      name: 'profile.jpg',
      type: 'image/jpeg',
    } as any);

    return await apiClient.post<{ profile_image_url: string }>('/profiles/me/image', formData);
  }

  async getPublicProfile(userId: number): Promise<UserProfile> {
    return await apiClient.get<UserProfile>(`/profiles/${userId}/public`);
  }

  async searchProfiles(params: {
    location?: string;
    user_role?: string;
    min_age?: number;
    max_age?: number;
    verified_only?: boolean;
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<UserProfile>> {
    return await apiClient.get<PaginatedResponse<UserProfile>>('/profiles/search', params);
  }

  async getBorrowingPreferences(): Promise<any> {
    return await apiClient.get('/profiles/me/borrowing-preferences');
  }

  async updateBorrowingPreferences(preferences: {
    loan_purpose?: string;
    requested_loan_amount?: number;
    preferred_loan_term?: number;
    max_acceptable_rate?: number;
  }): Promise<any> {
    return await apiClient.put('/profiles/me/borrowing-preferences', preferences);
  }

  async getLendingPreferences(): Promise<any> {
    return await apiClient.get('/profiles/me/lending-preferences');
  }

  async updateLendingPreferences(preferences: {
    min_loan_amount?: number;
    max_loan_amount?: number;
    preferred_loan_terms?: number[];
    max_interest_rate?: number;
    min_credit_score?: number;
    preferred_loan_purposes?: string[];
  }): Promise<any> {
    return await apiClient.put('/profiles/me/lending-preferences', preferences);
  }
}

export const profileService = new ProfileService();