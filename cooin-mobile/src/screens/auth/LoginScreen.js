/**
 * Login Screen
 *
 * NOTE: This is a container with business logic.
 * The actual UI components will be created with Uizard.
 *
 * Uizard will need to create:
 * - Email input field
 * - Password input field
 * - "Remember me" checkbox
 * - "Sign In" button
 * - "Forgot Password?" link
 * - "Don't have an account? Sign Up" link
 * - Loading state
 * - Error display
 */

import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  SafeAreaView,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigation } from '@react-navigation/native';
import Toast from 'react-native-toast-message';

// Redux actions
import { loginUser, clearError } from '../../store/slices/authSlice';

// This will be replaced with Uizard components
import { UizardLoginComponent } from '../../components/uizard/LoginComponent';

const LoginScreen = () => {
  const navigation = useNavigation();
  const dispatch = useDispatch();

  // Redux state
  const { loading, error } = useSelector((state) => state.auth);

  // Local state
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false,
  });

  // Form handlers
  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));

    // Clear error when user starts typing
    if (error) {
      dispatch(clearError());
    }
  };

  const handleLogin = async () => {
    try {
      const result = await dispatch(loginUser({
        email: formData.email.toLowerCase().trim(),
        password: formData.password,
        remember_me: formData.rememberMe,
      })).unwrap();

      Toast.show({
        type: 'success',
        text1: 'Welcome back!',
        text2: 'You have successfully signed in.',
      });

      // Navigation will be handled by RootNavigator based on auth state
    } catch (error) {
      Toast.show({
        type: 'error',
        text1: 'Sign In Failed',
        text2: error.detail || 'Please check your credentials and try again.',
      });
    }
  };

  // Navigation handlers
  const handleForgotPassword = () => {
    navigation.navigate('ForgotPassword');
  };

  const handleSignUp = () => {
    navigation.navigate('Register');
  };

  const handleGoBack = () => {
    navigation.goBack();
  };

  // Form validation
  const isFormValid = () => {
    return (
      formData.email.trim().length > 0 &&
      formData.password.length >= 6 &&
      formData.email.includes('@')
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        style={styles.keyboardView}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
        {/*
          TODO: Replace with Uizard component
          The Uizard component should receive these props:
          - formData: formData
          - onInputChange: handleInputChange
          - onLogin: handleLogin
          - onForgotPassword: handleForgotPassword
          - onSignUp: handleSignUp
          - onGoBack: handleGoBack
          - loading: loading
          - error: error
          - isFormValid: isFormValid()
        */}
        <UizardLoginComponent
          formData={formData}
          onInputChange={handleInputChange}
          onLogin={handleLogin}
          onForgotPassword={handleForgotPassword}
          onSignUp={handleSignUp}
          onGoBack={handleGoBack}
          loading={loading}
          error={error}
          isFormValid={isFormValid()}
        />
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
});

export default LoginScreen;