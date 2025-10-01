/**
 * Root Navigator
 */

import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { createStackNavigator } from '@react-navigation/stack';

// Redux actions
import { setAppLoading } from '../store/slices/appSlice';
import { getCurrentUser } from '../store/slices/authSlice';
import { getProfile } from '../store/slices/profileSlice';

// Navigators
import AuthNavigator from './AuthNavigator';
import MainNavigator from './MainNavigator';
import OnboardingNavigator from './OnboardingNavigator';

// Components
import LoadingScreen from '../components/LoadingScreen';
import SplashScreen from '../screens/SplashScreen';

const Stack = createStackNavigator();

const RootNavigator = () => {
  const dispatch = useDispatch();

  const { isAppLoading, isOnboardingCompleted } = useSelector((state) => state.app);
  const { isAuthenticated, user } = useSelector((state) => state.auth);
  const { hasProfile } = useSelector((state) => state.profile);

  useEffect(() => {
    const initializeApp = async () => {
      try {
        // If user is authenticated, get current user and profile
        if (isAuthenticated) {
          await Promise.all([
            dispatch(getCurrentUser()),
            dispatch(getProfile()),
          ]);
        }
      } catch (error) {
        console.error('App initialization error:', error);
      } finally {
        // Set app as loaded after 2 seconds minimum (for splash screen)
        setTimeout(() => {
          dispatch(setAppLoading(false));
        }, 2000);
      }
    };

    initializeApp();
  }, [dispatch, isAuthenticated]);

  // Show splash screen while app is loading
  if (isAppLoading) {
    return <SplashScreen />;
  }

  // Determine which navigator to show
  const getNavigator = () => {
    if (!isAuthenticated) {
      return <AuthNavigator />;
    }

    if (!isOnboardingCompleted || !hasProfile) {
      return <OnboardingNavigator />;
    }

    return <MainNavigator />;
  };

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Root" component={() => getNavigator()} />
    </Stack.Navigator>
  );
};

export default RootNavigator;