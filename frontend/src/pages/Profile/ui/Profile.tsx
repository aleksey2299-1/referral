import { Button, Input, List, Space, Spin, Typography } from 'antd';
import { Content, Header } from 'antd/es/layout/layout';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCookies } from 'react-cookie';

import { useAppDispatch, useAppSelector } from '@store/hooks';
import { profileRequest, removeUser } from '@store/reducers/profile/profileSlice';
import { fetchUser, patchUser } from '@utils/api/profileApi';

const Profile: React.FC = () => {
  const [__, _, removeCookie] = useCookies(['token']);
  const [code, setCode] = useState<string | undefined>();
  const [codeError, setCodeError] = useState(false);
  const { user, error } = useAppSelector(profileRequest);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const length = user?.referrals.length;

  useEffect(() => {
    if (error === 400) {
      setCodeError(true);
    } else if (error === 401) {
      removeCookie('token', { path: '/', maxAge: 0 });
      navigate('/login');
    }
  }, [error, removeCookie]);

  useEffect(() => {
    if (!user) {
      dispatch(fetchUser());
    }
  }, [dispatch]);

  const handleLogout = () => {
    dispatch(removeUser());
    removeCookie('token', { path: '/', maxAge: 0 });
    navigate('/login');
  };

  const handleUseCode = () => {
    if (!code) {
      setCodeError(true);
    } else {
      dispatch(patchUser({ used_referral_code: code! }));
    }
  };

  if (!user) {
    return <Spin></Spin>;
  }

  return (
    <>
      <Header style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }}>
        <Button onClick={handleLogout}>Logout</Button>
      </Header>
      <Content
        style={{
          padding: '30px',
        }}
      >
        <Typography.Paragraph>
          <strong>Телефон:</strong> {user?.phone}
        </Typography.Paragraph>
        <Typography.Paragraph copyable={{ text: user?.referral_code }}>
          <strong>Реферальный код:</strong> {user?.referral_code}
        </Typography.Paragraph>
        {!user?.used_referral_code ? (
          <>
            <Typography.Paragraph>Введите чужой код тут:</Typography.Paragraph>
            <Space>
              <Input.OTP
                status={codeError ? 'error' : ''}
                length={6}
                value={code}
                onChange={(v) => setCode(v)}
              />
              <Button type="primary" onClick={handleUseCode}>
                Подтвердить
              </Button>
            </Space>
            <br />
            {error === 400 && (
              <Typography.Text type="danger">Такого кода не существует</Typography.Text>
            )}
          </>
        ) : (
          <Typography.Paragraph>
            <strong>Использованный код:</strong> {user?.used_referral_code}
          </Typography.Paragraph>
        )}
        <List
          size="small"
          header={
            <Typography.Title level={5}>
              Ваш код ввел{length === 0 ? 'о' : length === 1 ? '' : 'и'} {length} человек
              {[...Array(5).keys()].slice(2).includes(length! % 10) &&
                (length! < 10 || length! > 20) &&
                'a'}
              :
            </Typography.Title>
          }
          style={{ width: 'fit-content' }}
          dataSource={user!.referrals}
          renderItem={(item, index) => (
            <List.Item style={{ marginLeft: '20px' }}>
              {index + 1}. {item.phone}
            </List.Item>
          )}
        />
      </Content>
    </>
  );
};

export default Profile;
