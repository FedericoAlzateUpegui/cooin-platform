import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
  TextInput,
  Modal,
  ScrollView,
  Alert,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useAuthStore } from '../../store/authStore';
import { COLORS } from '../../constants/config';
import { ticketService } from '../../services/ticketService';
import { Ticket } from '../../types/api';
import { CreateTicketModal } from './CreateTicketModal';

export const TicketsScreen: React.FC = () => {
  const { token, user } = useAuthStore();
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedTab, setSelectedTab] = useState<'lending_offer' | 'borrowing_request' | 'MY_TICKETS'>('lending_offer');
  const [filterModalVisible, setFilterModalVisible] = useState(false);
  const [createModalVisible, setCreateModalVisible] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);
  const [detailsModalVisible, setDetailsModalVisible] = useState(false);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  // Filter state
  const [filters, setFilters] = useState({
    minAmount: '',
    maxAmount: '',
    minInterestRate: '',
    maxInterestRate: '',
    loanType: '',
  });

  useEffect(() => {
    loadTickets();
  }, [selectedTab, token, page]);

  const loadTickets = async () => {
    try {
      setLoading(true);

      if (selectedTab === 'MY_TICKETS') {
        const response = await ticketService.getMyTickets();
        setTickets(response.tickets || []);
        setTotalCount(response.total || 0);
      } else {
        const response = await ticketService.getTickets({
          ticket_type: selectedTab,
          status: 'active',
          page: page,
          page_size: 20,
          sort_by: 'created_at',
          sort_order: 'desc'
        });
        setTickets(response.data || []);
        setTotalCount(response.total_count || 0);
      }
    } catch (error: any) {
      console.error('Error loading tickets:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to load tickets';
      if (Platform.OS === 'web') {
        window.alert(`Error: ${errorMessage}`);
      } else {
        Alert.alert('Error', errorMessage);
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    loadTickets();
  };

  const handleCreateDeal = async (ticketId: number) => {
    if (Platform.OS === 'web') {
      const message = window.prompt('Enter your message to the ticket creator (minimum 20 characters):');
      if (!message || message.trim().length < 20) {
        window.alert('Error: Message must be at least 20 characters');
        return;
      }

      try {
        await ticketService.createDealFromTicket({
          ticket_id: ticketId,
          message: message.trim(),
        });

        window.alert('Success! Deal created successfully! Check your connections.');
        setDetailsModalVisible(false);
        loadTickets();
      } catch (error: any) {
        console.error('Error creating deal:', error);
        const errorMessage = error.response?.data?.detail || error.response?.data?.error?.message || error.message || 'Failed to create deal';
        window.alert(`Error: ${errorMessage}`);
      }
    } else {
      Alert.prompt(
        'Create Deal',
        'Enter your message to the ticket creator:',
        async (message) => {
          if (!message || message.trim().length < 20) {
            Alert.alert('Error', 'Message must be at least 20 characters');
            return;
          }

          try {
            await ticketService.createDealFromTicket({
              ticket_id: ticketId,
              message: message.trim(),
            });

            Alert.alert('Success', 'Deal created successfully! Check your connections.');
            setDetailsModalVisible(false);
            loadTickets();
          } catch (error: any) {
            console.error('Error creating deal:', error);
            const errorMessage = error.response?.data?.detail || error.message || 'Failed to create deal';
            Alert.alert('Error', errorMessage);
          }
        },
        'plain-text'
      );
    }
  };

  const renderTicketCard = ({ item }: { item: Ticket }) => {
    const isLendingOffer = item.ticket_type === 'lending_offer';

    return (
      <TouchableOpacity
        style={styles.ticketCard}
        onPress={() => {
          setSelectedTicket(item);
          setDetailsModalVisible(true);
        }}
      >
        <View style={styles.ticketHeader}>
          <View style={[styles.ticketTypeBadge, { backgroundColor: isLendingOffer ? COLORS.success + '20' : COLORS.primary + '20' }]}>
            <Ionicons
              name={isLendingOffer ? 'cash-outline' : 'wallet-outline'}
              size={16}
              color={isLendingOffer ? COLORS.success : COLORS.primary}
            />
            <Text style={[styles.ticketTypeText, { color: isLendingOffer ? COLORS.success : COLORS.primary }]}>
              {isLendingOffer ? 'Lending Offer' : 'Borrowing Request'}
            </Text>
          </View>
          {item.flexible_terms && (
            <View style={styles.flexibleBadge}>
              <Text style={styles.flexibleText}>Flexible</Text>
            </View>
          )}
        </View>

        <Text style={styles.ticketTitle}>{item.title}</Text>
        <Text style={styles.ticketDescription} numberOfLines={2}>{item.description}</Text>

        <View style={styles.ticketDetails}>
          <View style={styles.detailRow}>
            <Ionicons name="cash-outline" size={16} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>${item.amount.toLocaleString()}</Text>
          </View>
          <View style={styles.detailRow}>
            <Ionicons name="trending-up-outline" size={16} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>{item.interest_rate}% APR</Text>
          </View>
          <View style={styles.detailRow}>
            <Ionicons name="time-outline" size={16} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>{item.term_months} months</Text>
          </View>
        </View>

        <View style={styles.ticketFooter}>
          <View style={styles.statsRow}>
            <Ionicons name="eye-outline" size={14} color={COLORS.textSecondary} />
            <Text style={styles.statText}>{item.views_count || 0} views</Text>
            <Ionicons name="chatbubble-outline" size={14} color={COLORS.textSecondary} style={{ marginLeft: 12 }} />
            <Text style={styles.statText}>{item.responses_count || 0} responses</Text>
          </View>
          <Text style={styles.loanTypeText}>{item.loan_type}</Text>
        </View>
      </TouchableOpacity>
    );
  };

  const renderDetailsModal = () => {
    if (!selectedTicket) return null;
    const isLendingOffer = selectedTicket.ticket_type === 'lending_offer';

    return (
      <Modal
        visible={detailsModalVisible}
        animationType="slide"
        transparent={true}
        onRequestClose={() => setDetailsModalVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Ticket Details</Text>
              <TouchableOpacity onPress={() => setDetailsModalVisible(false)}>
                <Ionicons name="close" size={24} color={COLORS.text} />
              </TouchableOpacity>
            </View>

            <ScrollView style={styles.modalBody}>
              <View style={[styles.ticketTypeBadge, { backgroundColor: isLendingOffer ? COLORS.success + '20' : COLORS.primary + '20' }]}>
                <Ionicons
                  name={isLendingOffer ? 'cash-outline' : 'wallet-outline'}
                  size={20}
                  color={isLendingOffer ? COLORS.success : COLORS.primary}
                />
                <Text style={[styles.ticketTypeText, { color: isLendingOffer ? COLORS.success : COLORS.primary }]}>
                  {isLendingOffer ? 'Lending Offer' : 'Borrowing Request'}
                </Text>
              </View>

              <Text style={styles.detailsTitle}>{selectedTicket.title}</Text>
              <Text style={styles.detailsDescription}>{selectedTicket.description}</Text>

              <View style={styles.detailsSection}>
                <Text style={styles.sectionTitle}>Financial Details</Text>
                <View style={styles.detailsGrid}>
                  <View style={styles.detailItem}>
                    <Text style={styles.detailLabel}>Amount</Text>
                    <Text style={styles.detailValue}>${selectedTicket.amount.toLocaleString()}</Text>
                  </View>
                  <View style={styles.detailItem}>
                    <Text style={styles.detailLabel}>Interest Rate</Text>
                    <Text style={styles.detailValue}>{selectedTicket.interest_rate}%</Text>
                  </View>
                  <View style={styles.detailItem}>
                    <Text style={styles.detailLabel}>Term</Text>
                    <Text style={styles.detailValue}>{selectedTicket.term_months} months</Text>
                  </View>
                  <View style={styles.detailItem}>
                    <Text style={styles.detailLabel}>Loan Type</Text>
                    <Text style={styles.detailValue}>{selectedTicket.loan_type}</Text>
                  </View>
                  <View style={styles.detailItem}>
                    <Text style={styles.detailLabel}>Warranty</Text>
                    <Text style={styles.detailValue}>{selectedTicket.warranty_type}</Text>
                  </View>
                  <View style={styles.detailItem}>
                    <Text style={styles.detailLabel}>Flexible Terms</Text>
                    <Text style={styles.detailValue}>{selectedTicket.flexible_terms ? 'Yes' : 'No'}</Text>
                  </View>
                </View>
              </View>

              <TouchableOpacity
                style={styles.createDealButton}
                onPress={() => handleCreateDeal(selectedTicket.id)}
              >
                <Ionicons name="handshake-outline" size={20} color="#fff" />
                <Text style={styles.createDealButtonText}>Create Deal</Text>
              </TouchableOpacity>
            </ScrollView>
          </View>
        </View>
      </Modal>
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Tickets Marketplace</Text>
        <View style={styles.headerActions}>
          <TouchableOpacity
            style={styles.iconButton}
            onPress={() => setFilterModalVisible(true)}
          >
            <Ionicons name="filter-outline" size={24} color={COLORS.text} />
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.createButton}
            onPress={() => setCreateModalVisible(true)}
          >
            <Ionicons name="add" size={24} color="#fff" />
            <Text style={styles.createButtonText}>Create Ticket</Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.tabContainer}>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'lending_offer' && styles.activeTab]}
          onPress={() => setSelectedTab('lending_offer')}
        >
          <Text style={[styles.tabText, selectedTab === 'lending_offer' && styles.activeTabText]}>
            Lending Offers
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'borrowing_request' && styles.activeTab]}
          onPress={() => setSelectedTab('borrowing_request')}
        >
          <Text style={[styles.tabText, selectedTab === 'borrowing_request' && styles.activeTabText]}>
            Borrowing Requests
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tab, selectedTab === 'MY_TICKETS' && styles.activeTab]}
          onPress={() => setSelectedTab('MY_TICKETS')}
        >
          <Text style={[styles.tabText, selectedTab === 'MY_TICKETS' && styles.activeTabText]}>
            My Tickets
          </Text>
        </TouchableOpacity>
      </View>

      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={COLORS.primary} />
        </View>
      ) : (
        <FlatList
          data={tickets}
          renderItem={renderTicketCard}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={styles.listContainer}
          refreshing={refreshing}
          onRefresh={handleRefresh}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Ionicons name="document-text-outline" size={64} color={COLORS.textSecondary} />
              <Text style={styles.emptyText}>No tickets available</Text>
              <Text style={styles.emptySubtext}>
                {selectedTab === 'MY_TICKETS'
                  ? 'Create your first ticket to get started'
                  : 'Check back later for new opportunities'}
              </Text>
            </View>
          }
        />
      )}

      {renderDetailsModal()}

      <CreateTicketModal
        visible={createModalVisible}
        onClose={() => setCreateModalVisible(false)}
        onSuccess={loadTickets}
        userRole={user?.role?.toUpperCase() as 'LENDER' | 'BORROWER' | 'BOTH' || 'BOTH'}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  headerActions: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  iconButton: {
    padding: 8,
  },
  createButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.primary,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
    gap: 6,
  },
  createButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
  },
  tabContainer: {
    flexDirection: 'row',
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  tab: {
    flex: 1,
    paddingVertical: 14,
    alignItems: 'center',
    borderBottomWidth: 2,
    borderBottomColor: 'transparent',
  },
  activeTab: {
    borderBottomColor: COLORS.primary,
  },
  tabText: {
    fontSize: 14,
    fontWeight: '500',
    color: COLORS.textSecondary,
  },
  activeTabText: {
    color: COLORS.primary,
    fontWeight: '600',
  },
  listContainer: {
    padding: 16,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  ticketCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  ticketHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  ticketTypeBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 6,
    gap: 6,
  },
  ticketTypeText: {
    fontSize: 12,
    fontWeight: '600',
  },
  flexibleBadge: {
    backgroundColor: COLORS.warning + '20',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  flexibleText: {
    fontSize: 11,
    fontWeight: '600',
    color: COLORS.warning,
  },
  ticketTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  ticketDescription: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 12,
    lineHeight: 20,
  },
  ticketDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
    paddingVertical: 12,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: COLORS.border,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  detailText: {
    fontSize: 14,
    fontWeight: '500',
    color: COLORS.text,
  },
  ticketFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  statText: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  loanTypeText: {
    fontSize: 12,
    fontWeight: '500',
    color: COLORS.primary,
    textTransform: 'capitalize',
  },
  emptyContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginTop: 16,
  },
  emptySubtext: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: 8,
    textAlign: 'center',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: COLORS.surface,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    maxHeight: '90%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  modalBody: {
    padding: 20,
  },
  detailsTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: COLORS.text,
    marginTop: 16,
    marginBottom: 12,
  },
  detailsDescription: {
    fontSize: 15,
    color: COLORS.textSecondary,
    lineHeight: 22,
    marginBottom: 24,
  },
  detailsSection: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  detailsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  detailItem: {
    flex: 1,
    minWidth: '45%',
    backgroundColor: COLORS.background,
    padding: 12,
    borderRadius: 8,
  },
  detailLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  detailValue: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  createDealButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.primary,
    paddingVertical: 14,
    borderRadius: 8,
    gap: 8,
    marginTop: 12,
  },
  createDealButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
