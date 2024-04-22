import { createBrowserRouter } from 'react-router-dom';

import { Login } from '@pages/Login';
import { Profile } from '@pages/Profile';
import { loginLoader } from '@utils/loader';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Profile />,
    loader: loginLoader,
  },
  {
    path: '/login',
    element: <Login />,
  },
]);

export default router;
