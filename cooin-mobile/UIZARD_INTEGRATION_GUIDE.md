# 🎨 Uizard Integration Guide for Cooin Mobile App

This guide provides detailed specifications for creating UI components in Uizard that will integrate with the Cooin mobile app.

## 📋 Overview

The Cooin app uses a **Container-Component architecture**:
- **Screen Containers** handle all business logic, state, and API calls
- **Uizard Components** handle only UI rendering and user interactions
- **Props Interface** provides clean communication between them

## 🎯 Required Components

### 1. Authentication Components

#### `UizardWelcomeComponent`
**Purpose**: First screen users see when opening the app

**Required Props**:
```javascript
{
  onGetStarted: () => void,  // Navigate to registration
  onSignIn: () => void       // Navigate to login
}
```

**UI Elements Needed**:
- Cooin logo/branding
- Hero section with app description
- "Get Started" primary button
- "Already have an account? Sign In" secondary button
- App features showcase (optional)

**Design Notes**:
- Should feel welcoming and trustworthy
- Emphasize financial security and connections
- Use Cooin brand colors (Primary: #2E86AB)

---

#### `UizardLoginComponent`
**Purpose**: User login screen

**Required Props**:
```javascript
{
  formData: {
    email: string,
    password: string,
    rememberMe: boolean
  },
  onInputChange: (field: string, value: any) => void,
  onLogin: () => void,
  onForgotPassword: () => void,
  onSignUp: () => void,
  onGoBack: () => void,
  loading: boolean,
  error: string | null,
  isFormValid: boolean
}
```

**UI Elements Needed**:
- Email input field with validation styling
- Password input field with show/hide toggle
- "Remember me" checkbox
- "Sign In" button (disabled when !isFormValid or loading)
- "Forgot Password?" link
- "Don't have an account? Sign Up" link
- Error message display (when error exists)
- Loading spinner (when loading is true)
- Back button/navigation

**Validation States**:
- Invalid email: red border, error text
- Valid input: green border or checkmark
- Loading state: disable inputs, show spinner

---

#### `UizardRegisterComponent`
**Purpose**: New user registration

**Required Props**:
```javascript
{
  formData: {
    email: string,
    username: string,
    password: string,
    confirmPassword: string,
    role: 'lender' | 'borrower' | 'both',
    agreeToTerms: boolean
  },
  onInputChange: (field: string, value: any) => void,
  onRegister: () => void,
  onSignIn: () => void,
  onGoBack: () => void,
  loading: boolean,
  error: string | null,
  isFormValid: boolean,
  passwordStrength: 'weak' | 'fair' | 'strong'
}
```

**UI Elements Needed**:
- Email input with validation
- Username input (min 3 characters)
- Password input with strength indicator
- Confirm password input with match indicator
- Role selection (Lender/Borrower/Both) - prominent feature
- "I agree to Terms & Conditions" checkbox
- "Create Account" button
- "Already have an account? Sign In" link
- Password strength indicator (weak/fair/strong)
- Error message display
- Loading state

**Role Selection Design**:
- Visual cards for each role
- Clear descriptions:
  - **Lender**: "I want to lend money to others"
  - **Borrower**: "I need to borrow money"
  - **Both**: "I want to both lend and borrow"

---

### 2. Profile Components

#### `UizardProfileSetupComponent`
**Purpose**: Initial profile setup after registration

**Required Props**:
```javascript
{
  formData: {
    firstName: string,
    lastName: string,
    displayName: string,
    bio: string,
    dateOfBirth: Date | null,
    phoneNumber: string,
    country: string,
    city: string,
    // ... other profile fields
  },
  onInputChange: (field: string, value: any) => void,
  onNext: () => void,
  onSkip: () => void,
  currentStep: number,
  totalSteps: number,
  loading: boolean
}
```

**UI Elements Needed**:
- Progress indicator (step X of Y)
- Form fields based on current step
- Profile photo upload area
- "Next" button
- "Skip for now" option (for optional fields)
- Step navigation
- Field validation indicators

**Multi-Step Flow**:
1. Basic Info (name, display name, bio)
2. Contact Info (phone, location)
3. Photo Upload
4. Role-specific preferences
5. Review & Complete

---

### 3. Discovery/Matching Components

#### `UizardDiscoveryComponent`
**Purpose**: Main discovery screen to find matches

**Required Props**:
```javascript
{
  matches: Array<{
    user_id: number,
    public_name: string,
    compatibility_score: number,
    match_reasons: string[],
    location_string: string,
    is_verified: boolean,
    loan_amount_range: string,
    // ... other match data
  }>,
  onViewProfile: (userId: number) => void,
  onSendConnection: (userId: number) => void,
  onSearch: () => void,
  onFilter: () => void,
  loading: boolean,
  hasSearched: boolean
}
```

**UI Elements Needed**:
- Search bar with filters button
- Match cards with:
  - Profile photo
  - Name and verification badge
  - Compatibility score (circular progress)
  - Location
  - Loan amount range
  - Match reasons (tags)
  - "Connect" button
  - "View Profile" button
- Empty state (no matches found)
- Loading state (skeleton cards)
- Pull-to-refresh

**Match Card Design**:
- Card-based layout
- Compatibility score prominently displayed
- Trust indicators (verification badges)
- Quick action buttons

---

### 4. Connection Components

#### `UizardConnectionsListComponent`
**Purpose**: List of user's connections

**Required Props**:
```javascript
{
  connections: Array<{
    id: number,
    status: 'pending' | 'accepted' | 'rejected',
    connection_type: string,
    message: string,
    loan_amount_requested: number,
    created_at: string,
    // ... other connection data
  }>,
  onViewConnection: (connectionId: number) => void,
  onAccept: (connectionId: number) => void,
  onReject: (connectionId: number) => void,
  loading: boolean,
  refreshing: boolean,
  onRefresh: () => void
}
```

**UI Elements Needed**:
- Tab navigation (All, Pending, Active)
- Connection cards with:
  - User info
  - Connection type badge
  - Status indicator
  - Loan amount (if applicable)
  - Time stamp
  - Action buttons (Accept/Reject for pending)
- Empty states for each tab
- Pull-to-refresh
- Loading states

---

### 5. Messaging Components

#### `UizardChatComponent`
**Purpose**: Chat interface between connected users

**Required Props**:
```javascript
{
  messages: Array<{
    id: number,
    sender_id: number,
    content: string,
    created_at: string,
    is_read: boolean,
    // ... other message data
  }>,
  currentUserId: number,
  connectionInfo: {
    other_user_name: string,
    other_user_avatar: string,
    connection_type: string
  },
  onSendMessage: (text: string) => void,
  onLoadMore: () => void,
  sending: boolean,
  loading: boolean
}
```

**UI Elements Needed**:
- Chat header with user info
- Message list with:
  - Message bubbles (sent/received styling)
  - Time stamps
  - Read receipts
  - Date separators
- Message input with:
  - Text input field
  - Send button
  - Attachment button (future)
- Loading states
- Typing indicator (future)

---

## 🎨 Design System

### Colors (from THEME)
```javascript
PRIMARY: '#2E86AB',        // Ocean Blue
PRIMARY_LIGHT: '#A23B72',  // Purple Pink
PRIMARY_DARK: '#F18F01',   // Orange
SUCCESS: '#10B981',
WARNING: '#F59E0B',
ERROR: '#EF4444',
LENDER_COLOR: '#059669',   // Green for lenders
BORROWER_COLOR: '#DC2626', // Red for borrowers
BOTH_COLOR: '#7C3AED'      // Purple for both roles
```

### Typography
- Headers: Bold, larger sizes
- Body text: Regular weight
- Captions: Smaller, lighter weight
- Form labels: Medium weight

### Spacing
- xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px

### Border Radius
- sm: 4px, md: 8px, lg: 12px, xl: 16px

### Shadows
Use elevation/shadow for cards and buttons

## 📱 Platform Considerations

### iOS Specific
- Use iOS-style navigation elements
- Follow iOS Human Interface Guidelines
- Native iOS form styling

### Android Specific
- Material Design components
- Android-style navigation
- Floating action buttons where appropriate

## 🔧 Technical Requirements

### Component Structure
```javascript
import React from 'react';
import { View, Text, TouchableOpacity, TextInput } from 'react-native';

const UizardLoginComponent = ({
  formData,
  onInputChange,
  onLogin,
  // ... other props
}) => {
  return (
    <View style={styles.container}>
      {/* Your UI code here */}
      <TextInput
        value={formData.email}
        onChangeText={(text) => onInputChange('email', text)}
        // ... other props
      />
      <TouchableOpacity onPress={onLogin}>
        <Text>Sign In</Text>
      </TouchableOpacity>
    </View>
  );
};

export default UizardLoginComponent;
```

### Required Imports
- React Native core components
- Vector icons (optional)
- Any animation libraries used

### Props Validation
Each component should handle:
- Missing props gracefully
- Loading states
- Error states
- Empty states

## ✅ Integration Checklist

For each component:
- [ ] All required props implemented
- [ ] Loading states handled
- [ ] Error states displayed
- [ ] Form validation styling
- [ ] Accessibility labels added
- [ ] iOS and Android tested
- [ ] Responsive design verified
- [ ] Animation states smooth

## 🚀 Next Steps

1. **Create components in Uizard** following these specifications
2. **Export as React Native components**
3. **Place in** `src/components/uizard/` directory
4. **Test integration** with existing containers
5. **Iterate on design** based on user feedback

## 📞 Questions?

If you need clarification on any component requirements or props, please ask! The container components are already implemented and waiting for your beautiful UI designs.

---

**Let's build something amazing together!** 🚀✨