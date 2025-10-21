import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  TouchableOpacity,
  Alert,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as DocumentPicker from 'expo-document-picker';

import { useAuthStore } from '../../store/authStore';
import { useProfileStore } from '../../store/profileStore';
import { Button } from '../../components/Button';
import { COLORS, SPACING, FONTS } from '../../constants/config';
import { apiClient } from '../../services/api';

interface VerificationScreenProps {
  navigation: any;
}

type VerificationStatus = 'not_uploaded' | 'pending' | 'verified' | 'rejected';

interface VerificationDocument {
  id: string;
  type: string;
  title: string;
  description: string;
  icon: keyof typeof Ionicons.glyphMap;
  status: VerificationStatus;
  required: boolean;
}

export const VerificationScreen: React.FC<VerificationScreenProps> = ({ navigation }) => {
  const { user } = useAuthStore();
  const { profile } = useProfileStore();
  const [uploading, setUploading] = useState<string | null>(null);

  const [documents, setDocuments] = useState<VerificationDocument[]>([
    {
      id: 'identity',
      type: 'identity_document',
      title: 'Identity Document',
      description: 'Government-issued ID, Passport, or Driver\'s License',
      icon: 'card',
      status: profile?.identity_verified ? 'verified' : 'not_uploaded',
      required: true,
    },
    {
      id: 'income',
      type: 'income_proof',
      title: 'Income Verification',
      description: 'Pay stubs, Tax returns, or Employment letter',
      icon: 'cash',
      status: profile?.income_verified ? 'verified' : 'not_uploaded',
      required: user?.role === 'BORROWER',
    },
    {
      id: 'bank',
      type: 'bank_statement',
      title: 'Bank Statement',
      description: 'Recent bank statements (last 3 months)',
      icon: 'business',
      status: profile?.bank_account_verified ? 'verified' : 'not_uploaded',
      required: true,
    },
    {
      id: 'address',
      type: 'address_proof',
      title: 'Proof of Address',
      description: 'Utility bill, Lease agreement, or Bank statement',
      icon: 'home',
      status: 'not_uploaded',
      required: false,
    },
  ]);

  const getStatusColor = (status: VerificationStatus): string => {
    switch (status) {
      case 'verified':
        return COLORS.success;
      case 'pending':
        return COLORS.warning;
      case 'rejected':
        return COLORS.error;
      default:
        return COLORS.textSecondary;
    }
  };

  const getStatusIcon = (status: VerificationStatus): keyof typeof Ionicons.glyphMap => {
    switch (status) {
      case 'verified':
        return 'checkmark-circle';
      case 'pending':
        return 'time';
      case 'rejected':
        return 'close-circle';
      default:
        return 'cloud-upload-outline';
    }
  };

  const getStatusText = (status: VerificationStatus): string => {
    switch (status) {
      case 'verified':
        return 'Verified';
      case 'pending':
        return 'Pending Review';
      case 'rejected':
        return 'Rejected';
      default:
        return 'Upload Document';
    }
  };

  const handleUploadDocument = async (document: VerificationDocument) => {
    try {
      setUploading(document.id);

      // Pick document
      const result = await DocumentPicker.getDocumentAsync({
        type: ['application/pdf', 'image/*', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        copyToCacheDirectory: true,
      });

      if (result.canceled) {
        setUploading(null);
        return;
      }

      const file = result.assets[0];

      // Create FormData
      const formData = new FormData();
      formData.append('file', {
        uri: file.uri,
        type: file.mimeType || 'application/pdf',
        name: file.name,
      } as any);
      formData.append('document_type', document.type);

      // Upload to backend
      const response = await apiClient.post('/uploads/documents/verification', formData);

      // Update document status
      setDocuments(docs =>
        docs.map(doc =>
          doc.id === document.id
            ? { ...doc, status: 'pending' as VerificationStatus }
            : doc
        )
      );

      Alert.alert(
        'Success',
        `${document.title} uploaded successfully. It will be reviewed within 24-48 hours.`
      );

      setUploading(null);
    } catch (error: any) {
      console.error('Error uploading document:', error);
      Alert.alert(
        'Upload Failed',
        error?.detail || error?.message || 'Failed to upload document. Please try again.'
      );
      setUploading(null);
    }
  };

  const verificationProgress = documents.filter(d => d.status === 'verified').length;
  const totalRequired = documents.filter(d => d.required).length;
  const progressPercentage = Math.round((verificationProgress / documents.length) * 100);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Ionicons name="arrow-back" size={24} color={COLORS.text} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Verification Center</Text>
          <View style={{ width: 44 }} />
        </View>

        {/* Progress Card */}
        <View style={styles.progressCard}>
          <View style={styles.progressHeader}>
            <Ionicons name="shield-checkmark" size={32} color={COLORS.primary} />
            <View style={styles.progressInfo}>
              <Text style={styles.progressTitle}>Verification Progress</Text>
              <Text style={styles.progressSubtitle}>
                {verificationProgress} of {documents.length} documents verified
              </Text>
            </View>
          </View>
          <View style={styles.progressBar}>
            <View style={[styles.progressFill, { width: `${progressPercentage}%` }]} />
          </View>
          <Text style={styles.progressPercentage}>{progressPercentage}% Complete</Text>
        </View>

        {/* Info Banner */}
        <View style={styles.infoBanner}>
          <Ionicons name="information-circle" size={20} color={COLORS.primary} />
          <Text style={styles.infoText}>
            Verified accounts build trust and unlock premium features. All documents are securely encrypted.
          </Text>
        </View>

        {/* Documents List */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Required Documents</Text>
          {documents.filter(d => d.required).map((document) => (
            <View key={document.id} style={styles.documentCard}>
              <View style={styles.documentHeader}>
                <View style={styles.documentIcon}>
                  <Ionicons name={document.icon} size={24} color={COLORS.primary} />
                </View>
                <View style={styles.documentInfo}>
                  <Text style={styles.documentTitle}>{document.title}</Text>
                  <Text style={styles.documentDescription}>{document.description}</Text>
                </View>
              </View>
              <View style={styles.documentFooter}>
                <View style={styles.statusContainer}>
                  <Ionicons
                    name={getStatusIcon(document.status)}
                    size={18}
                    color={getStatusColor(document.status)}
                  />
                  <Text style={[styles.statusText, { color: getStatusColor(document.status) }]}>
                    {getStatusText(document.status)}
                  </Text>
                </View>
                {document.status !== 'verified' && (
                  <TouchableOpacity
                    style={styles.uploadButton}
                    onPress={() => handleUploadDocument(document)}
                    disabled={uploading === document.id}
                  >
                    <Ionicons
                      name={uploading === document.id ? 'hourglass' : 'cloud-upload'}
                      size={20}
                      color={COLORS.primary}
                    />
                    <Text style={styles.uploadButtonText}>
                      {uploading === document.id ? 'Uploading...' : 'Upload'}
                    </Text>
                  </TouchableOpacity>
                )}
              </View>
            </View>
          ))}
        </View>

        {/* Optional Documents */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Optional Documents</Text>
          <Text style={styles.sectionSubtitle}>
            Additional verification improves your profile credibility
          </Text>
          {documents.filter(d => !d.required).map((document) => (
            <View key={document.id} style={styles.documentCard}>
              <View style={styles.documentHeader}>
                <View style={styles.documentIcon}>
                  <Ionicons name={document.icon} size={24} color={COLORS.textSecondary} />
                </View>
                <View style={styles.documentInfo}>
                  <Text style={styles.documentTitle}>{document.title}</Text>
                  <Text style={styles.documentDescription}>{document.description}</Text>
                </View>
              </View>
              <View style={styles.documentFooter}>
                <View style={styles.statusContainer}>
                  <Ionicons
                    name={getStatusIcon(document.status)}
                    size={18}
                    color={getStatusColor(document.status)}
                  />
                  <Text style={[styles.statusText, { color: getStatusColor(document.status) }]}>
                    {getStatusText(document.status)}
                  </Text>
                </View>
                {document.status !== 'verified' && (
                  <TouchableOpacity
                    style={styles.uploadButton}
                    onPress={() => handleUploadDocument(document)}
                    disabled={uploading === document.id}
                  >
                    <Ionicons
                      name={uploading === document.id ? 'hourglass' : 'cloud-upload'}
                      size={20}
                      color={COLORS.textSecondary}
                    />
                    <Text style={styles.uploadButtonText}>
                      {uploading === document.id ? 'Uploading...' : 'Upload'}
                    </Text>
                  </TouchableOpacity>
                )}
              </View>
            </View>
          ))}
        </View>

        {/* Help Section */}
        <View style={styles.helpCard}>
          <Ionicons name="help-circle" size={24} color={COLORS.primary} />
          <Text style={styles.helpTitle}>Need Help?</Text>
          <Text style={styles.helpText}>
            Documents are typically reviewed within 24-48 hours. Accepted formats: PDF, JPG, PNG, DOC.
            Maximum file size: 25MB.
          </Text>
          <Button
            title="Contact Support"
            onPress={() => Alert.alert('Support', 'Support feature coming soon!')}
            variant="outline"
            style={styles.helpButton}
          />
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
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: SPACING.lg,
  },
  backButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: COLORS.surface,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  headerTitle: {
    fontSize: 20,
    fontFamily: FONTS.bold,
    color: COLORS.text,
  },
  progressCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  progressHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  progressInfo: {
    flex: 1,
    marginLeft: SPACING.md,
  },
  progressTitle: {
    fontSize: 18,
    fontFamily: FONTS.bold,
    color: COLORS.text,
  },
  progressSubtitle: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs / 2,
  },
  progressBar: {
    height: 8,
    backgroundColor: COLORS.background,
    borderRadius: 4,
    marginBottom: SPACING.sm,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.primary,
    borderRadius: 4,
  },
  progressPercentage: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    color: COLORS.primary,
    textAlign: 'right',
  },
  infoBanner: {
    flexDirection: 'row',
    backgroundColor: `${COLORS.primary}10`,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.lg,
    borderLeftWidth: 3,
    borderLeftColor: COLORS.primary,
  },
  infoText: {
    flex: 1,
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.text,
    marginLeft: SPACING.sm,
    lineHeight: 20,
  },
  section: {
    marginBottom: SPACING.xl,
  },
  sectionTitle: {
    fontSize: 18,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginBottom: SPACING.xs,
  },
  sectionSubtitle: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    marginBottom: SPACING.md,
  },
  documentCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  documentHeader: {
    flexDirection: 'row',
    marginBottom: SPACING.md,
  },
  documentIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: `${COLORS.primary}10`,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  documentInfo: {
    flex: 1,
  },
  documentTitle: {
    fontSize: 16,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginBottom: SPACING.xs / 2,
  },
  documentDescription: {
    fontSize: 13,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    lineHeight: 18,
  },
  documentFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusText: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    marginLeft: SPACING.xs,
  },
  uploadButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: `${COLORS.primary}10`,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderRadius: 8,
  },
  uploadButtonText: {
    fontSize: 14,
    fontFamily: FONTS.medium,
    color: COLORS.primary,
    marginLeft: SPACING.xs,
  },
  helpCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.xl,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
    marginBottom: SPACING.xl,
  },
  helpTitle: {
    fontSize: 18,
    fontFamily: FONTS.bold,
    color: COLORS.text,
    marginTop: SPACING.sm,
    marginBottom: SPACING.sm,
  },
  helpText: {
    fontSize: 14,
    fontFamily: FONTS.regular,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: SPACING.md,
  },
  helpButton: {
    alignSelf: 'stretch',
  },
});
