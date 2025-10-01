import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Connection } from '../types/api';
import { Button } from './Button';
import { COLORS, SPACING, FONTS } from '../constants/config';

interface ConnectionCardProps {
  connection: Connection;
  currentUserId: number;
  onAccept?: () => void;
  onReject?: () => void;
  onMessage?: () => void;
  onViewProfile?: () => void;
  loading?: boolean;
}

export const ConnectionCard: React.FC<ConnectionCardProps> = ({
  connection,
  currentUserId,
  onAccept,
  onReject,
  onMessage,
  onViewProfile,
  loading = false,
}) => {
  const isRequester = connection.requester_id === currentUserId;
  const isReceiver = connection.receiver_id === currentUserId;
  const isPending = connection.status === 'pending';
  const isAccepted = connection.status === 'accepted';
  const isRejected = connection.status === 'rejected';

  const getStatusColor = () => {
    switch (connection.status) {
      case 'accepted':
        return COLORS.success;
      case 'rejected':
        return COLORS.error;
      case 'pending':
        return COLORS.accent;
      case 'blocked':
        return COLORS.error;
      default:
        return COLORS.textSecondary;
    }
  };

  const getStatusText = () => {
    if (isPending) {
      return isRequester ? 'Pending Response' : 'Awaiting Your Response';
    }
    return connection.status.charAt(0).toUpperCase() + connection.status.slice(1);
  };

  const renderConnectionType = () => {
    const typeMap = {
      lending_inquiry: { icon: 'cash', text: 'Lending Inquiry', color: COLORS.success },
      borrowing_request: { icon: 'card', text: 'Borrowing Request', color: COLORS.primary },
      general_connection: { icon: 'people', text: 'General Connection', color: COLORS.textSecondary },
      referral: { icon: 'share', text: 'Referral', color: COLORS.accent },
    };

    const type = typeMap[connection.connection_type] || typeMap.general_connection;

    return (
      <View style={[styles.typeChip, { backgroundColor: `${type.color}20` }]}>
        <Ionicons name={type.icon as any} size={14} color={type.color} />
        <Text style={[styles.typeText, { color: type.color }]}>{type.text}</Text>
      </View>
    );
  };

  const renderFinancialDetails = () => {
    if (!connection.loan_amount_requested && !connection.interest_rate_proposed) {
      return null;
    }

    return (
      <View style={styles.financialSection}>
        {connection.loan_amount_requested && (
          <View style={styles.detailRow}>
            <Ionicons name="cash" size={16} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>
              Amount: ${connection.loan_amount_requested.toLocaleString()}
            </Text>
          </View>
        )}

        {connection.loan_term_months && (
          <View style={styles.detailRow}>
            <Ionicons name="calendar" size={16} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>
              Term: {connection.loan_term_months} months
            </Text>
          </View>
        )}

        {connection.interest_rate_proposed && (
          <View style={styles.detailRow}>
            <Ionicons name="trending-up" size={16} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>
              Rate: {connection.interest_rate_proposed}%
            </Text>
          </View>
        )}

        {connection.loan_purpose && (
          <View style={styles.detailRow}>
            <Ionicons name="document-text" size={16} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>
              Purpose: {connection.loan_purpose}
            </Text>
          </View>
        )}
      </View>
    );
  };

  const renderMessage = () => {
    const message = connection.message || connection.response_message;
    if (!message) return null;

    return (
      <View style={styles.messageSection}>
        <Text style={styles.messageLabel}>
          {connection.message ? 'Initial Message:' : 'Response:'}
        </Text>
        <Text style={styles.messageText}>{message}</Text>
      </View>
    );
  };

  const renderActions = () => {
    if (isPending && isReceiver) {
      // Show accept/reject buttons for pending requests received
      return (
        <View style={styles.actions}>
          <Button
            title="Reject"
            onPress={onReject}
            variant="outline"
            style={styles.actionButton}
            loading={loading}
          />
          <Button
            title="Accept"
            onPress={onAccept}
            style={styles.actionButton}
            loading={loading}
          />
        </View>
      );
    }

    if (isAccepted) {
      // Show message button for accepted connections
      return (
        <View style={styles.actions}>
          <Button
            title="View Profile"
            onPress={onViewProfile}
            variant="outline"
            style={styles.actionButton}
          />
          <Button
            title="Message"
            onPress={onMessage}
            style={styles.actionButton}
          />
        </View>
      );
    }

    if (isPending && isRequester) {
      // Show view profile button for sent requests
      return (
        <View style={styles.actions}>
          <Button
            title="View Profile"
            onPress={onViewProfile}
            variant="outline"
            style={styles.singleActionButton}
          />
        </View>
      );
    }

    return null;
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.profileSection}>
          <View style={styles.avatar}>
            <Ionicons name="person" size={32} color={COLORS.textSecondary} />
          </View>
          <View style={styles.profileInfo}>
            <Text style={styles.name}>
              {isRequester ? 'Connection Request Sent' : 'Connection Request'}
            </Text>
            <Text style={styles.metadata}>
              {connection.days_since_created === 0
                ? 'Today'
                : `${connection.days_since_created} days ago`}
            </Text>
          </View>
        </View>

        <View style={styles.statusSection}>
          <View style={[styles.statusBadge, { backgroundColor: `${getStatusColor()}20` }]}>
            <Text style={[styles.statusText, { color: getStatusColor() }]}>
              {getStatusText()}
            </Text>
          </View>
          {renderConnectionType()}
        </View>
      </View>

      {renderFinancialDetails()}
      {renderMessage()}

      <View style={styles.metaInfo}>
        {connection.is_mutual && (
          <View style={styles.mutualBadge}>
            <Ionicons name="sync" size={14} color={COLORS.success} />
            <Text style={styles.mutualText}>Mutual Connection</Text>
          </View>
        )}

        {connection.message_count > 0 && (
          <View style={styles.messageCount}>
            <Ionicons name="chatbubbles" size={14} color={COLORS.primary} />
            <Text style={styles.messageCountText}>
              {connection.message_count} message{connection.message_count !== 1 ? 's' : ''}
            </Text>
          </View>
        )}

        {connection.priority_level > 1 && (
          <View style={[
            styles.priorityBadge,
            { backgroundColor: connection.priority_level === 3 ? COLORS.error : COLORS.accent }
          ]}>
            <Ionicons name="flag" size={12} color={COLORS.surface} />
            <Text style={styles.priorityText}>
              {connection.priority_level === 3 ? 'Urgent' : 'High Priority'}
            </Text>
          </View>
        )}
      </View>

      {renderActions()}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: SPACING.md,
  },
  profileSection: {
    flexDirection: 'row',
    flex: 1,
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
  profileInfo: {
    flex: 1,
  },
  name: {
    fontSize: 16,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginBottom: SPACING.xs,
  },
  metadata: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
  },
  statusSection: {
    alignItems: 'flex-end',
  },
  statusBadge: {
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: 8,
    marginBottom: SPACING.xs,
  },
  statusText: {
    fontSize: 12,
    fontFamily: FONTS.medium,
  },
  typeChip: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: 6,
  },
  typeText: {
    fontSize: 12,
    fontFamily: FONTS.medium,
    marginLeft: 4,
  },
  financialSection: {
    marginBottom: SPACING.md,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  detailText: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.text,
    marginLeft: SPACING.sm,
  },
  messageSection: {
    marginBottom: SPACING.md,
  },
  messageLabel: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    color: COLORS.text,
    marginBottom: SPACING.xs,
  },
  messageText: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    lineHeight: 20,
    fontStyle: 'italic',
  },
  metaInfo: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.sm,
    marginBottom: SPACING.md,
  },
  mutualBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: `${COLORS.success}20`,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 4,
    borderRadius: 6,
  },
  mutualText: {
    fontSize: 12,
    fontFamily: FONTS.medium,
    color: COLORS.success,
    marginLeft: 4,
  },
  messageCount: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: `${COLORS.primary}20`,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 4,
    borderRadius: 6,
  },
  messageCountText: {
    fontSize: 12,
    fontFamily: FONTS.medium,
    color: COLORS.primary,
    marginLeft: 4,
  },
  priorityBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.sm,
    paddingVertical: 4,
    borderRadius: 6,
  },
  priorityText: {
    fontSize: 12,
    fontFamily: FONTS.medium,
    color: COLORS.surface,
    marginLeft: 4,
  },
  actions: {
    flexDirection: 'row',
    gap: SPACING.md,
  },
  actionButton: {
    flex: 1,
  },
  singleActionButton: {
    alignSelf: 'flex-start',
    minWidth: 120,
  },
});