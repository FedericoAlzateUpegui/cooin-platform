/**
 * Message Service
 */

import apiClient from './apiClient';
import { ENDPOINTS } from '../constants/api';

class MessageService {
  // Get messages for a connection
  async getConnectionMessages(connectionId, params = {}) {
    try {
      const response = await apiClient.get(ENDPOINTS.CONNECTIONS.MESSAGES(connectionId), { params });
      return response.data;
    } catch (error) {
      console.error('Get connection messages error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Send message
  async sendMessage(connectionId, messageData) {
    try {
      const response = await apiClient.post(ENDPOINTS.CONNECTIONS.MESSAGES(connectionId), messageData);
      return response.data;
    } catch (error) {
      console.error('Send message error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Mark message as read
  async markMessageAsRead(connectionId, messageId) {
    try {
      const response = await apiClient.put(ENDPOINTS.CONNECTIONS.MESSAGE_READ(connectionId, messageId));
      return response.data;
    } catch (error) {
      console.error('Mark message as read error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Send text message (convenience method)
  async sendTextMessage(connectionId, text) {
    return this.sendMessage(connectionId, {
      content: text,
      message_type: 'text',
    });
  }

  // Send image message (if implemented)
  async sendImageMessage(connectionId, imageData) {
    try {
      const formData = new FormData();
      formData.append('content', 'Image message');
      formData.append('message_type', 'image');
      formData.append('file', {
        uri: imageData.uri,
        type: imageData.type || 'image/jpeg',
        name: imageData.fileName || 'image.jpg',
      });

      const response = await apiClient.post(
        ENDPOINTS.CONNECTIONS.MESSAGES(connectionId),
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      return response.data;
    } catch (error) {
      console.error('Send image message error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Send document message (if implemented)
  async sendDocumentMessage(connectionId, documentData) {
    try {
      const formData = new FormData();
      formData.append('content', 'Document message');
      formData.append('message_type', 'document');
      formData.append('file', {
        uri: documentData.uri,
        type: documentData.type || 'application/pdf',
        name: documentData.fileName || 'document.pdf',
      });

      const response = await apiClient.post(
        ENDPOINTS.CONNECTIONS.MESSAGES(connectionId),
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      return response.data;
    } catch (error) {
      console.error('Send document message error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Mark all messages in conversation as read
  async markConversationAsRead(connectionId) {
    try {
      // This would need to be implemented in the backend
      const response = await apiClient.put(`/connections/${connectionId}/messages/mark-all-read`);
      return response.data;
    } catch (error) {
      console.error('Mark conversation as read error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Delete message (soft delete)
  async deleteMessage(connectionId, messageId) {
    try {
      // This would need to be implemented in the backend
      const response = await apiClient.delete(ENDPOINTS.CONNECTIONS.MESSAGE_BY_ID(connectionId, messageId));
      return response.data;
    } catch (error) {
      console.error('Delete message error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get message statistics
  async getMessageStats(connectionId) {
    try {
      // This would need to be implemented in the backend
      const response = await apiClient.get(`/connections/${connectionId}/messages/stats`);
      return response.data;
    } catch (error) {
      console.error('Get message stats error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Search messages in a conversation
  async searchMessages(connectionId, query) {
    try {
      // This would need to be implemented in the backend
      const response = await apiClient.get(
        `/connections/${connectionId}/messages/search`,
        { params: { q: query } }
      );
      return response.data;
    } catch (error) {
      console.error('Search messages error:', error.response?.data || error.message);
      throw error;
    }
  }
}

export const messageService = new MessageService();