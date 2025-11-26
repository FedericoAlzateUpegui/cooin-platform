import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Modal,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
  Switch,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Picker } from '@react-native-picker/picker';
import { useAuthStore } from '../../store/authStore';
import { COLORS } from '../../constants/config';
import { useColors } from '../../hooks/useColors';
import { ticketService } from '../../services/ticketService';
import { logger } from '../../utils/logger';
import { getErrorMessage, getErrorDetails } from '../../utils/errorUtils';

interface CreateTicketModalProps {
  visible: boolean;
  onClose: () => void;
  onSuccess: () => void;
  userRole: 'lender' | 'borrower' | 'both';
}

type TicketType = 'lending_offer' | 'borrowing_request';
type LoanType = 'personal' | 'business' | 'education' | 'home_improvement' | 'debt_consolidation' | 'other';
type WarrantyType = 'none' | 'property' | 'vehicle' | 'savings' | 'investments' | 'other';

export const CreateTicketModal: React.FC<CreateTicketModalProps> = ({
  visible,
  onClose,
  onSuccess,
  userRole,
}) => {
  const colors = useColors();
  const styles = createStyles(colors);
  const { token } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1);
  const [validationError, setValidationError] = useState<string>('');

  // Form state
  const [ticketType, setTicketType] = useState<TicketType>(
    userRole?.toLowerCase() === 'lender' ? 'lending_offer' : 'borrowing_request'
  );
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [minAmount, setMinAmount] = useState('');
  const [maxAmount, setMaxAmount] = useState('');
  const [interestRate, setInterestRate] = useState('');
  const [minInterestRate, setMinInterestRate] = useState('');
  const [maxInterestRate, setMaxInterestRate] = useState('');
  const [termMonths, setTermMonths] = useState('');
  const [minTermMonths, setMinTermMonths] = useState('');
  const [maxTermMonths, setMaxTermMonths] = useState('');
  const [loanType, setLoanType] = useState<LoanType>('personal');
  const [loanPurpose, setLoanPurpose] = useState('');
  const [warrantyType, setWarrantyType] = useState<WarrantyType>('none');
  const [warrantyDescription, setWarrantyDescription] = useState('');
  const [warrantyValue, setWarrantyValue] = useState('');
  const [requirements, setRequirements] = useState('');
  const [preferredLocation, setPreferredLocation] = useState('');
  const [flexibleTerms, setFlexibleTerms] = useState(false);
  const [isPublic, setIsPublic] = useState(true);

  // Reset ticket type when modal opens or userRole changes
  useEffect(() => {
    if (visible) {
      const defaultType = userRole?.toLowerCase() === 'lender' ? 'lending_offer' : 'borrowing_request';
      setTicketType(defaultType);
    }
  }, [visible, userRole]);

  const resetForm = () => {
    setStep(1);
    setValidationError('');
    setTitle('');
    setDescription('');
    setAmount('');
    setMinAmount('');
    setMaxAmount('');
    setInterestRate('');
    setMinInterestRate('');
    setMaxInterestRate('');
    setTermMonths('');
    setMinTermMonths('');
    setMaxTermMonths('');
    setLoanType('personal');
    setLoanPurpose('');
    setWarrantyType('none');
    setWarrantyDescription('');
    setWarrantyValue('');
    setRequirements('');
    setPreferredLocation('');
    setFlexibleTerms(false);
    setIsPublic(true);
  };

  const handleClose = () => {
    resetForm();
    onClose();
  };

  const validateStep1 = (): boolean => {
    if (title.length < 10 || title.length > 200) {
      const message = `Title must be between 10 and 200 characters (current: ${title.length})`;
      setValidationError(message);
      return false;
    }
    if (description.length < 50) {
      const message = `Description must be at least 50 characters (current: ${description.length})`;
      setValidationError(message);
      return false;
    }
    setValidationError('');
    return true;
  };

  const validateStep2 = (): boolean => {
    const amountNum = parseFloat(amount);
    const interestNum = parseFloat(interestRate);
    const termNum = parseInt(termMonths);

    if (isNaN(amountNum) || amountNum <= 0) {
      setValidationError('Please enter a valid amount');
      return false;
    }
    if (isNaN(interestNum) || interestNum < 0 || interestNum > 100) {
      setValidationError('Interest rate must be between 0 and 100');
      return false;
    }
    if (isNaN(termNum) || termNum <= 0 || termNum > 360) {
      setValidationError('Term must be between 1 and 360 months');
      return false;
    }

    // Validate ranges if flexible terms is enabled
    if (flexibleTerms) {
      if (minAmount && parseFloat(minAmount) > amountNum) {
        setValidationError('Minimum amount cannot be greater than amount');
        return false;
      }
      if (maxAmount && parseFloat(maxAmount) < amountNum) {
        setValidationError('Maximum amount cannot be less than amount');
        return false;
      }
    }

    setValidationError('');
    return true;
  };

  const validateStep3 = (): boolean => {
    logger.debug('Validating step 3', { loanPurpose, loanPurposeLength: loanPurpose.length, warrantyType, warrantyValue });

    if (loanPurpose.length < 20) {
      const message = `Loan purpose must be at least 20 characters (current: ${loanPurpose.length})`;
      logger.warn('Validation failed', { message });
      setValidationError(message);
      return false;
    }
    if (warrantyType !== 'none' && !warrantyValue) {
      logger.warn('Validation failed: Warranty value required');
      setValidationError('Please enter warranty value');
      return false;
    }
    logger.debug('Step 3 validation passed');
    setValidationError('');
    return true;
  };

  const handleNext = () => {
    logger.debug('Next button clicked', { currentStep: step });
    if (step === 1) {
      logger.debug('Validating step 1', { title, descriptionLength: description.length });
      if (validateStep1()) {
        logger.info('Step 1 validated, moving to step 2');
        setStep(2);
      } else {
        logger.warn('Step 1 validation failed');
      }
    } else if (step === 2) {
      logger.debug('Validating step 2');
      if (validateStep2()) {
        logger.info('Step 2 validated, moving to step 3');
        setStep(3);
      } else {
        logger.warn('Step 2 validation failed');
      }
    } else if (step === 3) {
      logger.debug('Validating step 3');
      if (validateStep3()) {
        logger.info('Step 3 validated, moving to step 4');
        setStep(4);
      } else {
        logger.warn('Step 3 validation failed');
      }
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      logger.info('Creating ticket...');

      const ticketData: any = {
        ticket_type: ticketType,
        title,
        description,
        amount: parseFloat(amount),
        interest_rate: parseFloat(interestRate),
        term_months: parseInt(termMonths),
        loan_type: loanType,
        loan_purpose: loanPurpose,
        warranty_type: warrantyType,
        flexible_terms: flexibleTerms,
        is_public: isPublic,
      };

      // Add optional fields
      if (minAmount) ticketData.min_amount = parseFloat(minAmount);
      if (maxAmount) ticketData.max_amount = parseFloat(maxAmount);
      if (minInterestRate) ticketData.min_interest_rate = parseFloat(minInterestRate);
      if (maxInterestRate) ticketData.max_interest_rate = parseFloat(maxInterestRate);
      if (minTermMonths) ticketData.min_term_months = parseInt(minTermMonths);
      if (maxTermMonths) ticketData.max_term_months = parseInt(maxTermMonths);
      if (warrantyDescription) ticketData.warranty_description = warrantyDescription;
      if (warrantyValue) ticketData.warranty_value = parseFloat(warrantyValue);
      if (requirements) ticketData.requirements = requirements;
      if (preferredLocation) ticketData.preferred_location = preferredLocation;

      logger.debug('Ticket data', ticketData);

      const response = await ticketService.createTicket(ticketData);

      logger.info('Ticket created successfully', response);

      const successMessage = `Your ${ticketType === 'lending_offer' ? 'lending offer' : 'borrowing request'} has been created!`;

      if (Platform.OS === 'web') {
        window.alert(`Success! ${successMessage}`);
      } else {
        Alert.alert('Success', successMessage);
      }

      resetForm();
      onSuccess();
      onClose();
    } catch (error: unknown) {
      const errorDetails = getErrorDetails(error);
      logger.error('Error creating ticket', errorDetails);

      const errorMessage = getErrorMessage(error);
      logger.error('Displaying error', { errorMessage });

      if (Platform.OS === 'web') {
        window.alert(`Error: ${errorMessage}`);
      } else {
        Alert.alert('Error', errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  const renderStep1 = () => (
    <View style={styles.stepContainer}>
      <Text style={styles.stepTitle}>Basic Information</Text>
      <Text style={styles.stepDescription}>Tell us about your {ticketType === 'lending_offer' ? 'lending offer' : 'borrowing request'}</Text>

      {userRole === 'both' && (
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Type</Text>
          <View style={styles.typeButtons}>
            <TouchableOpacity
              style={[styles.typeButton, ticketType === 'lending_offer' && styles.typeButtonActive]}
              onPress={() => setTicketType('lending_offer')}
            >
              <Ionicons name="cash-outline" size={20} color={ticketType === 'lending_offer' ? colors.success : colors.text} />
              <Text style={[styles.typeButtonText, ticketType === 'lending_offer' && styles.typeButtonTextActive]}>
                Lending Offer
              </Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.typeButton, ticketType === 'borrowing_request' && styles.typeButtonActive]}
              onPress={() => setTicketType('borrowing_request')}
            >
              <Ionicons name="wallet-outline" size={20} color={ticketType === 'borrowing_request' ? colors.primary : colors.text} />
              <Text style={[styles.typeButtonText, ticketType === 'borrowing_request' && styles.typeButtonTextActive]}>
                Borrowing Request
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      )}

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Title *</Text>
        <TextInput
          style={styles.input}
          value={title}
          onChangeText={setTitle}
          placeholder="e.g., 'Offering $50,000 for small business loans'"
          placeholderTextColor={colors.textSecondary}
          maxLength={200}
        />
        <Text style={styles.charCount}>{title.length}/200 characters</Text>
      </View>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Description *</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          value={description}
          onChangeText={setDescription}
          placeholder="Provide a detailed description of your offer or request..."
          placeholderTextColor={colors.textSecondary}
          multiline
          numberOfLines={6}
          textAlignVertical="top"
        />
        <Text style={styles.charCount}>{description.length} characters (minimum 50)</Text>
      </View>
    </View>
  );

  const renderStep2 = () => (
    <View style={styles.stepContainer}>
      <Text style={styles.stepTitle}>Financial Terms</Text>
      <Text style={styles.stepDescription}>Set your financial terms and conditions</Text>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Amount *</Text>
        <TextInput
          style={styles.input}
          value={amount}
          onChangeText={setAmount}
          placeholder="e.g., 50000"
          placeholderTextColor={colors.textSecondary}
          keyboardType="decimal-pad"
        />
      </View>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Interest Rate (% APR) *</Text>
        <TextInput
          style={styles.input}
          value={interestRate}
          onChangeText={setInterestRate}
          placeholder="e.g., 8.5"
          placeholderTextColor={colors.textSecondary}
          keyboardType="decimal-pad"
        />
      </View>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Term (Months) *</Text>
        <TextInput
          style={styles.input}
          value={termMonths}
          onChangeText={setTermMonths}
          placeholder="e.g., 24"
          placeholderTextColor={colors.textSecondary}
          keyboardType="number-pad"
        />
      </View>

      <View style={styles.switchGroup}>
        <View>
          <Text style={styles.label}>Flexible Terms</Text>
          <Text style={styles.switchDescription}>Allow negotiation on amounts and rates</Text>
        </View>
        <Switch
          value={flexibleTerms}
          onValueChange={setFlexibleTerms}
          trackColor={{ false: colors.border, true: colors.primary + '60' }}
          thumbColor={flexibleTerms ? colors.primary : colors.textSecondary}
        />
      </View>

      {flexibleTerms && (
        <>
          <View style={styles.rangeRow}>
            <View style={[styles.inputGroup, { flex: 1, marginRight: 8 }]}>
              <Text style={styles.label}>Min Amount</Text>
              <TextInput
                style={styles.input}
                value={minAmount}
                onChangeText={setMinAmount}
                placeholder="Optional"
                placeholderTextColor={colors.textSecondary}
                keyboardType="decimal-pad"
              />
            </View>
            <View style={[styles.inputGroup, { flex: 1, marginLeft: 8 }]}>
              <Text style={styles.label}>Max Amount</Text>
              <TextInput
                style={styles.input}
                value={maxAmount}
                onChangeText={setMaxAmount}
                placeholder="Optional"
                placeholderTextColor={colors.textSecondary}
                keyboardType="decimal-pad"
              />
            </View>
          </View>

          <View style={styles.rangeRow}>
            <View style={[styles.inputGroup, { flex: 1, marginRight: 8 }]}>
              <Text style={styles.label}>Min Rate (%)</Text>
              <TextInput
                style={styles.input}
                value={minInterestRate}
                onChangeText={setMinInterestRate}
                placeholder="Optional"
                placeholderTextColor={colors.textSecondary}
                keyboardType="decimal-pad"
              />
            </View>
            <View style={[styles.inputGroup, { flex: 1, marginLeft: 8 }]}>
              <Text style={styles.label}>Max Rate (%)</Text>
              <TextInput
                style={styles.input}
                value={maxInterestRate}
                onChangeText={setMaxInterestRate}
                placeholder="Optional"
                placeholderTextColor={colors.textSecondary}
                keyboardType="decimal-pad"
              />
            </View>
          </View>

          <View style={styles.rangeRow}>
            <View style={[styles.inputGroup, { flex: 1, marginRight: 8 }]}>
              <Text style={styles.label}>Min Term (mo)</Text>
              <TextInput
                style={styles.input}
                value={minTermMonths}
                onChangeText={setMinTermMonths}
                placeholder="Optional"
                placeholderTextColor={colors.textSecondary}
                keyboardType="number-pad"
              />
            </View>
            <View style={[styles.inputGroup, { flex: 1, marginLeft: 8 }]}>
              <Text style={styles.label}>Max Term (mo)</Text>
              <TextInput
                style={styles.input}
                value={maxTermMonths}
                onChangeText={setMaxTermMonths}
                placeholder="Optional"
                placeholderTextColor={colors.textSecondary}
                keyboardType="number-pad"
              />
            </View>
          </View>
        </>
      )}
    </View>
  );

  const renderStep3 = () => (
    <View style={styles.stepContainer}>
      <Text style={styles.stepTitle}>Loan Details</Text>
      <Text style={styles.stepDescription}>Provide details about the loan</Text>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Loan Type *</Text>
        <View style={styles.pickerContainer}>
          <Picker
            selectedValue={loanType}
            onValueChange={(value) => setLoanType(value as LoanType)}
            style={styles.picker}
          >
            <Picker.Item label="Personal" value="personal" />
            <Picker.Item label="Business" value="business" />
            <Picker.Item label="Education" value="education" />
            <Picker.Item label="Home Improvement" value="home_improvement" />
            <Picker.Item label="Debt Consolidation" value="debt_consolidation" />
            <Picker.Item label="Other" value="other" />
          </Picker>
        </View>
      </View>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Loan Purpose *</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          value={loanPurpose}
          onChangeText={setLoanPurpose}
          placeholder="Explain the purpose or reason for this loan..."
          placeholderTextColor={colors.textSecondary}
          multiline
          numberOfLines={4}
          textAlignVertical="top"
        />
        <Text style={styles.charCount}>{loanPurpose.length} characters (minimum 20)</Text>
      </View>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Warranty/Collateral Type</Text>
        <View style={styles.pickerContainer}>
          <Picker
            selectedValue={warrantyType}
            onValueChange={(value) => setWarrantyType(value as WarrantyType)}
            style={styles.picker}
          >
            <Picker.Item label="None" value="none" />
            <Picker.Item label="Property" value="property" />
            <Picker.Item label="Vehicle" value="vehicle" />
            <Picker.Item label="Savings" value="savings" />
            <Picker.Item label="Investments" value="investments" />
            <Picker.Item label="Other" value="other" />
          </Picker>
        </View>
      </View>

      {warrantyType !== 'none' && (
        <>
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Warranty Description</Text>
            <TextInput
              style={[styles.input, styles.textArea]}
              value={warrantyDescription}
              onChangeText={setWarrantyDescription}
              placeholder="Describe the collateral..."
              placeholderTextColor={colors.textSecondary}
              multiline
              numberOfLines={3}
              textAlignVertical="top"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Estimated Value *</Text>
            <TextInput
              style={styles.input}
              value={warrantyValue}
              onChangeText={setWarrantyValue}
              placeholder="e.g., 100000"
              placeholderTextColor={colors.textSecondary}
              keyboardType="decimal-pad"
            />
          </View>
        </>
      )}
    </View>
  );

  const renderStep4 = () => (
    <View style={styles.stepContainer}>
      <Text style={styles.stepTitle}>Additional Details</Text>
      <Text style={styles.stepDescription}>Optional information</Text>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Requirements (Optional)</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          value={requirements}
          onChangeText={setRequirements}
          placeholder="Any specific requirements for applicants..."
          placeholderTextColor={colors.textSecondary}
          multiline
          numberOfLines={4}
          textAlignVertical="top"
        />
      </View>

      <View style={styles.inputGroup}>
        <Text style={styles.label}>Preferred Location (Optional)</Text>
        <TextInput
          style={styles.input}
          value={preferredLocation}
          onChangeText={setPreferredLocation}
          placeholder="e.g., New York, USA"
          placeholderTextColor={colors.textSecondary}
        />
      </View>

      <View style={styles.switchGroup}>
        <View>
          <Text style={styles.label}>Make Public</Text>
          <Text style={styles.switchDescription}>Visible in marketplace</Text>
        </View>
        <Switch
          value={isPublic}
          onValueChange={setIsPublic}
          trackColor={{ false: colors.border, true: colors.primary + '60' }}
          thumbColor={isPublic ? colors.primary : colors.textSecondary}
        />
      </View>

      <View style={styles.summaryBox}>
        <Text style={styles.summaryTitle}>Summary</Text>
        <View style={styles.summaryRow}>
          <Text style={styles.summaryLabel}>Type:</Text>
          <Text style={styles.summaryValue}>
            {ticketType === 'lending_offer' ? 'Lending Offer' : 'Borrowing Request'}
          </Text>
        </View>
        <View style={styles.summaryRow}>
          <Text style={styles.summaryLabel}>Amount:</Text>
          <Text style={styles.summaryValue}>${parseFloat(amount || '0').toLocaleString()}</Text>
        </View>
        <View style={styles.summaryRow}>
          <Text style={styles.summaryLabel}>Interest Rate:</Text>
          <Text style={styles.summaryValue}>{interestRate}% APR</Text>
        </View>
        <View style={styles.summaryRow}>
          <Text style={styles.summaryLabel}>Term:</Text>
          <Text style={styles.summaryValue}>{termMonths} months</Text>
        </View>
        <View style={styles.summaryRow}>
          <Text style={styles.summaryLabel}>Loan Type:</Text>
          <Text style={styles.summaryValue}>{loanType}</Text>
        </View>
      </View>
    </View>
  );

  return (
    <Modal visible={visible} animationType="slide" transparent={false}>
      <View style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={handleClose} style={styles.closeButton}>
            <Ionicons name="close" size={24} color={colors.text} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>
            Create {ticketType === 'lending_offer' ? 'Lending Offer' : 'Borrowing Request'}
          </Text>
          <View style={{ width: 24 }} />
        </View>

        <View style={styles.progressContainer}>
          {[1, 2, 3, 4].map((s) => (
            <View
              key={s}
              style={[
                styles.progressDot,
                s <= step && styles.progressDotActive,
                s < step && styles.progressDotCompleted,
              ]}
            />
          ))}
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {step === 1 && renderStep1()}
          {step === 2 && renderStep2()}
          {step === 3 && renderStep3()}
          {step === 4 && renderStep4()}
        </ScrollView>

        {validationError ? (
          <View style={styles.errorContainer}>
            <Ionicons name="alert-circle" size={20} color={colors.error} />
            <Text style={styles.errorText}>{validationError}</Text>
          </View>
        ) : null}

        <View style={styles.footer}>
          {step > 1 && (
            <TouchableOpacity
              style={styles.backButton}
              onPress={() => {
                setValidationError('');
                setStep(step - 1);
              }}
            >
              <Ionicons name="arrow-back" size={20} color={colors.primary} />
              <Text style={styles.backButtonText}>Back</Text>
            </TouchableOpacity>
          )}
          <View style={{ flex: 1 }} />
          {step < 4 ? (
            <TouchableOpacity style={styles.nextButton} onPress={handleNext}>
              <Text style={styles.nextButtonText}>Next</Text>
              <Ionicons name="arrow-forward" size={20} color="#fff" />
            </TouchableOpacity>
          ) : (
            <TouchableOpacity
              style={[styles.submitButton, loading && styles.submitButtonDisabled]}
              onPress={handleSubmit}
              disabled={loading}
            >
              <Text style={styles.submitButtonText}>
                {loading ? 'Creating...' : 'Create Ticket'}
              </Text>
            </TouchableOpacity>
          )}
        </View>
      </View>
    </Modal>
  );
};

const createStyles = (colors: ReturnType<typeof useColors>) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  closeButton: {
    padding: 4,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
  },
  progressContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 16,
    gap: 8,
  },
  progressDot: {
    width: 40,
    height: 4,
    backgroundColor: colors.border,
    borderRadius: 2,
  },
  progressDotActive: {
    backgroundColor: colors.primary + '60',
  },
  progressDotCompleted: {
    backgroundColor: colors.primary,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  stepContainer: {
    paddingBottom: 24,
  },
  stepTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.text,
    marginBottom: 8,
  },
  stepDescription: {
    fontSize: 14,
    color: colors.textSecondary,
    marginBottom: 24,
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 8,
  },
  input: {
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
    color: colors.text,
  },
  textArea: {
    minHeight: 100,
    paddingTop: 12,
  },
  charCount: {
    fontSize: 12,
    color: colors.textSecondary,
    marginTop: 4,
    textAlign: 'right',
  },
  typeButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  typeButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderWidth: 2,
    borderColor: colors.border,
    borderRadius: 8,
    gap: 8,
  },
  typeButtonActive: {
    borderColor: colors.primary,
    backgroundColor: colors.primary + '10',
  },
  typeButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.text,
  },
  typeButtonTextActive: {
    color: colors.primary,
  },
  pickerContainer: {
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 8,
    overflow: 'hidden',
  },
  picker: {
    color: colors.text,
    ...Platform.select({
      android: {
        backgroundColor: colors.surface,
      },
    }),
  },
  switchGroup: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
    paddingVertical: 12,
  },
  switchDescription: {
    fontSize: 12,
    color: colors.textSecondary,
    marginTop: 2,
  },
  rangeRow: {
    flexDirection: 'row',
  },
  summaryBox: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: colors.border,
    marginTop: 16,
  },
  summaryTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 12,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  summaryLabel: {
    fontSize: 14,
    color: colors.textSecondary,
  },
  summaryValue: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.text,
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.error + '15',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderTopWidth: 1,
    borderTopColor: colors.error + '30',
    gap: 8,
  },
  errorText: {
    flex: 1,
    fontSize: 14,
    color: colors.error,
    fontWeight: '500',
  },
  footer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: colors.surface,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  backButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.primary,
  },
  nextButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.primary,
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    gap: 8,
  },
  nextButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  submitButton: {
    backgroundColor: colors.primary,
    paddingVertical: 14,
    paddingHorizontal: 32,
    borderRadius: 8,
  },
  submitButtonDisabled: {
    opacity: 0.5,
  },
  submitButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
});
