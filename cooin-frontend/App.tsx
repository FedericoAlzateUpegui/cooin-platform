import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { AppNavigator } from './src/navigation/AppNavigator';
import { LanguageProvider } from './src/contexts/LanguageContext';
import { COLORS } from './src/constants/config';
import './src/i18n/i18n.config'; // Initialize i18n

export default function App() {
  return (
    <SafeAreaProvider>
      <LanguageProvider>
        <StatusBar style="auto" backgroundColor={COLORS.surface} />
        <AppNavigator />
      </LanguageProvider>
    </SafeAreaProvider>
  );
}
