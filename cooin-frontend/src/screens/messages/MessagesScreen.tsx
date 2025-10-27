import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  RefreshControl,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';

import { messagingService } from '../../services/messagingService';
import { COLORS, SPACING, FONTS } from '../../constants/config';
import { useLanguage } from '../../contexts/LanguageContext';

interface MessagesScreenProps {
  navigation: any;
}

interface Conversation {
  connection_id: number;
  other_user_name: string;
  last_message: string;
  last_message_time: string;
  unread_count: number;
  connection_status: string;
}

export const MessagesScreen: React.FC<MessagesScreenProps> = ({ navigation }) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const { t } = useLanguage();

  useFocusEffect(
    useCallback(() => {
      loadConversations();
    }, [])
  );

  const loadConversations = async () => {
    setIsLoading(true);
    try {
      const response = await messagingService.getConversations({
        page: 1,
        page_size: 50,
      });
      setConversations(response.data || []);
    } catch (error: any) {
      console.error('Failed to load conversations:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await loadConversations();
    setIsRefreshing(false);
  };

  const handleConversationPress = (conversation: Conversation) => {
    navigation.navigate('Chat', {
      connectionId: conversation.connection_id,
      otherUserName: conversation.other_user_name,
    });
  };

  const formatMessageTime = (timeString: string) => {
    const messageTime = new Date(timeString);
    const now = new Date();
    const diffInHours = (now.getTime() - messageTime.getTime()) / (1000 * 60 * 60);

    if (diffInHours < 1) {
      const diffInMinutes = Math.floor(diffInHours * 60);
      return diffInMinutes < 1 ? t('messages.just_now') : t('messages.minutes_ago', { count: diffInMinutes });
    } else if (diffInHours < 24) {
      return t('messages.hours_ago', { count: Math.floor(diffInHours) });
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return diffInDays === 1 ? t('messages.yesterday') : t('messages.days_ago', { count: diffInDays });
    }
  };

  const renderConversation = ({ item }: { item: Conversation }) => (
    <TouchableOpacity
      style={styles.conversationItem}
      onPress={() => handleConversationPress(item)}
    >
      <View style={styles.avatar}>
        <Ionicons name="person" size={24} color={COLORS.textSecondary} />
      </View>

      <View style={styles.conversationContent}>
        <View style={styles.conversationHeader}>
          <Text style={styles.userName}>{item.other_user_name}</Text>
          <Text style={styles.timestamp}>
            {formatMessageTime(item.last_message_time)}
          </Text>
        </View>

        <View style={styles.messagePreview}>
          <Text
            style={[
              styles.lastMessage,
              item.unread_count > 0 && styles.unreadMessage,
            ]}
            numberOfLines={1}
          >
            {item.last_message}
          </Text>
          {item.unread_count > 0 && (
            <View style={styles.unreadBadge}>
              <Text style={styles.unreadCount}>
                {item.unread_count > 9 ? '9+' : item.unread_count}
              </Text>
            </View>
          )}
        </View>

        {item.connection_status !== 'accepted' && (
          <View style={styles.statusBadge}>
            <Text style={styles.statusText}>
              {item.connection_status === 'pending' ? t('messages.pending_status') : t('messages.inactive_status')}
            </Text>
          </View>
        )}
      </View>

      <Ionicons name="chevron-forward" size={20} color={COLORS.textSecondary} />
    </TouchableOpacity>
  );

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Ionicons name="chatbubbles" size={64} color={COLORS.textSecondary} />
      <Text style={styles.emptyTitle}>{t('messages.no_messages')}</Text>
      <Text style={styles.emptyDescription}>
        {t('messages.start_connecting')}
      </Text>
      <TouchableOpacity
        style={styles.discoverButton}
        onPress={() => navigation.navigate('Matching')}
      >
        <Text style={styles.discoverButtonText}>{t('messages.discover_matches')}</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{t('messages.title')}</Text>
      </View>

      <FlatList
        data={conversations}
        renderItem={renderConversation}
        keyExtractor={(item) => item.connection_id.toString()}
        ListEmptyComponent={!isLoading ? renderEmptyState : null}
        contentContainerStyle={[
          styles.content,
          conversations.length === 0 && styles.centerContent,
        ]}
        refreshControl={
          <RefreshControl refreshing={isRefreshing} onRefresh={handleRefresh} />
        }
        showsVerticalScrollIndicator={false}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
    backgroundColor: COLORS.surface,
  },
  title: {
    fontSize: 28,
    fontFamily: FONTS.bold,
    color: COLORS.text,
  },
  content: {
    padding: SPACING.lg,
    flexGrow: 1,
  },
  centerContent: {
    justifyContent: 'center',
  },
  conversationItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: COLORS.background,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  conversationContent: {
    flex: 1,
  },
  conversationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  userName: {
    fontSize: 16,
    fontFamily: FONTS.bold,
    color: COLORS.text,
  },
  timestamp: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
  },
  messagePreview: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  lastMessage: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    flex: 1,
    marginRight: SPACING.sm,
  },
  unreadMessage: {
    fontFamily: FONTS.medium,
    color: COLORS.text,
  },
  unreadBadge: {
    backgroundColor: COLORS.primary,
    borderRadius: 10,
    minWidth: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: SPACING.xs,
  },
  unreadCount: {
    fontSize: 12,
    fontFamily: FONTS.bold,
    color: COLORS.surface,
  },
  statusBadge: {
    alignSelf: 'flex-start',
    backgroundColor: COLORS.accent,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 2,
    borderRadius: 8,
    marginTop: SPACING.xs,
  },
  statusText: {
    fontSize: 10,
    fontFamily: FONTS.medium,
    color: COLORS.surface,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING.xxl,
  },
  emptyTitle: {
    fontSize: 20,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginTop: SPACING.md,
    marginBottom: SPACING.sm,
  },
  emptyDescription: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: SPACING.lg,
  },
  discoverButton: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    borderRadius: 8,
  },
  discoverButtonText: {
    fontSize: 16,
    fontFamily: FONTS.medium,
    color: COLORS.surface,
  },
});