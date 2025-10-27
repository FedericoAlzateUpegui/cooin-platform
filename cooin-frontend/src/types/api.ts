// API Types based on backend schemas

// User types
export interface User {
  id: number;
  email: string;
  username?: string;
  role: 'lender' | 'borrower' | 'both';
  status: 'active' | 'inactive' | 'suspended' | 'pending_verification';
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string;
}

// Auth types
export interface LoginRequest {
  email: string;
  password: string;
  remember_me?: boolean;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  confirm_password: string;
  role: 'lender' | 'borrower' | 'both';
  agree_to_terms: boolean;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

// Profile types
export interface UserProfile {
  id: number;
  user_id: number;
  first_name?: string;
  last_name?: string;
  display_name?: string;
  bio?: string;
  date_of_birth?: string;
  phone_number?: string;
  city?: string;
  state_province?: string;
  country?: string;
  profile_completion_percentage: number;
  is_public: boolean;
  identity_verified: boolean;
  credit_score?: number;
  annual_income?: number;
  employment_status?: string;
  created_at: string;
  updated_at: string;
}

export interface ProfileUpdateRequest {
  first_name?: string;
  last_name?: string;
  display_name?: string;
  bio?: string;
  date_of_birth?: string;
  phone_number?: string;
  city?: string;
  state_province?: string;
  country?: string;
  is_public?: boolean;
  credit_score?: number;
  annual_income?: number;
  employment_status?: string;
}

// Connection types
export interface Connection {
  id: number;
  requester_id: number;
  receiver_id: number;
  connection_type: 'lending_inquiry' | 'borrowing_request' | 'general_connection' | 'referral';
  status: 'pending' | 'accepted' | 'rejected' | 'blocked' | 'expired';
  message?: string;
  response_message?: string;
  loan_amount_requested?: number;
  loan_term_months?: number;
  interest_rate_proposed?: number;
  loan_purpose?: string;
  priority_level: number;
  is_mutual: boolean;
  message_count: number;
  days_since_created: number;
  is_expired: boolean;
  created_at: string;
  updated_at: string;
  responded_at?: string;
}

export interface ConnectionCreateRequest {
  receiver_id: number;
  connection_type?: 'lending_inquiry' | 'borrowing_request' | 'general_connection' | 'referral';
  message?: string;
  loan_amount_requested?: number;
  loan_term_months?: number;
  interest_rate_proposed?: number;
  loan_purpose?: string;
  priority_level?: number;
}

export interface ConnectionUpdateRequest {
  status?: 'pending' | 'accepted' | 'rejected' | 'blocked' | 'expired';
  response_message?: string;
  interest_rate_proposed?: number;
  requester_notes?: string;
  receiver_notes?: string;
}

// Matching types
export interface MatchingCriteria {
  user_role?: string;
  location?: string;
  min_loan_amount?: number;
  max_loan_amount?: number;
  loan_purpose?: string;
  max_interest_rate?: number;
  min_loan_term?: number;
  max_loan_term?: number;
  income_range?: string;
  credit_score_min?: number;
  verified_only?: boolean;
}

export interface MatchingResult {
  user_id: number;
  compatibility_score: number;
  match_reasons: string[];
  public_name: string;
  location_string: string;
  profile_completion_percentage: number;
  is_verified: boolean;
  loan_amount_range?: string;
  interest_rate_range?: string;
  loan_terms?: string;
}

export interface MatchingResponse {
  matches: MatchingResult[];
  total_matches: number;
  search_criteria: MatchingCriteria;
  search_time_ms: number;
}

// Message types
export interface Message {
  id: number;
  connection_id: number;
  sender_id: number;
  receiver_id: number;
  content: string;
  message_type: string;
  is_read: boolean;
  is_deleted: boolean;
  attachment_url?: string;
  attachment_filename?: string;
  attachment_size?: number;
  created_at: string;
  updated_at: string;
  read_at?: string;
}

export interface MessageCreateRequest {
  content: string;
  message_type?: string;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}

export interface PaginatedResponse<T> {
  data: T[];
  total_count: number;
  page: number;
  page_size: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface ApiError {
  detail: string;
  status_code: number;
}