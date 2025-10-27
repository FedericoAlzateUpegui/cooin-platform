import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

import { useAuthStore } from '../../store/authStore';
import { useProfileStore } from '../../store/profileStore';
import { Button } from '../../components/Button';
import { COLORS, SPACING, FONTS } from '../../constants/config';
import { useLanguage } from '../../contexts/LanguageContext';

interface HomeScreenProps {
  navigation: any;
}

export const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const { user } = useAuthStore();
  const { profile, loadProfile, profileCompletion } = useProfileStore();
  const { t } = useLanguage();

  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await loadProfile();
    setIsRefreshing(false);
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return t('home.good_morning');
    if (hour < 18) return t('home.good_afternoon');
    return t('home.good_evening');
  };

  const quickActions = [
    {
      id: 'discover',
      title: t('home.discover_matches'),
      icon: 'people' as const,
      color: COLORS.primary,
      onPress: () => navigation.navigate('Matching'),
    },
    {
      id: 'connections',
      title: t('home.my_connections'),
      icon: 'link' as const,
      color: COLORS.accent,
      onPress: () => navigation.navigate('Connections'),
    },
    {
      id: 'messages',
      title: t('home.messages'),
      icon: 'chatbubbles' as const,
      color: COLORS.success,
      onPress: () => navigation.navigate('Messages'),
    },
    {
      id: 'profile',
      title: t('home.complete_profile'),
      icon: 'person' as const,
      color: COLORS.secondary,
      onPress: () => navigation.navigate('Profile'),
    },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.content}
        refreshControl={
          <RefreshControl refreshing={isRefreshing} onRefresh={handleRefresh} />
        }
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>{getGreeting()}</Text>
            <Text style={styles.userName}>
              {profile?.display_name || user?.username || user?.email?.split('@')[0] || 'User'}
            </Text>
          </View>
          <TouchableOpacity
            style={styles.notificationButton}
            onPress={() => {}}
          >
            <Ionicons name="notifications-outline" size={24} color={COLORS.text} />
          </TouchableOpacity>
        </View>

        {/* Profile Completion Card */}
        {profileCompletion !== undefined && profileCompletion < 100 && (
          <View style={styles.completionCard}>
            <View style={styles.completionHeader}>
              <Ionicons name="information-circle" size={24} color={COLORS.primary} />
              <Text style={styles.completionTitle}>{t('home.complete_your_profile')}</Text>
            </View>
            <Text style={styles.completionDescription}>
              {t('home.profile_completion_description', { percentage: profileCompletion })}
            </Text>
            <View style={styles.progressBar}>
              <View style={[styles.progressFill, { width: `${profileCompletion}%` }]} />
            </View>
            <Button
              title={t('home.complete_now')}
              onPress={() => navigation.navigate('Profile')}
              variant="outline"
              style={styles.completeButton}
            />
          </View>
        )}

        {/* Welcome Message */}
        <View style={styles.welcomeCard}>
          <Ionicons name="rocket" size={32} color={COLORS.primary} />
          <Text style={styles.welcomeTitle}>{t('home.welcome_title')}</Text>
          <Text style={styles.welcomeDescription}>
            {t('home.welcome_description', {
              role: user?.role === 'lender' ? t('home.borrowers') : t('home.lenders')
            })}
          </Text>
        </View>

        {/* Quick Actions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>{t('home.quick_actions')}</Text>
          <View style={styles.quickActionsGrid}>
            {quickActions.map((action) => (
              <TouchableOpacity
                key={action.id}
                style={styles.quickActionCard}
                onPress={action.onPress}
              >
                <View style={[styles.quickActionIcon, { backgroundColor: `${action.color}15` }]}>
                  <Ionicons name={action.icon} size={28} color={action.color} />
                </View>
                <Text style={styles.quickActionTitle}>{action.title}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Getting Started */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>{t('home.getting_started')}</Text>
          <View style={styles.guideCard}>
            <View style={styles.guideStep}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>1</Text>
              </View>
              <View style={styles.stepContent}>
                <Text style={styles.stepTitle}>{t('home.step1_title')}</Text>
                <Text style={styles.stepDescription}>
                  {t('home.step1_description')}
                </Text>
              </View>
            </View>

            <View style={styles.guideStep}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>2</Text>
              </View>
              <View style={styles.stepContent}>
                <Text style={styles.stepTitle}>{t('home.step2_title')}</Text>
                <Text style={styles.stepDescription}>
                  {t('home.step2_description')}
                </Text>
              </View>
            </View>

            <View style={styles.guideStep}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>3</Text>
              </View>
              <View style={styles.stepContent}>
                <Text style={styles.stepTitle}>{t('home.step3_title')}</Text>
                <Text style={styles.stepDescription}>
                  {t('home.step3_description')}
                </Text>
              </View>
            </View>

            <View style={styles.guideStep}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>4</Text>
              </View>
              <View style={styles.stepContent}>
                <Text style={styles.stepTitle}>{t('home.step4_title')}</Text>
                <Text style={styles.stepDescription}>
                  {t('home.step4_description')}
                </Text>
              </View>
            </View>
          </View>
        </View>

        {/* Role-specific tips */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>
            {user?.role === 'lender' ? t('home.lender_tips') : t('home.borrower_tips')}
          </Text>
          <View style={styles.tipsCard}>
            {user?.role === 'lender' ? (
              <>
                <Text style={styles.tipText}>
                  {t('home.lender_tip1')}
                </Text>
                <Text style={styles.tipText}>
                  {t('home.lender_tip2')}
                </Text>
                <Text style={styles.tipText}>
                  {t('home.lender_tip3')}
                </Text>
                <Text style={styles.tipText}>
                  {t('home.lender_tip4')}
                </Text>
              </>
            ) : (
              <>
                <Text style={styles.tipText}>
                  {t('home.borrower_tip1')}
                </Text>
                <Text style={styles.tipText}>
                  {t('home.borrower_tip2')}
                </Text>
                <Text style={styles.tipText}>
                  {t('home.borrower_tip3')}
                </Text>
                <Text style={styles.tipText}>
                  {t('home.borrower_tip4')}
                </Text>
              </>
            )}
          </View>
        </View>
      </ScrollView>
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
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  greeting: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
  },
  userName: {
    fontSize: 28,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginTop: SPACING.xs,
  },
  notificationButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: COLORS.surface,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  completionCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  completionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  completionTitle: {
    fontSize: 18,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginLeft: SPACING.sm,
  },
  completionDescription: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    marginBottom: SPACING.md,
  },
  progressBar: {
    height: 8,
    backgroundColor: COLORS.background,
    borderRadius: 4,
    marginBottom: SPACING.md,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.primary,
    borderRadius: 4,
  },
  completeButton: {
    alignSelf: 'flex-start',
  },
  welcomeCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.xl,
    marginBottom: SPACING.lg,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  welcomeTitle: {
    fontSize: 24,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginTop: SPACING.md,
    marginBottom: SPACING.sm,
  },
  welcomeDescription: {
    fontSize: 16,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
  },
  section: {
    marginBottom: SPACING.xl,
  },
  sectionTitle: {
    fontSize: 20,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  quickActionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.md,
  },
  quickActionCard: {
    flex: 1,
    minWidth: '45%',
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: SPACING.lg,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  quickActionIcon: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  quickActionTitle: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    color: COLORS.text,
    textAlign: 'center',
  },
  guideCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  guideStep: {
    flexDirection: 'row',
    marginBottom: SPACING.lg,
  },
  stepNumber: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  stepNumberText: {
    fontSize: 16,
    fontFamily: FONTS.bold,
    color: COLORS.surface,
  },
  stepContent: {
    flex: 1,
  },
  stepTitle: {
    fontSize: 16,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginBottom: SPACING.xs,
  },
  stepDescription: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    lineHeight: 20,
  },
  tipsCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  tipText: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.text,
    marginBottom: SPACING.sm,
    lineHeight: 22,
  },
});
