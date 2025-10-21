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
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

import { useAuthStore } from '../../store/authStore';
import { useLanguage } from '../../contexts/LanguageContext';
import { Button } from '../../components/Button';
import { COLORS, SPACING, FONTS } from '../../constants/config';

interface SettingsScreenProps {
  navigation: any;
}

export const SettingsScreen: React.FC<SettingsScreenProps> = ({ navigation }) => {
  const { user, logout } = useAuthStore();
  const { currentLanguage, changeLanguage } = useLanguage();
  const [notifications, setNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  const handleLogout = async () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Logout',
          style: 'destructive',
          onPress: async () => {
            await logout();
          },
        },
      ]
    );
  };

  const settingsSections = [
    {
      title: 'Preferences',
      items: [
        {
          id: 'language',
          icon: 'language' as const,
          label: 'Language',
          value: currentLanguage === 'en' ? 'English' : currentLanguage === 'es' ? 'Español' : currentLanguage,
          type: 'select' as const,
          onPress: () => {
            Alert.alert(
              'Select Language',
              'Choose your preferred language',
              [
                { text: 'English', onPress: async () => await changeLanguage('en') },
                { text: 'Español', onPress: async () => await changeLanguage('es') },
                { text: 'Cancel', style: 'cancel' },
              ]
            );
          },
        },
        {
          id: 'notifications',
          icon: 'notifications' as const,
          label: 'Push Notifications',
          type: 'toggle' as const,
          value: notifications,
          onToggle: setNotifications,
        },
        {
          id: 'darkMode',
          icon: 'moon' as const,
          label: 'Dark Mode',
          type: 'toggle' as const,
          value: darkMode,
          onToggle: setDarkMode,
        },
      ],
    },
    {
      title: 'Account',
      items: [
        {
          id: 'profile',
          icon: 'person' as const,
          label: 'Edit Profile',
          type: 'navigation' as const,
          onPress: () => navigation.navigate('Profile'),
        },
        {
          id: 'verification',
          icon: 'shield-checkmark' as const,
          label: 'Verification Center',
          type: 'navigation' as const,
          onPress: () => navigation.navigate('Verification'),
        },
        {
          id: 'password',
          icon: 'lock-closed' as const,
          label: 'Change Password',
          type: 'navigation' as const,
          onPress: () => {
            Alert.alert('Change Password', 'This feature is coming soon!');
          },
        },
        {
          id: 'privacy',
          icon: 'shield-checkmark' as const,
          label: 'Privacy Settings',
          type: 'navigation' as const,
          onPress: () => {
            Alert.alert('Privacy Settings', 'This feature is coming soon!');
          },
        },
      ],
    },
    {
      title: 'Support',
      items: [
        {
          id: 'help',
          icon: 'help-circle' as const,
          label: 'Help Center',
          type: 'navigation' as const,
          onPress: () => {
            Alert.alert('Help Center', 'This feature is coming soon!');
          },
        },
        {
          id: 'terms',
          icon: 'document-text' as const,
          label: 'Terms of Service',
          type: 'navigation' as const,
          onPress: () => {
            Alert.alert('Terms of Service', 'This feature is coming soon!');
          },
        },
        {
          id: 'privacy-policy',
          icon: 'document' as const,
          label: 'Privacy Policy',
          type: 'navigation' as const,
          onPress: () => {
            Alert.alert('Privacy Policy', 'This feature is coming soon!');
          },
        },
      ],
    },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* User Info */}
        <View style={styles.userCard}>
          <View style={styles.avatar}>
            <Ionicons name="person" size={40} color={COLORS.primary} />
          </View>
          <View style={styles.userInfo}>
            <Text style={styles.userName}>{user?.email?.split('@')[0] || 'User'}</Text>
            <Text style={styles.userEmail}>{user?.email}</Text>
            <View style={styles.roleBadge}>
              <Text style={styles.roleText}>{user?.role || 'User'}</Text>
            </View>
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
                        <Ionicons name={item.icon} size={20} color={COLORS.primary} />
                      </View>
                      <Text style={styles.settingLabel}>{item.label}</Text>
                    </View>
                    <View style={styles.settingRight}>
                      {item.type === 'select' && (
                        <>
                          <Text style={styles.settingValue}>{item.value}</Text>
                          <Ionicons name="chevron-forward" size={20} color={COLORS.textSecondary} />
                        </>
                      )}
                      {item.type === 'navigation' && (
                        <Ionicons name="chevron-forward" size={20} color={COLORS.textSecondary} />
                      )}
                      {item.type === 'toggle' && (
                        <Switch
                          value={item.value}
                          onValueChange={item.onToggle}
                          trackColor={{ false: COLORS.border, true: COLORS.primary }}
                          thumbColor={COLORS.surface}
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
          <Text style={styles.appInfoText}>Cooin v1.0.0</Text>
          <Text style={styles.appInfoText}>© 2025 Cooin. All rights reserved.</Text>
        </View>

        {/* Logout Button */}
        <Button
          title="Logout"
          onPress={handleLogout}
          variant="outline"
          style={styles.logoutButton}
        />
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    padding: SPACING.lg,
  },
  userCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  avatar: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: `${COLORS.primary}15`,
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
    color: COLORS.text,
    marginBottom: SPACING.xs,
  },
  userEmail: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
  },
  roleBadge: {
    alignSelf: 'flex-start',
    backgroundColor: `${COLORS.primary}15`,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs / 2,
    borderRadius: 12,
  },
  roleText: {
    fontSize: 12,
    fontFamily: FONTS.medium,
    color: COLORS.primary,
    textTransform: 'capitalize',
  },
  section: {
    marginBottom: SPACING.lg,
  },
  sectionTitle: {
    fontSize: 14,
    fontFamily: FONTS.bold,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  settingsCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
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
    backgroundColor: `${COLORS.primary}10`,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  settingLabel: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: COLORS.text,
  },
  settingRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  settingValue: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    marginRight: SPACING.sm,
  },
  divider: {
    height: 1,
    backgroundColor: COLORS.border,
    marginLeft: SPACING.lg + 36 + SPACING.md,
  },
  appInfo: {
    alignItems: 'center',
    marginVertical: SPACING.xl,
  },
  appInfoText: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    marginBottom: SPACING.xs,
  },
  logoutButton: {
    marginBottom: SPACING.xl,
  },
});
