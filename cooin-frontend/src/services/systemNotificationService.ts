import api from './api';

export interface SystemMessage {
  id: number;
  user_id: number;
  title: string;
  content: string;
  message_type: 'match_notification' | 'educational' | 'announcement' | 'reminder' | 'safety_tip' | 'feature_update';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  action_url?: string;
  action_label?: string;
  image_url?: string;
  category?: string;
  tags?: string;
  is_read: boolean;
  read_at?: string;
  is_archived: boolean;
  archived_at?: string;
  is_deleted: boolean;
  deleted_at?: string;
  created_at: string;
  updated_at: string;
  expires_at?: string;
}

export interface SystemMessageListResponse {
  messages: SystemMessage[];
  total_count: number;
  unread_count: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface SystemMessageStats {
  total_messages: number;
  unread_messages: number;
  archived_messages: number;
  messages_by_type: { [key: string]: number };
  messages_by_priority: { [key: string]: number };
}

class SystemNotificationService {
  /**
   * Get system messages/notifications for the current user
   */
  async getMessages(
    page: number = 1,
    pageSize: number = 50,
    messageType?: string,
    priority?: string,
    isRead?: boolean,
    isArchived?: boolean
  ): Promise<SystemMessageListResponse> {
    const params: any = { page, page_size: pageSize };

    if (messageType) params.message_type = messageType;
    if (priority) params.priority = priority;
    if (isRead !== undefined) params.is_read = isRead;
    if (isArchived !== undefined) params.is_archived = isArchived;

    const response = await api.get('/system-messages/', { params });
    return response.data;
  }

  /**
   * Get a specific system message by ID
   */
  async getMessage(messageId: number): Promise<SystemMessage> {
    const response = await api.get(`/system-messages/${messageId}`);
    return response.data;
  }

  /**
   * Get unread message count
   */
  async getUnreadCount(): Promise<number> {
    const response = await api.get('/system-messages/unread-count');
    return response.data.unread_count;
  }

  /**
   * Get message statistics
   */
  async getStats(): Promise<SystemMessageStats> {
    const response = await api.get('/system-messages/stats');
    return response.data;
  }

  /**
   * Mark a message as read
   */
  async markAsRead(messageId: number): Promise<SystemMessage> {
    const response = await api.put(`/system-messages/${messageId}/read`);
    return response.data;
  }

  /**
   * Mark all messages as read
   */
  async markAllAsRead(): Promise<{ message: string; updated_count: number }> {
    const response = await api.put('/system-messages/read-all');
    return response.data;
  }

  /**
   * Archive a message
   */
  async archiveMessage(messageId: number): Promise<SystemMessage> {
    const response = await api.put(`/system-messages/${messageId}/archive`);
    return response.data;
  }

  /**
   * Delete a message (soft delete)
   */
  async deleteMessage(messageId: number): Promise<void> {
    await api.delete(`/system-messages/${messageId}`);
  }

  /**
   * Get message type display name
   */
  getMessageTypeLabel(type: string): string {
    const labels: { [key: string]: string } = {
      match_notification: 'Match',
      educational: 'Educational',
      announcement: 'Announcement',
      reminder: 'Reminder',
      safety_tip: 'Safety',
      feature_update: 'Feature Update'
    };
    return labels[type] || type;
  }

  /**
   * Get message type icon
   */
  getMessageTypeIcon(type: string): string {
    const icons: { [key: string]: string } = {
      match_notification: '🤝',
      educational: '📚',
      announcement: '📢',
      reminder: '⏰',
      safety_tip: '🛡️',
      feature_update: '✨'
    };
    return icons[type] || '📬';
  }

  /**
   * Get priority color
   */
  getPriorityColor(priority: string): string {
    const colors: { [key: string]: string } = {
      low: '#6B7280',      // Gray
      medium: '#3B82F6',   // Blue
      high: '#F59E0B',     // Amber
      urgent: '#EF4444'    // Red
    };
    return colors[priority] || colors.medium;
  }
}

export default new SystemNotificationService();
