/**
 * Authentication Redux Slice
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { authService } from '../../services/authService';
import { secureStorage } from '../../utils/secureStorage';

// Async thunks
export const loginUser = createAsyncThunk(
  'auth/loginUser',
  async (credentials, { rejectWithValue }) => {
    try {
      const response = await authService.login(credentials);
      await secureStorage.storeTokens(response.tokens);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Login failed' });
    }
  }
);

export const registerUser = createAsyncThunk(
  'auth/registerUser',
  async (userData, { rejectWithValue }) => {
    try {
      const response = await authService.register(userData);
      await secureStorage.storeTokens(response.tokens);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Registration failed' });
    }
  }
);

export const refreshToken = createAsyncThunk(
  'auth/refreshToken',
  async (_, { rejectWithValue, getState }) => {
    try {
      const { refreshToken } = getState().auth.tokens || {};
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await authService.refreshToken(refreshToken);
      await secureStorage.storeTokens({
        accessToken: response.access_token,
        refreshToken: refreshToken, // Keep existing refresh token
      });
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Token refresh failed' });
    }
  }
);

export const getCurrentUser = createAsyncThunk(
  'auth/getCurrentUser',
  async (_, { rejectWithValue }) => {
    try {
      const response = await authService.getCurrentUser();
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to get user' });
    }
  }
);

export const logoutUser = createAsyncThunk(
  'auth/logoutUser',
  async (_, { getState }) => {
    try {
      const { tokens } = getState().auth;
      if (tokens?.refreshToken) {
        await authService.logout(tokens.refreshToken);
      }
    } catch (error) {
      // Continue with logout even if API call fails
      console.warn('Logout API call failed:', error);
    } finally {
      await secureStorage.clearTokens();
    }
  }
);

// Initial state
const initialState = {
  user: null,
  tokens: null,
  isAuthenticated: false,
  loading: false,
  error: null,
  loginAttempts: 0,
  lastLoginAttempt: null,
};

// Auth slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    resetAuth: (state) => {
      return initialState;
    },
    updateUser: (state, action) => {
      if (state.user) {
        state.user = { ...state.user, ...action.payload };
      }
    },
    incrementLoginAttempts: (state) => {
      state.loginAttempts += 1;
      state.lastLoginAttempt = new Date().toISOString();
    },
    resetLoginAttempts: (state) => {
      state.loginAttempts = 0;
      state.lastLoginAttempt = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(loginUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.tokens = action.payload.tokens;
        state.loginAttempts = 0;
        state.error = null;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.detail || 'Login failed';
        state.loginAttempts += 1;
        state.lastLoginAttempt = new Date().toISOString();
      })

      // Register
      .addCase(registerUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.tokens = action.payload.tokens;
        state.error = null;
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.detail || 'Registration failed';
      })

      // Refresh token
      .addCase(refreshToken.fulfilled, (state, action) => {
        state.tokens = {
          ...state.tokens,
          accessToken: action.payload.access_token,
        };
      })
      .addCase(refreshToken.rejected, (state) => {
        // Token refresh failed, logout user
        return initialState;
      })

      // Get current user
      .addCase(getCurrentUser.fulfilled, (state, action) => {
        state.user = action.payload;
      })

      // Logout
      .addCase(logoutUser.fulfilled, (state) => {
        return initialState;
      });
  },
});

export const {
  clearError,
  setLoading,
  resetAuth,
  updateUser,
  incrementLoginAttempts,
  resetLoginAttempts,
} = authSlice.actions;

export default authSlice.reducer;