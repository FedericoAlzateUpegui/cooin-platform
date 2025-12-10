import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Alert,
  Platform,
  TouchableOpacity,
} from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Ionicons } from '@expo/vector-icons';

import { useLanguage } from '../../contexts/LanguageContext';
import { Input } from '../../components/Input';
import { Button } from '../../components/Button';
import { COLORS, SPACING, FONTS } from '../../constants/config';
import { authService } from '../../services/authService';

type ChangePasswordFormData = {
  currentPassword: string;
  newPassword: string;
  confirmNewPassword: string;
};

interface ChangePasswordScreenProps {
  navigation: any;
}

export const ChangePasswordScreen: React.FC<ChangePasswordScreenProps> = ({ navigation }) => {
  const { t, currentLanguage } = useLanguage();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [passwordStrength, setPasswordStrength] = useState<'weak' | 'medium' | 'strong' | null>(null);
  const [touched, setTouched] = useState({
    currentPassword: false,
    newPassword: false,
    confirmNewPassword: false,
  });

  // Create dynamic schema with translated messages
  const changePasswordSchema = React.useMemo(() => z.object({
    currentPassword: z.string()
      .min(1, t('validation.password_required')),
    newPassword: z.string()
      .min(1, t('validation.password_required'))
      .min(8, t('validation.password_too_short'))
      .refine((val) => /[A-Z]/.test(val) && /[a-z]/.test(val) && /[0-9]/.test(val), {
        message: t('validation.password_weak'),
      }),
    confirmNewPassword: z.string()
      .min(1, t('validation.confirm_password_required')),
  }).refine((data) => data.newPassword === data.confirmNewPassword, {
    message: t('validation.passwords_must_match'),
    path: ["confirmNewPassword"],
  }), [t, currentLanguage]); // Re-create schema when language changes

  const {
    control,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
    trigger,
  } = useForm<ChangePasswordFormData>({
    resolver: zodResolver(changePasswordSchema),
    mode: 'onBlur', // Trigger validation on blur (when jumping between fields)
    reValidateMode: 'onChange', // Re-validate on change after first blur
    defaultValues: {
      currentPassword: '',
      newPassword: '',
      confirmNewPassword: '',
    },
  });

  // Watch password field for strength calculation
  const newPassword = watch('newPassword');
  const confirmNewPassword = watch('confirmNewPassword');

  // Calculate password strength (memoized to avoid recalculations)
  const calculatedStrength = React.useMemo(() => {
    if (!newPassword || newPassword.length === 0) {
      return null;
    }

    let strength = 0;

    // Length check
    if (newPassword.length >= 8) strength++;
    if (newPassword.length >= 12) strength++;

    // Character variety checks
    if (/[a-z]/.test(newPassword)) strength++;
    if (/[A-Z]/.test(newPassword)) strength++;
    if (/[0-9]/.test(newPassword)) strength++;
    if (/[^A-Za-z0-9]/.test(newPassword)) strength++;

    if (strength <= 2) return 'weak';
    if (strength <= 4) return 'medium';
    return 'strong';
  }, [newPassword]);

  // Update password strength state only when it actually changes
  React.useEffect(() => {
    if (calculatedStrength !== passwordStrength) {
      setPasswordStrength(calculatedStrength);
    }
  }, [calculatedStrength, passwordStrength]);

  // Trigger validation for confirm password when new password changes
  React.useEffect(() => {
    if (touched.confirmNewPassword && confirmNewPassword) {
      trigger('confirmNewPassword');
    }
  }, [newPassword, confirmNewPassword, touched.confirmNewPassword, trigger]);

  // Re-validate all fields when language changes to update error messages
  const prevLanguage = React.useRef(currentLanguage);
  React.useEffect(() => {
    if (prevLanguage.current !== currentLanguage && Object.keys(errors).length > 0) {
      trigger();
    }
    prevLanguage.current = currentLanguage;
  }, [currentLanguage, trigger, errors]);

  // Memoized handlers to avoid recreating on every render
  const handleFieldTouch = React.useCallback((fieldName: keyof typeof touched) => {
    setTouched(prev => {
      if (prev[fieldName]) return prev; // Already touched, don't update state
      return { ...prev, [fieldName]: true };
    });
  }, []);

  const onSubmit = async (data: ChangePasswordFormData) => {
    try {
      setError(null);
      setIsLoading(true);

      await authService.changePassword({
        current_password: data.currentPassword,
        new_password: data.newPassword,
        confirm_new_password: data.confirmNewPassword,
      });

      // Success
      if (Platform.OS === 'web') {
        window.alert(t('change_password.success_message'));
      } else {
        Alert.alert(
          t('change_password.success_title'),
          t('change_password.success_message')
        );
      }

      // Reset form and go back
      reset();
      navigation.goBack();

    } catch (error: any) {
      console.error('Change password error:', error);
      const errorMessage = error.detail || error.message || t('change_password.error_message');
      setError(errorMessage);

      if (Platform.OS === 'web') {
        window.alert(errorMessage);
      } else {
        Alert.alert(t('change_password.error_title'), errorMessage);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Render como modal en web
  if (Platform.OS === 'web') {
    return (
      <View style={styles.webModal}>
        <View style={styles.webModalContent}>
          {/* Back Button */}
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Ionicons name="arrow-back" size={24} color={COLORS.primary} />
            <Text style={styles.backText}>{t('common.back')}</Text>
          </TouchableOpacity>

          <View style={styles.header}>
            <View style={styles.iconContainer}>
              <Ionicons name="lock-closed" size={40} color={COLORS.primary} />
            </View>
            <Text style={styles.title}>{t('change_password.title')}</Text>
            <Text style={styles.subtitle}>{t('change_password.subtitle')}</Text>
          </View>

          <View style={styles.form}>
            <Controller
              control={control}
              name="currentPassword"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label={t('change_password.current_password')}
                  placeholder={t('change_password.current_password_placeholder')}
                  value={value}
                  onChangeText={(text) => {
                    onChange(text);
                    handleFieldTouch('currentPassword');
                  }}
                  onBlur={() => {
                    onBlur();
                    handleFieldTouch('currentPassword');
                  }}
                  error={touched.currentPassword ? errors.currentPassword?.message : undefined}
                  isPassword
                  leftIcon="lock-closed"
                />
              )}
            />

            <Controller
              control={control}
              name="newPassword"
              render={({ field: { onChange, onBlur, value } }) => (
                <>
                  <Input
                    label={t('change_password.new_password')}
                    placeholder={t('change_password.new_password_placeholder')}
                    value={value}
                    onChangeText={(text) => {
                      onChange(text);
                      handleFieldTouch('newPassword');
                    }}
                    onBlur={() => {
                      onBlur();
                      handleFieldTouch('newPassword');
                    }}
                    error={touched.newPassword ? errors.newPassword?.message : undefined}
                    isPassword
                    leftIcon="key"
                  />
                  {passwordStrength && touched.newPassword && (
                    <View style={styles.passwordStrengthContainer}>
                      <View style={styles.passwordStrengthBars}>
                        <View
                          style={[
                            styles.strengthBar,
                            passwordStrength === 'weak' && styles.strengthBarWeak,
                            passwordStrength === 'medium' && styles.strengthBarMedium,
                            passwordStrength === 'strong' && styles.strengthBarStrong,
                          ]}
                        />
                        <View
                          style={[
                            styles.strengthBar,
                            (passwordStrength === 'medium' || passwordStrength === 'strong') && styles.strengthBarMedium,
                            passwordStrength === 'strong' && styles.strengthBarStrong,
                          ]}
                        />
                        <View
                          style={[
                            styles.strengthBar,
                            passwordStrength === 'strong' && styles.strengthBarStrong,
                          ]}
                        />
                      </View>
                      <Text style={[
                        styles.passwordStrengthText,
                        passwordStrength === 'weak' && styles.strengthTextWeak,
                        passwordStrength === 'medium' && styles.strengthTextMedium,
                        passwordStrength === 'strong' && styles.strengthTextStrong,
                      ]}>
                        {passwordStrength === 'weak' && t('change_password.strength_weak')}
                        {passwordStrength === 'medium' && t('change_password.strength_medium')}
                        {passwordStrength === 'strong' && t('change_password.strength_strong')}
                      </Text>
                    </View>
                  )}
                </>
              )}
            />

            <Controller
              control={control}
              name="confirmNewPassword"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label={t('change_password.confirm_new_password')}
                  placeholder={t('change_password.confirm_new_password_placeholder')}
                  value={value}
                  onChangeText={(text) => {
                    onChange(text);
                    handleFieldTouch('confirmNewPassword');
                  }}
                  onBlur={() => {
                    onBlur();
                    handleFieldTouch('confirmNewPassword');
                  }}
                  error={touched.confirmNewPassword ? errors.confirmNewPassword?.message : undefined}
                  isPassword
                  leftIcon="key"
                />
              )}
            />

            {error && (
              <View style={styles.errorContainer}>
                <Text style={styles.errorText}>{error}</Text>
              </View>
            )}

            <Button
              title={t('change_password.submit_button')}
              onPress={handleSubmit(onSubmit)}
              loading={isLoading}
              style={styles.submitButton}
            />

            <Button
              title={t('common.cancel')}
              onPress={() => navigation.goBack()}
              variant="outline"
            />
          </View>
        </View>
      </View>
    );
  }

  // Render normal para mobile
  return (
    <View style={styles.container}>
      <View style={styles.content}>
        {/* Back Button */}
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Ionicons name="arrow-back" size={24} color={COLORS.primary} />
          <Text style={styles.backText}>{t('common.back')}</Text>
        </TouchableOpacity>

        <View style={styles.header}>
          <View style={styles.iconContainer}>
            <Ionicons name="lock-closed" size={40} color={COLORS.primary} />
          </View>
          <Text style={styles.title}>{t('change_password.title')}</Text>
          <Text style={styles.subtitle}>{t('change_password.subtitle')}</Text>
        </View>

        <View style={styles.form}>
          <Controller
            control={control}
            name="currentPassword"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label={t('change_password.current_password')}
                placeholder={t('change_password.current_password_placeholder')}
                value={value}
                onChangeText={(text) => {
                  onChange(text);
                  handleFieldTouch('currentPassword');
                }}
                onBlur={() => {
                  onBlur();
                  handleFieldTouch('currentPassword');
                }}
                error={touched.currentPassword ? errors.currentPassword?.message : undefined}
                isPassword
                leftIcon="lock-closed"
              />
            )}
          />

          <Controller
            control={control}
            name="newPassword"
            render={({ field: { onChange, onBlur, value } }) => (
              <>
                <Input
                  label={t('change_password.new_password')}
                  placeholder={t('change_password.new_password_placeholder')}
                  value={value}
                  onChangeText={(text) => {
                    onChange(text);
                    handleFieldTouch('newPassword');
                  }}
                  onBlur={() => {
                    onBlur();
                    handleFieldTouch('newPassword');
                  }}
                  error={touched.newPassword ? errors.newPassword?.message : undefined}
                  isPassword
                  leftIcon="key"
                />
                {passwordStrength && touched.newPassword && (
                  <View style={styles.passwordStrengthContainer}>
                    <View style={styles.passwordStrengthBars}>
                      <View
                        style={[
                          styles.strengthBar,
                          passwordStrength === 'weak' && styles.strengthBarWeak,
                          passwordStrength === 'medium' && styles.strengthBarMedium,
                          passwordStrength === 'strong' && styles.strengthBarStrong,
                        ]}
                      />
                      <View
                        style={[
                          styles.strengthBar,
                          (passwordStrength === 'medium' || passwordStrength === 'strong') && styles.strengthBarMedium,
                          passwordStrength === 'strong' && styles.strengthBarStrong,
                        ]}
                      />
                      <View
                        style={[
                          styles.strengthBar,
                          passwordStrength === 'strong' && styles.strengthBarStrong,
                        ]}
                      />
                    </View>
                    <Text style={[
                      styles.passwordStrengthText,
                      passwordStrength === 'weak' && styles.strengthTextWeak,
                      passwordStrength === 'medium' && styles.strengthTextMedium,
                      passwordStrength === 'strong' && styles.strengthTextStrong,
                    ]}>
                      {passwordStrength === 'weak' && t('change_password.strength_weak')}
                      {passwordStrength === 'medium' && t('change_password.strength_medium')}
                      {passwordStrength === 'strong' && t('change_password.strength_strong')}
                    </Text>
                  </View>
                )}
              </>
            )}
          />

          <Controller
            control={control}
            name="confirmNewPassword"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label={t('change_password.confirm_new_password')}
                placeholder={t('change_password.confirm_new_password_placeholder')}
                value={value}
                onChangeText={(text) => {
                  onChange(text);
                  handleFieldTouch('confirmNewPassword');
                }}
                onBlur={() => {
                  onBlur();
                  handleFieldTouch('confirmNewPassword');
                }}
                error={touched.confirmNewPassword ? errors.confirmNewPassword?.message : undefined}
                isPassword
                leftIcon="key"
              />
            )}
          />

          {error && (
            <View style={styles.errorContainer}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}

          <Button
            title={t('change_password.submit_button')}
            onPress={handleSubmit(onSubmit)}
            loading={isLoading}
            style={styles.submitButton}
          />

          <Button
            title={t('common.cancel')}
            onPress={() => navigation.goBack()}
            variant="outline"
          />
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  // Estilos para modal web
  webModal: {
    ...Platform.select({
      web: {
        position: 'fixed' as any,
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex' as any,
        justifyContent: 'center' as any,
        alignItems: 'center' as any,
        zIndex: 1000,
        padding: SPACING.lg,
      },
    }),
  },
  webModalContent: {
    ...Platform.select({
      web: {
        backgroundColor: COLORS.background,
        borderRadius: 16,
        maxWidth: '95%' as any,
        width: '100%' as any,
        height: '95vh' as any,
        overflowY: 'auto' as any,
        padding: SPACING.xl * 2,
        boxShadow: '0 10px 40px rgba(0, 0, 0, 0.2)' as any,
      },
    }),
  },
  // Estilos para mobile
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    flex: 1,
    padding: SPACING.lg,
    paddingBottom: SPACING.xxl,
  },
  header: {
    alignItems: 'center',
    marginBottom: SPACING.xxl,
    marginTop: SPACING.xl,
  },
  iconContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: `${COLORS.primary}15`,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  title: {
    fontSize: 28,
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
    maxWidth: 400,
  },
  form: {
    width: '100%',
    maxWidth: 500,
    alignSelf: 'center',
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
  submitButton: {
    marginBottom: SPACING.md,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.md,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.xs,
    alignSelf: 'flex-start',
  },
  backText: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: COLORS.primary,
    marginLeft: SPACING.xs,
  },
  // Password Strength Indicator Styles
  passwordStrengthContainer: {
    marginTop: SPACING.sm,
    marginBottom: SPACING.md,
  },
  passwordStrengthBars: {
    flexDirection: 'row',
    gap: SPACING.xs,
    marginBottom: SPACING.xs,
  },
  strengthBar: {
    flex: 1,
    height: 4,
    borderRadius: 2,
    backgroundColor: COLORS.border,
  },
  strengthBarWeak: {
    backgroundColor: '#EF4444', // Red
  },
  strengthBarMedium: {
    backgroundColor: '#F59E0B', // Orange/Yellow
  },
  strengthBarStrong: {
    backgroundColor: '#10B981', // Green
  },
  passwordStrengthText: {
    fontSize: 12,
    fontFamily: FONTS.medium,
    textAlign: 'right',
  },
  strengthTextWeak: {
    color: '#EF4444',
  },
  strengthTextMedium: {
    color: '#F59E0B',
  },
  strengthTextStrong: {
    color: '#10B981',
  },
});
