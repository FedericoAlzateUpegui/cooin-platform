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
      console.error('Failed to load connections data:', error);
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
    } catch (error: any) {
      Alert.alert('Error', error.detail || 'Failed to load connections');
    }
  };

  const loadPendingConnections = async () => {
    try {
      const response = await matchingService.getPendingConnections({
        page: 1,
        page_size: 20,
      });
      setPendingConnections(response.data || []);
    } catch (error: any) {
      console.error('Failed to load pending connections:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await matchingService.getConnectionStats();
      setStats(response);
    } catch (error: any) {
      console.error('Failed to load stats:', error);
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
        response_message: 'Connection accepted! Looking forward to connecting with you.',
      });

      Alert.alert(
        'Connection Accepted',
        'You have successfully accepted this connection request. You can now message each other.',
        [{ text: 'OK' }]
      );

      await loadData();
    } catch (error: any) {
      Alert.alert('Error', error.detail || 'Failed to accept connection');
    } finally {
      setActionLoading(null);
    }
  };

  const handleRejectConnection = async (connection: Connection) => {
    Alert.alert(
      'Reject Connection',
      'Are you sure you want to reject this connection request?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reject',
          style: 'destructive',
          onPress: async () => {
            setActionLoading(connection.id);
            try {
              await matchingService.updateConnection(connection.id, {
                status: 'rejected',
                response_message: 'Thank you for your interest, but I am not able to connect at this time.',
              });

              await loadData();
            } catch (error: any) {
              Alert.alert('Error', error.detail || 'Failed to reject connection');
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
        <Text style={styles.statsTitle}>Connection Stats</Text>
        <View style={styles.statsGrid}>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>{stats.total_connections}</Text>
            <Text style={styles.statLabel}>Total</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={[styles.statNumber, { color: COLORS.accent }]}>
              {stats.pending_received}
            </Text>
            <Text style={styles.statLabel}>Pending</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={[styles.statNumber, { color: COLORS.success }]}>
              {stats.accepted_connections}
            </Text>
            <Text style={styles.statLabel}>Accepted</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={[styles.statNumber, { color: COLORS.primary }]}>
              {stats.recent_activity}
            </Text>
            <Text style={styles.statLabel}>Recent</Text>
          </View>
        </View>
      </View>
    );
  };

  const renderTabs = () => {
    const tabs: { key: TabType; label: string; count?: number }[] = [
      { key: 'all', label: 'All', count: connections.length },
      { key: 'pending', label: 'Pending', count: pendingConnections.filter(c => c.receiver_id === user?.id).length },
      { key: 'accepted', label: 'Accepted', count: connections.filter(c => c.status === 'accepted').length },
      { key: 'sent', label: 'Sent', count: connections.filter(c => c.status === 'pending' && c.requester_id === user?.id).length },
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
      <Ionicons name="link" size={64} color={COLORS.textSecondary} />
      <Text style={styles.emptyTitle}>
        {activeTab === 'pending' && 'No Pending Requests'}
        {activeTab === 'accepted' && 'No Accepted Connections'}
        {activeTab === 'sent' && 'No Sent Requests'}
        {activeTab === 'all' && 'No Connections Yet'}
      </Text>
      <Text style={styles.emptyDescription}>
        {activeTab === 'all' && 'Start by discovering matches and sending connection requests.'}
        {activeTab === 'pending' && 'You don\'t have any pending connection requests at the moment.'}
        {activeTab === 'accepted' && 'Accept some connection requests to start building your network.'}
        {activeTab === 'sent' && 'Go to the Discover tab to find and connect with potential matches.'}
      </Text>
      {activeTab === 'all' && (
        <Button
          title="Discover Matches"
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
      <Text style={styles.title}>Connections</Text>
      {renderStatsCard()}
      {renderTabs()}
    </View>
  );

  const filteredConnections = getFilteredConnections();

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

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
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
    color: COLORS.text,
    marginBottom: SPACING.lg,
  },
  statsCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  statsTitle: {
    fontSize: 18,
    fontFamily: FONTS.bold,
    color: COLORS.text,
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
    color: COLORS.text,
    marginBottom: SPACING.xs,
  },
  statLabel: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
  },
  tabsContainer: {
    flexDirection: 'row',
    backgroundColor: COLORS.surface,
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
    backgroundColor: COLORS.primary,
  },
  tabText: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    color: COLORS.textSecondary,
  },
  activeTabText: {
    color: COLORS.surface,
  },
  tabBadge: {
    backgroundColor: COLORS.border,
    borderRadius: 10,
    minWidth: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: SPACING.xs,
  },
  activeTabBadge: {
    backgroundColor: COLORS.surface,
  },
  tabBadgeText: {
    fontSize: 12,
    fontFamily: FONTS.bold,
    color: COLORS.textSecondary,
  },
  activeTabBadgeText: {
    color: COLORS.primary,
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
    minWidth: 160,
  },
});