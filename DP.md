# Documentation Process Guide

**Purpose**: Maintain clean, up-to-date documentation for the Cooin project.

---

## 🖥️ MULTI-MACHINE DOCUMENTATION (CRITICAL!)

**This project is developed on TWO computers simultaneously:**
- 💻 **Windows** - Primary development machine
- 🍎 **Mac** - Secondary development machine

### 🚨 Machine-Specific Files

#### Windows Files (Windows ✍️ WRITES, Mac 👀 READS)
- `HISTORY.md`, `TODO.md`, `README.md`, `HOW-TO-LAUNCH-WEB-APP.md`

#### Mac Files (Mac ✍️ WRITES, Windows 👀 READS)
- `HISTORY_MAC.md`, `TODO_MAC.md`, `README_MAC.md`, `HOW-TO-LAUNCH-WEB-APP_MAC.md`

#### Shared Files (Both machines can read/edit carefully)
- `DP.md` - This documentation process guide
- `TECH_STACK.md` - Technology stack documentation
- Code files in `cooin-backend/`, `cooin-frontend/`, `cooin-ios/`

### 📝 Claude's Workflow

**EVERY session, Claude MUST:**
1. **Ask the user**: "¿Estás en Mac o Windows?"
   - If Mac 🍎 → Document in `*_MAC.md` files
   - If Windows 💻 → Document in regular files
2. **Never edit the other machine's files**

### 🔄 Sync Strategy
```bash
# Before starting work
git pull origin main

# After finishing work (Mac)
git add HISTORY_MAC.md TODO_MAC.md README_MAC.md
git commit -m "docs: Session X on Mac 🍎"
git push origin main

# After finishing work (Windows)
git add HISTORY.md TODO.md README.md
git commit -m "docs: Session X on Windows 💻"
git push origin main
```

---

## 📋 Documentation Files Overview

| File | Purpose | When to Read |
|------|---------|--------------|
| **README** | Project setup & overview | First time, setup changes |
| **TODO** | Current tasks & status | START of every session |
| **HISTORY** | Session changelog | When debugging, reviewing changes |
| **HOW-TO-LAUNCH** | Launch instructions | First launch, troubleshooting |
| **DP** | Documentation process | When unsure how to document |
| **TECH_STACK** | Technology details | When stack changes |

---

## 🔄 Standard Documentation Flow

### At START of Each Session
1. **Review TODO.md** - Check pending tasks
2. **Note Session Number** - Increment from last session (check HISTORY.md)

### DURING the Session
- Track files modified
- Note bugs fixed and features added

### At END of Each Session

#### 1. Update HISTORY.md (5 minutes)
```markdown
## YYYY-MM-DD (Session X) - Brief Title

**Goal**: One-sentence objective.

**Changes/Fixes**:
1. **Feature/Fix**: Description
2. **Another Change**: Description

**Files Changed**:
- `filename:line` - What changed

**Status**: ✅ Working / ⚠️ Blocked / 🔄 In Progress

---
```

#### 2. Update TODO.md (3 minutes)
- Update session header
- Move completed items to "✅ Completed This Session"
- Update "In Progress" section
- Add new tasks if discovered
- Update timestamp

#### 3. Update README.md (Only if needed)
- ✅ New major feature, setup changes, stack changes
- ❌ Don't update for minor fixes/refactors

#### 4. Update HOW-TO-LAUNCH.md (Only if needed)
- Update if: Launch commands changed, new steps, URL changes

---

## 📝 Writing Style Guide

### General Rules
1. **Be Concise**: 1-2 sentences per point
2. **Use Active Voice**: "Fixed bug" not "Bug was fixed"
3. **Include Context**: Why it matters, not just what changed
4. **Add Links**: Reference `file:line` for specific changes

### Emoji Guide
| Emoji | Meaning | Usage |
|-------|---------|-------|
| ✅ | Completed | Finished tasks, working features |
| ❌ | Failed/Broken | Things that don't work |
| ⚠️ | Warning | Known issues, be careful |
| 🔄 | In Progress | Currently working on |
| 🐛 | Bug | Bug fixes, issues |
| ✨ | New Feature | New functionality added |
| 🔧 | Configuration | Config changes, setup updates |
| 📝 | Documentation | Doc updates |

---

## 🎯 Quick Reference: Which File When?

| Situation | File to Read | Section |
|-----------|-------------|---------|
| Starting work today | TODO.md | Current Session → In Progress |
| Need to launch app | HOW-TO-LAUNCH.md | Quick Launch |
| App won't start | HOW-TO-LAUNCH.md | Troubleshooting |
| What changed recently? | HISTORY.md | Top 3 sessions |
| What are known bugs? | TODO.md | Known Issues |
| Project overview? | README.md | Entire file |

---

## 🚫 Common Mistakes to Avoid

1. **Over-documenting**: Keep it scannable
2. **Under-documenting**: Even small changes matter
3. **Inconsistent Formats**: Use the templates
4. **Missing Context**: Explain WHY, not just WHAT
5. **Stale TODOs**: Remove or archive old items
6. **Wrong Dates**: Use YYYY-MM-DD format
7. **Missing File References**: Always cite which files changed

---

## 🎯 Quick Action Commands

**Start New Session:**
```bash
# Check current session number
grep "Session" HISTORY.md | head -1

# Review pending tasks
grep "\[ \]" TODO.md | head -10
```

**End Session:**
```bash
# Commit docs
git add HISTORY.md TODO.md README.md
git commit -m "docs: update session X documentation"
```

---

**Last Updated**: 2025-12-06 (Session 18 - Mac 🍎)
## 🌙 Dark Mode Implementation Guide

**Completed**: 2025-11-25 (Windows 💻)

### Overview

Dark mode has been successfully implemented across the entire Cooin webapp. The theme toggle in Settings screen now controls app-wide appearance, including all screens and navigation components.

### Architecture

**Core Components:**
- **Theme Store**: `src/store/themeStore.ts` (Zustand) - Global theme state management
- **Colors Hook**: `src/hooks/useColors.ts` - Provides dynamic colors based on current theme
- **Settings Toggle**: Theme toggle in Settings screen controls app-wide dark mode

### Screens with Dark Mode Support

All screens now use dynamic styling:

**Main Screens:**
- ✅ HomeScreen
- ✅ TicketsScreen
- ✅ MatchingScreen
- ✅ ConnectionsScreen
- ✅ NotificationsScreen
- ✅ SettingsScreen

**Profile Screens:**
- ✅ ProfileSetupScreen
- ✅ EditProfileScreen

**Settings Screens:**
- ✅ PrivacySettingsScreen

**Auth Screens:**
- ✅ LoginScreen
- ✅ RegisterScreen

**Navigation Components:**
- ✅ Desktop Sidebar (AppNavigator - DesktopSidebarNavigator)
- ✅ Mobile Bottom Tabs (AppNavigator - MobileTabNavigator)
- ✅ Loading Screen

### Implementation Pattern

**Standard Pattern for Screen Components:**

```typescript
import { useColors } from '../../hooks/useColors';

export const YourScreen: React.FC<Props> = ({ navigation }) => {
  // 1. Add useColors hook at the top of the component
  const colors = useColors();

  // 2. Create styles immediately after
  const styles = createStyles(colors);

  // ... rest of component logic

  return (
    <View style={styles.container}>
      {/* Your UI */}
    </View>
  );
};

// 3. Convert StyleSheet to a function that accepts colors
const createStyles = (colors: ReturnType<typeof useColors>) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,  // Use dynamic colors
  },
  text: {
    color: colors.text,
  },
  surface: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
  },
  // ... more styles
});
```

**Key Steps:**
1. Import `useColors` hook
2. Call `const colors = useColors()` at the top of component
3. Call `const styles = createStyles(colors)` immediately after
4. Convert `const styles = StyleSheet.create` to `const createStyles = (colors: ReturnType<typeof useColors>) => StyleSheet.create`
5. Replace all `COLORS.xxx` with `colors.xxx` inside the styles
6. **CRITICAL**: Only call `const styles = createStyles(colors)` ONCE at the top of the component

### Common Pitfalls & Solutions

#### Problem 1: "Cannot access 'styles' before initialization"

**Cause**: Multiple `const styles = createStyles(colors)` declarations in the same component

**Solution**: Only declare styles ONCE at the top of the component (right after `const colors = useColors()`)

```typescript
// ❌ WRONG - Multiple declarations
export const MyScreen = () => {
  const colors = useColors();

  if (loading) {
    const styles = createStyles(colors);  // ❌ Don't do this
    return <LoadingView style={styles.container} />;
  }

  const styles = createStyles(colors);  // ❌ Duplicate
  return <MainView style={styles.container} />;
};

// ✅ CORRECT - Single declaration at top
export const MyScreen = () => {
  const colors = useColors();
  const styles = createStyles(colors);  // ✅ Only once, at top

  if (loading) {
    return <LoadingView style={styles.container} />;
  }

  return <MainView style={styles.container} />;
};
```

#### Problem 2: "ReferenceError: colors is not defined"

**Cause**: Using `colors` in static StyleSheet.create without converting to function

**Solution**: Convert to `createStyles` function with proper typing

```typescript
// ❌ WRONG - Static StyleSheet
const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.background,  // ❌ colors not defined
  },
});

// ✅ CORRECT - Function with colors parameter
const createStyles = (colors: ReturnType<typeof useColors>) => StyleSheet.create({
  container: {
    backgroundColor: colors.background,  // ✅ colors from parameter
  },
});
```

#### Problem 3: Variable Shadowing

**Cause**: Local variables named `colors` conflict with component-level colors

**Solution**: Rename local variables to avoid shadowing

```typescript
// ❌ WRONG - Shadowing
const MyScreen = () => {
  const colors = useColors();

  const getColor = (type: string) => {
    const colors: { [key: string]: string } = {  // ❌ Shadows component colors
      error: colors.error,  // Which colors? Confusing!
    };
    return colors[type];
  };
};

// ✅ CORRECT - No shadowing
const MyScreen = () => {
  const colors = useColors();

  const getColor = (type: string) => {
    const typeColors: { [key: string]: string } = {  // ✅ Different name
      error: colors.error,  // ✅ Clear reference
    };
    return typeColors[type];
  };
};
```

### Metro Bundler Cache Issues

**Symptoms**: Errors persist for code that's already been fixed

**Solution**:
```bash
# 1. Clear cache directories
rm -rf .expo
rm -rf node_modules/.cache

# 2. Kill Metro processes
# Windows: Find and kill process on port
# Unix: killall node

# 3. Restart with clear flag
npm start -- --clear
```

### Available Color Tokens

From `useColors()` hook:
```typescript
{
  background: string;      // Main background
  surface: string;         // Cards, panels
  text: string;           // Primary text
  textSecondary: string;  // Secondary text
  primary: string;        // Primary brand color
  accent: string;         // Accent color
  border: string;         // Borders
  success: string;        // Success states
  error: string;          // Error states
  warning: string;        // Warning states
  info: string;           // Info states
}
```

### Testing Checklist

When adding dark mode to a new screen:

- [ ] Add `useColors()` hook at component top
- [ ] Add `const styles = createStyles(colors)` immediately after
- [ ] Convert StyleSheet.create to createStyles function
- [ ] Replace all COLORS references with colors parameter
- [ ] Test theme toggle in Settings screen
- [ ] Verify all UI elements update colors correctly
- [ ] Check both light and dark modes for readability
- [ ] Test on both mobile and desktop viewports
- [ ] Clear Metro cache if seeing stale errors

### Automation Scripts

**Created for bulk updates:**
- `update-dark-mode.py` - Initial automation script
- `fix-styles.py` - Duplicate styles cleanup script

Both scripts are in the project root directory.

### Files Modified

**Navigation:**
- `src/navigation/AppNavigator.tsx`

**Main Screens:**
- `src/screens/home/HomeScreen.tsx`
- `src/screens/tickets/TicketsScreen.tsx`
- `src/screens/matching/MatchingScreen.tsx`
- `src/screens/connections/ConnectionsScreen.tsx`
- `src/screens/notifications/NotificationsScreen.tsx`
- `src/screens/settings/SettingsScreen.tsx`

**Profile Screens:**
- `src/screens/profile/ProfileSetupScreen.tsx`
- `src/screens/profile/EditProfileScreen.tsx`

**Settings Screens:**
- `src/screens/settings/PrivacySettingsScreen.tsx`

**Auth Screens:**
- `src/screens/auth/LoginScreen.tsx`
- `src/screens/auth/RegisterScreen.tsx`

### Git Commit Reference

```bash
git add .
git commit -m "feat: Implement dark mode across entire app

- Added dark mode support to all screens and navigation components
- Updated desktop sidebar and mobile tabs to use dynamic colors
- Converted all screens from static COLORS to dynamic useColors() hook
- Fixed duplicate style declarations and variable shadowing issues
- Created automation scripts for bulk updates
- Documented dark mode implementation pattern in DP.md

Theme toggle in Settings now controls app-wide theme consistently."
```

### Known Issues

None currently. All screens and navigation components support dark mode successfully.

### Next Steps for Dark Mode

1. **Accessibility**: Verify color contrast meets WCAG standards in both themes
2. **Animations**: Add smooth transitions when switching themes
3. **Persistence**: Consider saving theme preference to AsyncStorage
4. **System Preference**: Optionally detect OS-level dark mode preference

---

**Last Updated**: 2025-11-25 (Windows 💻 - Dark Mode Complete)
**Maintained By**: Development Team (Mac & Windows)

---

## 🎯 Quick Reference: Mac vs Windows

**If you're on Mac 🍎:**
- Edit: `HISTORY_MAC.md`, `TODO_MAC.md`, `README_MAC.md`, `HOW-TO-LAUNCH-WEB-APP_MAC.md`
- Read: All Windows files for context

**If you're on Windows 💻:**
- Edit: `HISTORY.md`, `TODO.md`, `README.md`, `HOW-TO-LAUNCH-WEB-APP.md`
- Read: All Mac files for context

**Claude MUST ask every session:** "¿Estás en Mac o Windows?"

---

## 🌐 Cloudflare-First Testing Policy

**IMPORTANT**: Always use Cloudflare tunnels for web app testing, never `localhost`.

### Why Cloudflare-First?

1. **Real-World Conditions**: Tests CORS, security headers, and production-like environment
2. **Team Collaboration**: Partners can test simultaneously from their devices
3. **Catch Issues Early**: Production-like setup prevents surprises during deployment
4. **Mobile Testing**: Easily test on physical devices without network configuration

### Testing Workflow

**Every Development Session:**

1. Start backend with Cloudflare tunnel: `cloudflared tunnel --url http://localhost:8000`
2. Start frontend normally: `npx expo start --web --port 8083`
3. Update frontend `.env` with Cloudflare backend URL
4. Test through frontend URL (usually `http://localhost:8083`)
5. Verify all API calls go through Cloudflare tunnel

**Configuration:**
```bash
# Backend: Always exposed via Cloudflare
cloudflared tunnel --url http://localhost:8000
# → https://random-subdomain.trycloudflare.com

# Frontend .env: Point to Cloudflare URL
EXPO_PUBLIC_API_URL=https://random-subdomain.trycloudflare.com/api/v1
```

**Benefits:**
- ✅ Tests production CORS configuration
- ✅ Validates security middleware with real IPs
- ✅ Ensures rate limiting works correctly
- ✅ Catches DNS/networking issues early
- ✅ Enables team collaboration without VPN

**Only Use localhost When:**
- Debugging specific backend issues that require direct access
- Testing without internet connection
- Profiling performance without network overhead

---
