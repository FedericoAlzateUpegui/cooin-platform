import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  RefreshControl,
  SafeAreaView,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';

import systemNotificationService, { SystemMessage } from '../../services/systemNotificationService';
import { COLORS, SPACING, FONTS } from '../../constants/config';
import { useColors } from '../../hooks/useColors';
import { useLanguage } from '../../contexts/LanguageContext';

import { logger } from '../../utils/logger';
interface NotificationsScreenProps {
  navigation: any;
}

export const NotificationsScreen: React.FC<NotificationsScreenProps> = ({ navigation }) => {
  const colors = useColors();
  const styles = createStyles(colors);
  const [notifications, setNotifications] = useState<SystemMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  const [filter, setFilter] = useState<'all' | 'unread' | 'educational'>('all');
  const { t } = useLanguage();

  useFocusEffect(
    useCallback(() => {
      loadNotifications();
      loadUnreadCount();
    }, [filter])
  );

  const loadNotifications = async () => {
    setIsLoading(true);
    try {
      const isRead = filter === 'unread' ? false : undefined;
      const messageType = filter === 'educational' ? 'educational' : undefined;

      const response = await systemNotificationService.getMessages(
        1,
        50,
        messageType,
        undefined,
        isRead,
        false // not archived
      );
      setNotifications(response.messages || []);
    } catch (error: unknown) {
      logger.error('Failed to load notifications:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadUnreadCount = async () => {
    try {
      const count = await systemNotificationService.getUnreadCount();
      setUnreadCount(count);
    } catch (error) {
      logger.error('Failed to load unread count:', error);
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await loadNotifications();
    await loadUnreadCount();
    setIsRefreshing(false);
  };

  const handleNotificationPress = async (notification: SystemMessage) => {
    // Mark as read if not already
    if (!notification.is_read) {
      try {
        await systemNotificationService.markAsRead(notification.id);
        // Update local state
        setNotifications(prev =>
          prev.map(n => (n.id === notification.id ? { ...n, is_read: true } : n))
        );
        setUnreadCount(prev => Math.max(0, prev - 1));
      } catch (error) {
        logger.error('Failed to mark as read:', error);
      }
    }

    // Handle action URL if available
    if (notification.action_url) {
      // Navigate based on action_url
      // This is a placeholder - you can implement routing logic here
      logger.debug('Navigate to:', notification.action_url);
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await systemNotificationService.markAllAsRead();
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
      setUnreadCount(0);
    } catch (error) {
      logger.error('Failed to mark all as read:', error);
    }
  };

  const handleDeleteNotification = async (notificationId: number) => {
    try {
      await systemNotificationService.deleteMessage(notificationId);
      setNotifications(prev => prev.filter(n => n.id !== notificationId));
    } catch (error) {
      logger.error('Failed to delete notification:', error);
    }
  };

  const formatNotificationTime = (timeString: string) => {
    const notificationTime = new Date(timeString);
    const now = new Date();
    const diffInHours = (now.getTime() - notificationTime.getTime()) / (1000 * 60 * 60);

    if (diffInHours < 1) {
      const diffInMinutes = Math.floor(diffInHours * 60);
      return diffInMinutes < 1 ? t('notifications.just_now') : t('notifications.minutes_ago', { count: diffInMinutes });
    } else if (diffInHours < 24) {
      return t('notifications.hours_ago', { count: Math.floor(diffInHours) });
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return diffInDays === 1 ? t('notifications.yesterday') : t('notifications.days_ago', { count: diffInDays });
    }
  };

  const getMessageTypeColor = (type: string) => {
    const typeColors: { [key: string]: string } = {
      match_notification: colors.success,
      educational: colors.info,
      announcement: colors.primary,
      reminder: colors.warning,
      safety_tip: colors.error,
      feature_update: colors.accent,
    };
    return typeColors[type] || colors.primary;
  };

  const renderNotification = ({ item }: { item: SystemMessage }) => {
    const typeColor = getMessageTypeColor(item.message_type);
    const icon = systemNotificationService.getMessageTypeIcon(item.message_type);


    return (
      <TouchableOpacity
        style={[
          styles.notificationItem,
          !item.is_read && styles.unreadNotification,
        ]}
        onPress={() => handleNotificationPress(item)}
      >
        <View style={[styles.iconContainer, { backgroundColor: typeColor + '20' }]}>
          <Text style={styles.iconEmoji}>{icon}</Text>
        </View>

        <View style={styles.notificationContent}>
          <View style={styles.notificationHeader}>
            <Text style={[styles.title, !item.is_read && styles.unreadTitle]}>
              {item.title}
            </Text>
            <Text style={styles.timestamp}>
              {formatNotificationTime(item.created_at)}
            </Text>
          </View>

          <Text style={styles.content} numberOfLines={2}>
            {item.content}
          </Text>

          {item.category && (
            <View style={[styles.categoryBadge, { backgroundColor: typeColor + '15' }]}>
              <Text style={[styles.categoryText, { color: typeColor }]}>
                {item.category}
              </Text>
            </View>
          )}

          {item.action_label && (
            <Text style={[styles.actionLabel, { color: typeColor }]}>
              {item.action_label} →
            </Text>
          )}

          {item.priority === 'urgent' && (
            <View style={styles.urgentBadge}>
              <Text style={styles.urgentText}>{t('notifications.urgent')}</Text>
            </View>
          )}
        </View>

        {!item.is_read && <View style={styles.unreadDot} />}
      </TouchableOpacity>
    );
  };

  const renderFilterTabs = () => (
    <View style={styles.filterContainer}>
      <TouchableOpacity
        style={[styles.filterTab, filter === 'all' && styles.activeFilterTab]}
        onPress={() => setFilter('all')}
      >
        <Text style={[styles.filterText, filter === 'all' && styles.activeFilterText]}>
          {t('notifications.filter_all')}
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.filterTab, filter === 'unread' && styles.activeFilterTab]}
        onPress={() => setFilter('unread')}
      >
        <Text style={[styles.filterText, filter === 'unread' && styles.activeFilterText]}>
          {t('notifications.filter_unread')} {unreadCount > 0 && `(${unreadCount})`}
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.filterTab, filter === 'educational' && styles.activeFilterTab]}
        onPress={() => setFilter('educational')}
      >
        <Text style={[styles.filterText, filter === 'educational' && styles.activeFilterText]}>
          📚 {t('notifications.filter_educational')}
        </Text>
      </TouchableOpacity>
    </View>
  );

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Ionicons name="notifications-outline" size={64} color={colors.textSecondary} />
      <Text style={styles.emptyTitle}>{t('notifications.no_notifications')}</Text>
      <Text style={styles.emptyDescription}>
        {filter === 'educational'
          ? t('notifications.no_educational_description')
          : t('notifications.no_notifications_description')}
      </Text>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>{t('notifications.title')}</Text>
        {unreadCount > 0 && (
          <TouchableOpacity
            style={styles.markAllButton}
            onPress={handleMarkAllRead}
          >
            <Text style={styles.markAllText}>{t('notifications.mark_all_read')}</Text>
          </TouchableOpacity>
        )}
      </View>

      {renderFilterTabs()}

      <FlatList
        data={notifications}
        renderItem={renderNotification}
        keyExtractor={(item) => item.id.toString()}
        ListEmptyComponent={!isLoading ? renderEmptyState : null}
        contentContainerStyle={[
          styles.content,
          notifications.length === 0 && styles.centerContent,
        ]}
        refreshControl={
          <RefreshControl refreshing={isRefreshing} onRefresh={handleRefresh} />
        }
        showsVerticalScrollIndicator={false}
      />
    </SafeAreaView>
  );
};

const createStyles = (colors: ReturnType<typeof useColors>) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    backgroundColor: colors.surface,
  },
  headerTitle: {
    fontSize: 28,
    fontFamily: FONTS.bold,
    color: colors.text,
  },
  markAllButton: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
  },
  markAllText: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    color: colors.primary,
  },
  filterContainer: {
    flexDirection: 'row',
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  filterTab: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    marginRight: SPACING.sm,
    borderRadius: 20,
    backgroundColor: colors.background,
  },
  activeFilterTab: {
    backgroundColor: colors.primary,
  },
  filterText: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    color: colors.textSecondary,
  },
  activeFilterText: {
    color: colors.surface,
  },
  content: {
    padding: SPACING.lg,
    flexGrow: 1,
  },
  centerContent: {
    justifyContent: 'center',
  },
  notificationItem: {
    flexDirection: 'row',
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    borderWidth: 1,
    borderColor: colors.border,
  },
  unreadNotification: {
    borderColor: colors.primary,
    borderWidth: 2,
  },
  iconContainer: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  iconEmoji: {
    fontSize: 24,
  },
  notificationContent: {
    flex: 1,
  },
  notificationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: SPACING.xs,
  },
  title: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: colors.text,
    flex: 1,
    marginRight: SPACING.sm,
  },
  unreadTitle: {
    fontFamily: FONTS.bold,
  },
  timestamp: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
  },
  content: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
    lineHeight: 20,
    marginBottom: SPACING.xs,
  },
  categoryBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: SPACING.sm,
    paddingVertical: 2,
    borderRadius: 8,
    marginTop: SPACING.xs,
  },
  categoryText: {
    fontSize: 10,
    fontFamily: FONTS.medium,
  },
  actionLabel: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    marginTop: SPACING.sm,
  },
  urgentBadge: {
    alignSelf: 'flex-start',
    backgroundColor: colors.error,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 2,
    borderRadius: 8,
    marginTop: SPACING.xs,
  },
  urgentText: {
    fontSize: 10,
    fontFamily: FONTS.bold,
    color: colors.surface,
  },
  unreadDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.primary,
    position: 'absolute',
    top: SPACING.md,
    right: SPACING.md,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING.xxl,
  },
  emptyTitle: {
    fontSize: 20,
    fontFamily: FONTS.bold,
    color: colors.text,
    marginTop: SPACING.md,
    marginBottom: SPACING.sm,
  },
  emptyDescription: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: SPACING.lg,
    paddingHorizontal: SPACING.xl,
  },
});
