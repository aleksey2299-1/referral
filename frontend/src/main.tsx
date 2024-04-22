import * as React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';

import { Provider } from 'react-redux';
import { RouterProvider } from 'react-router-dom';
import { CookiesProvider } from 'react-cookie';

import { router } from '@pages/Router';
import { store } from '@store/store.ts';

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <CookiesProvider>
      <Provider store={store}>
        <RouterProvider router={router} />
      </Provider>
    </CookiesProvider>
  </React.StrictMode>
);
