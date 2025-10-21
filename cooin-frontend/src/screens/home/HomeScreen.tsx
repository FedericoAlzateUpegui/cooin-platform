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

interface HomeScreenProps {
  navigation: any;
}

export const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const { user } = useAuthStore();
  const { profile, loadProfile, profileCompletion } = useProfileStore();

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
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

  const quickActions = [
    {
      id: 'discover',
      title: 'Discover Matches',
      icon: 'people' as const,
      color: COLORS.primary,
      onPress: () => navigation.navigate('Matching'),
    },
    {
      id: 'connections',
      title: 'My Connections',
      icon: 'link' as const,
      color: COLORS.accent,
      onPress: () => navigation.navigate('Connections'),
    },
    {
      id: 'messages',
      title: 'Messages',
      icon: 'chatbubbles' as const,
      color: COLORS.success,
      onPress: () => navigation.navigate('Messages'),
    },
    {
      id: 'profile',
      title: 'Complete Profile',
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
              {profile?.display_name || user?.email?.split('@')[0] || 'User'}
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
              <Text style={styles.completionTitle}>Complete Your Profile</Text>
            </View>
            <Text style={styles.completionDescription}>
              Your profile is {profileCompletion}% complete. Complete it to get better matches!
            </Text>
            <View style={styles.progressBar}>
              <View style={[styles.progressFill, { width: `${profileCompletion}%` }]} />
            </View>
            <Button
              title="Complete Now"
              onPress={() => navigation.navigate('Profile')}
              variant="outline"
              style={styles.completeButton}
            />
          </View>
        )}

        {/* Welcome Message */}
        <View style={styles.welcomeCard}>
          <Ionicons name="rocket" size={32} color={COLORS.primary} />
          <Text style={styles.welcomeTitle}>Welcome to Cooin</Text>
          <Text style={styles.welcomeDescription}>
            Connect with {user?.role === 'lender' ? 'borrowers' : 'lenders'} who match your
            criteria. Build trust, negotiate terms, and create successful lending relationships.
          </Text>
        </View>

        {/* Quick Actions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
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
          <Text style={styles.sectionTitle}>Getting Started</Text>
          <View style={styles.guideCard}>
            <View style={styles.guideStep}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>1</Text>
              </View>
              <View style={styles.stepContent}>
                <Text style={styles.stepTitle}>Complete Your Profile</Text>
                <Text style={styles.stepDescription}>
                  Add your information to build trust with potential matches
                </Text>
              </View>
            </View>

            <View style={styles.guideStep}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>2</Text>
              </View>
              <View style={styles.stepContent}>
                <Text style={styles.stepTitle}>Discover Matches</Text>
                <Text style={styles.stepDescription}>
                  Browse and filter to find the perfect lending partners
                </Text>
              </View>
            </View>

            <View style={styles.guideStep}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>3</Text>
              </View>
              <View style={styles.stepContent}>
                <Text style={styles.stepTitle}>Connect & Message</Text>
                <Text style={styles.stepDescription}>
                  Send connection requests and start conversations
                </Text>
              </View>
            </View>

            <View style={styles.guideStep}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>4</Text>
              </View>
              <View style={styles.stepContent}>
                <Text style={styles.stepTitle}>Negotiate Terms</Text>
                <Text style={styles.stepDescription}>
                  Discuss and agree on loan terms that work for both parties
                </Text>
              </View>
            </View>
          </View>
        </View>

        {/* Role-specific tips */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>
            {user?.role === 'lender' ? 'Lender Tips' : 'Borrower Tips'}
          </Text>
          <View style={styles.tipsCard}>
            {user?.role === 'lender' ? (
              <>
                <Text style={styles.tipText}>
                  • Review borrower profiles carefully before connecting
                </Text>
                <Text style={styles.tipText}>
                  • Set clear interest rates and repayment terms
                </Text>
                <Text style={styles.tipText}>
                  • Use the messaging feature to ask questions
                </Text>
                <Text style={styles.tipText}>
                  • Start with smaller amounts to build trust
                </Text>
              </>
            ) : (
              <>
                <Text style={styles.tipText}>
                  • Complete your profile to increase trust
                </Text>
                <Text style={styles.tipText}>
                  • Be clear about your borrowing needs
                </Text>
                <Text style={styles.tipText}>
                  • Respond promptly to connection requests
                </Text>
                <Text style={styles.tipText}>
                  • Be honest about your repayment ability
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
