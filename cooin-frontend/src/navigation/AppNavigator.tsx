import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { View, ActivityIndicator, useWindowDimensions, TouchableOpacity, Text, StyleSheet, Platform, ScrollView } from 'react-native';

import { useAuthStore } from '../store/authStore';
import { useLanguage } from '../contexts/LanguageContext';
import { AuthNavigator } from './AuthNavigator';
import { MatchingScreen } from '../screens/matching/MatchingScreen';
import { ConnectionsScreen } from '../screens/connections/ConnectionsScreen';
import { NotificationsScreen } from '../screens/notifications/NotificationsScreen';
import { ProfileSetupScreen } from '../screens/profile/ProfileSetupScreen';
import { HomeScreen } from '../screens/home/HomeScreen';
import { SettingsScreen } from '../screens/settings/SettingsScreen';
import { VerificationScreen } from '../screens/verification/VerificationScreen';
import { TicketsScreen } from '../screens/tickets/TicketsScreen';
import { COLORS } from '../constants/config';

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
}> = ({ item, isActive, onPress, label }) => {
  return (
    <TouchableOpacity
      style={[styles.sidebarItem, isActive && styles.sidebarItemActive]}
      onPress={onPress}
    >
      <Ionicons
        name={isActive ? item.iconFocused : item.iconOutline}
        size={24}
        color={isActive ? COLORS.primary : COLORS.textSecondary}
      />
      <Text style={[styles.sidebarLabel, isActive && styles.sidebarLabelActive]}>
        {label}
      </Text>
    </TouchableOpacity>
  );
};

// Desktop Sidebar Navigator
const DesktopSidebarNavigator = () => {
  const { t } = useLanguage();
  const [activeScreen, setActiveScreen] = useState('Home');

  const ActiveComponent = navigationItems.find(item => item.name === activeScreen)?.component || HomeScreen;

  return (
    <View style={styles.desktopContainer}>
      {/* Left Sidebar */}
      <View style={styles.sidebar}>
        <View style={styles.sidebarHeader}>
          <Text style={styles.sidebarTitle}>Cooin</Text>
        </View>
        <View style={styles.sidebarNav}>
          {navigationItems.map((item) => (
            <SidebarNavItem
              key={item.name}
              item={item}
              isActive={activeScreen === item.name}
              onPress={() => setActiveScreen(item.name)}
              label={t(item.labelKey)}
            />
          ))}
        </View>
      </View>

      {/* Main Content */}
      <View style={styles.mainContent}>
        <View style={styles.screenContainer}>
          <ActiveComponent />
        </View>
      </View>
    </View>
  );
};

// Mobile Bottom Tab Navigator
const MobileTabNavigator = () => {
  const { t } = useLanguage();

  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          const item = navigationItems.find(item => item.name === route.name);
          const iconName = focused ? item?.iconFocused : item?.iconOutline;
          return <Ionicons name={iconName || 'home-outline'} size={size} color={color} />;
        },
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.textSecondary,
        tabBarStyle: {
          backgroundColor: COLORS.surface,
          borderTopColor: COLORS.border,
        },
        headerStyle: {
          backgroundColor: COLORS.surface,
        },
        headerTintColor: COLORS.text,
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

const LoadingScreen = () => (
  <View style={{
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background
  }}>
    <ActivityIndicator size="large" color={COLORS.primary} />
  </View>
);

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
            <Stack.Screen name="Verification" component={VerificationScreen} />
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
      },
      default: {
        flex: 1,
      },
    }),
  },
});