import React, { useState, useEffect, useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Alert,
  TouchableOpacity,
  Platform,
} from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { useNavigation } from '@react-navigation/native';

import { useProfileStore } from '../../store/profileStore';
import { useAuthStore } from '../../store/authStore';
import { Input } from '../../components/Input';
import { Button } from '../../components/Button';
import { ProgressBar } from '../../components/ProgressBar';
import { COLORS, SPACING, FONTS } from '../../constants/config';
import { useLanguage } from '../../contexts/LanguageContext';

type ProfileFormData = {
  first_name: string;
  last_name: string;
  display_name: string;
  bio: string;
  phone_number?: string;
  date_of_birth?: string;
  city: string;
  state_province: string;
  country: string;
  annual_income?: number;
  employment_status?: string;
};

export const ProfileSetupScreen: React.FC = () => {
  const navigation = useNavigation();
  const [currentStep, setCurrentStep] = useState(1);
  const [profileImage, setProfileImage] = useState<string | null>(null);
  const { profile, isLoading, error, updateProfile, uploadProfileImage, loadProfile, checkProfileCompletion } = useProfileStore();
  const { user } = useAuthStore();
  const { t } = useLanguage();

  const totalSteps = 4;
  const progressPercentage = (currentStep / totalSteps) * 100;

  // Create schema with translated messages - recreates when language changes
  const profileSchema = useMemo(() => {
    return z.object({
      first_name: z.string().min(2, t('profile_setup.validation_first_name')),
      last_name: z.string().min(2, t('profile_setup.validation_last_name')),
      display_name: z.string().min(3, t('profile_setup.validation_display_name')),
      bio: z.string().min(50, t('profile_setup.validation_bio_min')).max(500, t('profile_setup.validation_bio_max')),
      phone_number: z.string().optional(),
      date_of_birth: z.string().optional(),
      city: z.string().min(2, t('profile_setup.validation_city')),
      state_province: z.string().min(2, t('profile_setup.validation_state')),
      country: z.string().min(2, t('profile_setup.validation_country')),
      annual_income: z.number().optional(),
      employment_status: z.string().optional(),
    });
  }, [t]);

  const {
    control,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      first_name: '',
      last_name: '',
      display_name: '',
      bio: '',
      phone_number: '',
      date_of_birth: '',
      city: '',
      state_province: '',
      country: '',
      employment_status: 'employed',
    },
  });

  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  useEffect(() => {
    if (profile) {
      setValue('first_name', profile.first_name || '');
      setValue('last_name', profile.last_name || '');
      setValue('display_name', profile.display_name || '');
      setValue('bio', profile.bio || '');
      setValue('phone_number', profile.phone_number || '');
      setValue('city', profile.city || '');
      setValue('state_province', profile.state_province || '');
      setValue('country', profile.country || '');
      setValue('employment_status', profile.employment_status || 'employed');
      if (profile.annual_income) {
        setValue('annual_income', profile.annual_income);
      }
    }
  }, [profile, setValue]);

  const pickImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert(t('profile_setup.permission_required_title'), t('profile_setup.permission_required_message'));
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.8,
    });

    if (!result.canceled && result.assets[0]) {
      setProfileImage(result.assets[0].uri);
    }
  };

  const onSubmit = async (data: ProfileFormData) => {
    try {
      await updateProfile(data);

      if (profileImage) {
        await uploadProfileImage(profileImage);
      }

      checkProfileCompletion();
      Alert.alert(
        t('profile_setup.profile_updated_title'),
        t('profile_setup.profile_updated_message'),
        [{ text: t('common.ok'), onPress: () => navigation.goBack() }]
      );
    } catch (error: any) {
      Alert.alert(t('profile_setup.update_failed_title'), error.detail || 'Failed to update profile');
    }
  };

  const nextStep = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <View style={styles.stepContent}>
            <Text style={styles.stepTitle}>{t('profile_setup.basic_info_title')}</Text>
            <Text style={styles.stepDescription}>
              {t('profile_setup.basic_info_description')}
            </Text>

            <Controller
              control={control}
              name="first_name"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label={t('profile_setup.first_name')}
                  placeholder={t('profile_setup.first_name_placeholder')}
                  value={value}
                  onChangeText={onChange}
                  onBlur={onBlur}
                  error={errors.first_name?.message}
                  leftIcon="person"
                />
              )}
            />

            <Controller
              control={control}
              name="last_name"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label={t('profile_setup.last_name')}
                  placeholder={t('profile_setup.last_name_placeholder')}
                  value={value}
                  onChangeText={onChange}
                  onBlur={onBlur}
                  error={errors.last_name?.message}
                  leftIcon="person"
                />
              )}
            />

            <Controller
              control={control}
              name="display_name"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label={t('profile_setup.display_name')}
                  placeholder={t('profile_setup.display_name_placeholder')}
                  value={value}
                  onChangeText={onChange}
                  onBlur={onBlur}
                  error={errors.display_name?.message}
                  leftIcon="at"
                />
              )}
            />
          </View>
        );

      case 2:
        return (
          <View style={styles.stepContent}>
            <Text style={styles.stepTitle}>{t('profile_setup.photo_bio_title')}</Text>
            <Text style={styles.stepDescription}>
              {t('profile_setup.photo_bio_description')}
            </Text>

            <View style={styles.imageSection}>
              <Text style={styles.inputLabel}>{t('profile_setup.profile_photo')}</Text>
              <TouchableOpacity style={styles.imagePicker} onPress={pickImage}>
                {profileImage ? (
                  <Text style={styles.imagePickerText}>{t('profile_setup.photo_selected')}</Text>
                ) : (
                  <>
                    <Ionicons name="camera" size={32} color={COLORS.textSecondary} />
                    <Text style={styles.imagePickerText}>{t('profile_setup.tap_to_add_photo')}</Text>
                  </>
                )}
              </TouchableOpacity>
            </View>

            <Controller
              control={control}
              name="bio"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label={t('profile_setup.bio')}
                  placeholder={t('profile_setup.bio_placeholder')}
                  value={value}
                  onChangeText={onChange}
                  onBlur={onBlur}
                  error={errors.bio?.message}
                  multiline
                  style={{ height: 100 }}
                />
              )}
            />

            <Controller
              control={control}
              name="phone_number"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label={t('profile_setup.phone_optional')}
                  placeholder={t('profile_setup.phone_placeholder')}
                  value={value}
                  onChangeText={onChange}
                  onBlur={onBlur}
                  error={errors.phone_number?.message}
                  keyboardType="phone-pad"
                  leftIcon="call"
                />
              )}
            />
          </View>
        );

      case 3:
        return (
          <View style={styles.stepContent}>
            <Text style={styles.stepTitle}>{t('profile_setup.location_title')}</Text>
            <Text style={styles.stepDescription}>
              {t('profile_setup.location_description')}
            </Text>

            <Controller
              control={control}
              name="city"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label={t('profile_setup.city')}
                  placeholder={t('profile_setup.city_placeholder')}
                  value={value}
                  onChangeText={onChange}
                  onBlur={onBlur}
                  error={errors.city?.message}
                  leftIcon="location"
                />
              )}
            />

            <Controller
              control={control}
              name="state_province"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label={t('profile_setup.state_province')}
                  placeholder={t('profile_setup.state_province_placeholder')}
                  value={value}
                  onChangeText={onChange}
                  onBlur={onBlur}
                  error={errors.state_province?.message}
                  leftIcon="location"
                />
              )}
            />

            <Controller
              control={control}
              name="country"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label={t('profile_setup.country')}
                  placeholder={t('profile_setup.country_placeholder')}
                  value={value}
                  onChangeText={onChange}
                  onBlur={onBlur}
                  error={errors.country?.message}
                  leftIcon="globe"
                />
              )}
            />
          </View>
        );

      case 4:
        return (
          <View style={styles.stepContent}>
            <Text style={styles.stepTitle}>{t('profile_setup.financial_info_title')}</Text>
            <Text style={styles.stepDescription}>
              {t('profile_setup.financial_info_description')}
            </Text>

            <Controller
              control={control}
              name="employment_status"
              render={({ field: { onChange, value } }) => (
                <View style={styles.fieldContainer}>
                  <Text style={styles.inputLabel}>{t('profile_setup.employment_status')}</Text>
                  <View style={styles.optionsContainer}>
                    {['employed', 'self_employed', 'student', 'unemployed', 'retired'].map((status) => (
                      <TouchableOpacity
                        key={status}
                        style={[
                          styles.optionButton,
                          value === status && styles.optionButtonSelected,
                        ]}
                        onPress={() => onChange(status)}
                      >
                        <Text style={[
                          styles.optionText,
                          value === status && styles.optionTextSelected,
                        ]}>
                          {t(`profile_setup.${status}`)}
                        </Text>
                      </TouchableOpacity>
                    ))}
                  </View>
                </View>
              )}
            />

            <Controller
              control={control}
              name="annual_income"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label={t('profile_setup.annual_income')}
                  placeholder={t('profile_setup.annual_income_placeholder')}
                  value={value?.toString() || ''}
                  onChangeText={(text) => {
                    const numericValue = parseInt(text.replace(/[^0-9]/g, ''));
                    onChange(isNaN(numericValue) ? undefined : numericValue);
                  }}
                  onBlur={onBlur}
                  keyboardType="numeric"
                  leftIcon="cash"
                />
              )}
            />
          </View>
        );

      default:
        return null;
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color={COLORS.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>{t('profile_setup.title')}</Text>
        <View style={styles.headerRight} />
      </View>

      <View style={styles.progressSection}>
        <ProgressBar
          progress={progressPercentage}
          label={t('profile_setup.step_of', { current: currentStep, total: totalSteps })}
        />
      </View>

      <ScrollView
        style={styles.content}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={true}
        keyboardShouldPersistTaps="handled"
      >
        {renderStepContent()}

        {error && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>{error}</Text>
          </View>
        )}
      </ScrollView>

      <View style={styles.footer}>
        <View style={styles.buttonRow}>
          {currentStep > 1 && (
            <Button
              title={t('profile_setup.previous')}
              onPress={prevStep}
              variant="outline"
              style={styles.footerButton}
            />
          )}

          {currentStep < totalSteps ? (
            <Button
              title={t('profile_setup.next')}
              onPress={nextStep}
              style={{
                ...styles.footerButton,
                ...(currentStep === 1 ? styles.fullWidthButton : {}),
              }}
            />
          ) : (
            <Button
              title={t('profile_setup.complete_profile')}
              onPress={handleSubmit(onSubmit)}
              loading={isLoading}
              style={styles.footerButton}
            />
          )}
        </View>
      </View>
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
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
    backgroundColor: COLORS.surface,
  },
  backButton: {
    padding: SPACING.xs,
  },
  headerTitle: {
    fontSize: 18,
    fontFamily: FONTS.bold,
    color: COLORS.text,
  },
  headerRight: {
    width: 40,
  },
  progressSection: {
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    backgroundColor: COLORS.surface,
  },
  content: {
    flex: 1,
    paddingHorizontal: SPACING.lg,
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
    paddingBottom: 200,
  },
  stepContent: {
    paddingVertical: SPACING.lg,
  },
  stepTitle: {
    fontSize: 24,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginBottom: SPACING.sm,
  },
  stepDescription: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    lineHeight: 24,
    marginBottom: SPACING.xl,
  },
  imageSection: {
    marginBottom: SPACING.lg,
  },
  inputLabel: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: COLORS.text,
    marginBottom: SPACING.xs,
  },
  imagePicker: {
    height: 120,
    borderWidth: 2,
    borderColor: COLORS.border,
    borderStyle: 'dashed',
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
  imagePickerText: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    marginTop: SPACING.sm,
  },
  fieldContainer: {
    marginBottom: SPACING.lg,
  },
  optionsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.sm,
  },
  optionButton: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 8,
    backgroundColor: COLORS.surface,
  },
  optionButtonSelected: {
    borderColor: COLORS.primary,
    backgroundColor: `${COLORS.primary}10`,
  },
  optionText: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.text,
  },
  optionTextSelected: {
    color: COLORS.primary,
    fontFamily: FONTS.medium,
  },
  errorContainer: {
    marginVertical: SPACING.md,
  },
  errorText: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.error,
    textAlign: 'center',
  },
  footer: {
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    backgroundColor: COLORS.surface,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: SPACING.md,
  },
  footerButton: {
    flex: 1,
  },
  fullWidthButton: {
    flex: 1,
  },
});