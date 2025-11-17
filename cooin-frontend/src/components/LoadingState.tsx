import React from 'react';
import {
  View,
  Text,
  ActivityIndicator,
  StyleSheet,
  ViewStyle,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SPACING, FONTS } from '../constants/config';

interface LoadingStateProps {
  /** Loading text to display */
  text?: string;
  /** Size of the loading indicator */
  size?: 'small' | 'large';
  /** Whether to show as full screen loading */
  fullScreen?: boolean;
  /** Custom style for the container */
  style?: ViewStyle;
  /** Loading variant */
  variant?: 'spinner' | 'dots' | 'skeleton';
}

/**
 * LoadingState Component
 *
 * Displays loading indicators with optional text.
 * Can be used inline or as a full-screen overlay.
 *
 * Usage:
 * ```tsx
 * // Inline loading
 * <LoadingState text="Loading data..." />
 *
 * // Full screen loading
 * <LoadingState text="Please wait..." fullScreen />
 *
 * // Small spinner
 * <LoadingState size="small" />
 * ```
 */
export const LoadingState: React.FC<LoadingStateProps> = ({
  text = 'Loading...',
  size = 'large',
  fullScreen = false,
  style,
  variant = 'spinner',
}) => {
  const containerStyle = fullScreen ? styles.fullScreenContainer : styles.inlineContainer;

  const renderLoadingIndicator = () => {
    switch (variant) {
      case 'spinner':
        return (
          <ActivityIndicator
            size={size}
            color={COLORS.primary}
            style={styles.indicator}
          />
        );

      case 'dots':
        return (
          <View style={styles.dotsContainer}>
            <View style={[styles.dot, styles.dot1]} />
            <View style={[styles.dot, styles.dot2]} />
            <View style={[styles.dot, styles.dot3]} />
          </View>
        );

      case 'skeleton':
        return (
          <View style={styles.skeletonContainer}>
            <View style={styles.skeletonLine} />
            <View style={[styles.skeletonLine, styles.skeletonLineShort]} />
            <View style={styles.skeletonLine} />
          </View>
        );

      default:
        return <ActivityIndicator size={size} color={COLORS.primary} />;
    }
  };

  return (
    <View style={[containerStyle, style]}>
      {renderLoadingIndicator()}
      {text && (
        <Text style={[styles.text, size === 'small' && styles.textSmall]}>
          {text}
        </Text>
      )}
    </View>
  );
};

/**
 * EmptyState Component
 *
 * Displays when there's no data to show.
 */
interface EmptyStateProps {
  icon?: keyof typeof Ionicons.glyphMap;
  title: string;
  message?: string;
  action?: {
    label: string;
    onPress: () => void;
  };
  style?: ViewStyle;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon = 'inbox',
  title,
  message,
  action,
  style,
}) => {
  return (
    <View style={[styles.emptyContainer, style]}>
      <Ionicons name={icon} size={64} color={COLORS.textSecondary} />
      <Text style={styles.emptyTitle}>{title}</Text>
      {message && <Text style={styles.emptyMessage}>{message}</Text>}
      {action && (
        <View style={styles.emptyAction}>
          <Text style={styles.emptyActionText} onPress={action.onPress}>
            {action.label}
          </Text>
        </View>
      )}
    </View>
  );
};

/**
 * ErrorState Component
 *
 * Displays when an error occurs with retry option.
 */
interface ErrorStateProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  style?: ViewStyle;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Oops! Something went wrong',
  message,
  onRetry,
  style,
}) => {
  return (
    <View style={[styles.errorContainer, style]}>
      <Ionicons name="alert-circle" size={64} color={COLORS.error} />
      <Text style={styles.errorTitle}>{title}</Text>
      <Text style={styles.errorMessage}>{message}</Text>
      {onRetry && (
        <View style={styles.errorAction}>
          <Ionicons name="refresh" size={20} color={COLORS.primary} />
          <Text style={styles.errorActionText} onPress={onRetry}>
            Try Again
          </Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  // Loading States
  fullScreenContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
  inlineContainer: {
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.xl,
  },
  indicator: {
    marginBottom: SPACING.md,
  },
  text: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: SPACING.sm,
  },
  textSmall: {
    fontSize: 14,
    marginTop: SPACING.xs,
  },

  // Dots variant
  dotsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: SPACING.sm,
  },
  dot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: COLORS.primary,
  },
  dot1: {
    opacity: 0.3,
  },
  dot2: {
    opacity: 0.6,
  },
  dot3: {
    opacity: 1,
  },

  // Skeleton variant
  skeletonContainer: {
    width: '100%',
    gap: SPACING.md,
  },
  skeletonLine: {
    height: 16,
    backgroundColor: COLORS.border,
    borderRadius: 4,
  },
  skeletonLineShort: {
    width: '60%',
  },

  // Empty State
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.xl,
  },
  emptyTitle: {
    fontSize: 20,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    textAlign: 'center',
    marginTop: SPACING.lg,
    marginBottom: SPACING.sm,
  },
  emptyMessage: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: SPACING.lg,
    lineHeight: 20,
  },
  emptyAction: {
    marginTop: SPACING.md,
  },
  emptyActionText: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: COLORS.primary,
  },

  // Error State
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.xl,
  },
  errorTitle: {
    fontSize: 20,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    textAlign: 'center',
    marginTop: SPACING.lg,
    marginBottom: SPACING.sm,
  },
  errorMessage: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: SPACING.lg,
    lineHeight: 20,
  },
  errorAction: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: SPACING.sm,
    marginTop: SPACING.md,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.lg,
    backgroundColor: COLORS.surface,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  errorActionText: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: COLORS.primary,
  },
});
