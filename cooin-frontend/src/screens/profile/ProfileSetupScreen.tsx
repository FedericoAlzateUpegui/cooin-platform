import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Alert,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';

import { useProfileStore } from '../../store/profileStore';
import { useAuthStore } from '../../store/authStore';
import { Input } from '../../components/Input';
import { Button } from '../../components/Button';
import { ProgressBar } from '../../components/ProgressBar';
import { COLORS, SPACING, FONTS } from '../../constants/config';

const profileSchema = z.object({
  first_name: z.string().min(2, 'First name must be at least 2 characters'),
  last_name: z.string().min(2, 'Last name must be at least 2 characters'),
  display_name: z.string().min(3, 'Display name must be at least 3 characters'),
  bio: z.string().min(50, 'Bio must be at least 50 characters').max(500, 'Bio must be less than 500 characters'),
  phone_number: z.string().optional(),
  date_of_birth: z.string().optional(),
  city: z.string().min(2, 'City is required'),
  state_province: z.string().min(2, 'State/Province is required'),
  country: z.string().min(2, 'Country is required'),
  annual_income: z.number().optional(),
  employment_status: z.string().optional(),
});

type ProfileFormData = z.infer<typeof profileSchema>;

interface ProfileSetupScreenProps {
  navigation: any;
}

export const ProfileSetupScreen: React.FC<ProfileSetupScreenProps> = ({ navigation }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [profileImage, setProfileImage] = useState<string | null>(null);
  const { profile, isLoading, error, updateProfile, uploadProfileImage, loadProfile, checkProfileCompletion } = useProfileStore();
  const { user } = useAuthStore();

  const totalSteps = 4;
  const progressPercentage = (currentStep / totalSteps) * 100;

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
      Alert.alert('Permission Required', 'Sorry, we need camera roll permissions to upload your photo.');
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
        'Profile Updated',
        'Your profile has been successfully updated!',
        [{ text: 'OK', onPress: () => navigation.goBack() }]
      );
    } catch (error: any) {
      Alert.alert('Update Failed', error.detail || 'Failed to update profile');
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
            <Text style={styles.stepTitle}>Basic Information</Text>
            <Text style={styles.stepDescription}>
              Let's start with your basic details to create your profile.
            </Text>

            <Controller
              control={control}
              name="first_name"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label="First Name"
                  placeholder="Enter your first name"
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
                  label="Last Name"
                  placeholder="Enter your last name"
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
                  label="Display Name"
                  placeholder="How others will see you"
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
            <Text style={styles.stepTitle}>Profile Photo & Bio</Text>
            <Text style={styles.stepDescription}>
              Add a photo and tell others about yourself.
            </Text>

            <View style={styles.imageSection}>
              <Text style={styles.inputLabel}>Profile Photo</Text>
              <TouchableOpacity style={styles.imagePicker} onPress={pickImage}>
                {profileImage ? (
                  <Text style={styles.imagePickerText}>Photo Selected ✓</Text>
                ) : (
                  <>
                    <Ionicons name="camera" size={32} color={COLORS.textSecondary} />
                    <Text style={styles.imagePickerText}>Tap to add photo</Text>
                  </>
                )}
              </TouchableOpacity>
            </View>

            <Controller
              control={control}
              name="bio"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label="Bio"
                  placeholder="Tell others about yourself, your goals, and what you're looking for..."
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
                  label="Phone Number (Optional)"
                  placeholder="Enter your phone number"
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
            <Text style={styles.stepTitle}>Location</Text>
            <Text style={styles.stepDescription}>
              Help others find you by sharing your location.
            </Text>

            <Controller
              control={control}
              name="city"
              render={({ field: { onChange, onBlur, value } }) => (
                <Input
                  label="City"
                  placeholder="Enter your city"
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
                  label="State/Province"
                  placeholder="Enter your state or province"
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
                  label="Country"
                  placeholder="Enter your country"
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
            <Text style={styles.stepTitle}>Financial Information</Text>
            <Text style={styles.stepDescription}>
              Optional information to help with better matching.
            </Text>

            <Controller
              control={control}
              name="employment_status"
              render={({ field: { onChange, value } }) => (
                <View style={styles.fieldContainer}>
                  <Text style={styles.inputLabel}>Employment Status</Text>
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
                          {status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
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
                  label="Annual Income (Optional)"
                  placeholder="Enter your annual income"
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
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color={COLORS.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Complete Your Profile</Text>
        <View style={styles.headerRight} />
      </View>

      <View style={styles.progressSection}>
        <ProgressBar
          progress={progressPercentage}
          label={`Step ${currentStep} of ${totalSteps}`}
        />
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
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
              title="Previous"
              onPress={prevStep}
              variant="outline"
              style={styles.footerButton}
            />
          )}

          {currentStep < totalSteps ? (
            <Button
              title="Next"
              onPress={nextStep}
              style={[styles.footerButton, currentStep === 1 && styles.fullWidthButton]}
            />
          ) : (
            <Button
              title="Complete Profile"
              onPress={handleSubmit(onSubmit)}
              loading={isLoading}
              style={styles.footerButton}
            />
          )}
        </View>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
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