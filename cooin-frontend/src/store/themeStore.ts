import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

type ThemeMode = 'light' | 'dark';

interface ThemeState {
  mode: ThemeMode;
  setMode: (mode: ThemeMode) => void;
  toggleMode: () => void;
  loadTheme: () => Promise<void>;
}

const THEME_STORAGE_KEY = '@cooin_theme';

export const useThemeStore = create<ThemeState>((set, get) => ({
  mode: 'light',

  setMode: async (mode: ThemeMode) => {
    set({ mode });
    try {
      await AsyncStorage.setItem(THEME_STORAGE_KEY, mode);
    } catch (error) {
      console.error('Failed to save theme:', error);
    }
  },

  toggleMode: () => {
    const newMode = get().mode === 'light' ? 'dark' : 'light';
    get().setMode(newMode);
  },

  loadTheme: async () => {
    try {
      const saved = await AsyncStorage.getItem(THEME_STORAGE_KEY);
      if (saved === 'dark' || saved === 'light') {
        set({ mode: saved });
      }
    } catch (error) {
      console.error('Failed to load theme:', error);
    }
  },
}));
