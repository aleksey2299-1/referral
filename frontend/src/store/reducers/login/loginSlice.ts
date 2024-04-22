import { createSlice } from '@reduxjs/toolkit';

import { TRequest } from '@pages/Login/types/types';
import { requestCode } from '@utils/api/loginApi';

export interface LoginState {
  request: TRequest | null;
  isLoading: boolean;
  error: string | null | unknown;
}

const initialState: LoginState = {
  request: null,
  isLoading: false,
  error: null,
};

const loginSlice = createSlice({
  name: 'login',
  initialState,
  reducers: {
    removeRequest: (state) => {
      state.request = null;
    },
  },
  extraReducers(builder) {
    builder
      .addCase(requestCode.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(requestCode.fulfilled, (state, action) => {
        state.request = action.payload;
        state.isLoading = false;
        state.error = null;
      })
      .addCase(requestCode.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const { removeRequest } = loginSlice.actions;
export const loginRequest = (state: { login: LoginState }) => state.login;

export default loginSlice.reducer;
