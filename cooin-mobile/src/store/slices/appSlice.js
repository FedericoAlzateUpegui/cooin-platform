/**
 * App Redux Slice (for global app state)
 */

import { createSlice } from '@reduxjs/toolkit';

// Initial state
const initialState = {
  isAppLoading: true,
  isOnboardingCompleted: false,
  theme: 'light',
  language: 'en',
  notifications: {
    enabled: true,
    pushEnabled: true,
    emailEnabled: true,
    marketing: false,
  },
  networkStatus: {
    isConnected: true,
    isInternetReachable: true,
  },
  location: {
    granted: false,
    coordinates: null,
    address: null,
  },
  biometrics: {
    available: false,
    enabled: false,
    type: null, // 'TouchID', 'FaceID', 'Fingerprint'
  },
  appState: 'active', // 'active', 'background', 'inactive'
  lastActiveTimestamp: null,
  onboardingStep: 0,
};

// App slice
const appSlice = createSlice({
  name: 'app',
  initialState,
  reducers: {
    setAppLoading: (state, action) => {
      state.isAppLoading = action.payload;
    },
    setOnboardingCompleted: (state, action) => {
      state.isOnboardingCompleted = action.payload;
    },
    setOnboardingStep: (state, action) => {
      state.onboardingStep = action.payload;
    },
    setTheme: (state, action) => {
      state.theme = action.payload;
    },
    setLanguage: (state, action) => {
      state.language = action.payload;
    },
    updateNotificationSettings: (state, action) => {
      state.notifications = { ...state.notifications, ...action.payload };
    },
    setNetworkStatus: (state, action) => {
      state.networkStatus = { ...state.networkStatus, ...action.payload };
    },
    setLocationPermission: (state, action) => {
      state.location.granted = action.payload;
    },
    setLocation: (state, action) => {
      state.location = { ...state.location, ...action.payload };
    },
    setBiometrics: (state, action) => {
      state.biometrics = { ...state.biometrics, ...action.payload };
    },
    setAppState: (state, action) => {
      state.appState = action.payload;
      if (action.payload === 'active') {
        state.lastActiveTimestamp = Date.now();
      }
    },
    resetApp: (state) => {
      return {
        ...initialState,
        isAppLoading: false,
      };
    },
  },
});

export const {
  setAppLoading,
  setOnboardingCompleted,
  setOnboardingStep,
  setTheme,
  setLanguage,
  updateNotificationSettings,
  setNetworkStatus,
  setLocationPermission,
  setLocation,
  setBiometrics,
  setAppState,
  resetApp,
} = appSlice.actions;

export default appSlice.reducer;