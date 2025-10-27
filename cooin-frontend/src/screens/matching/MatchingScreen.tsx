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
import { useForm, Controller } from 'react-hook-form';

import { MatchCard } from '../../components/MatchCard';
import { Button } from '../../components/Button';
import { Input } from '../../components/Input';
import { matchingService } from '../../services/matchingService';
import { useAuthStore } from '../../store/authStore';
import { MatchingResult, MatchingCriteria } from '../../types/api';
import { COLORS, SPACING, FONTS } from '../../constants/config';
import { useLanguage } from '../../contexts/LanguageContext';

interface MatchingScreenProps {
  navigation: any;
}

export const MatchingScreen: React.FC<MatchingScreenProps> = ({ navigation }) => {
  const [matches, setMatches] = useState<MatchingResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [searchStats, setSearchStats] = useState<{
    total_matches: number;
    search_time_ms: number;
  } | null>(null);
  const [connectingId, setConnectingId] = useState<number | null>(null);

  const { user } = useAuthStore();
  const { t } = useLanguage();

  const { control, handleSubmit, reset, watch } = useForm<MatchingCriteria>({
    defaultValues: {
      user_role: user?.role === 'lender' ? 'borrower' : 'lender',
      location: '',
      min_loan_amount: undefined,
      max_loan_amount: undefined,
      max_interest_rate: undefined,
      verified_only: false,
    },
  });

  useEffect(() => {
    loadMatches();
  }, []);

  const loadMatches = async (criteria?: MatchingCriteria) => {
    setIsLoading(true);
    try {
      const defaultCriteria: MatchingCriteria = {
        user_role: user?.role === 'lender' ? 'borrower' : 'lender',
        verified_only: false,
      };

      const searchCriteria = { ...defaultCriteria, ...criteria };
      const response = await matchingService.findMatches(searchCriteria);

      setMatches(response.matches);
      setSearchStats({
        total_matches: response.total_matches,
        search_time_ms: response.search_time_ms,
      });
    } catch (error: any) {
      Alert.alert(t('matching_screen.search_error_title'), error.detail || t('matching_screen.search_error_message'));
    } finally {
      setIsLoading(false);
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await loadMatches();
    setIsRefreshing(false);
  };

  const handleSearch = (data: MatchingCriteria) => {
    setShowFilters(false);
    loadMatches(data);
  };

  const handleConnect = async (match: MatchingResult) => {
    setConnectingId(match.user_id);
    try {
      await matchingService.createConnection({
        receiver_id: match.user_id,
        connection_type: user?.role === 'lender' ? 'lending_inquiry' : 'borrowing_request',
        message: t('matching_screen.connection_message', { name: match.public_name }),
      });

      Alert.alert(
        t('matching_screen.connection_sent_title'),
        t('matching_screen.connection_sent_message', { name: match.public_name }),
        [{ text: t('common.ok') }]
      );

      // Remove the match from the list since connection was sent
      setMatches(prev => prev.filter(m => m.user_id !== match.user_id));
    } catch (error: any) {
      Alert.alert(t('matching_screen.connection_failed_title'), error.detail || t('matching_screen.connection_failed_message'));
    } finally {
      setConnectingId(null);
    }
  };

  const handleViewProfile = (match: MatchingResult) => {
    navigation.navigate('PublicProfile', { userId: match.user_id });
  };

  const clearFilters = () => {
    reset();
    loadMatches();
    setShowFilters(false);
  };

  const renderHeader = () => (
    <View style={styles.header}>
      <View style={styles.headerTop}>
        <Text style={styles.title}>{t('matching_screen.title')}</Text>
        <TouchableOpacity
          style={styles.filterButton}
          onPress={() => setShowFilters(!showFilters)}
        >
          <Ionicons
            name={showFilters ? 'close' : 'filter'}
            size={24}
            color={COLORS.primary}
          />
        </TouchableOpacity>
      </View>

      {searchStats && (
        <Text style={styles.searchStats}>
          {t('matching_screen.found_matches', { count: searchStats.total_matches, time: searchStats.search_time_ms })}
        </Text>
      )}

      {showFilters && (
        <View style={styles.filtersContainer}>
          <Text style={styles.filtersTitle}>{t('matching_screen.search_filters')}</Text>

          <Controller
            control={control}
            name="location"
            render={({ field: { onChange, value } }) => (
              <Input
                label={t('matching_screen.location')}
                placeholder={t('matching_screen.location_placeholder')}
                value={value || ''}
                onChangeText={onChange}
                leftIcon="location"
              />
            )}
          />

          <View style={styles.amountRow}>
            <Controller
              control={control}
              name="min_loan_amount"
              render={({ field: { onChange, value } }) => (
                <Input
                  label={t('matching_screen.min_amount')}
                  placeholder={t('matching_screen.min_amount_placeholder')}
                  value={value?.toString() || ''}
                  onChangeText={(text) => {
                    const num = parseFloat(text.replace(/[^0-9.]/g, ''));
                    onChange(isNaN(num) ? undefined : num);
                  }}
                  keyboardType="numeric"
                  style={styles.halfInput}
                />
              )}
            />

            <Controller
              control={control}
              name="max_loan_amount"
              render={({ field: { onChange, value } }) => (
                <Input
                  label={t('matching_screen.max_amount')}
                  placeholder={t('matching_screen.max_amount_placeholder')}
                  value={value?.toString() || ''}
                  onChangeText={(text) => {
                    const num = parseFloat(text.replace(/[^0-9.]/g, ''));
                    onChange(isNaN(num) ? undefined : num);
                  }}
                  keyboardType="numeric"
                  style={styles.halfInput}
                />
              )}
            />
          </View>

          <Controller
            control={control}
            name="max_interest_rate"
            render={({ field: { onChange, value } }) => (
              <Input
                label={t('matching_screen.max_interest_rate')}
                placeholder={t('matching_screen.interest_rate_placeholder')}
                value={value?.toString() || ''}
                onChangeText={(text) => {
                  const num = parseFloat(text.replace(/[^0-9.]/g, ''));
                  onChange(isNaN(num) ? undefined : num);
                }}
                keyboardType="numeric"
              />
            )}
          />

          <Controller
            control={control}
            name="verified_only"
            render={({ field: { onChange, value } }) => (
              <TouchableOpacity
                style={styles.checkboxRow}
                onPress={() => onChange(!value)}
              >
                <View style={[styles.checkbox, value && styles.checkboxChecked]}>
                  {value && <Ionicons name="checkmark" size={16} color={COLORS.surface} />}
                </View>
                <Text style={styles.checkboxLabel}>{t('matching_screen.verified_only')}</Text>
              </TouchableOpacity>
            )}
          />

          <View style={styles.filterActions}>
            <Button
              title={t('matching_screen.clear')}
              onPress={clearFilters}
              variant="outline"
              style={styles.filterActionButton}
            />
            <Button
              title={t('matching_screen.search')}
              onPress={handleSubmit(handleSearch)}
              loading={isLoading}
              style={styles.filterActionButton}
            />
          </View>
        </View>
      )}
    </View>
  );

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Ionicons name="people" size={64} color={COLORS.textSecondary} />
      <Text style={styles.emptyTitle}>{t('matching_screen.no_matches_found')}</Text>
      <Text style={styles.emptyDescription}>
        {t('matching_screen.try_adjusting')}
      </Text>
      <Button
        title={t('matching_screen.refresh')}
        onPress={handleRefresh}
        variant="outline"
        style={styles.refreshButton}
      />
    </View>
  );

  const renderMatch = ({ item }: { item: MatchingResult }) => (
    <MatchCard
      match={item}
      onConnect={() => handleConnect(item)}
      onViewProfile={() => handleViewProfile(item)}
      loading={connectingId === item.user_id}
    />
  );

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={matches}
        renderItem={renderMatch}
        keyExtractor={(item) => item.user_id.toString()}
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
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  title: {
    fontSize: 28,
    fontFamily: FONTS.bold,
    color: COLORS.text,
  },
  filterButton: {
    padding: SPACING.sm,
    borderRadius: 8,
    backgroundColor: `${COLORS.primary}10`,
  },
  searchStats: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    marginBottom: SPACING.md,
  },
  filtersContainer: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: SPACING.lg,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  filtersTitle: {
    fontSize: 18,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  amountRow: {
    flexDirection: 'row',
    gap: SPACING.md,
  },
  halfInput: {
    flex: 1,
  },
  checkboxRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderWidth: 2,
    borderColor: COLORS.border,
    borderRadius: 6,
    marginRight: SPACING.md,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxChecked: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  checkboxLabel: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: COLORS.text,
  },
  filterActions: {
    flexDirection: 'row',
    gap: SPACING.md,
  },
  filterActionButton: {
    flex: 1,
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
  refreshButton: {
    minWidth: 120,
  },
});