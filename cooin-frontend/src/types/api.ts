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
  source_ticket_id?: number;
  proposed_amount?: number;
  proposed_interest_rate?: number;
  proposed_term_months?: number;
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

// Ticket types
export interface Ticket {
  id: number;
  user_id: number;
  ticket_type: 'lending_offer' | 'borrowing_request';
  status: 'active' | 'paused' | 'completed' | 'cancelled' | 'expired';
  title: string;
  description: string;
  amount?: number;
  min_amount?: number;
  max_amount?: number;
  interest_rate?: number;
  min_interest_rate?: number;
  max_interest_rate?: number;
  term_months?: number;
  min_term_months?: number;
  max_term_months?: number;
  loan_type: 'personal' | 'business' | 'education' | 'home_improvement' | 'debt_consolidation' | 'other';
  loan_purpose: string;
  warranty_type: 'none' | 'property' | 'vehicle' | 'savings' | 'investments' | 'other';
  warranty_description?: string;
  warranty_value?: number;
  requirements?: string;
  preferred_location?: string;
  flexible_terms: boolean;
  is_public: boolean;
  expires_at?: string;
  views_count: number;
  responses_count: number;
  deals_created: number;
  created_at: string;
  updated_at: string;
  last_viewed_at?: string;
  is_active: boolean;
  is_expired: boolean;
  days_active: number;
  is_lending_offer: boolean;
  is_borrowing_request: boolean;
  has_warranty: boolean;
}

export interface TicketCreateRequest {
  ticket_type: 'lending_offer' | 'borrowing_request';
  title: string;
  description: string;
  amount?: number;
  min_amount?: number;
  max_amount?: number;
  interest_rate?: number;
  min_interest_rate?: number;
  max_interest_rate?: number;
  term_months?: number;
  min_term_months?: number;
  max_term_months?: number;
  loan_type: 'personal' | 'business' | 'education' | 'home_improvement' | 'debt_consolidation' | 'other';
  loan_purpose: string;
  warranty_type?: 'none' | 'property' | 'vehicle' | 'savings' | 'investments' | 'other';
  warranty_description?: string;
  warranty_value?: number;
  requirements?: string;
  preferred_location?: string;
  flexible_terms?: boolean;
  is_public?: boolean;
  expires_at?: string;
}

export interface TicketUpdateRequest {
  title?: string;
  description?: string;
  status?: 'active' | 'paused' | 'completed' | 'cancelled';
  amount?: number;
  min_amount?: number;
  max_amount?: number;
  interest_rate?: number;
  min_interest_rate?: number;
  max_interest_rate?: number;
  term_months?: number;
  min_term_months?: number;
  max_term_months?: number;
  loan_purpose?: string;
  warranty_description?: string;
  warranty_value?: number;
  requirements?: string;
  preferred_location?: string;
  flexible_terms?: boolean;
  is_public?: boolean;
  expires_at?: string;
}

export interface TicketFilterParams {
  ticket_type?: 'lending_offer' | 'borrowing_request';
  status?: 'active' | 'paused' | 'completed' | 'cancelled' | 'expired';
  loan_type?: 'personal' | 'business' | 'education' | 'home_improvement' | 'debt_consolidation' | 'other';
  warranty_type?: 'none' | 'property' | 'vehicle' | 'savings' | 'investments' | 'other';
  min_amount?: number;
  max_amount?: number;
  min_interest_rate?: number;
  max_interest_rate?: number;
  min_term_months?: number;
  max_term_months?: number;
  location?: string;
  flexible_terms_only?: boolean;
  sort_by?: 'created_at' | 'amount' | 'interest_rate' | 'views_count';
  sort_order?: 'asc' | 'desc';
  page?: number;
  page_size?: number;
}

export interface CreateDealFromTicketRequest {
  ticket_id: number;
  message?: string;
  proposed_amount?: number;
  proposed_interest_rate?: number;
  proposed_term_months?: number;
}