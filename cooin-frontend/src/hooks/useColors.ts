import { useMemo } from 'react';
import { useThemeStore } from '../store/themeStore';
import { lightTheme, darkTheme } from '../theme/colors';

export const useColors = () => {
  const mode = useThemeStore((state) => state.mode);

  return useMemo(() => {
    return mode === 'dark' ? darkTheme : lightTheme;
  }, [mode]);
};
