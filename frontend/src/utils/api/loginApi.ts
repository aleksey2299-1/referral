import { createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

import { TLoginData, TRequest } from '@pages/Login/types/types';

import { BASE_URL } from '../constants/env_constants';

export const requestCode = createAsyncThunk(
  'login/requestCode',
  async (postData: TLoginData, { rejectWithValue }) => {
    try {
      const { data } = await axios.post<TRequest>(`${BASE_URL}/api/v1/login/`, postData);
      return data;
    } catch (e: any) {
      return rejectWithValue(e.message);
    }
  }
);
