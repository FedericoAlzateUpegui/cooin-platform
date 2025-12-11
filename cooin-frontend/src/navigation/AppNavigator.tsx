import React, { useEffect, useState } from 'react';
import { NavigationContainer, useNavigation } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { View, ActivityIndicator, useWindowDimensions, TouchableOpacity, Text, StyleSheet, Platform, ScrollView } from 'react-native';

import { useAuthStore } from '../store/authStore';
import { useLanguage } from '../contexts/LanguageContext';
import { COLORS } from '../constants/config';
import { useColors } from '../hooks/useColors';
import { AuthNavigator } from './AuthNavigator';
import { MatchingScreen } from '../screens/matching/MatchingScreen';
import { ConnectionsScreen } from '../screens/connections/ConnectionsScreen';
import { NotificationsScreen } from '../screens/notifications/NotificationsScreen';
import { ProfileSetupScreen } from '../screens/profile/ProfileSetupScreen';
import { EditProfileScreen } from '../screens/profile/EditProfileScreen';
import { HomeScreen } from '../screens/home/HomeScreen';
import { SettingsScreen } from '../screens/settings/SettingsScreen';
import { PrivacySettingsScreen } from '../screens/settings/PrivacySettingsScreen';
import { VerificationScreen } from '../screens/verification/VerificationScreen';
import { ChangePasswordScreen } from '../screens/settings/ChangePasswordScreen';
import { TicketsScreen } from '../screens/tickets/TicketsScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Breakpoint for responsive design
const DESKTOP_BREAKPOINT = 768;

// Navigation items configuration
const navigationItems = [
  { name: 'Home', component: HomeScreen, iconFocused: 'home', iconOutline: 'home-outline', labelKey: 'navigation.home' },
  { name: 'Tickets', component: TicketsScreen, iconFocused: 'ticket', iconOutline: 'ticket-outline', labelKey: 'navigation.tickets' },
  { name: 'Matching', component: MatchingScreen, iconFocused: 'people', iconOutline: 'people-outline', labelKey: 'navigation.matching' },
  { name: 'Connections', component: ConnectionsScreen, iconFocused: 'link', iconOutline: 'link-outline', labelKey: 'navigation.connections' },
  { name: 'Notifications', component: NotificationsScreen, iconFocused: 'notifications', iconOutline: 'notifications-outline', labelKey: 'navigation.notifications' },
  { name: 'Settings', component: SettingsScreen, iconFocused: 'settings', iconOutline: 'settings-outline', labelKey: 'navigation.settings' },
];

// Sidebar Navigation Item Component
const SidebarNavItem: React.FC<{
  item: typeof navigationItems[0];
  isActive: boolean;
  onPress: () => void;
  label: string;
  colors: ReturnType<typeof useColors>;
}> = ({ item, isActive, onPress, label, colors }) => {
  return (
    <TouchableOpacity
      style={[
        {
          flexDirection: 'row',
          alignItems: 'center',
          paddingVertical: 14,
          paddingHorizontal: 20,
          marginHorizontal: 8,
          marginVertical: 2,
          borderRadius: 8,
        },
        isActive && { backgroundColor: colors.primary + '15' }
      ]}
      onPress={onPress}
    >
      <Ionicons
        name={isActive ? item.iconFocused : item.iconOutline}
        size={24}
        color={isActive ? colors.primary : colors.textSecondary}
      />
      <Text style={[
        {
          marginLeft: 12,
          fontSize: 16,
          color: colors.textSecondary,
          fontWeight: '500',
        },
        isActive && {
          color: colors.primary,
          fontWeight: '600',
        }
      ]}>
        {label}
      </Text>
    </TouchableOpacity>
  );
};

// Desktop Sidebar Navigator
const DesktopSidebarNavigator = () => {
  const { t } = useLanguage();
  const navigation = useNavigation();
  const colors = useColors();
  const [activeScreen, setActiveScreen] = useState('Home');

  const ActiveComponent = navigationItems.find(item => item.name === activeScreen)?.component || HomeScreen;

  return (
    <View style={[styles.desktopContainer, { backgroundColor: colors.background }]}>
      {/* Left Sidebar */}
      <View style={[styles.sidebar, { backgroundColor: colors.surface, borderRightColor: colors.border }]}>
        <View style={[styles.sidebarHeader, { borderBottomColor: colors.border }]}>
          <Text style={[styles.sidebarTitle, { color: colors.primary }]}>Cooin</Text>
        </View>
        <View style={styles.sidebarNav}>
          {navigationItems.map((item) => (
            <SidebarNavItem
              key={item.name}
              item={item}
              isActive={activeScreen === item.name}
              onPress={() => setActiveScreen(item.name)}
              label={t(item.labelKey)}
              colors={colors}
            />
          ))}
        </View>
      </View>

      {/* Main Content */}
      <View style={[styles.mainContent, { backgroundColor: colors.background }]}>
        <View style={styles.screenContainer}>
          <ActiveComponent navigation={navigation} />
        </View>
      </View>
    </View>
  );
};

// Mobile Bottom Tab Navigator
const MobileTabNavigator = () => {
  const { t } = useLanguage();
  const colors = useColors();

  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          const item = navigationItems.find(item => item.name === route.name);
          const iconName = focused ? item?.iconFocused : item?.iconOutline;
          return <Ionicons name={iconName || 'home-outline'} size={size} color={color} />;
        },
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textSecondary,
        tabBarStyle: {
          backgroundColor: colors.surface,
          borderTopColor: colors.border,
        },
        headerStyle: {
          backgroundColor: colors.surface,
        },
        headerTintColor: colors.text,
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      })}
    >
      {navigationItems.map((item) => (
        <Tab.Screen
          key={item.name}
          name={item.name}
          component={item.component}
          options={{ title: t(item.labelKey) }}
        />
      ))}
    </Tab.Navigator>
  );
};

// Main Tab Navigator with responsive layout
const MainTabNavigator = () => {
  const { width } = useWindowDimensions();
  const isDesktop = width >= DESKTOP_BREAKPOINT;

  return isDesktop ? <DesktopSidebarNavigator /> : <MobileTabNavigator />;
};

const LoadingScreen = () => {
  const colors = useColors();
  return (
    <View style={{
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: colors.background
    }}>
      <ActivityIndicator size="large" color={colors.primary} />
    </View>
  );
};

export const AppNavigator: React.FC = () => {
  const { isAuthenticated, isInitializing, checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  if (isInitializing) {
    return <LoadingScreen />;
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {isAuthenticated ? (
          <>
            <Stack.Screen name="Main" component={MainTabNavigator} />
            <Stack.Screen name="Profile" component={ProfileSetupScreen} />
            <Stack.Screen name="EditProfile" component={EditProfileScreen} />
            <Stack.Screen name="PrivacySettings" component={PrivacySettingsScreen} />
            <Stack.Screen name="Verification" component={VerificationScreen} />
            <Stack.Screen name="ChangePassword" component={ChangePasswordScreen} />
          </>
        ) : (
          <Stack.Screen name="Auth" component={AuthNavigator} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  // Desktop Sidebar Styles
  desktopContainer: {
    flexDirection: 'row',
    backgroundColor: COLORS.background,
    ...Platform.select({
      web: {
        width: '100vw',
        height: '100vh',
      },
      default: {
        flex: 1,
      },
    }),
  },
  sidebar: {
    width: 240,
    backgroundColor: COLORS.surface,
    borderRightWidth: 1,
    borderRightColor: COLORS.border,
    ...Platform.select({
      web: {
        boxShadow: '2px 0 8px rgba(0, 0, 0, 0.1)',
      },
    }),
  },
  sidebarHeader: {
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  sidebarTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  sidebarNav: {
    flex: 1,
    paddingTop: 16,
  },
  sidebarItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 14,
    paddingHorizontal: 20,
    marginHorizontal: 8,
    marginVertical: 2,
    borderRadius: 8,
  },
  sidebarItemActive: {
    backgroundColor: COLORS.primary + '15', // 15% opacity
  },
  sidebarLabel: {
    marginLeft: 12,
    fontSize: 16,
    color: COLORS.textSecondary,
    fontWeight: '500',
  },
  sidebarLabelActive: {
    color: COLORS.primary,
    fontWeight: '600',
  },
  mainContent: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  screenContainer: {
    ...Platform.select({
      web: {
        width: '100%',
        height: '100%',
        overflow: 'auto' as any,
      },
      default: {
        flex: 1,
      },
    }),
  },
});