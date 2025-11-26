import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  TouchableOpacity,
  Switch,
  Alert,
  Platform,
  Modal,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

import { useAuthStore } from '../../store/authStore';
import { useThemeStore } from '../../store/themeStore';
import { useLanguage } from '../../contexts/LanguageContext';
import { Button } from '../../components/Button';
import { COLORS, SPACING, FONTS } from '../../constants/config';
import { apiClient } from '../../services/api';
import { useColors } from '../../hooks/useColors';

import { logger } from '../../utils/logger';
export const SettingsScreen: React.FC = () => {
  const navigation = useNavigation();
  const { user, logout, updateUser } = useAuthStore();
  const { currentLanguage, changeLanguage, t } = useLanguage();
  const { mode: themeMode, toggleMode: toggleTheme } = useThemeStore();
  const colors = useColors();
  const [notifications, setNotifications] = useState(true);
  const [showLanguageModal, setShowLanguageModal] = useState(false);
  const [showRoleModal, setShowRoleModal] = useState(false);
  const [updatingRole, setUpdatingRole] = useState(false);

  const handleRoleChange = async (newRole: string) => {
    try {
      setUpdatingRole(true);
      logger.debug('Updating role to:', newRole);

      // Call API to update user role
      const response = await apiClient.put('/auth/me', {
        role: newRole,
      });

      logger.debug('Role update response:', response);

      // Update local user data
      if (updateUser) {
        updateUser({ ...user, role: newRole });
      }

      setShowRoleModal(false);

      if (Platform.OS === 'web') {
        window.alert(`Role updated to ${newRole.toUpperCase()} successfully!`);
      } else {
        Alert.alert('Success', `Role updated to ${newRole.toUpperCase()} successfully!`);
      }
    } catch (error: unknown) {
      logger.error('Error updating role:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to update role';

      if (Platform.OS === 'web') {
        window.alert('Error: ' + errorMessage);
      } else {
        Alert.alert('Error', errorMessage);
      }
    } finally {
      setUpdatingRole(false);
    }
  };

  const handleLogout = async () => {
    logger.debug('Logout button pressed');

    if (Platform.OS === 'web') {
      // Use window.confirm for web
      const confirmed = window.confirm(
        `${t('settings.logout_confirm_title')}\n\n${t('settings.logout_confirm_message')}`
      );
      if (confirmed) {
        logger.debug('Logout confirmed');
        logout();
      }
    } else {
      // Use Alert.alert for mobile
      Alert.alert(
        t('settings.logout_confirm_title'),
        t('settings.logout_confirm_message'),
        [
          { text: t('settings.cancel'), style: 'cancel' },
          {
            text: t('settings.logout'),
            style: 'destructive',
            onPress: () => {
              logger.debug('Logout confirmed');
              logout();
            },
          },
        ]
      );
    }
  };

  const settingsSections = [
    {
      title: t('settings.preferences'),
      items: [
        {
          id: 'language',
          icon: 'language' as const,
          label: t('settings.language'),
          value: currentLanguage === 'en' ? t('settings.english') : currentLanguage === 'es' ? t('settings.spanish') : currentLanguage,
          type: 'select' as const,
          onPress: () => {
            logger.debug('Language selector pressed');
            setShowLanguageModal(true);
          },
        },
        {
          id: 'notifications',
          icon: 'notifications' as const,
          label: t('settings.push_notifications'),
          type: 'toggle' as const,
          value: notifications,
          onToggle: setNotifications,
        },
        {
          id: 'darkMode',
          icon: 'moon' as const,
          label: t('settings.dark_mode'),
          type: 'toggle' as const,
          value: themeMode === 'dark',
          onToggle: toggleTheme,
        },
      ],
    },
    {
      title: t('settings.account_section'),
      items: [
        {
          id: 'profile',
          icon: 'person' as const,
          label: t('settings.edit_profile'),
          type: 'navigation' as const,
          onPress: () => navigation.navigate('EditProfile'),
        },
        {
          id: 'verification',
          icon: 'shield-checkmark' as const,
          label: t('settings.verification_center'),
          type: 'navigation' as const,
          onPress: () => navigation.navigate('Verification'),
        },
        {
          id: 'password',
          icon: 'lock-closed' as const,
          label: t('settings.change_password'),
          type: 'navigation' as const,
          onPress: () => {
            Alert.alert(t('settings.coming_soon_title'), t('settings.coming_soon_message'));
          },
        },
        {
          id: 'privacy',
          icon: 'shield-checkmark' as const,
          label: t('settings.privacy_settings'),
          type: 'navigation' as const,
          onPress: () => {
            navigation.navigate('PrivacySettings');
          },
        },
      ],
    },
    {
      title: t('settings.support_section'),
      items: [
        {
          id: 'help',
          icon: 'help-circle' as const,
          label: t('settings.help_center'),
          type: 'navigation' as const,
          onPress: () => {
            Alert.alert(t('settings.coming_soon_title'), t('settings.coming_soon_message'));
          },
        },
        {
          id: 'terms',
          icon: 'document-text' as const,
          label: t('settings.terms_of_service'),
          type: 'navigation' as const,
          onPress: () => {
            Alert.alert(t('settings.coming_soon_title'), t('settings.coming_soon_message'));
          },
        },
        {
          id: 'privacy-policy',
          icon: 'document' as const,
          label: t('settings.privacy_policy'),
          type: 'navigation' as const,
          onPress: () => {
            Alert.alert(t('settings.coming_soon_title'), t('settings.coming_soon_message'));
          },
        },
      ],
    },
  ];

  const styles = createStyles(colors);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
        bounces={true}
        keyboardShouldPersistTaps="handled"
      >
        {/* User Info */}
        <View style={styles.userCard}>
          <View style={styles.avatar}>
            <Ionicons name="person" size={40} color={colors.primary} />
          </View>
          <View style={styles.userInfo}>
            <Text style={styles.userName}>{user?.email?.split('@')[0] || 'User'}</Text>
            <Text style={styles.userEmail}>{user?.email}</Text>
            <TouchableOpacity
              style={styles.roleBadge}
              onPress={() => setShowRoleModal(true)}
            >
              <Text style={styles.roleText}>{user?.role || 'User'}</Text>
              <Ionicons name="create-outline" size={14} color={colors.primary} style={{ marginLeft: 4 }} />
            </TouchableOpacity>
          </View>
        </View>

        {/* Settings Sections */}
        {settingsSections.map((section, sectionIndex) => (
          <View key={section.title} style={styles.section}>
            <Text style={styles.sectionTitle}>{section.title}</Text>
            <View style={styles.settingsCard}>
              {section.items.map((item, itemIndex) => (
                <View key={item.id}>
                  <TouchableOpacity
                    style={styles.settingItem}
                    onPress={item.type === 'toggle' ? undefined : item.onPress}
                    disabled={item.type === 'toggle'}
                  >
                    <View style={styles.settingLeft}>
                      <View style={styles.iconContainer}>
                        <Ionicons name={item.icon} size={20} color={colors.primary} />
                      </View>
                      <Text style={styles.settingLabel}>{item.label}</Text>
                    </View>
                    <View style={styles.settingRight}>
                      {item.type === 'select' && (
                        <>
                          <Text style={styles.settingValue}>{item.value}</Text>
                          <Ionicons name="chevron-forward" size={20} color={colors.textSecondary} />
                        </>
                      )}
                      {item.type === 'navigation' && (
                        <Ionicons name="chevron-forward" size={20} color={colors.textSecondary} />
                      )}
                      {item.type === 'toggle' && (
                        <Switch
                          value={item.value}
                          onValueChange={item.onToggle}
                          trackColor={{ false: colors.border, true: colors.primary }}
                          thumbColor={colors.surface}
                        />
                      )}
                    </View>
                  </TouchableOpacity>
                  {itemIndex < section.items.length - 1 && <View style={styles.divider} />}
                </View>
              ))}
            </View>
          </View>
        ))}

        {/* App Info */}
        <View style={styles.appInfo}>
          <Text style={styles.appInfoText}>{t('settings.app_version')}</Text>
          <Text style={styles.appInfoText}>{t('settings.copyright')}</Text>
        </View>

        {/* Logout Button */}
        <Button
          title={t('settings.logout')}
          onPress={handleLogout}
          variant="outline"
          style={styles.logoutButton}
        />
      </ScrollView>

      {/* Language Selection Modal */}
      <Modal
        visible={showLanguageModal}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setShowLanguageModal(false)}
      >
        <TouchableOpacity
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={() => setShowLanguageModal(false)}
        >
          <View style={styles.modalContent} onStartShouldSetResponder={() => true}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>{t('settings.select_language')}</Text>
              <TouchableOpacity onPress={() => setShowLanguageModal(false)}>
                <Ionicons name="close" size={24} color={colors.text} />
              </TouchableOpacity>
            </View>

            <Text style={styles.modalDescription}>{t('settings.choose_language')}</Text>

            {/* Language Options */}
            <TouchableOpacity
              style={[
                styles.languageOption,
                currentLanguage === 'en' && styles.languageOptionSelected
              ]}
              onPress={() => {
                changeLanguage('en');
                setShowLanguageModal(false);
              }}
            >
              <View style={styles.languageOptionContent}>
                <View style={styles.languageFlag}>
                  <Text style={styles.flagEmoji}>🇺🇸</Text>
                </View>
                <View style={styles.languageInfo}>
                  <Text style={styles.languageName}>{t('settings.english')}</Text>
                  <Text style={styles.languageNative}>English</Text>
                </View>
              </View>
              {currentLanguage === 'en' && (
                <Ionicons name="checkmark-circle" size={24} color={colors.primary} />
              )}
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.languageOption,
                currentLanguage === 'es' && styles.languageOptionSelected
              ]}
              onPress={() => {
                changeLanguage('es');
                setShowLanguageModal(false);
              }}
            >
              <View style={styles.languageOptionContent}>
                <View style={styles.languageFlag}>
                  <Text style={styles.flagEmoji}>🇪🇸</Text>
                </View>
                <View style={styles.languageInfo}>
                  <Text style={styles.languageName}>{t('settings.spanish')}</Text>
                  <Text style={styles.languageNative}>Español</Text>
                </View>
              </View>
              {currentLanguage === 'es' && (
                <Ionicons name="checkmark-circle" size={24} color={colors.primary} />
              )}
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      </Modal>

      {/* Role Selection Modal */}
      <Modal
        visible={showRoleModal}
        transparent={true}
        animationType="fade"
        onRequestClose={() => !updatingRole && setShowRoleModal(false)}
      >
        <TouchableOpacity
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={() => !updatingRole && setShowRoleModal(false)}
          disabled={updatingRole}
        >
          <View style={styles.modalContent} onStartShouldSetResponder={() => true}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Change Role</Text>
              <TouchableOpacity
                onPress={() => !updatingRole && setShowRoleModal(false)}
                disabled={updatingRole}
              >
                <Ionicons name="close" size={24} color={colors.text} />
              </TouchableOpacity>
            </View>

            <Text style={styles.modalDescription}>
              Choose your role to enable appropriate features. This determines what types of tickets you can create.
            </Text>

            {/* Role Options */}
            <TouchableOpacity
              style={[
                styles.languageOption,
                user?.role === 'lender' && styles.languageOptionSelected
              ]}
              onPress={() => !updatingRole && handleRoleChange('lender')}
              disabled={updatingRole}
            >
              <View style={styles.languageOptionContent}>
                <View style={styles.languageFlag}>
                  <Ionicons name="cash" size={28} color={colors.success} />
                </View>
                <View style={styles.languageInfo}>
                  <Text style={styles.languageName}>Lender</Text>
                  <Text style={styles.languageNative}>I want to lend money</Text>
                </View>
              </View>
              {user?.role === 'lender' && (
                <Ionicons name="checkmark-circle" size={24} color={colors.primary} />
              )}
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.languageOption,
                user?.role === 'borrower' && styles.languageOptionSelected
              ]}
              onPress={() => !updatingRole && handleRoleChange('borrower')}
              disabled={updatingRole}
            >
              <View style={styles.languageOptionContent}>
                <View style={styles.languageFlag}>
                  <Ionicons name="wallet" size={28} color={colors.info} />
                </View>
                <View style={styles.languageInfo}>
                  <Text style={styles.languageName}>Borrower</Text>
                  <Text style={styles.languageNative}>I need to borrow money</Text>
                </View>
              </View>
              {user?.role === 'borrower' && (
                <Ionicons name="checkmark-circle" size={24} color={colors.primary} />
              )}
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.languageOption,
                user?.role === 'both' && styles.languageOptionSelected
              ]}
              onPress={() => !updatingRole && handleRoleChange('both')}
              disabled={updatingRole}
            >
              <View style={styles.languageOptionContent}>
                <View style={styles.languageFlag}>
                  <Ionicons name="swap-horizontal" size={28} color={colors.warning} />
                </View>
                <View style={styles.languageInfo}>
                  <Text style={styles.languageName}>Both</Text>
                  <Text style={styles.languageNative}>I want to lend and borrow</Text>
                </View>
              </View>
              {user?.role === 'both' && (
                <Ionicons name="checkmark-circle" size={24} color={colors.primary} />
              )}
            </TouchableOpacity>

            {updatingRole && (
              <View style={{ marginTop: SPACING.md, alignItems: 'center' }}>
                <Text style={{ color: colors.textSecondary }}>Updating role...</Text>
              </View>
            )}
          </View>
        </TouchableOpacity>
      </Modal>
    </SafeAreaView>
  );
};

const createStyles = (colors: ReturnType<typeof useColors>) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    padding: SPACING.lg,
  },
  userCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
    borderWidth: 1,
    borderColor: colors.border,
  },
  avatar: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: `${colors.primary}15`,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  userInfo: {
    flex: 1,
  },
  userName: {
    fontSize: 20,
    fontFamily: FONTS.bold,
    color: colors.text,
    marginBottom: SPACING.xs,
  },
  userEmail: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
    marginBottom: SPACING.sm,
  },
  roleBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    backgroundColor: `${colors.primary}15`,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs / 2,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: `${colors.primary}30`,
  },
  roleText: {
    fontSize: 12,
    fontFamily: FONTS.medium,
    color: colors.primary,
    textTransform: 'capitalize',
  },
  section: {
    marginBottom: SPACING.lg,
  },
  sectionTitle: {
    fontSize: 14,
    fontFamily: FONTS.bold,
    color: colors.textSecondary,
    marginBottom: SPACING.sm,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  settingsCard: {
    backgroundColor: colors.surface,
    borderRadius: 16,
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
  },
  iconContainer: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: `${colors.primary}10`,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  settingLabel: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: colors.text,
  },
  settingRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  settingValue: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
    marginRight: SPACING.sm,
  },
  divider: {
    height: 1,
    backgroundColor: colors.border,
    marginLeft: SPACING.lg + 36 + SPACING.md,
  },
  appInfo: {
    alignItems: 'center',
    marginVertical: SPACING.xl,
  },
  appInfoText: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
    marginBottom: SPACING.xs,
  },
  logoutButton: {
    marginBottom: SPACING.xl,
  },
  // Language Modal Styles
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.lg,
  },
  modalContent: {
    backgroundColor: colors.surface,
    borderRadius: 20,
    padding: SPACING.xl,
    width: '100%',
    maxWidth: 400,
    borderWidth: 1,
    borderColor: colors.border,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  modalTitle: {
    fontSize: 24,
    fontFamily: FONTS.bold,
    color: colors.text,
  },
  modalDescription: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
    marginBottom: SPACING.lg,
  },
  languageOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: SPACING.lg,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: colors.border,
    marginBottom: SPACING.md,
    backgroundColor: colors.background,
  },
  languageOptionSelected: {
    borderColor: colors.primary,
    backgroundColor: `${colors.primary}08`,
  },
  languageOptionContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  languageFlag: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: colors.surface,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
    borderWidth: 1,
    borderColor: colors.border,
  },
  flagEmoji: {
    fontSize: 28,
  },
  languageInfo: {
    flex: 1,
  },
  languageName: {
    fontSize: 16,
    fontFamily: FONTS.bold,
    color: colors.text,
    marginBottom: 2,
  },
  languageNative: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
  },
});
