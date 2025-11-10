import { create } from 'zustand';
import { UserProfile, ProfileUpdateRequest } from '../types/api';
import { profileService } from '../services/profileService';

interface ProfileState {
  profile: UserProfile | null;
  isLoading: boolean;
  error: string | null;
  isProfileComplete: boolean;
  profileCompletion: number;

  // Actions
  loadProfile: () => Promise<void>;
  updateProfile: (profileData: ProfileUpdateRequest) => Promise<void>;
  uploadProfileImage: (imageUri: string) => Promise<void>;
  clearError: () => void;
  checkProfileCompletion: () => void;
}

export const useProfileStore = create<ProfileState>((set, get) => ({
  profile: null,
  isLoading: false,
  error: null,
  isProfileComplete: false,
  profileCompletion: 0,

  loadProfile: async () => {
    set({ isLoading: true, error: null });
    try {
      const profile = await profileService.getCurrentProfile();
      set({
        profile,
        isLoading: false,
        error: null
      });
      get().checkProfileCompletion();
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.detail || 'Failed to load profile',
        profile: null,
      });
    }
  },

  updateProfile: async (profileData: ProfileUpdateRequest) => {
    set({ isLoading: true, error: null });
    try {
      const updatedProfile = await profileService.updateProfile(profileData);
      set({
        profile: updatedProfile,
        isLoading: false,
        error: null
      });
      get().checkProfileCompletion();
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.detail || 'Failed to update profile',
      });
      throw error;
    }
  },

  uploadProfileImage: async (imageUri: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await profileService.uploadProfileImage(imageUri);
      const currentProfile = get().profile;
      if (currentProfile) {
        set({
          profile: {
            ...currentProfile,
            profile_image_url: response.profile_image_url,
          },
          isLoading: false,
          error: null,
        });
      }
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.detail || 'Failed to upload image',
      });
      throw error;
    }
  },

  clearError: () => {
    set({ error: null });
  },

  checkProfileCompletion: () => {
    const profile = get().profile;
    if (!profile) {
      set({ isProfileComplete: false, profileCompletion: 0 });
      return;
    }

    // Check if essential profile fields are completed
    const requiredFields = [
      profile.first_name,
      profile.last_name,
      profile.display_name,
      profile.bio,
      profile.city,
      profile.state_province,
      profile.country,
      profile.phone_number,
      profile.profile_image_url,
      profile.employment_status,
    ];

    const completedFields = requiredFields.filter(field => field && String(field).trim().length > 0).length;
    const percentage = Math.round((completedFields / requiredFields.length) * 100);
    const isComplete = percentage === 100;

    set({ isProfileComplete: isComplete, profileCompletion: percentage });
  },
}));