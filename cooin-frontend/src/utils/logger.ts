/**
 * Development Logger Utility
 *
 * Provides conditional logging based on environment.
 * In production, logs are suppressed to improve performance and security.
 *
 * Usage:
 *   import { logger } from '../utils/logger';
 *   logger.debug('Debug info', { data });
 *   logger.info('Info message');
 *   logger.warn('Warning');
 *   logger.error('Error occurred', error);
 */

import { Platform } from 'react-native';

// Check if we're in development mode
const isDevelopment = __DEV__;

/**
 * Log levels for filtering
 */
export enum LogLevel {
  DEBUG = 'DEBUG',
  INFO = 'INFO',
  WARN = 'WARN',
  ERROR = 'ERROR',
}

/**
 * Logger configuration
 */
interface LoggerConfig {
  enabled: boolean;
  minLevel: LogLevel;
  includeTimestamp: boolean;
  includeLocation: boolean;
}

const defaultConfig: LoggerConfig = {
  enabled: isDevelopment,
  minLevel: LogLevel.DEBUG,
  includeTimestamp: true,
  includeLocation: false,
};

let config = { ...defaultConfig };

/**
 * Configure logger settings
 */
export const configureLogger = (options: Partial<LoggerConfig>) => {
  config = { ...config, ...options };
};

/**
 * Format timestamp
 */
const getTimestamp = (): string => {
  const now = new Date();
  return now.toISOString().split('T')[1].split('.')[0]; // HH:MM:SS
};

/**
 * Get emoji for log level
 */
const getLevelEmoji = (level: LogLevel): string => {
  switch (level) {
    case LogLevel.DEBUG:
      return '🔍';
    case LogLevel.INFO:
      return 'ℹ️';
    case LogLevel.WARN:
      return '⚠️';
    case LogLevel.ERROR:
      return '❌';
    default:
      return '';
  }
};

/**
 * Format log message
 */
const formatMessage = (level: LogLevel, message: string): string => {
  const parts: string[] = [];

  if (config.includeTimestamp) {
    parts.push(`[${getTimestamp()}]`);
  }

  parts.push(getLevelEmoji(level));
  parts.push(`[${level}]`);
  parts.push(message);

  return parts.join(' ');
};

/**
 * Check if log level should be printed
 */
const shouldLog = (level: LogLevel): boolean => {
  if (!config.enabled) return false;

  const levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARN, LogLevel.ERROR];
  const currentLevelIndex = levels.indexOf(level);
  const minLevelIndex = levels.indexOf(config.minLevel);

  return currentLevelIndex >= minLevelIndex;
};

/**
 * Core logging function
 */
const log = (level: LogLevel, message: string, ...args: any[]) => {
  if (!shouldLog(level)) return;

  const formattedMessage = formatMessage(level, message);

  switch (level) {
    case LogLevel.DEBUG:
    case LogLevel.INFO:
      console.log(formattedMessage, ...args);
      break;
    case LogLevel.WARN:
      console.warn(formattedMessage, ...args);
      break;
    case LogLevel.ERROR:
      console.error(formattedMessage, ...args);
      break;
  }
};

/**
 * Logger instance
 */
export const logger = {
  /**
   * Debug level - Detailed information for debugging
   */
  debug: (message: string, ...args: any[]) => {
    log(LogLevel.DEBUG, message, ...args);
  },

  /**
   * Info level - General information
   */
  info: (message: string, ...args: any[]) => {
    log(LogLevel.INFO, message, ...args);
  },

  /**
   * Warning level - Warning messages
   */
  warn: (message: string, ...args: any[]) => {
    log(LogLevel.WARN, message, ...args);
  },

  /**
   * Error level - Error messages
   */
  error: (message: string, ...args: any[]) => {
    log(LogLevel.ERROR, message, ...args);
  },

  /**
   * Group logs together (web only)
   */
  group: (label: string) => {
    if (config.enabled && Platform.OS === 'web' && console.group) {
      console.group(formatMessage(LogLevel.INFO, label));
    }
  },

  /**
   * End log group (web only)
   */
  groupEnd: () => {
    if (config.enabled && Platform.OS === 'web' && console.groupEnd) {
      console.groupEnd();
    }
  },

  /**
   * Log table data (web only)
   */
  table: (data: any) => {
    if (config.enabled && Platform.OS === 'web' && console.table) {
      console.table(data);
    }
  },

  /**
   * Time a block of code
   */
  time: (label: string) => {
    if (config.enabled && console.time) {
      console.time(label);
    }
  },

  /**
   * End timing
   */
  timeEnd: (label: string) => {
    if (config.enabled && console.timeEnd) {
      console.timeEnd(label);
    }
  },
};

/**
 * Production-safe logger - Only logs errors in production
 */
export const safeLogger = {
  debug: isDevelopment ? logger.debug : () => {},
  info: isDevelopment ? logger.info : () => {},
  warn: isDevelopment ? logger.warn : () => {},
  error: logger.error, // Always log errors
};

export default logger;
