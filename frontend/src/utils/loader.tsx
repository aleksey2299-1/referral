import { Cookies } from 'react-cookie';

export const loginLoader = () => {
  const token = new Cookies().get('token');
  if (!token) {
    throw new Response('', {
      status: 302,
      headers: {
        Location: '/login',
      },
    });
  }
  return null;
};
