/**
 * Profile Redux Slice
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { profileService } from '../../services/profileService';

// Async thunks
export const getProfile = createAsyncThunk(
  'profile/getProfile',
  async (_, { rejectWithValue }) => {
    try {
      const response = await profileService.getMyProfile();
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to fetch profile' });
    }
  }
);

export const createProfile = createAsyncThunk(
  'profile/createProfile',
  async (profileData, { rejectWithValue }) => {
    try {
      const response = await profileService.createProfile(profileData);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to create profile' });
    }
  }
);

export const updateProfile = createAsyncThunk(
  'profile/updateProfile',
  async (profileData, { rejectWithValue }) => {
    try {
      const response = await profileService.updateProfile(profileData);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to update profile' });
    }
  }
);

export const updateFinancialInfo = createAsyncThunk(
  'profile/updateFinancialInfo',
  async (financialData, { rejectWithValue }) => {
    try {
      const response = await profileService.updateFinancialInfo(financialData);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to update financial info' });
    }
  }
);

export const updateLendingPreferences = createAsyncThunk(
  'profile/updateLendingPreferences',
  async (lendingData, { rejectWithValue }) => {
    try {
      const response = await profileService.updateLendingPreferences(lendingData);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to update lending preferences' });
    }
  }
);

export const updateBorrowingPreferences = createAsyncThunk(
  'profile/updateBorrowingPreferences',
  async (borrowingData, { rejectWithValue }) => {
    try {
      const response = await profileService.updateBorrowingPreferences(borrowingData);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to update borrowing preferences' });
    }
  }
);

export const getProfileCompletion = createAsyncThunk(
  'profile/getProfileCompletion',
  async (_, { rejectWithValue }) => {
    try {
      const response = await profileService.getProfileCompletion();
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to get profile completion' });
    }
  }
);

// Initial state
const initialState = {
  profile: null,
  profileCompletion: null,
  loading: false,
  updating: false,
  error: null,
  hasProfile: false,
};

// Profile slice
const profileSlice = createSlice({
  name: 'profile',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    resetProfile: (state) => {
      return initialState;
    },
    updateProfileField: (state, action) => {
      if (state.profile) {
        state.profile = { ...state.profile, ...action.payload };
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Get profile
      .addCase(getProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.profile = action.payload;
        state.hasProfile = true;
        state.error = null;
      })
      .addCase(getProfile.rejected, (state, action) => {
        state.loading = false;
        state.hasProfile = false;
        if (action.payload?.status_code === 404) {
          state.error = null; // Profile doesn't exist yet
        } else {
          state.error = action.payload?.detail || 'Failed to fetch profile';
        }
      })

      // Create profile
      .addCase(createProfile.pending, (state) => {
        state.updating = true;
        state.error = null;
      })
      .addCase(createProfile.fulfilled, (state, action) => {
        state.updating = false;
        state.profile = action.payload;
        state.hasProfile = true;
        state.error = null;
      })
      .addCase(createProfile.rejected, (state, action) => {
        state.updating = false;
        state.error = action.payload?.detail || 'Failed to create profile';
      })

      // Update profile
      .addCase(updateProfile.pending, (state) => {
        state.updating = true;
        state.error = null;
      })
      .addCase(updateProfile.fulfilled, (state, action) => {
        state.updating = false;
        state.profile = action.payload;
        state.error = null;
      })
      .addCase(updateProfile.rejected, (state, action) => {
        state.updating = false;
        state.error = action.payload?.detail || 'Failed to update profile';
      })

      // Update financial info
      .addCase(updateFinancialInfo.fulfilled, (state, action) => {
        state.profile = action.payload;
      })

      // Update lending preferences
      .addCase(updateLendingPreferences.fulfilled, (state, action) => {
        state.profile = action.payload;
      })

      // Update borrowing preferences
      .addCase(updateBorrowingPreferences.fulfilled, (state, action) => {
        state.profile = action.payload;
      })

      // Get profile completion
      .addCase(getProfileCompletion.fulfilled, (state, action) => {
        state.profileCompletion = action.payload;
      });
  },
});

export const {
  clearError,
  resetProfile,
  updateProfileField,
} = profileSlice.actions;

export default profileSlice.reducer;