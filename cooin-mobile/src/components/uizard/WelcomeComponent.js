/**
 * UizardWelcomeComponent - Luxury Fintech Welcome Screen
 *
 * Premium onboarding experience with luxury styling
 * Features: Hero section, trust indicators, elegant call-to-actions
 *
 * Required Props:
 * - onGetStarted: () => void
 * - onSignIn: () => void
 */

import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  StatusBar,
  Dimensions
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import { COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS } from '../../constants/theme';

const { width, height } = Dimensions.get('window');

export const UizardWelcomeComponent = ({
  onGetStarted,
  onSignIn,
}) => {
  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.PRIMARY} />

      {/* Hero Section with Gradient Background */}
      <LinearGradient
        colors={[COLORS.PRIMARY, COLORS.PRIMARY_LIGHT]}
        style={styles.heroSection}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <View style={styles.heroContent}>
          {/* Logo Area */}
          <View style={styles.logoContainer}>
            <View style={styles.logoCircle}>
              <Text style={styles.logoText}>₡</Text>
            </View>
            <Text style={styles.brandText}>Cooin</Text>
          </View>

          {/* Hero Text */}
          <Text style={styles.heroTitle}>
            Connect with Trusted{'\n'}Financial Partners
          </Text>
          <Text style={styles.heroSubtitle}>
            Join a premium community where lenders and borrowers create meaningful financial connections
          </Text>
        </View>
      </LinearGradient>

      {/* Content Section */}
      <View style={styles.contentSection}>
        {/* Trust Indicators */}
        <View style={styles.trustIndicators}>
          <View style={styles.trustItem}>
            <View style={[styles.trustIcon, { backgroundColor: COLORS.SUCCESS }]}>
              <Text style={styles.trustIconText}>🛡️</Text>
            </View>
            <Text style={styles.trustText}>Bank-Level Security</Text>
          </View>

          <View style={styles.trustItem}>
            <View style={[styles.trustIcon, { backgroundColor: COLORS.EMERALD }]}>
              <Text style={styles.trustIconText}>🤝</Text>
            </View>
            <Text style={styles.trustText}>Trusted Community</Text>
          </View>

          <View style={styles.trustItem}>
            <View style={[styles.trustIcon, { backgroundColor: COLORS.WARM_ORANGE }]}>
              <Text style={styles.trustIconText}>💰</Text>
            </View>
            <Text style={styles.trustText}>Fair Rates</Text>
          </View>
        </View>

        {/* Action Buttons */}
        <View style={styles.actionSection}>
          <TouchableOpacity style={styles.primaryButton} onPress={onGetStarted}>
            <LinearGradient
              colors={[COLORS.PRIMARY, COLORS.PRIMARY_DARK]}
              style={styles.primaryButtonGradient}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
            >
              <Text style={styles.primaryButtonText}>Get Started</Text>
            </LinearGradient>
          </TouchableOpacity>

          <TouchableOpacity style={styles.secondaryButton} onPress={onSignIn}>
            <Text style={styles.secondaryButtonText}>
              Already have an account? <Text style={styles.signInText}>Sign In</Text>
            </Text>
          </TouchableOpacity>
        </View>

        {/* Security Badge */}
        <View style={styles.securityBadge}>
          <Text style={styles.securityText}>🔒 256-bit encryption • FDIC insured</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.WHITE,
  },

  // Hero Section
  heroSection: {
    height: height * 0.5,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: SPACING.SCREEN_PADDING,
  },
  heroContent: {
    alignItems: 'center',
    marginTop: SPACING.XXL,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: SPACING.XXL,
  },
  logoCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: COLORS.WHITE_90,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.MD,
    ...SHADOWS.FLOATING,
  },
  logoText: {
    fontSize: 36,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
    color: COLORS.PRIMARY,
  },
  brandText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_TITLE,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
    color: COLORS.WHITE,
    letterSpacing: 2,
  },
  heroTitle: {
    fontSize: TYPOGRAPHY.FONT_SIZE_LARGE,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_BOLD,
    color: COLORS.WHITE,
    textAlign: 'center',
    marginBottom: SPACING.MD,
    lineHeight: TYPOGRAPHY.LINE_HEIGHT_TIGHT * TYPOGRAPHY.FONT_SIZE_LARGE,
  },
  heroSubtitle: {
    fontSize: TYPOGRAPHY.FONT_SIZE_BODY,
    color: COLORS.WHITE_90,
    textAlign: 'center',
    lineHeight: TYPOGRAPHY.LINE_HEIGHT_RELAXED * TYPOGRAPHY.FONT_SIZE_BODY,
    paddingHorizontal: SPACING.MD,
  },

  // Content Section
  contentSection: {
    flex: 1,
    backgroundColor: COLORS.WHITE,
    paddingHorizontal: SPACING.SCREEN_PADDING,
    paddingTop: SPACING.XXL,
  },

  // Trust Indicators
  trustIndicators: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: SPACING.XXL,
  },
  trustItem: {
    flex: 1,
    alignItems: 'center',
    paddingHorizontal: SPACING.SM,
  },
  trustIcon: {
    width: 56,
    height: 56,
    borderRadius: BORDER_RADIUS.XL,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.SM,
    ...SHADOWS.CARD,
  },
  trustIconText: {
    fontSize: 24,
  },
  trustText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_MEDIUM,
    color: COLORS.DARK_GRAY,
    textAlign: 'center',
    lineHeight: TYPOGRAPHY.LINE_HEIGHT_NORMAL * TYPOGRAPHY.FONT_SIZE_CAPTION,
  },

  // Action Section
  actionSection: {
    marginBottom: SPACING.XL,
  },
  primaryButton: {
    marginBottom: SPACING.LG,
    borderRadius: BORDER_RADIUS.MD,
    ...SHADOWS.BUTTON,
  },
  primaryButtonGradient: {
    height: SPACING.BUTTON_HEIGHT,
    borderRadius: BORDER_RADIUS.MD,
    justifyContent: 'center',
    alignItems: 'center',
  },
  primaryButtonText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_BODY,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_SEMIBOLD,
    color: COLORS.WHITE,
    letterSpacing: 0.5,
  },
  secondaryButton: {
    paddingVertical: SPACING.MD,
    alignItems: 'center',
  },
  secondaryButtonText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_CAPTION,
    color: COLORS.MEDIUM_GRAY,
  },
  signInText: {
    color: COLORS.PRIMARY,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_SEMIBOLD,
  },

  // Security Badge
  securityBadge: {
    alignItems: 'center',
    paddingBottom: SPACING.XL,
  },
  securityText: {
    fontSize: TYPOGRAPHY.FONT_SIZE_SMALL,
    color: COLORS.MEDIUM_GRAY,
    fontWeight: TYPOGRAPHY.FONT_WEIGHT_MEDIUM,
  },
});