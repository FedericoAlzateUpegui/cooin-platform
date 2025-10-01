/**
 * Loading Screen Component
 */

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import { THEME } from '../constants/theme';

const LoadingScreen = ({ message = 'Loading...' }) => {
  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color={THEME.colors.PRIMARY} />
      <Text style={styles.message}>{message}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: THEME.colors.BACKGROUND_PRIMARY,
  },
  message: {
    marginTop: THEME.spacing.md,
    fontSize: THEME.fontSizes.md,
    color: THEME.colors.TEXT_SECONDARY,
    fontFamily: THEME.fonts.regular,
  },
});

export default LoadingScreen;