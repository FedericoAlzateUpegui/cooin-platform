import React, { useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { AppNavigator } from './src/navigation/AppNavigator';
import { LanguageProvider } from './src/contexts/LanguageContext';
import { ErrorBoundary } from './src/components/ErrorBoundary';
import { useThemeStore } from './src/store/themeStore';
import { useColors } from './src/hooks/useColors';
import './src/i18n/i18n.config'; // Initialize i18n

export default function App() {
  const loadTheme = useThemeStore((state) => state.loadTheme);
  const isDark = useThemeStore((state) => state.mode === 'dark');
  const colors = useColors();

  useEffect(() => {
    loadTheme();
  }, [loadTheme]);

  return (
    <ErrorBoundary>
      <SafeAreaProvider>
        <LanguageProvider>
          <StatusBar style={isDark ? 'light' : 'dark'} backgroundColor={colors.surface} />
          <AppNavigator />
        </LanguageProvider>
      </SafeAreaProvider>
    </ErrorBoundary>
  );
}
