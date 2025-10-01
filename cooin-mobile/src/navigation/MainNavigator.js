/**
 * Main App Navigator (Bottom Tabs)
 */

import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialIcons';

// Stack Navigators
import HomeStackNavigator from './stacks/HomeStackNavigator';
import MatchingStackNavigator from './stacks/MatchingStackNavigator';
import ConnectionsStackNavigator from './stacks/ConnectionsStackNavigator';
import MessagesStackNavigator from './stacks/MessagesStackNavigator';
import ProfileStackNavigator from './stacks/ProfileStackNavigator';

// Theme
import { THEME } from '../constants/theme';

const Tab = createBottomTabNavigator();

const MainNavigator = () => {
  const { user } = useSelector((state) => state.auth);
  const { stats } = useSelector((state) => state.connections);

  const getTabBarIcon = (name, focused, color, size) => {
    const iconName = getIconName(name, focused);
    return <Icon name={iconName} size={size} color={color} />;
  };

  const getIconName = (routeName, focused) => {
    const iconMap = {
      Home: focused ? 'home' : 'home',
      Matching: focused ? 'search' : 'search',
      Connections: focused ? 'people' : 'people-outline',
      Messages: focused ? 'chat' : 'chat-bubble-outline',
      Profile: focused ? 'person' : 'person-outline',
    };
    return iconMap[routeName] || 'help';
  };

  const getTabBarBadge = (routeName) => {
    switch (routeName) {
      case 'Connections':
        return stats?.pending_received > 0 ? stats.pending_received : null;
      case 'Messages':
        // This would need unread message count from messages state
        return null;
      default:
        return null;
    }
  };

  return (
    <Tab.Navigator
      initialRouteName="Home"
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarIcon: ({ focused, color, size }) =>
          getTabBarIcon(route.name, focused, color, size),
        tabBarActiveTintColor: THEME.colors.PRIMARY,
        tabBarInactiveTintColor: THEME.colors.GRAY,
        tabBarStyle: {
          backgroundColor: THEME.colors.WHITE,
          borderTopWidth: 1,
          borderTopColor: THEME.colors.BORDER_LIGHT,
          paddingBottom: 5,
          paddingTop: 5,
          height: THEME.layout.tabBarHeight,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '600',
        },
        tabBarBadge: getTabBarBadge(route.name),
        tabBarBadgeStyle: {
          backgroundColor: THEME.colors.ERROR,
          color: THEME.colors.WHITE,
          fontSize: 10,
          minWidth: 16,
          height: 16,
        },
      })}>
      <Tab.Screen
        name="Home"
        component={HomeStackNavigator}
        options={{
          tabBarLabel: 'Home',
        }}
      />
      <Tab.Screen
        name="Matching"
        component={MatchingStackNavigator}
        options={{
          tabBarLabel: 'Discover',
        }}
      />
      <Tab.Screen
        name="Connections"
        component={ConnectionsStackNavigator}
        options={{
          tabBarLabel: 'Connections',
        }}
      />
      <Tab.Screen
        name="Messages"
        component={MessagesStackNavigator}
        options={{
          tabBarLabel: 'Messages',
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileStackNavigator}
        options={{
          tabBarLabel: 'Profile',
        }}
      />
    </Tab.Navigator>
  );
};

export default MainNavigator;