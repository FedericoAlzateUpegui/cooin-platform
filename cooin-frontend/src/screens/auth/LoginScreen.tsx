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
import { useColors } from '../../hooks/useColors';

type LoginFormData = {
  email: string;
  password: string;
};

interface LoginScreenProps {
  navigation: any;
}

export const LoginScreen: React.FC<LoginScreenProps> = ({ navigation }) => {
  const colors = useColors();
  const [rememberMe, setRememberMe] = useState(false);
  const { login, isLoading, error, clearError } = useAuthStore();
  const { width } = useWindowDimensions();
  const { t } = useLanguage();

  // Create dynamic schema with translated messages
  const loginSchema = React.useMemo(() => z.object({
    email: z.string()
      .min(1, t('validation.email_required'))
      .email(t('validation.email_invalid')),
    password: z.string()
      .min(1, t('validation.password_required')),
  }), [t]);

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      clearError();
      await login(data.email, data.password, rememberMe);
      // Navigation will be handled by the auth flow
    } catch (error: unknown) {
      Alert.alert(
        'Login Failed',
        error.detail || 'Please check your credentials and try again.'
      );
    }
  };

  const handleRegisterPress = () => {
    navigation.navigate('Register');
  };

  const handleForgotPasswordPress = () => {
    navigation.navigate('ForgotPassword');
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

  const styles = createStyles(colors);

  


  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.languageSwitcherContainer}>
        <LanguageSwitcher variant="button" />
      </View>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
        showsVerticalScrollIndicator={true}
      >
        <View style={styles.contentWrapper}>
          <View style={[styles.header, { width: responsiveWidth }]}>
            <Text style={styles.title}>{t('welcome.title')}</Text>
            <Text style={styles.subtitle}>
              {t('welcome.subtitle')}
            </Text>
          </View>

          <View style={[styles.form, { width: responsiveWidth }]}>
            <Controller
            control={control}
            name="email"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label={t('common.email')}
                placeholder={t('login.email_placeholder')}
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
                placeholder={t('login.password_placeholder')}
                value={value}
                onChangeText={onChange}
                onBlur={onBlur}
                error={errors.password?.message}
                isPassword
                leftIcon="lock-closed"
              />
            )}
          />

          <View style={styles.optionsRow}>
            <TouchableOpacity
              style={styles.checkboxContainer}
              onPress={() => setRememberMe(!rememberMe)}
            >
              <View style={[styles.checkbox, rememberMe && styles.checkboxChecked]}>
                {rememberMe && <Text style={styles.checkmark}>✓</Text>}
              </View>
              <Text style={styles.checkboxLabel}>{t('login.remember_me')}</Text>
            </TouchableOpacity>

            <TouchableOpacity onPress={handleForgotPasswordPress}>
              <Text style={styles.forgotPassword}>{t('login.forgot_password')}</Text>
            </TouchableOpacity>
          </View>

          {error && (
            <View style={styles.errorContainer}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}

          <Button
            title={t('auth.login')}
            onPress={handleSubmit(onSubmit)}
            loading={isLoading}
            style={styles.loginButton}
          />

          <View style={styles.divider}>
            <View style={styles.dividerLine} />
            <Text style={styles.dividerText}>{t('login.or')}</Text>
            <View style={styles.dividerLine} />
          </View>

          <View style={styles.registerContainer}>
            <Text style={styles.registerText}>{t('login.no_account')} </Text>
            <TouchableOpacity onPress={handleRegisterPress}>
              <Text style={styles.registerLink}>{t('login.sign_up_link')}</Text>
            </TouchableOpacity>
          </View>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const createStyles = (colors: ReturnType<typeof useColors>) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
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
    alignItems: 'center',
    minHeight: '100%',
    paddingBottom: SPACING.xxl,
  },
  contentWrapper: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
  },
  header: {
    alignItems: 'center',
    marginBottom: SPACING.xxl,
  },
  title: {
    fontSize: 32,
    fontFamily: FONTS.bold,
    color: colors.text,
    marginBottom: SPACING.sm,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
  },
  form: {
    // Width is set dynamically based on screen size
  },
  optionsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  checkbox: {
    width: 20,
    height: 20,
    borderWidth: 2,
    borderColor: colors.border,
    borderRadius: 4,
    marginRight: SPACING.sm,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxChecked: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  checkmark: {
    color: colors.surface,
    fontSize: 12,
    fontFamily: FONTS.bold,
  },
  checkboxLabel: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: colors.text,
  },
  forgotPassword: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    color: colors.primary,
  },
  errorContainer: {
    marginBottom: SPACING.md,
  },
  errorText: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: colors.error,
    textAlign: 'center',
  },
  loginButton: {
    marginBottom: SPACING.lg,
  },
  divider: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: colors.border,
  },
  dividerText: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
    paddingHorizontal: SPACING.md,
  },
  registerContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  registerText: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
  },
  registerLink: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: colors.primary,
  },
});