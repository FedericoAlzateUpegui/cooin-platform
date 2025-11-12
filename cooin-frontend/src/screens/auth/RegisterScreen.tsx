import React, { useState, useEffect, useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  useWindowDimensions,
  Platform,
} from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Ionicons } from '@expo/vector-icons';
import { useAuthStore } from '../../store/authStore';
import { Input } from '../../components/Input';
import { Button } from '../../components/Button';
import { LanguageSwitcher } from '../../components/LanguageSwitcher';
import { useLanguage } from '../../contexts/LanguageContext';
import { COLORS, SPACING, FONTS } from '../../constants/config';

// Type for form data (will be inferred from schema)
type RegisterFormData = {
  email: string;
  username: string;
  password: string;
  confirmPassword: string;
};

interface RegisterScreenProps {
  navigation: any;
}

export const RegisterScreen: React.FC<RegisterScreenProps> = ({ navigation }) => {
  const [selectedRole, setSelectedRole] = useState<'lender' | 'borrower' | 'both'>('borrower');
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);
  const { register, isLoading, isAuthenticated, logout } = useAuthStore();
  const { width } = useWindowDimensions();
  const { t } = useLanguage();

  // Create schema with translated messages - recreates when language changes
  const registerSchema = useMemo(() => {
    return z.object({
      email: z.string()
        .min(1, t('validation.email_required'))
        .email(t('validation.email_invalid')),
      username: z.string()
        .min(3, t('validation.username_min'))
        .max(30, t('validation.username_max')),
      password: z.string()
        .min(8, t('validation.password_too_short')),
      confirmPassword: z.string()
        .min(1, t('validation.confirm_password_required')),
    }).refine((data) => data.password === data.confirmPassword, {
      message: t('validation.passwords_must_match'),
      path: ["confirmPassword"],
    });
  }, [t]);

  // Safety check: if there's a local error, make sure we're not authenticated
  useEffect(() => {
    if (localError && isAuthenticated) {
      console.log('ERROR: User authenticated despite error! Forcing logout...');
      logout();
    }
  }, [localError, isAuthenticated, logout]);

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    mode: 'onBlur',
    reValidateMode: 'onBlur',
    defaultValues: {
      email: '',
      username: '',
      password: '',
      confirmPassword: '',
    },
  });

  // Helper function to map backend errors to translated messages
  const getTranslatedErrorMessage = (error: any): string => {
    console.error('Registration error FULL OBJECT:', JSON.stringify(error, null, 2));
    console.error('Registration error detail:', error.detail);
    console.error('Registration error message:', error.message);
    console.error('Registration error status_code:', error.status_code);

    // Extract the raw error message
    const rawError = error.detail || error.message || '';

    // Map common backend error messages to translation keys
    const errorMappings: Record<string, string> = {
      'An account with this email already exists': 'validation.email_already_exists',
      'This username is already taken': 'validation.username_already_exists',
      'Username can only contain letters, numbers, underscores, and hyphens': 'validation.username_invalid',
      'Value error, Username can only contain letters, numbers, underscores, and hyphens': 'validation.value_error_username',
      'Password must contain at least one uppercase letter, one lowercase letter, and one number': 'validation.password_weak',
      'Password must be at least 8 characters long': 'validation.password_too_short',
      'Password confirmation does not match password': 'validation.passwords_must_match',
      'Registration failed': 'validation.registration_failed',
    };

    // Check for exact matches
    if (errorMappings[rawError]) {
      return t(errorMappings[rawError]);
    }

    // Check for partial matches
    const lowerError = rawError.toLowerCase();
    if (lowerError.includes('email already exists') || lowerError.includes('email') && lowerError.includes('exists')) {
      return t('validation.email_already_exists');
    }
    if (lowerError.includes('username') && lowerError.includes('taken')) {
      return t('validation.username_already_exists');
    }
    if (lowerError.includes('username') && (lowerError.includes('letters') || lowerError.includes('contain'))) {
      return t('validation.username_invalid');
    }
    if (lowerError.includes('password') && lowerError.includes('uppercase')) {
      return t('validation.password_weak');
    }
    if (lowerError.includes('passwords') && lowerError.includes('match')) {
      return t('validation.passwords_must_match');
    }

    // If no mapping found, return the original message or a generic error
    return rawError || t('validation.backend_error');
  };

  const onSubmit = async (data: RegisterFormData) => {
    if (!agreedToTerms) {
      setLocalError(t('validation.terms_required'));
      return;
    }

    try {
      // Clear any previous errors
      setLocalError(null);

      // Attempt registration
      await register(data.email, data.username, data.password, data.confirmPassword, selectedRole, agreedToTerms);
      // If successful, navigation will be handled by the auth flow
    } catch (error: any) {
      // Get translated error message
      const translatedError = getTranslatedErrorMessage(error);

      // Set local error to display
      setLocalError(translatedError);

      // Prevent any navigation by not re-throwing the error
      return; // Explicitly return to prevent any further execution
    }
  };

  const handleLoginPress = () => {
    navigation.navigate('Login');
  };

  // Responsive width calculation
  const getResponsiveWidth = () => {
    if (width < 768) {
      // Mobile: full width with padding
      return '100%';
    } else if (width < 1024) {
      // Tablet: 80% width
      return '80%';
    } else {
      // Desktop: fixed max width
      return Math.min(600, width * 0.4);
    }
  };

  const responsiveWidth = getResponsiveWidth();

  const roleOptions = [
    {
      key: 'borrower' as const,
      title: t('register.role_borrower_title'),
      description: t('register.role_borrower_description'),
    },
    {
      key: 'lender' as const,
      title: t('register.role_lender_title'),
      description: t('register.role_lender_description'),
    },
    {
      key: 'both' as const,
      title: t('register.role_both_title'),
      description: t('register.role_both_description'),
    },
  ];

  return (
    <View style={styles.container}>
      <View style={styles.languageSwitcherContainer}>
        <LanguageSwitcher variant="button" />
      </View>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
        showsVerticalScrollIndicator={true}
      >
        <View style={[styles.header, { width: responsiveWidth }]}>
          <Text style={styles.title}>{t('register.join_cooin')}</Text>
          <Text style={styles.subtitle}>
            {t('register.create_account_subtitle')}
          </Text>
        </View>

        <View style={[styles.form, { width: responsiveWidth }]}>
          <Controller
            control={control}
            name="email"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label={t('common.email')}
                placeholder={t('register.email_placeholder')}
                value={value}
                onChangeText={onChange}
                onBlur={onBlur}
                error={errors.email?.message}
                keyboardType="email-address"
                autoCapitalize="none"
                autoComplete="email"
                leftIcon="mail"
              />
            )}
          />

          <Controller
            control={control}
            name="username"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label={t('register.username')}
                placeholder={t('register.username_placeholder')}
                value={value}
                onChangeText={onChange}
                onBlur={onBlur}
                error={errors.username?.message}
                autoCapitalize="none"
                autoComplete="username"
                leftIcon="person"
              />
            )}
          />

          <Controller
            control={control}
            name="password"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label={t('common.password')}
                placeholder={t('register.password_placeholder')}
                value={value}
                onChangeText={onChange}
                onBlur={onBlur}
                error={errors.password?.message}
                isPassword
                leftIcon="lock-closed"
              />
            )}
          />

          <Controller
            control={control}
            name="confirmPassword"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label={t('register.confirm_password')}
                placeholder={t('register.confirm_password_placeholder')}
                value={value}
                onChangeText={onChange}
                onBlur={onBlur}
                error={errors.confirmPassword?.message}
                isPassword
                leftIcon="lock-closed"
              />
            )}
          />

          <View style={styles.roleSection}>
            <Text style={styles.roleLabel}>{t('register.interested_in')}</Text>
            {roleOptions.map((option) => (
              <TouchableOpacity
                key={option.key}
                style={[
                  styles.roleOption,
                  selectedRole === option.key && styles.roleOptionSelected,
                ]}
                onPress={() => setSelectedRole(option.key)}
              >
                <View style={styles.roleOptionContent}>
                  <View style={[
                    styles.radioButton,
                    selectedRole === option.key && styles.radioButtonSelected,
                  ]}>
                    {selectedRole === option.key && <View style={styles.radioButtonInner} />}
                  </View>
                  <View style={styles.roleText}>
                    <Text style={[
                      styles.roleTitle,
                      selectedRole === option.key && styles.roleTextSelected,
                    ]}>
                      {option.title}
                    </Text>
                    <Text style={[
                      styles.roleDescription,
                      selectedRole === option.key && styles.roleDescriptionSelected,
                    ]}>
                      {option.description}
                    </Text>
                  </View>
                </View>
              </TouchableOpacity>
            ))}
          </View>

          <TouchableOpacity
            style={styles.termsContainer}
            onPress={() => setAgreedToTerms(!agreedToTerms)}
          >
            <View style={[styles.checkbox, agreedToTerms && styles.checkboxChecked]}>
              {agreedToTerms && <Text style={styles.checkmark}>✓</Text>}
            </View>
            <Text style={styles.termsText}>
              {t('register.agree_terms_prefix')}{' '}
              <Text style={styles.termsLink}>{t('register.terms_of_service')}</Text>
              {' '}{t('register.agree_terms_and')}{' '}
              <Text style={styles.termsLink}>{t('register.privacy_policy')}</Text>
            </Text>
          </TouchableOpacity>

          {localError && (
            <View style={styles.errorContainer}>
              <View style={styles.errorIconContainer}>
                <Ionicons name="alert-circle" size={20} color={COLORS.error} />
              </View>
              <Text style={styles.errorText}>{localError}</Text>
            </View>
          )}

          <Button
            title={t('auth.create_account')}
            onPress={handleSubmit(onSubmit)}
            loading={isLoading}
            style={styles.registerButton}
          />

          <View style={styles.loginContainer}>
            <Text style={styles.loginText}>{t('register.already_have_account')} </Text>
            <TouchableOpacity onPress={handleLoginPress}>
              <Text style={styles.loginLink}>{t('register.log_in_link')}</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    ...Platform.select({
      web: {
        height: '100vh' as any,
        maxHeight: '100vh' as any,
        overflow: 'hidden',
        display: 'flex' as any,
        flexDirection: 'column' as any,
      },
    }),
  },
  languageSwitcherContainer: {
    position: 'absolute',
    top: SPACING.md,
    right: SPACING.md,
    zIndex: 100,
  },
  scrollView: {
    flex: 1,
    ...Platform.select({
      web: {
        height: '100%' as any,
        maxHeight: '100%' as any,
        overflowY: 'scroll' as any,
        overflowX: 'hidden' as any,
        WebkitOverflowScrolling: 'touch' as any,
      },
    }),
  },
  scrollContent: {
    padding: SPACING.lg,
    paddingTop: SPACING.xl * 2,
    paddingBottom: 200,
    alignItems: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: SPACING.xl,
  },
  title: {
    fontSize: 32,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginBottom: SPACING.sm,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
  },
  form: {
    // Width is set dynamically based on screen size
  },
  roleSection: {
    marginBottom: SPACING.lg,
  },
  roleLabel: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  roleOption: {
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    backgroundColor: COLORS.surface,
  },
  roleOptionSelected: {
    borderColor: COLORS.primary,
    backgroundColor: `${COLORS.primary}10`,
  },
  roleOptionContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  radioButton: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: COLORS.border,
    marginRight: SPACING.md,
    justifyContent: 'center',
    alignItems: 'center',
  },
  radioButtonSelected: {
    borderColor: COLORS.primary,
  },
  radioButtonInner: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: COLORS.primary,
  },
  roleText: {
    flex: 1,
  },
  roleTitle: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: COLORS.text,
    marginBottom: 2,
  },
  roleTextSelected: {
    color: COLORS.primary,
  },
  roleDescription: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
  },
  roleDescriptionSelected: {
    color: COLORS.primary,
  },
  termsContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: SPACING.lg,
  },
  checkbox: {
    width: 20,
    height: 20,
    borderWidth: 2,
    borderColor: COLORS.border,
    borderRadius: 4,
    marginRight: SPACING.sm,
    marginTop: 2,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxChecked: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  checkmark: {
    color: COLORS.surface,
    fontSize: 12,
    fontFamily: FONTS.bold,
  },
  termsText: {
    flex: 1,
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.text,
    lineHeight: 20,
  },
  termsLink: {
    color: COLORS.primary,
    fontFamily: FONTS.medium,
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: `${COLORS.error}15`,
    borderWidth: 1,
    borderColor: COLORS.error,
    borderRadius: 8,
    padding: SPACING.md,
    marginBottom: SPACING.md,
  },
  errorIconContainer: {
    marginRight: SPACING.sm,
  },
  errorText: {
    flex: 1,
    fontSize: 14,
    fontFamily: FONTS.medium,
    color: COLORS.error,
    lineHeight: 20,
  },
  registerButton: {
    marginBottom: SPACING.lg,
  },
  loginContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 100,
  },
  loginText: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
  },
  loginLink: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: COLORS.primary,
  },
});