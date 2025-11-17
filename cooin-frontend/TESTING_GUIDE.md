# Testing Guide for Cooin Frontend

Complete guide for testing the Cooin React Native application.

---

## 📦 Testing Stack

- **Jest**: Testing framework
- **React Native Testing Library**: Component testing
- **Jest Expo**: Expo-specific Jest preset

---

## 🚀 Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run specific test file
npm test -- RegisterScreen.test.tsx
```

---

## 📝 Test Examples

### Example 1: Component Unit Test

Create: `src/components/__tests__/Button.test.tsx`

```typescript
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { Button } from '../Button';

describe('Button Component', () => {
  it('renders correctly with title', () => {
    const { getByText } = render(<Button title="Click Me" onPress={() => {}} />);
    expect(getByText('Click Me')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPressMock = jest.fn();
    const { getByText } = render(<Button title="Click Me" onPress={onPressMock} />);

    fireEvent.press(getByText('Click Me'));
    expect(onPressMock).toHaveBeenCalledTimes(1);
  });

  it('shows loading indicator when loading', () => {
    const { getByTestId } = render(
      <Button title="Submit" onPress={() => {}} loading />
    );

    expect(getByTestId('activity-indicator')).toBeTruthy();
  });

  it('is disabled when disabled prop is true', () => {
    const onPressMock = jest.fn();
    const { getByText } = render(
      <Button title="Click Me" onPress={onPressMock} disabled />
    );

    fireEvent.press(getByText('Click Me'));
    expect(onPressMock).not.toHaveBeenCalled();
  });
});
```

### Example 2: Form Validation Test

Create: `src/screens/auth/__tests__/RegisterScreen.test.tsx`

```typescript
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { RegisterScreen } from '../RegisterScreen';
import { authService } from '../../../services/authService';

// Mock the auth service
jest.mock('../../../services/authService');

// Mock the language context
jest.mock('../../../contexts/LanguageContext', () => ({
  useLanguage: () => ({
    t: (key: string) => key,
    currentLanguage: 'en',
    changeLanguage: jest.fn(),
  }),
}));

describe('RegisterScreen - Form Validation', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('shows validation error for invalid email', async () => {
    const { getByPlaceholderText, getByText, findByText } = render(
      <RegisterScreen navigation={{} as any} />
    );

    const emailInput = getByPlaceholderText(/email/i);
    const submitButton = getByText(/register/i);

    fireEvent.changeText(emailInput, 'invalid-email');
    fireEvent.press(submitButton);

    const errorMessage = await findByText(/valid email/i);
    expect(errorMessage).toBeTruthy();
  });

  it('shows validation error for short password', async () => {
    const { getByPlaceholderText, getByText, findByText } = render(
      <RegisterScreen navigation={{} as any} />
    );

    const passwordInput = getByPlaceholderText(/password/i);
    const submitButton = getByText(/register/i);

    fireEvent.changeText(passwordInput, '123');
    fireEvent.press(submitButton);

    const errorMessage = await findByText(/at least 8 characters/i);
    expect(errorMessage).toBeTruthy();
  });

  it('successfully submits with valid data', async () => {
    (authService.register as jest.Mock).mockResolvedValue({
      user: { id: 1, email: 'test@example.com' },
      access_token: 'fake-token',
    });

    const { getByPlaceholderText, getByText } = render(
      <RegisterScreen navigation={{} as any} />
    );

    fireEvent.changeText(getByPlaceholderText(/email/i), 'test@example.com');
    fireEvent.changeText(getByPlaceholderText(/password/i), 'password123');
    fireEvent.changeText(getByPlaceholderText(/confirm password/i), 'password123');

    fireEvent.press(getByText(/register/i));

    await waitFor(() => {
      expect(authService.register).toHaveBeenCalledWith(
        expect.objectContaining({
          email: 'test@example.com',
          password: 'password123',
        })
      );
    });
  });

  it('shows error message when registration fails', async () => {
    (authService.register as jest.Mock).mockRejectedValue({
      detail: 'Email already exists',
    });

    const { getByPlaceholderText, getByText, findByText } = render(
      <RegisterScreen navigation={{} as any} />
    );

    fireEvent.changeText(getByPlaceholderText(/email/i), 'existing@example.com');
    fireEvent.changeText(getByPlaceholderText(/password/i), 'password123');
    fireEvent.changeText(getByPlaceholderText(/confirm password/i), 'password123');

    fireEvent.press(getByText(/register/i));

    const errorMessage = await findByText(/email already exists/i);
    expect(errorMessage).toBeTruthy();
  });
});
```

### Example 3: Integration Test - Auth Flow

Create: `src/__tests__/integration/authFlow.test.tsx`

```typescript
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { NavigationContainer } from '@react-navigation/native';
import { AuthNavigator } from '../../navigation/AuthNavigator';
import { authService } from '../../services/authService';
import * as SecureStore from 'expo-secure-store';

jest.mock('../../services/authService');
jest.mock('expo-secure-store');

describe('Authentication Flow Integration Test', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('complete registration to login flow', async () => {
    (authService.register as jest.Mock).mockResolvedValue({
      user: { id: 1, email: 'newuser@example.com', role: 'lender' },
      access_token: 'fake-access-token',
      refresh_token: 'fake-refresh-token',
    });

    (SecureStore.setItemAsync as jest.Mock).mockResolvedValue(undefined);

    const { getByPlaceholderText, getByText, findByText } = render(
      <NavigationContainer>
        <AuthNavigator />
      </NavigationContainer>
    );

    // Fill registration form
    fireEvent.changeText(getByPlaceholderText(/email/i), 'newuser@example.com');
    fireEvent.changeText(getByPlaceholderText(/password/i), 'SecurePass123!');
    fireEvent.changeText(getByPlaceholderText(/confirm password/i), 'SecurePass123!');

    // Submit registration
    fireEvent.press(getByText(/register/i));

    // Wait for registration to complete
    await waitFor(() => {
      expect(authService.register).toHaveBeenCalled();
      expect(SecureStore.setItemAsync).toHaveBeenCalledWith(
        'access_token',
        'fake-access-token'
      );
    });

    // Verify navigation to next screen
    const welcomeText = await findByText(/welcome/i);
    expect(welcomeText).toBeTruthy();
  });

  it('handles network error gracefully', async () => {
    (authService.register as jest.Mock).mockRejectedValue(
      new Error('Network request failed')
    );

    const { getByPlaceholderText, getByText, findByText } = render(
      <NavigationContainer>
        <AuthNavigator />
      </NavigationContainer>
    );

    fireEvent.changeText(getByPlaceholderText(/email/i), 'test@example.com');
    fireEvent.changeText(getByPlaceholderText(/password/i), 'password123');
    fireEvent.changeText(getByPlaceholderText(/confirm password/i), 'password123');

    fireEvent.press(getByText(/register/i));

    const errorMessage = await findByText(/network request failed/i);
    expect(errorMessage).toBeTruthy();
  });
});
```

### Example 4: Service/API Test

Create: `src/services/__tests__/authService.test.ts`

```typescript
import { authService } from '../authService';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('AuthService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('register', () => {
    it('successfully registers a new user', async () => {
      const mockResponse = {
        data: {
          user: { id: 1, email: 'test@example.com', role: 'lender' },
          access_token: 'token123',
          refresh_token: 'refresh123',
        },
      };

      mockedAxios.post.mockResolvedValue(mockResponse);

      const result = await authService.register({
        email: 'test@example.com',
        password: 'password123',
        password_confirmation: 'password123',
        role: 'lender',
      });

      expect(result).toEqual(mockResponse.data);
      expect(mockedAxios.post).toHaveBeenCalledWith(
        '/auth/register',
        expect.objectContaining({
          email: 'test@example.com',
        })
      );
    });

    it('throws error when email already exists', async () => {
      mockedAxios.post.mockRejectedValue({
        response: {
          status: 400,
          data: { detail: 'Email already registered' },
        },
      });

      await expect(
        authService.register({
          email: 'existing@example.com',
          password: 'password123',
          password_confirmation: 'password123',
          role: 'lender',
        })
      ).rejects.toThrow();
    });
  });

  describe('login', () => {
    it('successfully logs in user', async () => {
      const mockResponse = {
        data: {
          user: { id: 1, email: 'test@example.com' },
          access_token: 'token123',
        },
      };

      mockedAxios.post.mockResolvedValue(mockResponse);

      const result = await authService.login({
        email: 'test@example.com',
        password: 'password123',
      });

      expect(result).toEqual(mockResponse.data);
    });

    it('throws error with invalid credentials', async () => {
      mockedAxios.post.mockRejectedValue({
        response: {
          status: 401,
          data: { detail: 'Invalid credentials' },
        },
      });

      await expect(
        authService.login({
          email: 'wrong@example.com',
          password: 'wrongpass',
        })
      ).rejects.toThrow();
    });
  });
});
```

### Example 5: Store/State Management Test

Create: `src/store/__tests__/authStore.test.ts`

```typescript
import { renderHook, act } from '@testing-library/react-hooks';
import { useAuthStore } from '../authStore';
import { authService } from '../../services/authService';
import * as SecureStore from 'expo-secure-store';

jest.mock('../../services/authService');
jest.mock('expo-secure-store');

describe('AuthStore', () => {
  beforeEach(() => {
    // Reset store state
    useAuthStore.setState({
      user: null,
      isAuthenticated: false,
      isInitializing: false,
    });
    jest.clearAllMocks();
  });

  it('initializes with default state', () => {
    const { result } = renderHook(() => useAuthStore());

    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.isInitializing).toBe(false);
  });

  it('successfully logs in and updates state', async () => {
    const mockUser = {
      id: 1,
      email: 'test@example.com',
      role: 'lender',
    };

    (authService.login as jest.Mock).mockResolvedValue({
      user: mockUser,
      access_token: 'token123',
    });

    (SecureStore.setItemAsync as jest.Mock).mockResolvedValue(undefined);

    const { result } = renderHook(() => useAuthStore());

    await act(async () => {
      await result.current.login('test@example.com', 'password123');
    });

    expect(result.current.user).toEqual(mockUser);
    expect(result.current.isAuthenticated).toBe(true);
    expect(SecureStore.setItemAsync).toHaveBeenCalledWith(
      'access_token',
      'token123'
    );
  });

  it('logs out and clears state', async () => {
    // Set initial authenticated state
    useAuthStore.setState({
      user: { id: 1, email: 'test@example.com', role: 'lender' },
      isAuthenticated: true,
    });

    (SecureStore.deleteItemAsync as jest.Mock).mockResolvedValue(undefined);

    const { result } = renderHook(() => useAuthStore());

    await act(async () => {
      await result.current.logout();
    });

    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
    expect(SecureStore.deleteItemAsync).toHaveBeenCalledWith('access_token');
  });
});
```

---

## 📊 Test Coverage Goals

Aim for the following coverage targets:

- **Statements**: > 80%
- **Branches**: > 75%
- **Functions**: > 80%
- **Lines**: > 80%

Run coverage report:
```bash
npm run test:coverage
```

---

## 🎯 Best Practices

### 1. AAA Pattern
```typescript
it('description', () => {
  // Arrange
  const { getByText } = render(<Component />);

  // Act
  fireEvent.press(getByText('Button'));

  // Assert
  expect(mockFunction).toHaveBeenCalled();
});
```

### 2. Use data-testid for complex queries
```tsx
<View testID="user-profile-container">
  {/* content */}
</View>
```

```typescript
const { getByTestId } = render(<Component />);
expect(getByTestId('user-profile-container')).toBeTruthy();
```

### 3. Mock external dependencies
```typescript
jest.mock('../../services/api');
jest.mock('@react-navigation/native');
```

### 4. Test user interactions, not implementation
```typescript
// ❌ Bad
expect(component.state.count).toBe(1);

// ✅ Good
expect(getByText('Count: 1')).toBeTruthy();
```

### 5. Use async utilities for async code
```typescript
await waitFor(() => {
  expect(getByText('Loaded')).toBeTruthy();
});
```

---

## 🔍 Common Testing Scenarios

### Testing Forms
```typescript
fireEvent.changeText(input, 'value');
fireEvent.press(submitButton);
await waitFor(() => expect(mockSubmit).toHaveBeenCalled());
```

### Testing Navigation
```typescript
const mockNavigate = jest.fn();
jest.mock('@react-navigation/native', () => ({
  useNavigation: () => ({ navigate: mockNavigate }),
}));

fireEvent.press(button);
expect(mockNavigate).toHaveBeenCalledWith('ScreenName');
```

### Testing API Calls
```typescript
jest.mock('axios');
mockedAxios.get.mockResolvedValue({ data: mockData });

await waitFor(() => {
  expect(getByText(mockData.title)).toBeTruthy();
});
```

### Testing Loading States
```typescript
const { getByTestId, queryByTestId } = render(<Component />);
expect(getByTestID('loading-indicator')).toBeTruthy();

await waitFor(() => {
  expect(queryByTestId('loading-indicator')).toBeNull();
});
```

---

## 🚨 Debugging Tests

### Enable verbose mode
```bash
npm test -- --verbose
```

### Run specific test
```bash
npm test -- --testNamePattern="should render correctly"
```

### Debug in VS Code
Add to `.vscode/launch.json`:
```json
{
  "type": "node",
  "request": "launch",
  "name": "Jest Debug",
  "program": "${workspaceFolder}/node_modules/.bin/jest",
  "args": ["--runInBand"],
  "console": "integratedTerminal",
  "internalConsoleOptions": "neverOpen"
}
```

---

## 📦 Continuous Integration

Add to your CI/CD pipeline:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v2
```

---

## 🔗 Resources

- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [React Native Testing Library](https://callstack.github.io/react-native-testing-library/)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

---

**Last Updated**: 2025-11-17 (Session 14)
