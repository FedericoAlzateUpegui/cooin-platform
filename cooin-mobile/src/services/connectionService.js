/**
 * Connection Service
 */

import apiClient from './apiClient';
import { ENDPOINTS } from '../constants/api';

class ConnectionService {
  // Get user connections
  async getConnections(params = {}) {
    try {
      const response = await apiClient.get(ENDPOINTS.CONNECTIONS.BASE, { params });
      return response.data;
    } catch (error) {
      console.error('Get connections error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get pending connections
  async getPendingConnections(params = {}) {
    try {
      const response = await apiClient.get(ENDPOINTS.CONNECTIONS.PENDING, { params });
      return response.data;
    } catch (error) {
      console.error('Get pending connections error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Create connection request
  async createConnection(connectionData) {
    try {
      const response = await apiClient.post(ENDPOINTS.CONNECTIONS.BASE, connectionData);
      return response.data;
    } catch (error) {
      console.error('Create connection error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get specific connection
  async getConnection(connectionId) {
    try {
      const response = await apiClient.get(ENDPOINTS.CONNECTIONS.BY_ID(connectionId));
      return response.data;
    } catch (error) {
      console.error('Get connection error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Update connection (accept/reject/etc.)
  async updateConnection(connectionId, updateData) {
    try {
      const response = await apiClient.put(ENDPOINTS.CONNECTIONS.BY_ID(connectionId), updateData);
      return response.data;
    } catch (error) {
      console.error('Update connection error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Delete connection
  async deleteConnection(connectionId) {
    try {
      const response = await apiClient.delete(ENDPOINTS.CONNECTIONS.BY_ID(connectionId));
      return response.data;
    } catch (error) {
      console.error('Delete connection error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Block connection
  async blockConnection(connectionId) {
    try {
      const response = await apiClient.post(ENDPOINTS.CONNECTIONS.BLOCK(connectionId));
      return response.data;
    } catch (error) {
      console.error('Block connection error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Report connection
  async reportConnection(connectionId, reason) {
    try {
      const response = await apiClient.post(
        ENDPOINTS.CONNECTIONS.REPORT(connectionId),
        null,
        { params: { reason } }
      );
      return response.data;
    } catch (error) {
      console.error('Report connection error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get connection statistics
  async getConnectionStats() {
    try {
      const response = await apiClient.get(ENDPOINTS.CONNECTIONS.STATS);
      return response.data;
    } catch (error) {
      console.error('Get connection stats error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Search for matches
  async searchMatches(criteria) {
    try {
      const response = await apiClient.post(ENDPOINTS.CONNECTIONS.MATCHING, criteria);
      return response.data;
    } catch (error) {
      console.error('Search matches error:', error.response?.data || error.message);
      throw error;
    }
  }

  // Accept connection
  async acceptConnection(connectionId, responseMessage = null) {
    return this.updateConnection(connectionId, {
      status: 'accepted',
      response_message: responseMessage,
    });
  }

  // Reject connection
  async rejectConnection(connectionId, responseMessage = null) {
    return this.updateConnection(connectionId, {
      status: 'rejected',
      response_message: responseMessage,
    });
  }

  // Send connection request with predefined data
  async sendLendingInquiry(receiverId, loanAmount, message, loanPurpose = null) {
    return this.createConnection({
      receiver_id: receiverId,
      connection_type: 'lending_inquiry',
      message: message,
      loan_amount_requested: loanAmount,
      loan_purpose: loanPurpose,
      priority_level: 1,
    });
  }

  // Send borrowing request
  async sendBorrowingRequest(receiverId, loanAmount, message, loanPurpose = null) {
    return this.createConnection({
      receiver_id: receiverId,
      connection_type: 'borrowing_request',
      message: message,
      loan_amount_requested: loanAmount,
      loan_purpose: loanPurpose,
      priority_level: 1,
    });
  }

  // Send general connection
  async sendGeneralConnection(receiverId, message) {
    return this.createConnection({
      receiver_id: receiverId,
      connection_type: 'general_connection',
      message: message,
      priority_level: 1,
    });
  }
}

export const connectionService = new ConnectionService();