import { apiClient } from './api';
import { Message, MessageCreateRequest, PaginatedResponse } from '../types/api';

class MessagingService {
  async getMessages(connectionId: number, params?: {
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<Message>> {
    return await apiClient.get<PaginatedResponse<Message>>(`/connections/${connectionId}/messages`, params);
  }

  async sendMessage(connectionId: number, messageData: MessageCreateRequest): Promise<Message> {
    return await apiClient.post<Message>(`/connections/${connectionId}/messages`, messageData);
  }

  async markAsRead(connectionId: number, messageId: number): Promise<void> {
    return await apiClient.post(`/connections/${connectionId}/messages/${messageId}/read`);
  }

  async getUnreadCount(): Promise<{ total_unread: number }> {
    return await apiClient.get('/messages/unread-count');
  }

  async getConversations(params?: {
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<{
    connection_id: number;
    other_user_name: string;
    last_message: string;
    last_message_time: string;
    unread_count: number;
    connection_status: string;
  }>> {
    return await apiClient.get('/messages/conversations', params);
  }
}

export const messagingService = new MessagingService();