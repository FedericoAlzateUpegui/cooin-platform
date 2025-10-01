/**
 * Toast Configuration
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { THEME } from '../constants/theme';

export const toastConfig = {
  success: ({ text1, text2 }) => (
    <View style={[styles.container, styles.success]}>
      <Icon name="check-circle" size={24} color={THEME.colors.WHITE} />
      <View style={styles.textContainer}>
        <Text style={styles.title}>{text1}</Text>
        {text2 ? <Text style={styles.subtitle}>{text2}</Text> : null}
      </View>
    </View>
  ),
  error: ({ text1, text2 }) => (
    <View style={[styles.container, styles.error]}>
      <Icon name="error" size={24} color={THEME.colors.WHITE} />
      <View style={styles.textContainer}>
        <Text style={styles.title}>{text1}</Text>
        {text2 ? <Text style={styles.subtitle}>{text2}</Text> : null}
      </View>
    </View>
  ),
  info: ({ text1, text2 }) => (
    <View style={[styles.container, styles.info]}>
      <Icon name="info" size={24} color={THEME.colors.WHITE} />
      <View style={styles.textContainer}>
        <Text style={styles.title}>{text1}</Text>
        {text2 ? <Text style={styles.subtitle}>{text2}</Text> : null}
      </View>
    </View>
  ),
  warning: ({ text1, text2 }) => (
    <View style={[styles.container, styles.warning]}>
      <Icon name="warning" size={24} color={THEME.colors.WHITE} />
      <View style={styles.textContainer}>
        <Text style={styles.title}>{text1}</Text>
        {text2 ? <Text style={styles.subtitle}>{text2}</Text> : null}
      </View>
    </View>
  ),
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: THEME.spacing.md,
    paddingVertical: THEME.spacing.sm,
    marginHorizontal: THEME.spacing.md,
    borderRadius: THEME.borderRadius.lg,
    ...THEME.shadows.medium,
  },
  success: {
    backgroundColor: THEME.colors.SUCCESS,
  },
  error: {
    backgroundColor: THEME.colors.ERROR,
  },
  info: {
    backgroundColor: THEME.colors.INFO,
  },
  warning: {
    backgroundColor: THEME.colors.WARNING,
  },
  textContainer: {
    flex: 1,
    marginLeft: THEME.spacing.sm,
  },
  title: {
    fontSize: THEME.fontSizes.md,
    fontFamily: THEME.fonts.medium,
    color: THEME.colors.WHITE,
  },
  subtitle: {
    fontSize: THEME.fontSizes.sm,
    fontFamily: THEME.fonts.regular,
    color: THEME.colors.WHITE,
    opacity: 0.9,
    marginTop: 2,
  },
});