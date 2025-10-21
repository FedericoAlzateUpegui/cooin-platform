import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';

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
        console.error('Error setting item in localStorage:', error);
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
        return localStorage.getItem(key);
      } catch (error) {
        console.error('Error getting item from localStorage:', error);
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
        console.error('Error deleting item from localStorage:', error);
      }
    } else {
      // Use SecureStore on native platforms
      await SecureStore.deleteItemAsync(key);
    }
  }
}

export const secureStorage = new SecureStorage();
