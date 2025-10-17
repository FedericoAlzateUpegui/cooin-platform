import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, SPACING } from '../constants/config';

interface PasswordRequirementRowProps {
  text: string;
  isMet: boolean;
}

export const PasswordRequirementRow: React.FC<PasswordRequirementRowProps> = ({ text, isMet }) => {
  return (
    <View style={styles.container}>
      <Text style={[styles.icon, isMet && styles.iconMet]}>
        {isMet ? '✓' : '○'}
      </Text>
      <Text style={[styles.text, isMet && styles.textMet]}>
        {text}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  icon: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginRight: SPACING.sm,
    width: 16,
  },
  iconMet: {
    color: COLORS.success,
  },
  text: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  textMet: {
    color: COLORS.success,
  },
});
