import { createSlice } from '@reduxjs/toolkit';

import { TUser } from '@pages/Profile/types/types';
import { fetchUser, patchUser } from '@utils/api/profileApi';

export interface ProfileState {
  user: TUser | null;
  isLoading: boolean;
  error: number | null | unknown;
}

const initialState: ProfileState = {
  user: null,
  isLoading: false,
  error: null,
};

const profileSlice = createSlice({
  name: 'profile',
  initialState,
  reducers: {
    removeUser: (state) => {
      state.user = null;
    },
  },
  extraReducers(builder) {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.user = action.payload;
        state.isLoading = false;
        state.error = null;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      .addCase(patchUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(patchUser.fulfilled, (state, action) => {
        state.user = action.payload;
        state.isLoading = false;
        state.error = null;
      })
      .addCase(patchUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const { removeUser } = profileSlice.actions;
export const profileRequest = (state: { profile: ProfileState }) => state.profile;

export default profileSlice.reducer;
