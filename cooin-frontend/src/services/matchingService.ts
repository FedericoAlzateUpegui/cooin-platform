import { apiClient } from './api';
import {
  MatchingCriteria,
  MatchingResponse,
  Connection,
  ConnectionCreateRequest,
  PaginatedResponse
} from '../types/api';

class MatchingService {
  async findMatches(criteria: MatchingCriteria): Promise<MatchingResponse> {
    return await apiClient.post<MatchingResponse>('/connections/matching/search', criteria);
  }

  async createConnection(connectionData: ConnectionCreateRequest): Promise<Connection> {
    return await apiClient.post<Connection>('/connections/', connectionData);
  }

  async getMyConnections(params?: {
    page?: number;
    page_size?: number;
    status_filter?: string;
    connection_type?: string;
  }): Promise<PaginatedResponse<Connection>> {
    return await apiClient.get<PaginatedResponse<Connection>>('/connections/', params);
  }

  async updateConnection(connectionId: number, data: {
    status?: 'accepted' | 'rejected' | 'blocked';
    response_message?: string;
  }): Promise<Connection> {
    return await apiClient.put<Connection>(`/connections/${connectionId}`, data);
  }

  async blockConnection(connectionId: number): Promise<void> {
    return await apiClient.post(`/connections/${connectionId}/block`);
  }

  async reportConnection(connectionId: number, reason: string): Promise<void> {
    return await apiClient.post(`/connections/${connectionId}/report?reason=${encodeURIComponent(reason)}`);
  }

  async getConnectionStats(): Promise<{
    total_connections: number;
    pending_sent: number;
    pending_received: number;
    accepted_connections: number;
    rejected_connections: number;
    mutual_connections: number;
    recent_activity: number;
  }> {
    return await apiClient.get('/connections/stats');
  }

  async getPendingConnections(params?: {
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<Connection>> {
    return await apiClient.get<PaginatedResponse<Connection>>('/connections/pending', params);
  }
}

export const matchingService = new MatchingService();