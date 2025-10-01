import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { MatchingResult } from '../types/api';
import { Button } from './Button';
import { COLORS, SPACING, FONTS } from '../constants/config';

interface MatchCardProps {
  match: MatchingResult;
  onConnect: () => void;
  onViewProfile: () => void;
  loading?: boolean;
}

export const MatchCard: React.FC<MatchCardProps> = ({
  match,
  onConnect,
  onViewProfile,
  loading = false,
}) => {
  const getCompatibilityColor = (score: number) => {
    if (score >= 80) return COLORS.success;
    if (score >= 60) return COLORS.accent;
    return COLORS.textSecondary;
  };

  const renderVerificationBadge = () => {
    if (match.is_verified) {
      return (
        <View style={styles.verifiedBadge}>
          <Ionicons name="checkmark-circle" size={16} color={COLORS.success} />
          <Text style={styles.verifiedText}>Verified</Text>
        </View>
      );
    }
    return null;
  };

  const renderMatchReasons = () => {
    return match.match_reasons.slice(0, 2).map((reason, index) => (
      <View key={index} style={styles.reasonChip}>
        <Text style={styles.reasonText}>{reason}</Text>
      </View>
    ));
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.profileSection}>
          <View style={styles.avatar}>
            <Ionicons name="person" size={32} color={COLORS.textSecondary} />
          </View>
          <View style={styles.profileInfo}>
            <View style={styles.nameRow}>
              <Text style={styles.name}>{match.public_name}</Text>
              {renderVerificationBadge()}
            </View>
            <Text style={styles.location}>{match.location_string}</Text>
            <View style={styles.profileMeta}>
              <View style={styles.completionBadge}>
                <Text style={styles.completionText}>
                  {Math.round(match.profile_completion_percentage)}% complete
                </Text>
              </View>
            </View>
          </View>
        </View>

        <View style={styles.compatibilitySection}>
          <View style={[
            styles.compatibilityScore,
            { borderColor: getCompatibilityColor(match.compatibility_score) }
          ]}>
            <Text style={[
              styles.scoreText,
              { color: getCompatibilityColor(match.compatibility_score) }
            ]}>
              {Math.round(match.compatibility_score)}%
            </Text>
          </View>
          <Text style={styles.compatibilityLabel}>Match</Text>
        </View>
      </View>

      <View style={styles.detailsSection}>
        {match.loan_amount_range && (
          <View style={styles.detailRow}>
            <Ionicons name="cash" size={16} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>Amount: {match.loan_amount_range}</Text>
          </View>
        )}

        {match.interest_rate_range && (
          <View style={styles.detailRow}>
            <Ionicons name="trending-up" size={16} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>Rate: {match.interest_rate_range}</Text>
          </View>
        )}

        {match.loan_terms && (
          <View style={styles.detailRow}>
            <Ionicons name="calendar" size={16} color={COLORS.textSecondary} />
            <Text style={styles.detailText}>Terms: {match.loan_terms}</Text>
          </View>
        )}
      </View>

      <View style={styles.reasonsSection}>
        <Text style={styles.reasonsTitle}>Why this is a good match:</Text>
        <View style={styles.reasonsContainer}>
          {renderMatchReasons()}
          {match.match_reasons.length > 2 && (
            <Text style={styles.moreReasons}>
              +{match.match_reasons.length - 2} more reasons
            </Text>
          )}
        </View>
      </View>

      <View style={styles.actionsSection}>
        <Button
          title="View Profile"
          onPress={onViewProfile}
          variant="outline"
          style={styles.actionButton}
        />
        <Button
          title="Connect"
          onPress={onConnect}
          loading={loading}
          style={styles.actionButton}
        />
      </View>
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
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: COLORS.background,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  profileInfo: {
    flex: 1,
  },
  nameRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  name: {
    fontSize: 18,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginRight: SPACING.sm,
  },
  verifiedBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: `${COLORS.success}20`,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 2,
    borderRadius: 12,
  },
  verifiedText: {
    fontSize: 12,
    fontFamily: FONTS.medium,
    color: COLORS.success,
    marginLeft: 4,
  },
  location: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    marginBottom: SPACING.xs,
  },
  profileMeta: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  completionBadge: {
    backgroundColor: COLORS.background,
    paddingHorizontal: SPACING.sm,
    paddingVertical: 2,
    borderRadius: 8,
  },
  completionText: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
  },
  compatibilitySection: {
    alignItems: 'center',
    marginLeft: SPACING.md,
  },
  compatibilityScore: {
    width: 50,
    height: 50,
    borderRadius: 25,
    borderWidth: 3,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
  },
  scoreText: {
    fontSize: 14,
    fontFamily: FONTS.bold,
  },
  compatibilityLabel: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs,
  },
  detailsSection: {
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
  reasonsSection: {
    marginBottom: SPACING.lg,
  },
  reasonsTitle: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    color: COLORS.text,
    marginBottom: SPACING.sm,
  },
  reasonsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.xs,
  },
  reasonChip: {
    backgroundColor: `${COLORS.primary}10`,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderRadius: 8,
    marginRight: SPACING.xs,
    marginBottom: SPACING.xs,
  },
  reasonText: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: COLORS.primary,
  },
  moreReasons: {
    fontSize: 12,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    alignSelf: 'center',
  },
  actionsSection: {
    flexDirection: 'row',
    gap: SPACING.md,
  },
  actionButton: {
    flex: 1,
  },
});