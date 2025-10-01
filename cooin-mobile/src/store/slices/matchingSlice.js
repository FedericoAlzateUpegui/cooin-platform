/**
 * Matching Redux Slice
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { connectionService } from '../../services/connectionService';

// Async thunks
export const searchMatches = createAsyncThunk(
  'matching/searchMatches',
  async (criteria, { rejectWithValue }) => {
    try {
      const response = await connectionService.searchMatches(criteria);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to search matches' });
    }
  }
);

// Initial state
const initialState = {
  matches: [],
  searchCriteria: null,
  searchTime: 0,
  totalMatches: 0,
  loading: false,
  error: null,
  hasSearched: false,
};

// Matching slice
const matchingSlice = createSlice({
  name: 'matching',
  initialState,
  reducers: {
    clearMatches: (state) => {
      state.matches = [];
      state.hasSearched = false;
      state.error = null;
    },
    clearError: (state) => {
      state.error = null;
    },
    updateSearchCriteria: (state, action) => {
      state.searchCriteria = action.payload;
    },
    removeMatchById: (state, action) => {
      state.matches = state.matches.filter(match => match.user_id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      // Search matches
      .addCase(searchMatches.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(searchMatches.fulfilled, (state, action) => {
        state.loading = false;
        state.matches = action.payload.matches || [];
        state.searchCriteria = action.payload.search_criteria || null;
        state.searchTime = action.payload.search_time_ms || 0;
        state.totalMatches = action.payload.total_matches || 0;
        state.hasSearched = true;
        state.error = null;
      })
      .addCase(searchMatches.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.detail || 'Failed to search matches';
        state.hasSearched = true;
      });
  },
});

export const {
  clearMatches,
  clearError,
  updateSearchCriteria,
  removeMatchById,
} = matchingSlice.actions;

export default matchingSlice.reducer;