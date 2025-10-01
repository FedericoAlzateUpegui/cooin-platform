/**
 * Register Screen
 *
 * NOTE: This is a container with business logic.
 * The actual UI components will be created with Uizard.
 *
 * Uizard will need to create:
 * - Email input field
 * - Username input field
 * - Password input field
 * - Confirm password input field
 * - Role selection (Lender/Borrower/Both)
 * - "Agree to terms" checkbox
 * - "Create Account" button
 * - "Already have an account? Sign In" link
 * - Loading state
 * - Error display
 * - Password strength indicator
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
import { registerUser, clearError } from '../../store/slices/authSlice';

// This will be replaced with Uizard components
import { UizardRegisterComponent } from '../../components/uizard/RegisterComponent';

const RegisterScreen = () => {
  const navigation = useNavigation();
  const dispatch = useDispatch();

  // Redux state
  const { loading, error } = useSelector((state) => state.auth);

  // Local state
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    role: 'borrower', // 'lender', 'borrower', 'both'
    agreeToTerms: false,
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

  const handleRegister = async () => {
    try {
      // Validate passwords match
      if (formData.password !== formData.confirmPassword) {
        Toast.show({
          type: 'error',
          text1: 'Password Mismatch',
          text2: 'Passwords do not match. Please try again.',
        });
        return;
      }

      const result = await dispatch(registerUser({
        email: formData.email.toLowerCase().trim(),
        username: formData.username.trim(),
        password: formData.password,
        confirm_password: formData.confirmPassword,
        role: formData.role,
        agree_to_terms: formData.agreeToTerms,
      })).unwrap();

      Toast.show({
        type: 'success',
        text1: 'Account Created!',
        text2: 'Welcome to Cooin! Let\\'s set up your profile.',
      });

      // Navigation will be handled by RootNavigator based on auth state
    } catch (error) {
      Toast.show({
        type: 'error',
        text1: 'Registration Failed',
        text2: error.detail || 'Please check your information and try again.',
      });
    }
  };

  // Navigation handlers
  const handleSignIn = () => {
    navigation.navigate('Login');
  };

  const handleGoBack = () => {
    navigation.goBack();
  };

  // Form validation
  const isFormValid = () => {
    return (
      formData.email.trim().length > 0 &&
      formData.username.trim().length >= 3 &&
      formData.password.length >= 8 &&
      formData.confirmPassword.length >= 8 &&
      formData.password === formData.confirmPassword &&
      formData.email.includes('@') &&
      formData.agreeToTerms
    );
  };

  // Password strength validation
  const getPasswordStrength = () => {
    const password = formData.password;
    if (password.length < 6) return 'weak';
    if (password.length < 8) return 'fair';
    if (password.match(/(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])/)) return 'strong';
    return 'fair';
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
          - onRegister: handleRegister
          - onSignIn: handleSignIn
          - onGoBack: handleGoBack
          - loading: loading
          - error: error
          - isFormValid: isFormValid()
          - passwordStrength: getPasswordStrength()
        */}
        <UizardRegisterComponent
          formData={formData}
          onInputChange={handleInputChange}
          onRegister={handleRegister}
          onSignIn={handleSignIn}
          onGoBack={handleGoBack}
          loading={loading}
          error={error}
          isFormValid={isFormValid()}
          passwordStrength={getPasswordStrength()}
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

export default RegisterScreen;