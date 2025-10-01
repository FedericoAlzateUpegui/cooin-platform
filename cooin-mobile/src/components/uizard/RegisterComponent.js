/**
 * UizardRegisterComponent - Luxury Fintech Registration Screen
 *
 * Premium account creation with sophisticated role selection
 * Features: Elegant form design, role cards, password strength, trust elements
 *
 * Required Props:
 * - formData: { email, username, password, confirmPassword, role, agreeToTerms }
 * - onInputChange: (field: string, value: any) => void
 * - onRegister: () => void
 * - onSignIn: () => void
 * - onGoBack: () => void
 * - loading: boolean
 * - error: string | null
 * - isFormValid: boolean
 * - passwordStrength: 'weak' | 'fair' | 'strong'
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  ScrollView,
  StatusBar,
  KeyboardAvoidingView,
  Platform
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

export const UizardRegisterComponent = ({
  formData,
  onInputChange,
  onRegister,
  onSignIn,
  onGoBack,
  loading,
  error,
  isFormValid,
  passwordStrength,
}) => {
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [confirmPasswordVisible, setConfirmPasswordVisible] = useState(false);
  const [focusedField, setFocusedField] = useState(null);

  const getPasswordStrengthColor = () => {
    switch (passwordStrength) {
      case 'weak': return COLORS.ERROR;
      case 'fair': return COLORS.WARNING;
      case 'strong': return COLORS.SUCCESS;
      default: return COLORS.MEDIUM_GRAY;
    }
  };

  const getRoleConfig = (role) => {
    switch (role) {
      case 'lender':
        return {
          color: COLORS.LENDER_COLOR,
          icon: '💰',
          title: 'Lend Money',
          description: 'Earn competitive returns by lending to trusted borrowers',
          benefit: 'Competitive Returns'
        };
      case 'borrower':
        return {
          color: COLORS.BORROWER_COLOR,
          icon: '🏠',
          title: 'Borrow Money',
          description: 'Access fair-rate loans from trusted community lenders',
          benefit: 'Fair Rate Loans'
        };
      case 'both':
        return {
          color: COLORS.BOTH_COLOR,
          icon: '⚖️',
          title: 'Both',
          description: 'Maximum flexibility to both lend and borrow as needed',
          benefit: 'Complete Flexibility'
        };
      default:
        return { color: COLORS.MEDIUM_GRAY, icon: '●', title: '', description: '', benefit: '' };
    }
  };

  const getInputBorderColor = (fieldName) => {
    if (error) return COLORS.ERROR;
    if (focusedField === fieldName) return COLORS.PRIMARY;
    if (formData[fieldName] && formData[fieldName].length > 0) {
      if (fieldName === 'confirmPassword') {
        return formData.password === formData.confirmPassword ? COLORS.SUCCESS : COLORS.ERROR;
      }
      return COLORS.SUCCESS;
    }
    return COLORS.BORDER_GRAY;
  };

  const passwordsMatch = formData.password === formData.confirmPassword && formData.confirmPassword.length > 0;

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
            <View style={styles.logoContainer}>
              <View style={styles.logoCircle}>
                <Text style={styles.logoText}>₡</Text>
              </View>
            </View>
            <Text style={styles.title}>Join Cooin</Text>
            <Text style={styles.subtitle}>
              Create your premium financial network account
            </Text>
          </View>

          {/* Error Display */}
          {error && (
            <View style={styles.errorContainer}>
              <View style={styles.errorIcon}>
                <Text style={styles.errorIconText}>⚠️</Text>
              </View>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}

          {/* Form Section */}
          <View style={styles.formSection}>
            {/* Email Input */}
            <View style={styles.inputContainer}>
              <Text style={styles.inputLabel}>Email Address</Text>
              <TextInput
                style={[
                  styles.input,
                  { borderColor: getInputBorderColor('email') }
                ]}
                placeholder="Enter your email"
                placeholderTextColor={COLORS.MEDIUM_GRAY}
                value={formData.email}
                onChangeText={(text) => onInputChange('email', text)}
                onFocus={() => setFocusedField('email')}
                onBlur={() => setFocusedField(null)}
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

            {/* Username Input */}
            <View style={styles.inputContainer}>
              <Text style={styles.inputLabel}>Username</Text>
              <TextInput
                style={[
                  styles.input,
                  { borderColor: getInputBorderColor('username') }
                ]}
                placeholder="Choose a username (min 3 characters)"
                placeholderTextColor={COLORS.MEDIUM_GRAY}
                value={formData.username}
                onChangeText={(text) => onInputChange('username', text)}
                onFocus={() => setFocusedField('username')}
                onBlur={() => setFocusedField(null)}
                autoCapitalize="none"
                autoCorrect={false}
                editable={!loading}
              />
              {formData.username && formData.username.length >= 3 && (
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
                    { borderColor: getInputBorderColor('password') }
                  ]}
                  placeholder="Create a strong password (min 8 characters)"
                  placeholderTextColor={COLORS.MEDIUM_GRAY}
                  value={formData.password}
                  onChangeText={(text) => onInputChange('password', text)}
                  onFocus={() => setFocusedField('password')}
                  onBlur={() => setFocusedField(null)}
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

              {/* Password Strength Indicator */}
              {formData.password.length > 0 && (
                <View style={styles.passwordStrengthContainer}>
                  <Text style={styles.passwordStrengthLabel}>Password Strength: </Text>
                  <View style={[
                    styles.passwordStrengthBadge,
                    { backgroundColor: getPasswordStrengthColor() }
                  ]}>
                    <Text style={styles.passwordStrengthText}>
                      {passwordStrength.toUpperCase()}
                    </Text>
                  </View>
                </View>
              )}
            </View>

            {/* Confirm Password Input */}
            <View style={styles.inputContainer}>
              <Text style={styles.inputLabel}>Confirm Password</Text>
              <View style={styles.passwordContainer}>
                <TextInput
                  style={[
                    styles.input,
                    styles.passwordInput,
                    { borderColor: getInputBorderColor('confirmPassword') }
                  ]}
                  placeholder="Confirm your password"
                  placeholderTextColor={COLORS.MEDIUM_GRAY}
                  value={formData.confirmPassword}
                  onChangeText={(text) => onInputChange('confirmPassword', text)}
                  onFocus={() => setFocusedField('confirmPassword')}
                  onBlur={() => setFocusedField(null)}
                  secureTextEntry={!confirmPasswordVisible}
                  editable={!loading}
                />
                <TouchableOpacity
                  style={styles.passwordToggle}
                  onPress={() => setConfirmPasswordVisible(!confirmPasswordVisible)}
                >
                  <Text style={styles.passwordToggleText}>
                    {confirmPasswordVisible ? '🙈' : '👁️'}
                  </Text>
                </TouchableOpacity>
              </View>
              {passwordsMatch && (
                <View style={styles.validationIcon}>
                  <Text style={styles.validationText}>✓</Text>
                </View>
              )}
            </View>
          </View>

          {/* Role Selection Section */}
          <View style={styles.roleSection}>
            <Text style={styles.roleSectionTitle}>What brings you to Cooin?</Text>
            <Text style={styles.roleSectionSubtitle}>Choose your primary financial goal</Text>

            {['lender', 'borrower', 'both'].map((role) => {
              const config = getRoleConfig(role);
              const isSelected = formData.role === role;

              return (
                <TouchableOpacity
                  key={role}
                  style={[
                    styles.roleCard,
                    isSelected && styles.roleCardSelected,
                    isSelected && { borderColor: config.color }
                  ]}
                  onPress={() => onInputChange('role', role)}
                  disabled={loading}
                >
                  <LinearGradient
                    colors={isSelected ? [config.color + '20', config.color + '10'] : [COLORS.WHITE, COLORS.WHITE]}
                    style={styles.roleCardGradient}
                  >
                    <View style={styles.roleCardContent}>
                      <View style={[styles.roleIcon, { backgroundColor: config.color }]}>
                        <Text style={styles.roleIconText}>{config.icon}</Text>
                      </View>
                      <View style={styles.roleInfo}>
                        <Text style={styles.roleTitle}>{config.title}</Text>
                        <Text style={styles.roleDescription}>{config.description}</Text>
                        <View style={styles.roleBenefit}>
                          <Text style={[styles.roleBenefitText, { color: config.color }]}>
                            ✓ {config.benefit}
                          </Text>
                        </View>
                      </View>
                      {isSelected && (
                        <View style={[styles.roleSelected, { backgroundColor: config.color }]}>
                          <Text style={styles.roleSelectedText}>✓</Text>
                        </View>
                      )}
                    </View>
                  </LinearGradient>
                </TouchableOpacity>
              );
            })}
          </View>

          {/* Terms & Conditions */}
          <View style={styles.termsSection}>
            <TouchableOpacity
              style={styles.checkboxContainer}
              onPress={() => onInputChange('agreeToTerms', !formData.agreeToTerms)}
              disabled={loading}
            >
              <View style={[
                styles.checkbox,
                formData.agreeToTerms && styles.checkboxChecked
              ]}>
                {formData.agreeToTerms && <Text style={styles.checkmark}>✓</Text>}
              </View>
              <Text style={styles.checkboxLabel}>
                I agree to Cooin's{' '}
                <Text style={styles.termsLink}>Terms & Conditions</Text>
                {' '}and{' '}
                <Text style={styles.termsLink}>Privacy Policy</Text>
              </Text>
            </TouchableOpacity>
          </View>

          {/* Create Account Button */}
          <TouchableOpacity
            style={[
              styles.primaryButton,
              (!isFormValid || loading) && styles.primaryButtonDisabled
            ]}
            onPress={onRegister}
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
                <Text style={styles.primaryButtonText}>Create Account</Text>
              )}
            </LinearGradient>
          </TouchableOpacity>

          {/* Footer */}
          <View style={styles.footerSection}>
            <View style={styles.securityBadge}>
              <Text style={styles.securityText}>🔒 Your data is encrypted and secure</Text>
            </View>

            <TouchableOpacity style={styles.signInContainer} onPress={onSignIn}>
              <Text style={styles.signInText}>
                Already have an account?{' '}
                <Text style={styles.signInLink}>Sign In</Text>
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
    paddingTop: SPACING.XL,
    paddingBottom: SPACING.LG,
    alignItems: 'center',
  },
  logoContainer: {
    marginBottom: SPACING.MD,
  },
  logoCircle: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: COLORS.PRIMARY,
    justifyContent: 'center',
    alignItems: 'center',
    ...SHADOWS.CARD,
  },
  logoText: {
    fontSize: 24,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
    color: COLORS.WHITE,
  },
  title: {
    fontSize: TYPOGRAPHY.FONT_SIZE_TITLE,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
    color: COLORS.DARK_GRAY,
    marginBottom: SPACING.XS,
  },
  subtitle: {
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    color: COLORS.MEDIUM_GRAY,
    textAlign: 'center',
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

  // Form Section
  formSection: {
    marginBottom: SPACING.LG,
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

  // Password Strength
  passwordStrengthContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: SPACING.SM,
  },
  passwordStrengthLabel: {
    fontSize: TYPOGRAPHY.FONT_SIZE_SMALL,
    color: COLORS.MEDIUM_GRAY,
    marginRight: SPACING.SM,
  },
  passwordStrengthBadge: {
    paddingHorizontal: SPACING.SM,
    paddingVertical: SPACING.XS,
    borderRadius: BORDER_RADIUS.SM,
  },
  passwordStrengthText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_SMALL,
    color: COLORS.WHITE,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
  },

  // Role Selection
  roleSection: {
    marginBottom: SPACING.XL,
  },
  roleSectionTitle: {
    fontSize: TYPOGRAPHY.FONT_SIZE_HEADING,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
    color: COLORS.DARK_GRAY,
    marginBottom: SPACING.XS,
  },
  roleSectionSubtitle: {
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    color: COLORS.MEDIUM_GRAY,
    marginBottom: SPACING.LG,
  },
  roleCard: {
    borderRadius: BORDER_RADIUS.LG,
    marginBottom: SPACING.MD,
    borderWidth: 2,
    borderColor: COLORS.BORDER_GRAY,
    overflow: 'hidden',
    ...SHADOWS.CARD,
  },
  roleCardSelected: {
    ...SHADOWS.FLOATING,
  },
  roleCardGradient: {
    padding: SPACING.CARD_PADDING,
  },
  roleCardContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  roleIcon: {
    width: 48,
    height: 48,
    borderRadius: BORDER_RADIUS.LG,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.MD,
  },
  roleIconText: {
    fontSize: 20,
  },
  roleInfo: {
    flex: 1,
  },
  roleTitle: {
    fontSize: TYPOGRAPHY.FONT_SIZE_BODY,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_SEMIBOLD,
    color: COLORS.DARK_GRAY,
    marginBottom: SPACING.XS,
  },
  roleDescription: {
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    color: COLORS.MEDIUM_GRAY,
    lineHeight: TYPOGRAPHY.LINE_HEIGHT_NORMAL * TYPOGRAPHY.FONT_SIZE_CAPTION,
    marginBottom: SPACING.XS,
  },
  roleBenefit: {
    marginTop: SPACING.XS,
  },
  roleBenefitText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_SMALL,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_MEDIUM,
  },
  roleSelected: {
    width: 28,
    height: 28,
    borderRadius: 14,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: SPACING.SM,
  },
  roleSelectedText: {
    color: COLORS.WHITE,
    fontSize: 14,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
  },

  // Terms Section
  termsSection: {
    marginBottom: SPACING.XL,
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  checkbox: {
    width: 20,
    height: 20,
    borderWidth: 2,
    borderColor: COLORS.PRIMARY,
    borderRadius: BORDER_RADIUS.SM,
    marginRight: SPACING.SM,
    marginTop: 2,
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
    flex: 1,
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    color: COLORS.DARK_GRAY,
    lineHeight: TYPOGRAPHY.LINE_HEIGHT_NORMAL * TYPOGRAPHY.FONT_SIZE_CAPTION,
  },
  termsLink: {
    color: COLORS.PRIMARY,
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

  // Footer Section
  footerSection: {
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
  signInContainer: {
    paddingVertical: SPACING.MD,
  },
  signInText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    color: COLORS.MEDIUM_GRAY,
  },
  signInLink: {
    color: COLORS.PRIMARY,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_SEMIBOLD,
  },
});