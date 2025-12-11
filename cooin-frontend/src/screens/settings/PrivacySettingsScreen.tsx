import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  Switch,
  TouchableOpacity,
  Platform,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useProfileStore } from '../../store/profileStore';
import { useLanguage } from '../../contexts/LanguageContext';
import { Button } from '../../components/Button';
import { COLORS, SPACING, FONTS } from '../../constants/config';
import { useColors } from '../../hooks/useColors';
import { logger } from '../../utils/logger';

interface PrivacySettingsScreenProps {
  navigation: any;
}

export const PrivacySettingsScreen: React.FC<PrivacySettingsScreenProps> = ({ navigation }) => {
  const colors = useColors();
  const styles = createStyles(colors);
  const { profile, isLoading, updateProfile, loadProfile } = useProfileStore();
  const { t } = useLanguage();

  const [showRealName, setShowRealName] = useState(false);
  const [showLocation, setShowLocation] = useState(true);
  const [showIncomeRange, setShowIncomeRange] = useState(true);
  const [showEmployment, setShowEmployment] = useState(true);
  const [isProfilePublic, setIsProfilePublic] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  // Load profile data on mount
  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  // Populate settings with existing profile data
  useEffect(() => {
    if (profile) {
      setShowRealName(profile.show_real_name ?? false);
      setShowLocation(profile.show_location ?? true);
      setShowIncomeRange(profile.show_income_range ?? true);
      setShowEmployment(profile.show_employment ?? true);
      setIsProfilePublic(profile.is_profile_public ?? true);
    }
  }, [profile]);

  // Track changes
  useEffect(() => {
    if (profile) {
      const changed =
        showRealName !== (profile.show_real_name ?? false) ||
        showLocation !== (profile.show_location ?? true) ||
        showIncomeRange !== (profile.show_income_range ?? true) ||
        showEmployment !== (profile.show_employment ?? true) ||
        isProfilePublic !== (profile.is_profile_public ?? true);
      setHasChanges(changed);
    }
  }, [showRealName, showLocation, showIncomeRange, showEmployment, isProfilePublic, profile]);

  const handleSave = async () => {
    try {
      setIsSaving(true);

      await updateProfile({
        show_real_name: showRealName,
        show_location: showLocation,
        show_income_range: showIncomeRange,
        show_employment: showEmployment,
        is_profile_public: isProfilePublic,
      });

      if (Platform.OS === 'web') {
        window.alert('Privacy settings updated successfully!');
      } else {
        Alert.alert('Success', 'Privacy settings updated successfully!');
      }

      setHasChanges(false);
      navigation.goBack();
    } catch (error: unknown) {
      logger.error('Error updating privacy settings', error);

      if (Platform.OS === 'web') {
        window.alert('Error: Failed to update privacy settings');
      } else {
        Alert.alert('Error', 'Failed to update privacy settings');
      }
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    if (hasChanges) {
      if (Platform.OS === 'web') {
        const confirmed = window.confirm('You have unsaved changes. Are you sure you want to leave?');
        if (confirmed) {
          navigation.goBack();
        }
      } else {
        Alert.alert(
          'Unsaved Changes',
          'You have unsaved changes. Are you sure you want to leave?',
          [
            { text: 'Stay', style: 'cancel' },
            { text: 'Leave', style: 'destructive', onPress: () => navigation.goBack() },
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
          <Text style={styles.loadingText}>Loading privacy settings...</Text>
        </View>
      </SafeAreaView>
    );
  }


  


  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={handleCancel} style={styles.headerButton}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Privacy Settings</Text>
        <View style={styles.headerButton} />
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={true}
      >
        {/* Profile Visibility Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Profile Visibility</Text>
          <Text style={styles.sectionDescription}>
            Control who can see your profile and what information is visible to others.
          </Text>

          <View style={styles.settingCard}>
            <View style={styles.settingItem}>
              <View style={styles.settingLeft}>
                <View style={[styles.iconContainer, { backgroundColor: isProfilePublic ? colors.success + '15' : colors.error + '15' }]}>
                  <Ionicons
                    name={isProfilePublic ? "eye" : "eye-off"}
                    size={20}
                    color={isProfilePublic ? colors.success : colors.error}
                  />
                </View>
                <View style={styles.settingTextContainer}>
                  <Text style={styles.settingLabel}>Public Profile</Text>
                  <Text style={styles.settingHint}>
                    {isProfilePublic
                      ? 'Your profile is visible to everyone'
                      : 'Your profile is hidden from searches'}
                  </Text>
                </View>
              </View>
              <Switch
                value={isProfilePublic}
                onValueChange={setIsProfilePublic}
                trackColor={{ false: colors.border, true: colors.success + '60' }}
                thumbColor={colors.surface}
              />
            </View>
          </View>
        </View>

        {/* Personal Information Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Personal Information</Text>
          <Text style={styles.sectionDescription}>
            Choose what personal information to display on your profile.
          </Text>

          <View style={styles.settingCard}>
            {/* Show Real Name */}
            <View style={styles.settingItem}>
              <View style={styles.settingLeft}>
                <View style={styles.iconContainer}>
                  <Ionicons name="person" size={20} color={colors.primary} />
                </View>
                <View style={styles.settingTextContainer}>
                  <Text style={styles.settingLabel}>Show Real Name</Text>
                  <Text style={styles.settingHint}>
                    {showRealName
                      ? 'Display your first and last name'
                      : 'Use display name instead'}
                  </Text>
                </View>
              </View>
              <Switch
                value={showRealName}
                onValueChange={setShowRealName}
                trackColor={{ false: colors.border, true: colors.primary + '60' }}
                thumbColor={colors.surface}
              />
            </View>

            <View style={styles.divider} />

            {/* Show Location */}
            <View style={styles.settingItem}>
              <View style={styles.settingLeft}>
                <View style={styles.iconContainer}>
                  <Ionicons name="location" size={20} color={colors.primary} />
                </View>
                <View style={styles.settingTextContainer}>
                  <Text style={styles.settingLabel}>Show Location</Text>
                  <Text style={styles.settingHint}>
                    {showLocation
                      ? 'Display your city and country'
                      : 'Location will be hidden'}
                  </Text>
                </View>
              </View>
              <Switch
                value={showLocation}
                onValueChange={setShowLocation}
                trackColor={{ false: colors.border, true: colors.primary + '60' }}
                thumbColor={colors.surface}
              />
            </View>
          </View>
        </View>

        {/* Financial Information Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Financial Information</Text>
          <Text style={styles.sectionDescription}>
            Control visibility of your financial details.
          </Text>

          <View style={styles.settingCard}>
            {/* Show Income Range */}
            <View style={styles.settingItem}>
              <View style={styles.settingLeft}>
                <View style={styles.iconContainer}>
                  <Ionicons name="cash" size={20} color={colors.primary} />
                </View>
                <View style={styles.settingTextContainer}>
                  <Text style={styles.settingLabel}>Show Income Range</Text>
                  <Text style={styles.settingHint}>
                    {showIncomeRange
                      ? 'Display your income bracket'
                      : 'Income range will be hidden'}
                  </Text>
                </View>
              </View>
              <Switch
                value={showIncomeRange}
                onValueChange={setShowIncomeRange}
                trackColor={{ false: colors.border, true: colors.primary + '60' }}
                thumbColor={colors.surface}
              />
            </View>

            <View style={styles.divider} />

            {/* Show Employment */}
            <View style={styles.settingItem}>
              <View style={styles.settingLeft}>
                <View style={styles.iconContainer}>
                  <Ionicons name="briefcase" size={20} color={colors.primary} />
                </View>
                <View style={styles.settingTextContainer}>
                  <Text style={styles.settingLabel}>Show Employment</Text>
                  <Text style={styles.settingHint}>
                    {showEmployment
                      ? 'Display employment status and employer'
                      : 'Employment info will be hidden'}
                  </Text>
                </View>
              </View>
              <Switch
                value={showEmployment}
                onValueChange={setShowEmployment}
                trackColor={{ false: colors.border, true: colors.primary + '60' }}
                thumbColor={colors.surface}
              />
            </View>
          </View>
        </View>

        {/* Information Box */}
        <View style={styles.infoBox}>
          <Ionicons name="information-circle" size={20} color={colors.info} />
          <Text style={styles.infoText}>
            These settings control what information is visible to other users when they view your profile.
            Your email and password are always kept private.
          </Text>
        </View>

        {/* Action Buttons */}
        <View style={styles.buttonContainer}>
          <Button
            title="Save Changes"
            onPress={handleSave}
            loading={isSaving}
            disabled={isSaving || !hasChanges}
          />

          <Button
            title="Cancel"
            onPress={handleCancel}
            variant="outline"
            disabled={isSaving}
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
    marginBottom: SPACING.xs,
  },
  sectionDescription: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
    marginBottom: SPACING.md,
    lineHeight: 20,
  },
  settingCard: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.border,
    overflow: 'hidden',
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: SPACING.lg,
  },
  settingLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    marginRight: SPACING.md,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: `${colors.primary}10`,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  settingTextContainer: {
    flex: 1,
  },
  settingLabel: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: colors.text,
    marginBottom: 2,
  },
  settingHint: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
    lineHeight: 16,
  },
  divider: {
    height: 1,
    backgroundColor: colors.border,
    marginLeft: SPACING.lg + 40 + SPACING.md,
  },
  infoBox: {
    flexDirection: 'row',
    backgroundColor: `${colors.info}10`,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.lg,
    borderWidth: 1,
    borderColor: `${colors.info}30`,
  },
  infoText: {
    flex: 1,
    fontSize: 13,
    fontFamily: FONTS.regular,
    color: colors.text,
    lineHeight: 18,
    marginLeft: SPACING.sm,
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
