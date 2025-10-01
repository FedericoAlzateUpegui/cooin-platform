/**
 * Messages Redux Slice
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { messageService } from '../../services/messageService';

// Async thunks
export const getConnectionMessages = createAsyncThunk(
  'messages/getConnectionMessages',
  async ({ connectionId, page = 1 }, { rejectWithValue }) => {
    try {
      const response = await messageService.getConnectionMessages(connectionId, { page });
      return { connectionId, ...response };
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to fetch messages' });
    }
  }
);

export const sendMessage = createAsyncThunk(
  'messages/sendMessage',
  async ({ connectionId, messageData }, { rejectWithValue }) => {
    try {
      const response = await messageService.sendMessage(connectionId, messageData);
      return { connectionId, message: response };
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to send message' });
    }
  }
);

export const markMessageAsRead = createAsyncThunk(
  'messages/markMessageAsRead',
  async ({ connectionId, messageId }, { rejectWithValue }) => {
    try {
      await messageService.markMessageAsRead(connectionId, messageId);
      return { connectionId, messageId };
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to mark message as read' });
    }
  }
);

// Initial state
const initialState = {
  conversations: {}, // { connectionId: { messages: [], pagination: {}, unreadCount: 0 } }
  loading: false,
  sending: false,
  error: null,
  typingUsers: {}, // { connectionId: [userId1, userId2] }
};

// Messages slice
const messagesSlice = createSlice({
  name: 'messages',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearConversation: (state, action) => {
      const connectionId = action.payload;
      delete state.conversations[connectionId];
    },
    clearAllConversations: (state) => {
      state.conversations = {};
    },
    addMessage: (state, action) => {
      const { connectionId, message } = action.payload;
      if (!state.conversations[connectionId]) {
        state.conversations[connectionId] = {
          messages: [],
          pagination: { page: 1, hasNext: false, hasPrevious: false, totalCount: 0 },
          unreadCount: 0,
        };
      }

      // Add message to the beginning (newest first)
      state.conversations[connectionId].messages.unshift(message);

      // Update unread count if message is from other user
      if (!message.is_read && message.receiver_id === getCurrentUserId()) {
        state.conversations[connectionId].unreadCount += 1;
      }
    },
    updateMessage: (state, action) => {
      const { connectionId, messageId, updates } = action.payload;
      const conversation = state.conversations[connectionId];
      if (conversation) {
        const messageIndex = conversation.messages.findIndex(msg => msg.id === messageId);
        if (messageIndex !== -1) {
          conversation.messages[messageIndex] = {
            ...conversation.messages[messageIndex],
            ...updates,
          };
        }
      }
    },
    setTypingUsers: (state, action) => {
      const { connectionId, users } = action.payload;
      state.typingUsers[connectionId] = users;
    },
    updateUnreadCount: (state, action) => {
      const { connectionId, count } = action.payload;
      if (state.conversations[connectionId]) {
        state.conversations[connectionId].unreadCount = count;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Get connection messages
      .addCase(getConnectionMessages.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getConnectionMessages.fulfilled, (state, action) => {
        state.loading = false;
        const { connectionId, messages, unread_count, ...pagination } = action.payload;

        state.conversations[connectionId] = {
          messages: messages || [],
          pagination: {
            page: pagination.page || 1,
            hasNext: pagination.has_next || false,
            hasPrevious: pagination.has_previous || false,
            totalCount: pagination.total_count || 0,
          },
          unreadCount: unread_count || 0,
        };
        state.error = null;
      })
      .addCase(getConnectionMessages.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.detail || 'Failed to fetch messages';
      })

      // Send message
      .addCase(sendMessage.pending, (state) => {
        state.sending = true;
        state.error = null;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.sending = false;
        const { connectionId, message } = action.payload;

        if (!state.conversations[connectionId]) {
          state.conversations[connectionId] = {
            messages: [],
            pagination: { page: 1, hasNext: false, hasPrevious: false, totalCount: 0 },
            unreadCount: 0,
          };
        }

        // Add new message to the beginning
        state.conversations[connectionId].messages.unshift(message);
        state.error = null;
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.sending = false;
        state.error = action.payload?.detail || 'Failed to send message';
      })

      // Mark message as read
      .addCase(markMessageAsRead.fulfilled, (state, action) => {
        const { connectionId, messageId } = action.payload;
        const conversation = state.conversations[connectionId];

        if (conversation) {
          const message = conversation.messages.find(msg => msg.id === messageId);
          if (message && !message.is_read) {
            message.is_read = true;
            message.read_at = new Date().toISOString();
            conversation.unreadCount = Math.max(0, conversation.unreadCount - 1);
          }
        }
      });
  },
});

// Helper function to get current user ID (would need to be implemented based on auth state)
const getCurrentUserId = () => {
  // This would typically come from the auth slice
  return null; // Placeholder
};

export const {
  clearError,
  clearConversation,
  clearAllConversations,
  addMessage,
  updateMessage,
  setTypingUsers,
  updateUnreadCount,
} = messagesSlice.actions;

export default messagesSlice.reducer;