import { createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { Cookies } from 'react-cookie';

import { TUser } from '@pages/Profile/types/types';

import { BASE_URL } from '../constants/env_constants';

export const fetchUser = createAsyncThunk('profile/fetchUser', async (_, { rejectWithValue }) => {
  const token = new Cookies().get('token');
  try {
    const { data } = await axios.get<TUser>(`${BASE_URL}/api/v1/profile`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return data;
  } catch (e: any) {
    return rejectWithValue(e.response.status);
  }
});

export const patchUser = createAsyncThunk(
  'profile/patchUser',
  async (patchData: { used_referral_code: string }, { rejectWithValue }) => {
    const token = new Cookies().get('token');
    try {
      const { data } = await axios.patch<TUser>(`${BASE_URL}/api/v1/profile`, patchData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return data;
    } catch (e: any) {
      return rejectWithValue(e.response.status);
    }
  }
);
