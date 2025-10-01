/**
 * Splash Screen Component
 */

import React, { useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  Dimensions,
} from 'react-native';
import { THEME } from '../constants/theme';

const { width, height } = Dimensions.get('window');

const SplashScreen = () => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;

  useEffect(() => {
    // Animate logo appearance
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        tension: 50,
        friction: 7,
        useNativeDriver: true,
      }),
    ]).start();
  }, [fadeAnim, scaleAnim]);

  return (
    <View style={styles.container}>
      <Animated.View
        style={[
          styles.logoContainer,
          {
            opacity: fadeAnim,
            transform: [{ scale: scaleAnim }],
          },
        ]}>
        <View style={styles.logo}>
          <Text style={styles.logoText}>Cooin</Text>
        </View>
        <Text style={styles.tagline}>Connect • Lend • Grow</Text>
      </Animated.View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>Building financial connections</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: THEME.colors.PRIMARY,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: height * 0.1,
  },
  logo: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: THEME.colors.WHITE,
    justifyContent: 'center',
    alignItems: 'center',
    ...THEME.shadows.large,
    marginBottom: THEME.spacing.lg,
  },
  logoText: {
    fontSize: 36,
    fontWeight: 'bold',
    color: THEME.colors.PRIMARY,
    fontFamily: THEME.fonts.bold,
  },
  tagline: {
    fontSize: THEME.fontSizes.lg,
    color: THEME.colors.WHITE,
    fontFamily: THEME.fonts.medium,
    opacity: 0.9,
  },
  footer: {
    position: 'absolute',
    bottom: 50,
    alignItems: 'center',
  },
  footerText: {
    fontSize: THEME.fontSizes.sm,
    color: THEME.colors.WHITE,
    fontFamily: THEME.fonts.light,
    opacity: 0.8,
  },
});

export default SplashScreen;