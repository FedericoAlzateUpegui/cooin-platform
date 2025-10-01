/**
 * Connections Redux Slice
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { connectionService } from '../../services/connectionService';

// Async thunks
export const getConnections = createAsyncThunk(
  'connections/getConnections',
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await connectionService.getConnections(params);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to fetch connections' });
    }
  }
);

export const getPendingConnections = createAsyncThunk(
  'connections/getPendingConnections',
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await connectionService.getPendingConnections(params);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to fetch pending connections' });
    }
  }
);

export const createConnection = createAsyncThunk(
  'connections/createConnection',
  async (connectionData, { rejectWithValue }) => {
    try {
      const response = await connectionService.createConnection(connectionData);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to create connection' });
    }
  }
);

export const updateConnection = createAsyncThunk(
  'connections/updateConnection',
  async ({ connectionId, updateData }, { rejectWithValue }) => {
    try {
      const response = await connectionService.updateConnection(connectionId, updateData);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to update connection' });
    }
  }
);

export const deleteConnection = createAsyncThunk(
  'connections/deleteConnection',
  async (connectionId, { rejectWithValue }) => {
    try {
      await connectionService.deleteConnection(connectionId);
      return connectionId;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to delete connection' });
    }
  }
);

export const blockConnection = createAsyncThunk(
  'connections/blockConnection',
  async (connectionId, { rejectWithValue }) => {
    try {
      await connectionService.blockConnection(connectionId);
      return connectionId;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to block connection' });
    }
  }
);

export const getConnectionStats = createAsyncThunk(
  'connections/getConnectionStats',
  async (_, { rejectWithValue }) => {
    try {
      const response = await connectionService.getConnectionStats();
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to fetch connection stats' });
    }
  }
);

// Initial state
const initialState = {
  connections: [],
  pendingConnections: [],
  stats: null,
  loading: false,
  creating: false,
  updating: false,
  error: null,
  pagination: {
    page: 1,
    hasNext: false,
    hasPrevious: false,
    totalCount: 0,
  },
};

// Connections slice
const connectionsSlice = createSlice({
  name: 'connections',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    resetConnections: (state) => {
      return initialState;
    },
    addConnection: (state, action) => {
      state.connections.unshift(action.payload);
    },
    removeConnection: (state, action) => {
      state.connections = state.connections.filter(
        conn => conn.id !== action.payload
      );
      state.pendingConnections = state.pendingConnections.filter(
        conn => conn.id !== action.payload
      );
    },
    updateConnectionInList: (state, action) => {
      const { id, updates } = action.payload;

      // Update in main connections list
      const connIndex = state.connections.findIndex(conn => conn.id === id);
      if (connIndex !== -1) {
        state.connections[connIndex] = { ...state.connections[connIndex], ...updates };
      }

      // Update in pending connections list
      const pendingIndex = state.pendingConnections.findIndex(conn => conn.id === id);
      if (pendingIndex !== -1) {
        if (updates.status && updates.status !== 'pending') {
          // Remove from pending if status changed from pending
          state.pendingConnections.splice(pendingIndex, 1);
        } else {
          state.pendingConnections[pendingIndex] = { ...state.pendingConnections[pendingIndex], ...updates };
        }
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Get connections
      .addCase(getConnections.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getConnections.fulfilled, (state, action) => {
        state.loading = false;
        state.connections = action.payload.connections || [];
        state.pagination = {
          page: action.payload.page || 1,
          hasNext: action.payload.has_next || false,
          hasPrevious: action.payload.has_previous || false,
          totalCount: action.payload.total_count || 0,
        };
        state.error = null;
      })
      .addCase(getConnections.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.detail || 'Failed to fetch connections';
      })

      // Get pending connections
      .addCase(getPendingConnections.fulfilled, (state, action) => {
        state.pendingConnections = action.payload.connections || [];
      })

      // Create connection
      .addCase(createConnection.pending, (state) => {
        state.creating = true;
        state.error = null;
      })
      .addCase(createConnection.fulfilled, (state, action) => {
        state.creating = false;
        state.connections.unshift(action.payload);
        state.error = null;
      })
      .addCase(createConnection.rejected, (state, action) => {
        state.creating = false;
        state.error = action.payload?.detail || 'Failed to create connection';
      })

      // Update connection
      .addCase(updateConnection.pending, (state) => {
        state.updating = true;
        state.error = null;
      })
      .addCase(updateConnection.fulfilled, (state, action) => {
        state.updating = false;
        const updatedConnection = action.payload;

        // Update in connections list
        const index = state.connections.findIndex(conn => conn.id === updatedConnection.id);
        if (index !== -1) {
          state.connections[index] = updatedConnection;
        }

        // Remove from pending if status changed from pending
        if (updatedConnection.status !== 'pending') {
          state.pendingConnections = state.pendingConnections.filter(
            conn => conn.id !== updatedConnection.id
          );
        }

        state.error = null;
      })
      .addCase(updateConnection.rejected, (state, action) => {
        state.updating = false;
        state.error = action.payload?.detail || 'Failed to update connection';
      })

      // Delete connection
      .addCase(deleteConnection.fulfilled, (state, action) => {
        const connectionId = action.payload;
        state.connections = state.connections.filter(conn => conn.id !== connectionId);
        state.pendingConnections = state.pendingConnections.filter(conn => conn.id !== connectionId);
      })

      // Block connection
      .addCase(blockConnection.fulfilled, (state, action) => {
        const connectionId = action.payload;
        // Update connection status to blocked
        const connection = state.connections.find(conn => conn.id === connectionId);
        if (connection) {
          connection.status = 'blocked';
        }
      })

      // Get connection stats
      .addCase(getConnectionStats.fulfilled, (state, action) => {
        state.stats = action.payload;
      });
  },
});

export const {
  clearError,
  resetConnections,
  addConnection,
  removeConnection,
  updateConnectionInList,
} = connectionsSlice.actions;

export default connectionsSlice.reducer;