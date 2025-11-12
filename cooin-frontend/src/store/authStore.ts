import { create } from 'zustand';
import { User } from '../types/api';
import { authService } from '../services/authService';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  isInitializing: boolean; // Separate flag for initial auth check
  error: string | null;

  // Actions
  login: (email: string, password: string, rememberMe?: boolean) => Promise<void>;
  register: (email: string, username: string, password: string, confirmPassword: string, role: 'lender' | 'borrower' | 'both', agreeToTerms: boolean) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  clearError: () => void;
  updateUser: (userData: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  isInitializing: true, // Start as true for initial auth check
  error: null,

  login: async (email: string, password: string, rememberMe = false) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authService.login({
        email,
        password,
        remember_me: rememberMe,
      });

      set({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.detail || 'Login failed',
        isAuthenticated: false,
        user: null,
      });
      throw error;
    }
  },

  register: async (email: string, username: string, password: string, confirmPassword: string, role: 'lender' | 'borrower' | 'both', agreeToTerms: boolean) => {
    console.log('[authStore] Starting registration...');
    set({ isLoading: true, error: null, isAuthenticated: false, user: null });
    try {
      const response = await authService.register({
        email,
        username,
        password,
        confirm_password: confirmPassword,
        role,
        agree_to_terms: agreeToTerms,
      });

      console.log('[authStore] Registration response received:', { hasUser: !!response.user, hasToken: !!response.access_token });

      // Only set authenticated if we have a valid user and tokens
      if (response.user && response.access_token) {
        console.log('[authStore] Setting user as authenticated');
        set({
          user: response.user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
      } else {
        // Registration response incomplete
        console.error('[authStore] Invalid registration response - missing user or token');
        throw new Error('Invalid registration response');
      }
    } catch (error: any) {
      // Make sure we DON'T authenticate on error
      console.error('[authStore] Registration error:', error);
      console.log('[authStore] Setting isAuthenticated to FALSE due to error');
      set({
        isLoading: false,
        error: error.detail || error.message || 'Registration failed',
        isAuthenticated: false,
        user: null,
      });
      // Re-throw error so RegisterScreen can catch it
      throw error;
    }
  },

  logout: async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.warn('Logout error:', error);
    } finally {
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    }
  },

  checkAuth: async () => {
    set({ isInitializing: true });
    try {
      const isAuthenticated = await authService.isAuthenticated();
      if (isAuthenticated) {
        const user = await authService.getCurrentUser();
        set({
          user,
          isAuthenticated: !!user,
          isInitializing: false,
        });
      } else {
        set({
          user: null,
          isAuthenticated: false,
          isInitializing: false,
        });
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      set({
        user: null,
        isAuthenticated: false,
        isInitializing: false,
      });
    }
  },

  clearError: () => {
    set({ error: null });
  },

  updateUser: (userData: Partial<User>) => {
    const currentUser = get().user;
    if (currentUser) {
      set({
        user: { ...currentUser, ...userData },
      });
    }
  },
}));