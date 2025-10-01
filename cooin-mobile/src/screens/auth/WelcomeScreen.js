/**
 * Welcome Screen - First screen users see
 *
 * NOTE: This is a container with business logic.
 * The actual UI components will be created with Uizard.
 *
 * Uizard will need to create:
 * - Welcome hero section with Cooin branding
 * - "Get Started" button
 * - "Already have an account? Sign In" button
 * - App features showcase (optional)
 */

import React from 'react';
import {
  View,
  StyleSheet,
  SafeAreaView,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';

// This will be replaced with Uizard components
import { UizardWelcomeComponent } from '../../components/uizard/WelcomeComponent';

const WelcomeScreen = () => {
  const navigation = useNavigation();

  // Navigation handlers
  const handleGetStarted = () => {
    navigation.navigate('Register');
  };

  const handleSignIn = () => {
    navigation.navigate('Login');
  };

  return (
    <SafeAreaView style={styles.container}>
      {/*
        TODO: Replace with Uizard component
        The Uizard component should receive these props:
        - onGetStarted: handleGetStarted
        - onSignIn: handleSignIn
      */}
      <UizardWelcomeComponent
        onGetStarted={handleGetStarted}
        onSignIn={handleSignIn}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default WelcomeScreen;