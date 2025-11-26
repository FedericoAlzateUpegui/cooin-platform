import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';

import { logger } from '../utils/logger';
/**
 * Cross-platform secure storage utility
 * Uses SecureStore on native platforms and localStorage on web
 */
class SecureStorage {
  async setItem(key: string, value: string): Promise<void> {
    if (Platform.OS === 'web') {
      // Use localStorage on web
      try {
        localStorage.setItem(key, value);
      } catch (error) {
        logger.error('Error setting item in localStorage:', error);
        throw error;
      }
    } else {
      // Use SecureStore on native platforms
      await SecureStore.setItemAsync(key, value);
    }
  }

  async getItem(key: string): Promise<string | null> {
    if (Platform.OS === 'web') {
      // Use localStorage on web
      try {
        const value = localStorage.getItem(key);

        // Check if the value is corrupted (e.g., "[object Object]")
        if (value && value.startsWith('[object') && value.endsWith(']')) {
          logger.warn(`Corrupted data found for key "${key}". Clearing it.`);
          localStorage.removeItem(key);
          return null;
        }

        return value;
      } catch (error) {
        logger.error('Error getting item from localStorage:', error);
        return null;
      }
    } else {
      // Use SecureStore on native platforms
      return await SecureStore.getItemAsync(key);
    }
  }

  async deleteItem(key: string): Promise<void> {
    if (Platform.OS === 'web') {
      // Use localStorage on web
      try {
        localStorage.removeItem(key);
      } catch (error) {
        logger.error('Error deleting item from localStorage:', error);
      }
    } else {
      // Use SecureStore on native platforms
      await SecureStore.deleteItemAsync(key);
    }
  }
}

export const secureStorage = new SecureStorage();
