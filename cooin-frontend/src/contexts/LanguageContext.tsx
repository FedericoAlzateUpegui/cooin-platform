import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import i18n from '../i18n/i18n.config';
import AsyncStorage from '@react-native-async-storage/async-storage';

const LANGUAGE_KEY = '@cooin_language';

interface LanguageContextType {
  currentLanguage: string;
  changeLanguage: (language: string) => Promise<void>;
  t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState<string>(i18n.language || 'en');
  const [isI18nInitialized, setIsI18nInitialized] = useState<boolean>(false);

  useEffect(() => {
    // Wait for i18n to fully initialize
    const initializeI18n = async () => {
      if (!i18n.isInitialized) {
        await new Promise((resolve) => {
          i18n.on('initialized', resolve);
        });
      }
      setCurrentLanguage(i18n.language || 'en');
      setIsI18nInitialized(true);
    };

    initializeI18n();

    // Listen for language changes
    const handleLanguageChange = (lng: string) => {
      console.log('Language changed to:', lng);
      setCurrentLanguage(lng);
    };

    i18n.on('languageChanged', handleLanguageChange);

    return () => {
      i18n.off('languageChanged', handleLanguageChange);
    };
  }, []);

  const changeLanguage = async (language: string) => {
    try {
      console.log('Changing language to:', language);
      await i18n.changeLanguage(language);
      await AsyncStorage.setItem(LANGUAGE_KEY, language);
      setCurrentLanguage(language);
      console.log('Language changed successfully to:', language);
    } catch (error) {
      console.error('Error changing language:', error);
    }
  };

  const t = (key: string): string => {
    if (!isI18nInitialized) {
      console.warn('i18n not initialized yet, returning key:', key);
      return key;
    }
    return i18n.t(key);
  };

  // Show loading or return null while i18n initializes
  if (!isI18nInitialized) {
    console.log('Waiting for i18n initialization...');
    return null;
  }

  return (
    <LanguageContext.Provider value={{ currentLanguage, changeLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};
