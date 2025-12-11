import { apiClient } from './api';
import {
  Ticket,
  TicketCreateRequest,
  TicketUpdateRequest,
  TicketFilterParams,
  CreateDealFromTicketRequest,
  PaginatedResponse,
  Connection
} from '../types/api';

class TicketService {
  /**
   * Get all tickets with optional filtering and pagination
   */
  async getTickets(filters?: TicketFilterParams): Promise<PaginatedResponse<Ticket>> {
    return await apiClient.get<PaginatedResponse<Ticket>>('/tickets/', filters);
  }

  /**
   * Get a specific ticket by ID
   */
  async getTicket(ticketId: number, incrementView: boolean = false): Promise<Ticket> {
    return await apiClient.get<Ticket>(`/tickets/${ticketId}`, { increment_view: incrementView });
  }

  /**
   * Get current user's tickets
   */
  async getMyTickets(params?: {
    ticket_type?: 'lending_offer' | 'borrowing_request';
    status?: 'active' | 'paused' | 'completed' | 'cancelled' | 'expired';
    skip?: number;
    limit?: number;
  }): Promise<{ tickets: Ticket[]; total: number }> {
    return await apiClient.get<{ tickets: Ticket[]; total: number }>('/tickets/my-tickets', params);
  }

  /**
   * Create a new ticket
   */
  async createTicket(ticketData: TicketCreateRequest): Promise<Ticket> {
    return await apiClient.post<Ticket>('/tickets/', ticketData);
  }

  /**
   * Update an existing ticket
   */
  async updateTicket(ticketId: number, ticketData: TicketUpdateRequest): Promise<Ticket> {
    return await apiClient.put<Ticket>(`/tickets/${ticketId}`, ticketData);
  }

  /**
   * Delete (cancel) a ticket
   */
  async deleteTicket(ticketId: number): Promise<{ message: string }> {
    return await apiClient.delete<{ message: string }>(`/tickets/${ticketId}`);
  }

  /**
   * Create a deal (connection) from a ticket
   */
  async createDealFromTicket(dealData: CreateDealFromTicketRequest): Promise<Connection> {
    return await apiClient.post<Connection>('/tickets/create-deal', dealData);
  }

  /**
   * Get statistics for user's tickets
   */
  async getMyTicketStats(): Promise<{
    total_tickets: number;
    active_tickets: number;
    completed_tickets: number;
    total_views: number;
    total_responses: number;
    total_deals: number;
    lending_offers: number;
    borrowing_requests: number;
  }> {
    return await apiClient.get('/tickets/me/stats');
  }

  /**
   * Search tickets with text query
   */
  async searchTickets(query: string, filters?: TicketFilterParams): Promise<PaginatedResponse<Ticket>> {
    return await apiClient.get<PaginatedResponse<Ticket>>('/tickets/search', {
      q: query,
      ...filters
    });
  }
}

export const ticketService = new TicketService();
