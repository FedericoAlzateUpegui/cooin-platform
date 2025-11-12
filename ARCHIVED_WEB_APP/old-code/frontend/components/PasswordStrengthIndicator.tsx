import React from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import { COLORS, SPACING } from '../constants/config';
import { useLanguage } from '../contexts/LanguageContext';

interface PasswordStrengthIndicatorProps {
  password: string;
}

type PasswordStrength = 'weak' | 'medium' | 'strong';

interface StrengthConfig {
  textKey: string;
  color: string;
  percentage: number;
}

const strengthConfig: Record<PasswordStrength, StrengthConfig> = {
  weak: {
    textKey: 'password_strength.weak',
    color: COLORS.error,
    percentage: 0.33,
  },
  medium: {
    textKey: 'password_strength.good',
    color: COLORS.warning,
    percentage: 0.66,
  },
  strong: {
    textKey: 'password_strength.strong',
    color: COLORS.success,
    percentage: 1.0,
  },
};

export const PasswordStrengthIndicator: React.FC<PasswordStrengthIndicatorProps> = ({ password }) => {
  const animatedWidth = React.useRef(new Animated.Value(0)).current;
  const { t } = useLanguage();

  const calculateStrength = (pwd: string): PasswordStrength => {
    const hasMinLength = pwd.length >= 8;
    const hasUppercase = /[A-Z]/.test(pwd);
    const hasLowercase = /[a-z]/.test(pwd);
    const hasNumber = /[0-9]/.test(pwd);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(pwd);

    const metRequirements = [hasMinLength, hasUppercase, hasLowercase, hasNumber].filter(Boolean).length;

    if (metRequirements === 4 && hasSpecialChar) {
      return 'strong';
    } else if (metRequirements >= 3) {
      return 'medium';
    } else {
      return 'weak';
    }
  };

  const strength = calculateStrength(password);
  const config = strengthConfig[strength];

  React.useEffect(() => {
    Animated.timing(animatedWidth, {
      toValue: config.percentage,
      duration: 300,
      useNativeDriver: false,
    }).start();
  }, [config.percentage, animatedWidth]);

  return (
    <View style={styles.container}>
      <Text style={[styles.label, { color: config.color }]}>
        {t('password_strength.label')} {t(config.textKey)}
      </Text>
      <View style={styles.progressBarBackground}>
        <Animated.View
          style={[
            styles.progressBarFill,
            {
              backgroundColor: config.color,
              width: animatedWidth.interpolate({
                inputRange: [0, 1],
                outputRange: ['0%', '100%'],
              }),
            },
          ]}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginTop: SPACING.sm,
  },
  label: {
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 4,
  },
  progressBarBackground: {
    height: 4,
    backgroundColor: `${COLORS.border}`,
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    borderRadius: 2,
  },
});
