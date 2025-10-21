import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  SafeAreaView,
  useWindowDimensions,
} from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useAuthStore } from '../../store/authStore';
import { Input } from '../../components/Input';
import { Button } from '../../components/Button';
import { LanguageSwitcher } from '../../components/LanguageSwitcher';
import { useLanguage } from '../../contexts/LanguageContext';
import { COLORS, SPACING, FONTS } from '../../constants/config';

const registerSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

type RegisterFormData = z.infer<typeof registerSchema>;

interface RegisterScreenProps {
  navigation: any;
}

export const RegisterScreen: React.FC<RegisterScreenProps> = ({ navigation }) => {
  const [selectedRole, setSelectedRole] = useState<'lender' | 'borrower' | 'both'>('borrower');
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const { register, isLoading, error, clearError } = useAuthStore();
  const { width } = useWindowDimensions();
  const { t } = useLanguage();

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    if (!agreedToTerms) {
      Alert.alert('Terms Required', 'Please agree to the Terms of Service and Privacy Policy');
      return;
    }

    try {
      clearError();
      await register(data.email, data.password, data.confirmPassword, selectedRole, agreedToTerms);
      // Navigation will be handled by the auth flow
    } catch (error: any) {
      Alert.alert(
        'Registration Failed',
        error.detail || 'Please check your information and try again.'
      );
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
    <SafeAreaView style={styles.container}>
      <View style={styles.languageSwitcherContainer}>
        <LanguageSwitcher variant="button" />
      </View>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
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

          {error && (
            <View style={styles.errorContainer}>
              <Text style={styles.errorText}>{error}</Text>
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
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  languageSwitcherContainer: {
    position: 'absolute',
    top: SPACING.md,
    right: SPACING.md,
    zIndex: 100,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    padding: SPACING.lg,
    justifyContent: 'center',
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
    marginBottom: SPACING.md,
  },
  errorText: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.error,
    textAlign: 'center',
  },
  registerButton: {
    marginBottom: SPACING.lg,
  },
  loginContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
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