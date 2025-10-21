import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Modal,
  Platform,
  useWindowDimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useLanguage } from '../contexts/LanguageContext';
import { COLORS, SPACING, FONTS } from '../constants/config';

interface Language {
  code: string;
  name: string;
  nativeName: string;
  flag: string;
}

const LANGUAGES: Language[] = [
  {
    code: 'en',
    name: 'English',
    nativeName: 'English',
    flag: '🇺🇸',
  },
  {
    code: 'es',
    name: 'Spanish',
    nativeName: 'Español',
    flag: '🇪🇸',
  },
];

interface LanguageSwitcherProps {
  variant?: 'button' | 'icon' | 'dropdown';
  showLabel?: boolean;
}

export const LanguageSwitcher: React.FC<LanguageSwitcherProps> = ({
  variant = 'icon',
  showLabel = true,
}) => {
  const { currentLanguage, changeLanguage } = useLanguage();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const { width } = useWindowDimensions();

  const currentLang = LANGUAGES.find((lang) => lang.code === currentLanguage) || LANGUAGES[0];

  const handleLanguageChange = async (languageCode: string) => {
    await changeLanguage(languageCode);
    setIsModalVisible(false);
  };

  const toggleModal = () => {
    setIsModalVisible(!isModalVisible);
  };

  // Responsive modal width
  const getModalWidth = () => {
    if (width < 480) {
      return '90%';
    } else if (width < 768) {
      return '70%';
    } else {
      return Math.min(400, width * 0.4);
    }
  };

  if (variant === 'button') {
    return (
      <>
        <TouchableOpacity
          style={styles.buttonContainer}
          onPress={toggleModal}
          accessibilityLabel="Change language"
        >
          <Text style={styles.flagText}>{currentLang.flag}</Text>
          {showLabel && (
            <Text style={styles.buttonLabel}>{currentLang.nativeName}</Text>
          )}
          <Ionicons name="chevron-down" size={16} color={COLORS.textSecondary} />
        </TouchableOpacity>
        {renderModal()}
      </>
    );
  }

  if (variant === 'dropdown') {
    return (
      <>
        <TouchableOpacity
          style={styles.dropdownContainer}
          onPress={toggleModal}
          accessibilityLabel="Change language"
        >
          <View style={styles.dropdownContent}>
            <Text style={styles.flagTextLarge}>{currentLang.flag}</Text>
            <View style={styles.dropdownTextContainer}>
              <Text style={styles.dropdownLabel}>Language</Text>
              <Text style={styles.dropdownValue}>{currentLang.nativeName}</Text>
            </View>
          </View>
          <Ionicons name="chevron-forward" size={20} color={COLORS.textSecondary} />
        </TouchableOpacity>
        {renderModal()}
      </>
    );
  }

  // Default: icon variant
  return (
    <>
      <TouchableOpacity
        style={styles.iconContainer}
        onPress={toggleModal}
        accessibilityLabel="Change language"
      >
        <Text style={styles.flagText}>{currentLang.flag}</Text>
        {showLabel && Platform.OS === 'web' && (
          <Text style={styles.iconLabel}>{currentLang.code.toUpperCase()}</Text>
        )}
      </TouchableOpacity>
      {renderModal()}
    </>
  );

  function renderModal() {
    return (
      <Modal
        visible={isModalVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={toggleModal}
      >
        <TouchableOpacity
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={toggleModal}
        >
          <View
            style={[styles.modalContent, { width: getModalWidth() }]}
            onStartShouldSetResponder={() => true}
          >
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Select Language</Text>
              <TouchableOpacity onPress={toggleModal} style={styles.closeButton}>
                <Ionicons name="close" size={24} color={COLORS.text} />
              </TouchableOpacity>
            </View>

            <View style={styles.languageList}>
              {LANGUAGES.map((language) => (
                <TouchableOpacity
                  key={language.code}
                  style={[
                    styles.languageOption,
                    language.code === currentLanguage && styles.languageOptionSelected,
                  ]}
                  onPress={() => handleLanguageChange(language.code)}
                >
                  <View style={styles.languageOptionContent}>
                    <Text style={styles.languageFlag}>{language.flag}</Text>
                    <View style={styles.languageTextContainer}>
                      <Text style={styles.languageName}>{language.name}</Text>
                      <Text style={styles.languageNativeName}>{language.nativeName}</Text>
                    </View>
                  </View>
                  {language.code === currentLanguage && (
                    <Ionicons name="checkmark-circle" size={24} color={COLORS.primary} />
                  )}
                </TouchableOpacity>
              ))}
            </View>
          </View>
        </TouchableOpacity>
      </Modal>
    );
  }
};

const styles = StyleSheet.create({
  // Icon variant styles
  iconContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: SPACING.sm,
    borderRadius: 8,
    backgroundColor: COLORS.surface,
    ...Platform.select({
      web: {
        cursor: 'pointer',
      },
    }),
  },
  flagText: {
    fontSize: 24,
  },
  iconLabel: {
    marginLeft: SPACING.xs,
    fontSize: 12,
    fontFamily: FONTS.medium,
    color: COLORS.text,
  },

  // Button variant styles
  buttonContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    borderRadius: 8,
    backgroundColor: COLORS.surface,
    borderWidth: 1,
    borderColor: COLORS.border,
    ...Platform.select({
      web: {
        cursor: 'pointer',
      },
    }),
  },
  buttonLabel: {
    marginLeft: SPACING.sm,
    marginRight: SPACING.xs,
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.text,
  },

  // Dropdown variant styles
  dropdownContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.md,
    backgroundColor: COLORS.surface,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.border,
    ...Platform.select({
      web: {
        cursor: 'pointer',
      },
    }),
  },
  dropdownContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  flagTextLarge: {
    fontSize: 32,
    marginRight: SPACING.md,
  },
  dropdownTextContainer: {
    flexDirection: 'column',
  },
  dropdownLabel: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    marginBottom: 2,
  },
  dropdownValue: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: COLORS.text,
  },

  // Modal styles
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    maxWidth: 500,
    ...Platform.select({
      web: {
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      },
      default: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 4,
        elevation: 5,
      },
    }),
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  modalTitle: {
    fontSize: 20,
    fontFamily: FONTS.bold,
    color: COLORS.text,
  },
  closeButton: {
    padding: SPACING.xs,
    ...Platform.select({
      web: {
        cursor: 'pointer',
      },
    }),
  },
  languageList: {
    gap: SPACING.sm,
  },
  languageOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: SPACING.md,
    borderRadius: 8,
    backgroundColor: COLORS.background,
    borderWidth: 2,
    borderColor: 'transparent',
    ...Platform.select({
      web: {
        cursor: 'pointer',
      },
    }),
  },
  languageOptionSelected: {
    borderColor: COLORS.primary,
    backgroundColor: `${COLORS.primary}10`,
  },
  languageOptionContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  languageFlag: {
    fontSize: 32,
    marginRight: SPACING.md,
  },
  languageTextContainer: {
    flexDirection: 'column',
  },
  languageName: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: COLORS.text,
    marginBottom: 2,
  },
  languageNativeName: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
  },
});
