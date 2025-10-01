# 🎨 Uizard Design Prompt for Cooin Mobile App

## 🎯 Design Brief

Create a **luxury yet fresh** mobile app interface for Cooin, a premium peer-to-peer lending platform that connects trusted lenders and borrowers. The design should convey **financial sophistication, trust, and modern elegance** while maintaining accessibility and user-friendliness.

---

## 🎨 Visual Style & Brand Identity

### **Design Philosophy**
- **Luxury Financial Services**: Think premium banking apps like Chase Private Client, Goldman Sachs, or Revolut Premium
- **Fresh & Modern**: Clean, minimalist interface with subtle premium touches
- **Trust & Security**: Professional appearance that inspires confidence in financial transactions
- **Human Connection**: Warm, approachable elements that emphasize the community aspect

### **Color Palette**

#### **Primary Colors**
- **Ocean Blue**: `#2E86AB` - Main brand color (trust, stability, finance)
- **Success Green**: `#10B981` - Confirmations, success states, positive actions
- **Emerald Accent**: `#059669` - Lender role indicator, premium highlights

#### **Secondary Colors**
- **Purple Pink**: `#A23B72` - Premium accents, special features
- **Warm Orange**: `#F18F01` - Call-to-action highlights, energy
- **Deep Purple**: `#7C3AED` - "Both" role indicator, premium features

#### **Role-Specific Colors**
- **Lender Green**: `#059669` - For lender-specific UI elements
- **Borrower Red**: `#DC2626` - For borrower-specific UI elements
- **Both Purple**: `#7C3AED` - For users who both lend and borrow

#### **Neutral Palette**
- **Premium White**: `#FFFFFF` - Clean backgrounds
- **Light Gray**: `#F8F9FA` - Secondary backgrounds
- **Medium Gray**: `#6C757D` - Secondary text
- **Dark Gray**: `#212529` - Primary text
- **Success**: `#10B981` - Positive states
- **Warning**: `#F59E0B` - Caution states
- **Error**: `#EF4444` - Error states

---

## 📱 Design Components to Create

### **1. UizardWelcomeComponent - App Landing Screen**

**Purpose**: First impression - premium onboarding experience

**Design Requirements**:
- **Hero Section**:
  - Elegant Cooin logo with premium typography
  - Tagline: "Connect with Trusted Financial Partners"
  - Subtle gradient background (ocean blue to light)
  - Minimalist illustration of people connecting (line art style)

- **Feature Highlights**:
  - 3 key benefits with icons:
    - 🛡️ "Bank-Level Security"
    - 🤝 "Trusted Community"
    - 💰 "Fair Rates"
  - Clean card-based layout with subtle shadows

- **Action Buttons**:
  - **Primary**: "Get Started" (Ocean Blue, prominent)
  - **Secondary**: "Already a member? Sign In" (text link)

**Luxury Elements**:
- Subtle geometric patterns in background
- Premium typography (clean, modern sans-serif)
- Generous white space
- Soft drop shadows on cards
- Smooth gradient overlays

---

### **2. UizardLoginComponent - Sign In Form**

**Purpose**: Secure, premium login experience

**Design Requirements**:
- **Header**:
  - "Welcome Back" with elegant typography
  - Subtle Cooin logo/wordmark

- **Form Fields**:
  - **Email**: Clean input with floating labels
  - **Password**: Show/hide toggle with eye icon
  - **Remember Me**: Premium checkbox design
  - Validation states: green border (valid), red border (error)

- **Actions**:
  - **Primary Button**: "Sign In" (Ocean Blue, full width)
  - **Links**: "Forgot Password?" | "Don't have an account? Sign Up"
  - Loading state with elegant spinner

- **Trust Elements**:
  - Small security badge/icon
  - "256-bit encryption" text

**Luxury Elements**:
- Floating labels with smooth animations
- Subtle input field shadows
- Premium button with hover states
- Clean error message styling
- Biometric login icon (fingerprint/face)

---

### **3. UizardRegisterComponent - Account Creation**

**Purpose**: Premium onboarding with role selection

**Design Requirements**:
- **Header**:
  - "Join Cooin" with welcoming copy
  - Progress indicator if multi-step

- **Form Fields**:
  - Email, Username, Password, Confirm Password
  - **Password Strength**: Visual indicator (weak=red, fair=orange, strong=green)
  - Real-time validation with green checkmarks

- **Role Selection** (Premium Card Design):
  - **Lender Card**:
    - Green accent color (#059669)
    - Icon: Giving hand or arrow up
    - "I want to lend money to others"
    - Benefits: "Earn competitive returns"

  - **Borrower Card**:
    - Red accent color (#DC2626)
    - Icon: Receiving hand or arrow down
    - "I need to borrow money"
    - Benefits: "Access fair rate loans"

  - **Both Card**:
    - Purple accent color (#7C3AED)
    - Icon: Two-way arrows or balance scale
    - "I want to both lend and borrow"
    - Benefits: "Maximum flexibility"

- **Trust Elements**:
  - "I agree to Terms & Conditions" with elegant checkbox
  - Security badges
  - "Your data is encrypted and secure"

**Luxury Elements**:
- Premium card selection with subtle animations
- Elegant role icons (line art style)
- Smooth transitions between states
- Premium typography hierarchy
- Sophisticated color coding for roles

---

## 🎨 Visual Design Guidelines

### **Typography**
- **Headers**: Bold, modern sans-serif (like SF Pro Display, Inter, or similar)
- **Body Text**: Clean, readable (like SF Pro Text, Inter Regular)
- **Hierarchy**: Clear size differentiation (24px → 18px → 16px → 14px)
- **Color**: Dark gray (#212529) for primary, medium gray (#6C757D) for secondary

### **Spacing & Layout**
- **Margins**: 32px horizontal padding on mobile
- **Component Spacing**: 24px between major sections
- **Input Spacing**: 16px between form fields
- **Card Padding**: 20px internal padding
- **Button Height**: 56px (comfortable touch target)

### **Shadows & Elevation**
- **Cards**: Subtle shadow (0px 2px 8px rgba(0,0,0,0.1))
- **Buttons**: Light shadow (0px 1px 3px rgba(0,0,0,0.2))
- **Floating Elements**: Medium shadow (0px 4px 12px rgba(0,0,0,0.15))

### **Icons & Graphics**
- **Style**: Line art or minimalist filled icons
- **Size**: 24px for standard icons, 32px for feature icons
- **Color**: Match the context (green for success, blue for primary actions)

### **Buttons & Interactive Elements**
- **Primary Button**: Ocean Blue background, white text, rounded corners (8px)
- **Secondary Button**: White background, Ocean Blue border and text
- **Hover States**: Subtle darken effect (10% opacity overlay)
- **Disabled State**: Gray background (#ADB5BD)

---

## 📱 Platform Considerations

### **iOS Design Elements**
- Use iOS-style navigation patterns
- Follow Human Interface Guidelines for spacing
- Implement iOS-style form validation
- Use appropriate iOS icons and patterns

### **Android Design Elements**
- Material Design 3 influences
- Floating Action Buttons where appropriate
- Android-style navigation
- Material Design elevation and shadows

---

## 🎯 Key Success Metrics

Your designs should achieve:
1. **Trust**: Users feel confident about financial security
2. **Clarity**: Clear understanding of lender vs borrower roles
3. **Premium Feel**: App feels sophisticated and professional
4. **Accessibility**: Easy to read and navigate for all users
5. **Modern**: Feels current and technologically advanced

---

## 🚀 Technical Requirements for Export

When exporting from Uizard:

### **React Native Components Needed**:
```javascript
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator
} from 'react-native';
```

### **Props to Include** (EXACTLY as specified):

**UizardWelcomeComponent**:
```javascript
{
  onGetStarted: () => void,
  onSignIn: () => void
}
```

**UizardLoginComponent**:
```javascript
{
  formData: { email: string, password: string, rememberMe: boolean },
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

**UizardRegisterComponent**:
```javascript
{
  formData: { email, username, password, confirmPassword, role, agreeToTerms },
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

---

## 💎 Luxury Design Inspiration

Think of these premium apps for inspiration:
- **Revolut Premium**: Clean, modern, trustworthy
- **Goldman Sachs Marcus**: Sophisticated, minimal
- **Chase Private Client**: Professional, premium
- **Stripe Dashboard**: Clean, functional, beautiful
- **Coinbase Pro**: Modern fintech aesthetic

---

## 🎨 Final Design Checklist

✅ **Brand Colors**: Ocean blue primary, green accents, luxury feel
✅ **Typography**: Clear hierarchy, premium fonts
✅ **Role Differentiation**: Clear lender (green) vs borrower (red) vs both (purple)
✅ **Trust Elements**: Security badges, encryption mentions
✅ **Accessibility**: High contrast, readable text, proper touch targets
✅ **Luxury Feel**: Subtle shadows, generous spacing, premium interactions
✅ **Fresh Look**: Modern, clean, not cluttered
✅ **Mobile-First**: Optimized for mobile screen sizes

---

**Create these components with luxury and freshness in mind - users should feel like they're using a premium financial service that they can trust with their money!** 💰✨