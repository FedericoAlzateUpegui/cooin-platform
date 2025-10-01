/**
 * Cooin Design System - Luxury Fintech Theme
 * Premium color palette and styling constants
 */

// Brand Colors - Luxury Fintech Palette
export const COLORS = {
  // Primary Brand Colors
  PRIMARY: '#2E86AB',        // Ocean Blue - Main brand color
  PRIMARY_LIGHT: '#4A9BC7',  // Lighter ocean blue
  PRIMARY_DARK: '#1E5F7B',   // Darker ocean blue

  // Success & Green Accents
  SUCCESS: '#10B981',        // Success Green
  EMERALD: '#059669',        // Emerald Accent (Lender color)
  SUCCESS_LIGHT: '#34D399',  // Light success

  // Secondary Colors
  PURPLE_PINK: '#A23B72',    // Premium accents
  WARM_ORANGE: '#F18F01',    // Call-to-action highlights
  DEEP_PURPLE: '#7C3AED',    // "Both" role indicator

  // Role-Specific Colors
  LENDER_COLOR: '#059669',   // Green for lenders
  BORROWER_COLOR: '#DC2626', // Red for borrowers
  BOTH_COLOR: '#7C3AED',     // Purple for both roles

  // Neutral Palette
  WHITE: '#FFFFFF',
  LIGHT_GRAY: '#F8F9FA',
  MEDIUM_GRAY: '#6C757D',
  DARK_GRAY: '#212529',
  BORDER_GRAY: '#E9ECEF',

  // Status Colors
  WARNING: '#F59E0B',
  ERROR: '#EF4444',
  INFO: '#3B82F6',

  // Transparency overlays
  BLACK_10: 'rgba(0, 0, 0, 0.1)',
  BLACK_20: 'rgba(0, 0, 0, 0.2)',
  WHITE_90: 'rgba(255, 255, 255, 0.9)',
};

// Typography - Premium Font System
export const TYPOGRAPHY = {
  // Font Families
  FONT_FAMILY_PRIMARY: 'System',
  FONT_FAMILY_SECONDARY: 'System',

  // Font Sizes
  FONT_SIZE_LARGE: 28,    // Hero titles
  FONT_SIZE_TITLE: 24,    // Page titles
  FONT_SIZE_HEADING: 20,  // Section headings
  FONT_SIZE_BODY: 16,     // Body text
  FONT_SIZE_CAPTION: 14,  // Captions, secondary text
  FONT_SIZE_SMALL: 12,    // Small text, labels

  // Font Weights
  FONT_WEIGHT_LIGHT: '300',
  FONT_WEIGHT_REGULAR: '400',
  FONT_WEIGHT_MEDIUM: '500',
  FONT_WEIGHT_SEMIBOLD: '600',
  FONT_WEIGHT_BOLD: '700',

  // Line Heights
  LINE_HEIGHT_TIGHT: 1.2,
  LINE_HEIGHT_NORMAL: 1.4,
  LINE_HEIGHT_RELAXED: 1.6,
};

// Spacing System - Premium Layout
export const SPACING = {
  XS: 4,
  SM: 8,
  MD: 16,
  LG: 24,
  XL: 32,
  XXL: 48,
  XXXL: 64,

  // Specific Use Cases
  SCREEN_PADDING: 32,
  CARD_PADDING: 20,
  BUTTON_HEIGHT: 56,
  INPUT_HEIGHT: 52,
  SECTION_SPACING: 24,
};

// Border Radius - Modern Rounded Corners
export const BORDER_RADIUS = {
  SM: 4,
  MD: 8,
  LG: 12,
  XL: 16,
  XXL: 24,
  ROUND: 50, // For circular elements
};

// Shadows - Luxury Elevation
export const SHADOWS = {
  CARD: {
    shadowColor: COLORS.BLACK_10,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3, // Android
  },
  BUTTON: {
    shadowColor: COLORS.BLACK_20,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
    elevation: 2,
  },
  FLOATING: {
    shadowColor: COLORS.BLACK_20,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 6,
  },
};

// Component Styles - Reusable Premium Components
export const COMPONENT_STYLES = {
  // Primary Button
  PRIMARY_BUTTON: {
    backgroundColor: COLORS.PRIMARY,
    height: SPACING.BUTTON_HEIGHT,
    borderRadius: BORDER_RADIUS.MD,
    justifyContent: 'center',
    alignItems: 'center',
    ...SHADOWS.BUTTON,
  },

  // Secondary Button
  SECONDARY_BUTTON: {
    backgroundColor: COLORS.WHITE,
    height: SPACING.BUTTON_HEIGHT,
    borderRadius: BORDER_RADIUS.MD,
    borderWidth: 1,
    borderColor: COLORS.PRIMARY,
    justifyContent: 'center',
    alignItems: 'center',
    ...SHADOWS.BUTTON,
  },

  // Input Field
  INPUT_FIELD: {
    backgroundColor: COLORS.WHITE,
    height: SPACING.INPUT_HEIGHT,
    borderRadius: BORDER_RADIUS.MD,
    borderWidth: 1,
    borderColor: COLORS.BORDER_GRAY,
    paddingHorizontal: SPACING.MD,
    fontSize: TYPOGRAPHY.FONT_SIZE_BODY,
    color: COLORS.DARK_GRAY,
  },

  // Card Container
  CARD: {
    backgroundColor: COLORS.WHITE,
    borderRadius: BORDER_RADIUS.LG,
    padding: SPACING.CARD_PADDING,
    ...SHADOWS.CARD,
  },

  // Screen Container
  SCREEN_CONTAINER: {
    flex: 1,
    backgroundColor: COLORS.LIGHT_GRAY,
    paddingHorizontal: SPACING.SCREEN_PADDING,
  },
};

export const THEME = {
  colors: COLORS,
  typography: TYPOGRAPHY,
  spacing: SPACING,
  borderRadius: BORDER_RADIUS,
  shadows: SHADOWS,
  componentStyles: COMPONENT_STYLES,
};