import React, { useState, useEffect, useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  TouchableOpacity,
  Platform,
  Alert,
} from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Ionicons } from '@expo/vector-icons';

import { useProfileStore } from '../../store/profileStore';
import { useAuthStore } from '../../store/authStore';
import { Input } from '../../components/Input';
import { Button } from '../../components/Button';
import { COLORS, SPACING, FONTS } from '../../constants/config';
import { useColors } from '../../hooks/useColors';
import { useLanguage } from '../../contexts/LanguageContext';

import { logger } from '../../utils/logger';
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
  postal_code?: string;
};

interface EditProfileScreenProps {
  navigation: any;
}

export const EditProfileScreen: React.FC<EditProfileScreenProps> = ({ navigation }) => {
  const colors = useColors();
  const styles = createStyles(colors);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { profile, isLoading, updateProfile, loadProfile } = useProfileStore();
  const { user } = useAuthStore();
  const { t } = useLanguage();

  // Create schema with translated messages
  const profileSchema = useMemo(() => {
    return z.object({
      first_name: z.string().min(2, t('profile_setup.validation_first_name')),
      last_name: z.string().min(2, t('profile_setup.validation_last_name')),
      display_name: z.string().min(3, t('profile_setup.validation_display_name')),
      bio: z.string().min(20, t('profile_setup.validation_bio_min')).max(1000, t('profile_setup.validation_bio_max')),
      phone_number: z.string().optional(),
      date_of_birth: z.string().optional(),
      city: z.string().min(2, t('profile_setup.validation_city')),
      state_province: z.string().min(2, t('profile_setup.validation_state')),
      country: z.string().min(2, t('profile_setup.validation_country')),
      postal_code: z.string().optional(),
    });
  }, [t]);

  const {
    control,
    handleSubmit,
    formState: { errors, isDirty },
    setValue,
    reset,
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
      postal_code: '',
    },
  });

  // Load profile data on mount
  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  // Populate form with existing profile data
  useEffect(() => {
    if (profile) {
      reset({
        first_name: profile.first_name || '',
        last_name: profile.last_name || '',
        display_name: profile.display_name || '',
        bio: profile.bio || '',
        phone_number: profile.phone_number || '',
        date_of_birth: profile.date_of_birth || '',
        city: profile.city || '',
        state_province: profile.state_province || '',
        country: profile.country || '',
        postal_code: profile.postal_code || '',
      });
    }
  }, [profile, reset]);

  const onSubmit = async (data: ProfileFormData) => {
    try {
      setIsSubmitting(true);

      await updateProfile(data);

      if (Platform.OS === 'web') {
        window.alert(t('edit_profile.success_message'));
      } else {
        Alert.alert(t('edit_profile.success_title'), t('edit_profile.success_message'));
      }

      navigation.goBack();
    } catch (error: unknown) {
      logger.error('Error updating profile:', error);
      const errorMessage = error.message || t('edit_profile.error_message');

      if (Platform.OS === 'web') {
        window.alert(`${t('edit_profile.error_title')}: ${errorMessage}`);
      } else {
        Alert.alert(t('edit_profile.error_title'), errorMessage);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    if (isDirty) {
      if (Platform.OS === 'web') {
        const confirmed = window.confirm(t('edit_profile.cancel_confirm'));
        if (confirmed) {
          navigation.goBack();
        }
      } else {
        Alert.alert(
          t('edit_profile.cancel_title'),
          t('edit_profile.cancel_message'),
          [
            { text: t('edit_profile.stay'), style: 'cancel' },
            { text: t('edit_profile.discard'), style: 'destructive', onPress: () => navigation.goBack() },
          ]
        );
      }
    } else {
      navigation.goBack();
    }
  };

  if (isLoading && !profile) {
    

    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>{t('edit_profile.loading')}</Text>
        </View>
      </SafeAreaView>
    );
  }


  


  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={handleCancel} style={styles.headerButton}>
          <Ionicons name="close" size={24} color={colors.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>{t('edit_profile.title')}</Text>
        <View style={styles.headerButton} />
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={true}
        keyboardShouldPersistTaps="handled"
        nestedScrollEnabled={true}
      >
        {/* Personal Information Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>{t('edit_profile.personal_info')}</Text>

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
                leftIcon="document-text"
                multiline
                numberOfLines={4}
                style={{ height: 100 }}
              />
            )}
          />

          <Controller
            control={control}
            name="phone_number"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label={t('profile_setup.phone_number')}
                placeholder={t('profile_setup.phone_placeholder')}
                value={value}
                onChangeText={onChange}
                onBlur={onBlur}
                error={errors.phone_number?.message}
                leftIcon="call"
                keyboardType="phone-pad"
              />
            )}
          />

          <Controller
            control={control}
            name="date_of_birth"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label={t('profile_setup.date_of_birth')}
                placeholder="YYYY-MM-DD"
                value={value}
                onChangeText={onChange}
                onBlur={onBlur}
                error={errors.date_of_birth?.message}
                leftIcon="calendar"
              />
            )}
          />
        </View>

        {/* Location Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>{t('edit_profile.location_info')}</Text>

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
                leftIcon="business"
              />
            )}
          />

          <Controller
            control={control}
            name="state_province"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label={t('profile_setup.state_province')}
                placeholder={t('profile_setup.state_placeholder')}
                value={value}
                onChangeText={onChange}
                onBlur={onBlur}
                error={errors.state_province?.message}
                leftIcon="map"
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

          <Controller
            control={control}
            name="postal_code"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label={t('profile_setup.postal_code')}
                placeholder={t('profile_setup.postal_code_placeholder')}
                value={value}
                onChangeText={onChange}
                onBlur={onBlur}
                error={errors.postal_code?.message}
                leftIcon="mail"
              />
            )}
          />
        </View>

        {/* Action Buttons */}
        <View style={styles.buttonContainer}>
          <Button
            title={t('edit_profile.save_changes')}
            onPress={handleSubmit(onSubmit)}
            loading={isSubmitting}
            disabled={isSubmitting || !isDirty}
          />

          <Button
            title={t('edit_profile.cancel')}
            onPress={handleCancel}
            variant="outline"
            disabled={isSubmitting}
            style={{ marginTop: SPACING.md }}
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const createStyles = (colors: ReturnType<typeof useColors>) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    ...(Platform.OS === 'web' && {
      height: '100vh' as any,
      overflow: 'hidden' as any,
    }),
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    backgroundColor: colors.surface,
  },
  headerButton: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 18,
    fontFamily: FONTS.bold,
    color: colors.text,
  },
  scrollView: {
    flex: 1,
    ...(Platform.OS === 'web' && {
      overflow: 'auto' as any,
      maxHeight: 'calc(100vh - 60px)' as any,
    }),
  },
  content: {
    padding: SPACING.lg,
    paddingBottom: SPACING.xl * 2,
  },
  section: {
    marginBottom: SPACING.xl,
  },
  sectionTitle: {
    fontSize: 16,
    fontFamily: FONTS.bold,
    color: colors.text,
    marginBottom: SPACING.md,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  buttonContainer: {
    marginTop: SPACING.md,
    marginBottom: SPACING.xl,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: colors.textSecondary,
  },
});
