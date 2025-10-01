/**
 * Main App Component
 */

import React, { useEffect } from 'react';
import { StatusBar, LogBox } from 'react-native';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { NavigationContainer } from '@react-navigation/native';
import { Provider as PaperProvider } from 'react-native-paper';
import Toast from 'react-native-toast-message';

// Store
import { store, persistor } from './store';

// Navigation
import RootNavigator from './navigation/RootNavigator';

// Theme
import { THEME } from './constants/theme';

// Components
import LoadingScreen from './components/LoadingScreen';
import { toastConfig } from './utils/toastConfig';

// Ignore specific warnings in development
if (__DEV__) {
  LogBox.ignoreLogs([
    'VirtualizedLists should never be nested',
    'Warning: Each child in a list should have a unique "key" prop',
  ]);
}

const App = () => {
  useEffect(() => {
    // Any app initialization logic
    console.log('Cooin app started');
  }, []);

  return (
    <Provider store={store}>
      <PersistGate loading={<LoadingScreen />} persistor={persistor}>
        <PaperProvider theme={THEME}>
          <NavigationContainer>
            <StatusBar
              barStyle="dark-content"
              backgroundColor={THEME.colors.WHITE}
              translucent={false}
            />
            <RootNavigator />
            <Toast config={toastConfig} />
          </NavigationContainer>
        </PaperProvider>
      </PersistGate>
    </Provider>
  );
};

export default App;