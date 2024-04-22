import { configureStore } from '@reduxjs/toolkit';

import loginReducer from './reducers/login/loginSlice';
import profileReducer from './reducers/profile/profileSlice';

export const store = configureStore({
  reducer: {
    login: loginReducer,
    profile: profileReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
