/**
 * UizardLoginComponent - Luxury Fintech Login Screen
 *
 * Premium authentication experience with trust elements
 * Features: Elegant form design, biometric hints, security indicators
 *
 * Required Props:
 * - formData: { email: string, password: string, rememberMe: boolean }
 * - onInputChange: (field: string, value: any) => void
 * - onLogin: () => void
 * - onForgotPassword: () => void
 * - onSignUp: () => void
 * - onGoBack: () => void
 * - loading: boolean
 * - error: string | null
 * - isFormValid: boolean
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  StatusBar,
  KeyboardAvoidingView,
  Platform,
  ScrollView
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

export const UizardLoginComponent = ({
  formData,
  onInputChange,
  onLogin,
  onForgotPassword,
  onSignUp,
  onGoBack,
  loading,
  error,
  isFormValid,
}) => {
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [emailFocused, setEmailFocused] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);

  const getInputBorderColor = (fieldName, focused) => {
    if (error) return COLORS.ERROR;
    if (focused) return COLORS.PRIMARY;
    if (formData[fieldName] && formData[fieldName].length > 0) return COLORS.SUCCESS;
    return COLORS.BORDER_GRAY;
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor={COLORS.WHITE} />

      <KeyboardAvoidingView
        style={styles.keyboardView}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        >
          {/* Header Section */}
          <View style={styles.headerSection}>
            {/* Logo */}
            <View style={styles.logoContainer}>
              <View style={styles.logoCircle}>
                <Text style={styles.logoText}>₡</Text>
              </View>
            </View>

            {/* Welcome Text */}
            <Text style={styles.title}>Welcome Back</Text>
            <Text style={styles.subtitle}>
              Sign in to access your premium financial network
            </Text>
          </View>

          {/* Form Section */}
          <View style={styles.formSection}>
            {/* Error Display */}
            {error && (
              <View style={styles.errorContainer}>
                <View style={styles.errorIcon}>
                  <Text style={styles.errorIconText}>⚠️</Text>
                </View>
                <Text style={styles.errorText}>{error}</Text>
              </View>
            )}

            {/* Email Input */}
            <View style={styles.inputContainer}>
              <Text style={styles.inputLabel}>Email Address</Text>
              <TextInput
                style={[
                  styles.input,
                  { borderColor: getInputBorderColor('email', emailFocused) }
                ]}
                placeholder="Enter your email"
                placeholderTextColor={COLORS.MEDIUM_GRAY}
                value={formData.email}
                onChangeText={(text) => onInputChange('email', text)}
                onFocus={() => setEmailFocused(true)}
                onBlur={() => setEmailFocused(false)}
                keyboardType="email-address"
                autoCapitalize="none"
                autoCorrect={false}
                editable={!loading}
              />
              {formData.email && formData.email.includes('@') && (
                <View style={styles.validationIcon}>
                  <Text style={styles.validationText}>✓</Text>
                </View>
              )}
            </View>

            {/* Password Input */}
            <View style={styles.inputContainer}>
              <Text style={styles.inputLabel}>Password</Text>
              <View style={styles.passwordContainer}>
                <TextInput
                  style={[
                    styles.input,
                    styles.passwordInput,
                    { borderColor: getInputBorderColor('password', passwordFocused) }
                  ]}
                  placeholder="Enter your password"
                  placeholderTextColor={COLORS.MEDIUM_GRAY}
                  value={formData.password}
                  onChangeText={(text) => onInputChange('password', text)}
                  onFocus={() => setPasswordFocused(true)}
                  onBlur={() => setPasswordFocused(false)}
                  secureTextEntry={!passwordVisible}
                  editable={!loading}
                />
                <TouchableOpacity
                  style={styles.passwordToggle}
                  onPress={() => setPasswordVisible(!passwordVisible)}
                >
                  <Text style={styles.passwordToggleText}>
                    {passwordVisible ? '🙈' : '👁️'}
                  </Text>
                </TouchableOpacity>
              </View>
            </View>

            {/* Remember Me & Biometric Hint */}
            <View style={styles.optionsContainer}>
              <TouchableOpacity
                style={styles.checkboxContainer}
                onPress={() => onInputChange('rememberMe', !formData.rememberMe)}
                disabled={loading}
              >
                <View style={[
                  styles.checkbox,
                  formData.rememberMe && styles.checkboxChecked
                ]}>
                  {formData.rememberMe && <Text style={styles.checkmark}>✓</Text>}
                </View>
                <Text style={styles.checkboxLabel}>Remember me</Text>
              </TouchableOpacity>

              <View style={styles.biometricHint}>
                <Text style={styles.biometricText}>🔐</Text>
                <Text style={styles.biometricLabel}>Biometric available</Text>
              </View>
            </View>

            {/* Login Button */}
            <TouchableOpacity
              style={[
                styles.primaryButton,
                (!isFormValid || loading) && styles.primaryButtonDisabled
              ]}
              onPress={onLogin}
              disabled={!isFormValid || loading}
            >
              <LinearGradient
                colors={
                  !isFormValid || loading
                    ? [COLORS.MEDIUM_GRAY, COLORS.MEDIUM_GRAY]
                    : [COLORS.PRIMARY, COLORS.PRIMARY_DARK]
                }
                style={styles.primaryButtonGradient}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
              >
                {loading ? (
                  <ActivityIndicator color={COLORS.WHITE} size="small" />
                ) : (
                  <Text style={styles.primaryButtonText}>Sign In</Text>
                )}
              </LinearGradient>
            </TouchableOpacity>

            {/* Forgot Password */}
            <TouchableOpacity style={styles.linkButton} onPress={onForgotPassword}>
              <Text style={styles.forgotPasswordText}>Forgot your password?</Text>
            </TouchableOpacity>
          </View>

          {/* Footer Section */}
          <View style={styles.footerSection}>
            {/* Security Badge */}
            <View style={styles.securityBadge}>
              <Text style={styles.securityText}>🔒 Secured with 256-bit encryption</Text>
            </View>

            {/* Sign Up Link */}
            <TouchableOpacity style={styles.signUpContainer} onPress={onSignUp}>
              <Text style={styles.signUpText}>
                Don't have an account?{' '}
                <Text style={styles.signUpLink}>Join Cooin</Text>
              </Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.WHITE,
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    paddingHorizontal: SPACING.SCREEN_PADDING,
  },

  // Header Section
  headerSection: {
    paddingTop: SPACING.XXL,
    paddingBottom: SPACING.XL,
    alignItems: 'center',
  },
  logoContainer: {
    marginBottom: SPACING.LG,
  },
  logoCircle: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: COLORS.PRIMARY,
    justifyContent: 'center',
    alignItems: 'center',
    ...SHADOWS.CARD,
  },
  logoText: {
    fontSize: 28,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
    color: COLORS.WHITE,
  },
  title: {
    fontSize: TYPOGRAPHY.FONT_SIZE_TITLE,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
    color: COLORS.DARK_GRAY,
    marginBottom: SPACING.SM,
  },
  subtitle: {
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    color: COLORS.MEDIUM_GRAY,
    textAlign: 'center',
    lineHeight: TYPOGRAPHY.LINE_HEIGHT_RELAXED * TYPOGRAPHY.FONT_SIZE_CAPTION,
  },

  // Form Section
  formSection: {
    flex: 1,
    paddingBottom: SPACING.LG,
  },

  // Error Display
  errorContainer: {
    flexDirection: 'row',
    backgroundColor: COLORS.ERROR + '10',
    borderLeftWidth: 4,
    borderLeftColor: COLORS.ERROR,
    padding: SPACING.MD,
    borderRadius: BORDER_RADIUS.MD,
    marginBottom: SPACING.LG,
    alignItems: 'center',
  },
  errorIcon: {
    marginRight: SPACING.SM,
  },
  errorIconText: {
    fontSize: 20,
  },
  errorText: {
    flex: 1,
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    color: COLORS.ERROR,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_MEDIUM,
  },

  // Input Styling
  inputContainer: {
    marginBottom: SPACING.LG,
    position: 'relative',
  },
  inputLabel: {
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_MEDIUM,
    color: COLORS.DARK_GRAY,
    marginBottom: SPACING.SM,
  },
  input: {
    backgroundColor: COLORS.WHITE,
    height: SPACING.INPUT_HEIGHT,
    borderRadius: BORDER_RADIUS.MD,
    borderWidth: 2,
    paddingHorizontal: SPACING.MD,
    fontSize: TYPOGRAPHY.FONT_SIZE_BODY,
    color: COLORS.DARK_GRAY,
    ...SHADOWS.CARD,
  },
  passwordContainer: {
    position: 'relative',
  },
  passwordInput: {
    paddingRight: 50,
  },
  passwordToggle: {
    position: 'absolute',
    right: SPACING.MD,
    top: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
    width: 30,
  },
  passwordToggleText: {
    fontSize: 18,
  },
  validationIcon: {
    position: 'absolute',
    right: SPACING.MD,
    top: 35,
    backgroundColor: COLORS.SUCCESS,
    borderRadius: 10,
    width: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  validationText: {
    color: COLORS.WHITE,
    fontSize: 12,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
  },

  // Options Container
  optionsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.XL,
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  checkbox: {
    width: 20,
    height: 20,
    borderWidth: 2,
    borderColor: COLORS.PRIMARY,
    borderRadius: BORDER_RADIUS.SM,
    marginRight: SPACING.SM,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxChecked: {
    backgroundColor: COLORS.PRIMARY,
  },
  checkmark: {
    color: COLORS.WHITE,
    fontSize: 12,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
  },
  checkboxLabel: {
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    color: COLORS.DARK_GRAY,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_MEDIUM,
  },
  biometricHint: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  biometricText: {
    fontSize: 16,
    marginRight: SPACING.XS,
  },
  biometricLabel: {
    fontSize: TYPOGRAPHY.FONT_SIZE_SMALL,
    color: COLORS.SUCCESS,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_MEDIUM,
  },

  // Primary Button
  primaryButton: {
    borderRadius: BORDER_RADIUS.MD,
    marginBottom: SPACING.LG,
    ...SHADOWS.BUTTON,
  },
  primaryButtonDisabled: {
    opacity: 0.6,
  },
  primaryButtonGradient: {
    height: SPACING.BUTTON_HEIGHT,
    borderRadius: BORDER_RADIUS.MD,
    justifyContent: 'center',
    alignItems: 'center',
  },
  primaryButtonText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_BODY,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_SEMIBOLD,
    color: COLORS.WHITE,
    letterSpacing: 0.5,
  },

  // Links
  linkButton: {
    alignItems: 'center',
    paddingVertical: SPACING.SM,
  },
  forgotPasswordText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    color: COLORS.PRIMARY,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_MEDIUM,
  },

  // Footer Section
  footerSection: {
    paddingTop: SPACING.LG,
    paddingBottom: SPACING.XL,
    alignItems: 'center',
  },
  securityBadge: {
    marginBottom: SPACING.LG,
  },
  securityText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_SMALL,
    color: COLORS.MEDIUM_GRAY,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_MEDIUM,
  },
  signUpContainer: {
    paddingVertical: SPACING.MD,
  },
  signUpText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    color: COLORS.MEDIUM_GRAY,
  },
  signUpLink: {
    color: COLORS.PRIMARY,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_SEMIBOLD,
  },
});