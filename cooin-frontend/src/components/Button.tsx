import React from 'react';
import {
  TouchableOpacity,
  Text,
  StyleSheet,
  ActivityIndicator,
  ViewStyle,
  TextStyle,
} from 'react-native';
import { COLORS, SPACING, FONTS } from '../constants/config';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

export const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  style,
  textStyle,
}) => {
  const isDisabled = disabled || loading;

  const getButtonStyle = (): ViewStyle => {
    const baseStyle: ViewStyle = {
      ...styles.button,
      ...styles[`button${size.charAt(0).toUpperCase() + size.slice(1)}` as keyof typeof styles],
    };

    switch (variant) {
      case 'primary':
        return {
          ...baseStyle,
          backgroundColor: isDisabled ? COLORS.border : COLORS.primary,
        };
      case 'secondary':
        return {
          ...baseStyle,
          backgroundColor: isDisabled ? COLORS.border : COLORS.secondary,
        };
      case 'outline':
        return {
          ...baseStyle,
          backgroundColor: 'transparent',
          borderWidth: 1,
          borderColor: isDisabled ? COLORS.border : COLORS.primary,
        };
      case 'ghost':
        return {
          ...baseStyle,
          backgroundColor: 'transparent',
        };
      default:
        return baseStyle;
    }
  };

  const getTextStyle = (): TextStyle => {
    const baseTextStyle: TextStyle = {
      ...styles.text,
      ...styles[`text${size.charAt(0).toUpperCase() + size.slice(1)}` as keyof typeof styles],
    };

    switch (variant) {
      case 'primary':
      case 'secondary':
        return {
          ...baseTextStyle,
          color: isDisabled ? COLORS.textSecondary : COLORS.surface,
        };
      case 'outline':
      case 'ghost':
        return {
          ...baseTextStyle,
          color: isDisabled ? COLORS.textSecondary : COLORS.primary,
        };
      default:
        return baseTextStyle;
    }
  };

  const getLoadingColor = (): string => {
    switch (variant) {
      case 'primary':
      case 'secondary':
        return COLORS.surface;
      case 'outline':
      case 'ghost':
        return COLORS.primary;
      default:
        return COLORS.surface;
    }
  };

  return (
    <TouchableOpacity
      style={[getButtonStyle(), style]}
      onPress={onPress}
      disabled={isDisabled}
      activeOpacity={0.8}
    >
      {loading ? (
        <ActivityIndicator
          size="small"
          color={getLoadingColor()}
        />
      ) : (
        <Text style={[getTextStyle(), textStyle]}>{title}</Text>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 12,
    paddingHorizontal: SPACING.lg,
  },
  buttonSmall: {
    height: 36,
    paddingHorizontal: SPACING.md,
  },
  buttonMedium: {
    height: 48,
  },
  buttonLarge: {
    height: 56,
    paddingHorizontal: SPACING.xl,
  },
  text: {
    fontFamily: FONTS.medium,
    textAlign: 'center',
  },
  textSmall: {
    fontSize: 14,
  },
  textMedium: {
    fontSize: 16,
  },
  textLarge: {
    fontSize: 18,
  },
});