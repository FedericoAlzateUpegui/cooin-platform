/**
 * Secure Storage Utility
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import Keychain from 'react-native-keychain';

const STORAGE_KEYS = {
  TOKENS: 'cooin_tokens',
  USER_PREFERENCES: 'cooin_user_preferences',
  ONBOARDING: 'cooin_onboarding_completed',
  BIOMETRIC_ENABLED: 'cooin_biometric_enabled',
};

class SecureStorage {
  // Token management (secure)
  async storeTokens(tokens) {
    try {
      const tokenString = JSON.stringify(tokens);
      await Keychain.setInternetCredentials(
        STORAGE_KEYS.TOKENS,
        'cooin_user',
        tokenString
      );
      return true;
    } catch (error) {
      console.error('Failed to store tokens:', error);
      // Fallback to AsyncStorage if Keychain fails
      try {
        await AsyncStorage.setItem(STORAGE_KEYS.TOKENS, JSON.stringify(tokens));
        return true;
      } catch (fallbackError) {
        console.error('Failed to store tokens in AsyncStorage:', fallbackError);
        return false;
      }
    }
  }

  async getTokens() {
    try {
      const credentials = await Keychain.getInternetCredentials(STORAGE_KEYS.TOKENS);
      if (credentials && credentials.password) {
        return JSON.parse(credentials.password);
      }
      return null;
    } catch (error) {
      console.error('Failed to get tokens:', error);
      // Fallback to AsyncStorage
      try {
        const tokens = await AsyncStorage.getItem(STORAGE_KEYS.TOKENS);
        return tokens ? JSON.parse(tokens) : null;
      } catch (fallbackError) {
        console.error('Failed to get tokens from AsyncStorage:', fallbackError);
        return null;
      }
    }
  }

  async clearTokens() {
    try {
      await Keychain.resetInternetCredentials(STORAGE_KEYS.TOKENS);
      await AsyncStorage.removeItem(STORAGE_KEYS.TOKENS);
      return true;
    } catch (error) {
      console.error('Failed to clear tokens:', error);
      return false;
    }
  }

  // Regular storage (non-sensitive data)
  async setItem(key, value) {
    try {
      const stringValue = typeof value === 'string' ? value : JSON.stringify(value);
      await AsyncStorage.setItem(key, stringValue);
      return true;
    } catch (error) {
      console.error(`Failed to store item ${key}:`, error);
      return false;
    }
  }

  async getItem(key) {
    try {
      const value = await AsyncStorage.getItem(key);
      if (value !== null) {
        try {
          return JSON.parse(value);
        } catch {
          return value; // Return as string if not JSON
        }
      }
      return null;
    } catch (error) {
      console.error(`Failed to get item ${key}:`, error);
      return null;
    }
  }

  async removeItem(key) {
    try {
      await AsyncStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error(`Failed to remove item ${key}:`, error);
      return false;
    }
  }

  async clear() {
    try {
      await AsyncStorage.clear();
      await Keychain.resetInternetCredentials(STORAGE_KEYS.TOKENS);
      return true;
    } catch (error) {
      console.error('Failed to clear storage:', error);
      return false;
    }
  }

  // User preferences
  async storeUserPreferences(preferences) {
    return this.setItem(STORAGE_KEYS.USER_PREFERENCES, preferences);
  }

  async getUserPreferences() {
    return this.getItem(STORAGE_KEYS.USER_PREFERENCES);
  }

  // Onboarding status
  async setOnboardingCompleted(completed = true) {
    return this.setItem(STORAGE_KEYS.ONBOARDING, completed);
  }

  async isOnboardingCompleted() {
    return this.getItem(STORAGE_KEYS.ONBOARDING) || false;
  }

  // Biometric settings
  async setBiometricEnabled(enabled = true) {
    return this.setItem(STORAGE_KEYS.BIOMETRIC_ENABLED, enabled);
  }

  async isBiometricEnabled() {
    return this.getItem(STORAGE_KEYS.BIOMETRIC_ENABLED) || false;
  }

  // Check if storage is available
  async isAvailable() {
    try {
      await AsyncStorage.setItem('test_key', 'test_value');
      await AsyncStorage.removeItem('test_key');
      return true;
    } catch (error) {
      return false;
    }
  }

  // Get storage info
  async getStorageInfo() {
    try {
      const keys = await AsyncStorage.getAllKeys();
      return {
        totalKeys: keys.length,
        keys: keys,
        keychainAvailable: await Keychain.getSupportedBiometryType() !== null,
      };
    } catch (error) {
      console.error('Failed to get storage info:', error);
      return null;
    }
  }
}

export const secureStorage = new SecureStorage();