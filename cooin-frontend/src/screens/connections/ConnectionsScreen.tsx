import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  RefreshControl,
  Alert,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

import { ConnectionCard } from '../../components/ConnectionCard';
import { Button } from '../../components/Button';
import { matchingService } from '../../services/matchingService';
import { useAuthStore } from '../../store/authStore';
import { Connection } from '../../types/api';
import { COLORS, SPACING, FONTS } from '../../constants/config';
import { useLanguage } from '../../contexts/LanguageContext';
import { useColors } from '../../hooks/useColors';

import { logger } from '../../utils/logger';
interface ConnectionsScreenProps {
  navigation: any;
}

type TabType = 'all' | 'pending' | 'accepted' | 'sent';

export const ConnectionsScreen: React.FC<ConnectionsScreenProps> = ({ navigation }) => {
  const [connections, setConnections] = useState<Connection[]>([]);
  const [pendingConnections, setPendingConnections] = useState<Connection[]>([]);
  const [activeTab, setActiveTab] = useState<TabType>('all');
  const [isLoading, setIsLoading] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [actionLoading, setActionLoading] = useState<number | null>(null);
  const [stats, setStats] = useState<{
    total_connections: number;
    pending_sent: number;
    pending_received: number;
    accepted_connections: number;
    recent_activity: number;
  } | null>(null);

  const { user } = useAuthStore();
  const { t } = useLanguage();
  const colors = useColors();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setIsLoading(true);
    try {
      await Promise.all([
        loadConnections(),
        loadPendingConnections(),
        loadStats(),
      ]);
    } catch (error) {
      logger.error('Failed to load connections data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadConnections = async () => {
    try {
      const response = await matchingService.getMyConnections({
        page: 1,
        page_size: 50,
      });
      setConnections(response.data || []);
    } catch (error: unknown) {
      Alert.alert(t('common.error'), error.detail || t('connections.error_loading'));
    }
  };

  const loadPendingConnections = async () => {
    try {
      const response = await matchingService.getPendingConnections({
        page: 1,
        page_size: 20,
      });
      setPendingConnections(response.data || []);
    } catch (error: unknown) {
      logger.error('Failed to load pending connections:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await matchingService.getConnectionStats();
      setStats(response);
    } catch (error: unknown) {
      logger.error('Failed to load stats:', error);
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await loadData();
    setIsRefreshing(false);
  };

  const handleAcceptConnection = async (connection: Connection) => {
    setActionLoading(connection.id);
    try {
      await matchingService.updateConnection(connection.id, {
        status: 'accepted',
        response_message: t('connections.accept_response_message'),
      });

      Alert.alert(
        t('connections.connection_accepted_title'),
        t('connections.connection_accepted_message'),
        [{ text: t('common.ok') }]
      );

      await loadData();
    } catch (error: unknown) {
      Alert.alert(t('common.error'), error.detail || t('connections.error_accept'));
    } finally {
      setActionLoading(null);
    }
  };

  const handleRejectConnection = async (connection: Connection) => {
    Alert.alert(
      t('connections.reject_connection_title'),
      t('connections.reject_connection_message'),
      [
        { text: t('common.cancel'), style: 'cancel' },
        {
          text: t('connections.reject_button'),
          style: 'destructive',
          onPress: async () => {
            setActionLoading(connection.id);
            try {
              await matchingService.updateConnection(connection.id, {
                status: 'rejected',
                response_message: t('connections.reject_response_message'),
              });

              await loadData();
            } catch (error: unknown) {
              Alert.alert(t('common.error'), error.detail || t('connections.error_reject'));
            } finally {
              setActionLoading(null);
            }
          },
        },
      ]
    );
  };

  const handleMessageConnection = (connection: Connection) => {
    navigation.navigate('Messages', {
      screen: 'Chat',
      params: { connectionId: connection.id },
    });
  };

  const handleViewProfile = (connection: Connection) => {
    const otherUserId = connection.requester_id === user?.id
      ? connection.receiver_id
      : connection.requester_id;

    navigation.navigate('PublicProfile', { userId: otherUserId });
  };

  const getFilteredConnections = () => {
    switch (activeTab) {
      case 'pending':
        return pendingConnections.filter(c => c.receiver_id === user?.id);
      case 'sent':
        return connections.filter(c => c.status === 'pending' && c.requester_id === user?.id);
      case 'accepted':
        return connections.filter(c => c.status === 'accepted');
      case 'all':
      default:
        return connections;
    }
  };

  const renderStatsCard = () => {
    if (!stats) return null;

    return (
      <View style={styles.statsCard}>
        <Text style={styles.statsTitle}>{t('connections.stats_title')}</Text>
        <View style={styles.statsGrid}>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>{stats.total_connections}</Text>
            <Text style={styles.statLabel}>{t('connections.total')}</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={[styles.statNumber, { color: colors.accent }]}>
              {stats.pending_received}
            </Text>
            <Text style={styles.statLabel}>{t('connections.pending')}</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={[styles.statNumber, { color: colors.success }]}>
              {stats.accepted_connections}
            </Text>
            <Text style={styles.statLabel}>{t('connections.accepted')}</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={[styles.statNumber, { color: colors.primary }]}>
              {stats.recent_activity}
            </Text>
            <Text style={styles.statLabel}>{t('connections.recent')}</Text>
          </View>
        </View>
      </View>
    );
  };

  const renderTabs = () => {
    const tabs: { key: TabType; label: string; count?: number }[] = [
      { key: 'all', label: t('connections.all'), count: connections.length },
      { key: 'pending', label: t('connections.pending'), count: pendingConnections.filter(c => c.receiver_id === user?.id).length },
      { key: 'accepted', label: t('connections.accepted'), count: connections.filter(c => c.status === 'accepted').length },
      { key: 'sent', label: t('connections.sent'), count: connections.filter(c => c.status === 'pending' && c.requester_id === user?.id).length },
    ];

    return (
      <View style={styles.tabsContainer}>
        {tabs.map((tab) => (
          <TouchableOpacity
            key={tab.key}
            style={[
              styles.tab,
              activeTab === tab.key && styles.activeTab,
            ]}
            onPress={() => setActiveTab(tab.key)}
          >
            <Text style={[
              styles.tabText,
              activeTab === tab.key && styles.activeTabText,
            ]}>
              {tab.label}
            </Text>
            {tab.count !== undefined && tab.count > 0 && (
              <View style={[
                styles.tabBadge,
                activeTab === tab.key && styles.activeTabBadge,
              ]}>
                <Text style={[
                  styles.tabBadgeText,
                  activeTab === tab.key && styles.activeTabBadgeText,
                ]}>
                  {tab.count}
                </Text>
              </View>
            )}
          </TouchableOpacity>
        ))}
      </View>
    );
  };

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Ionicons name="link" size={64} color={colors.textSecondary} />
      <Text style={styles.emptyTitle}>
        {activeTab === 'pending' && t('connections.no_pending_requests')}
        {activeTab === 'accepted' && t('connections.no_accepted_connections')}
        {activeTab === 'sent' && t('connections.no_sent_requests')}
        {activeTab === 'all' && t('connections.no_connections_yet')}
      </Text>
      <Text style={styles.emptyDescription}>
        {activeTab === 'all' && t('connections.start_discovering')}
        {activeTab === 'pending' && t('connections.no_pending_at_moment')}
        {activeTab === 'accepted' && t('connections.accept_to_build_network')}
        {activeTab === 'sent' && t('connections.go_discover')}
      </Text>
      {activeTab === 'all' && (
        <Button
          title={t('connections.discover_matches')}
          onPress={() => navigation.navigate('Matching')}
          style={styles.discoverButton}
        />
      )}
    </View>
  );

  const renderConnection = ({ item }: { item: Connection }) => (
    <ConnectionCard
      connection={item}
      currentUserId={user?.id || 0}
      onAccept={() => handleAcceptConnection(item)}
      onReject={() => handleRejectConnection(item)}
      onMessage={() => handleMessageConnection(item)}
      onViewProfile={() => handleViewProfile(item)}
      loading={actionLoading === item.id}
    />
  );

  const renderHeader = () => (
    <View style={styles.header}>
      <Text style={styles.title}>{t('connections.title')}</Text>
      {renderStatsCard()}
      {renderTabs()}
    </View>
  );

  const filteredConnections = getFilteredConnections();
  const styles = createStyles(colors);

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={filteredConnections}
        renderItem={renderConnection}
        keyExtractor={(item) => `${item.id}-${activeTab}`}
        ListHeaderComponent={renderHeader}
        ListEmptyComponent={!isLoading ? renderEmptyState : null}
        contentContainerStyle={styles.content}
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
  content: {
    padding: SPACING.lg,
    flexGrow: 1,
  },
  header: {
    marginBottom: SPACING.lg,
  },
  title: {
    fontSize: 28,
    fontFamily: FONTS.bold,
    color: colors.text,
    marginBottom: SPACING.lg,
  },
  statsCard: {
    backgroundColor: colors.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
    borderWidth: 1,
    borderColor: colors.border,
  },
  statsTitle: {
    fontSize: 18,
    fontFamily: FONTS.bold,
    color: colors.text,
    marginBottom: SPACING.md,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statItem: {
    alignItems: 'center',
    flex: 1,
  },
  statNumber: {
    fontSize: 24,
    fontFamily: FONTS.bold,
    color: colors.text,
    marginBottom: SPACING.xs,
  },
  statLabel: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: colors.textSecondary,
  },
  tabsContainer: {
    flexDirection: 'row',
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding: SPACING.xs,
    marginBottom: SPACING.md,
  },
  tab: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    borderRadius: 8,
  },
  activeTab: {
    backgroundColor: colors.primary,
  },
  tabText: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    color: colors.textSecondary,
  },
  activeTabText: {
    color: colors.surface,
  },
  tabBadge: {
    backgroundColor: colors.border,
    borderRadius: 10,
    minWidth: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: SPACING.xs,
  },
  activeTabBadge: {
    backgroundColor: colors.surface,
  },
  tabBadgeText: {
    fontSize: 12,
    fontFamily: FONTS.bold,
    color: colors.textSecondary,
  },
  activeTabBadgeText: {
    color: colors.primary,
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
  },
  discoverButton: {
    minWidth: 160,
  },
});