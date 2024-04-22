import { QuestionCircleOutlined } from '@ant-design/icons';

import { Button, Input, Select, Space, Tooltip, Typography } from 'antd';
import { useCallback, useEffect, useState } from 'react';

import { Controller, FieldValues, FormProvider, useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { useCookies } from 'react-cookie';

import { useAppDispatch, useAppSelector } from '@store/hooks';
import { loginRequest, removeRequest } from '@store/reducers/login/loginSlice';
import { requestCode } from '@utils/api/loginApi';

import { countries } from '../data/data';

const Login: React.FC = () => {
  const methods = useForm();
  const [_, setCookie] = useCookies(['token']);
  const [showCode, setShowCode] = useState(false);
  const [codeLocal, setCodeLocal] = useState<number | null>(null);
  const [ready, setReady] = useState(true);
  const [time, setTime] = useState(60);
  const { isLoading, error, request } = useAppSelector(loginRequest);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const filterOption = (input: string, option?: { label: string; value: string; name: string }) =>
    (option?.name ?? '').toLowerCase().includes(input.toLowerCase());

  useEffect(() => {
    if (request?.token) {
      setCookie('token', request.token, { path: '/', maxAge: 86400 });
      dispatch(removeRequest());
      navigate('/');
    }
  }, [request?.token, navigate, setCookie]);

  const handleSubmit = (data: FieldValues) => {
    const new_data = {
      phone: data.phone.country_code + data.phone.number,
      confirmation_code: parseInt(data.confirmation_code),
    };
    dispatch(requestCode(new_data));
  };

  const countDown = useCallback(() => {
    setReady(false);
    let secondsToGo = time;

    const timer = setInterval(() => {
      secondsToGo -= 1;
      setTime(secondsToGo);
    }, 1000);

    setTimeout(() => {
      clearInterval(timer);
      setReady(true);
      setTime(60);
    }, secondsToGo * 1000);
  }, [time]);

  useEffect(() => {
    if (request?.confirmation_code) {
      setShowCode(true);
      setCodeLocal(request.confirmation_code);
      dispatch(removeRequest());
      countDown();
    }
  }, [request?.confirmation_code, countDown, dispatch]);

  const handleRequestCode = () => {
    const data = methods.getValues();
    const new_data = {
      phone: data.phone.country_code + data.phone.number,
      send_code: true,
    };
    dispatch(requestCode(new_data));
  };

  return (
    <div
      style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}
    >
      <FormProvider {...methods}>
        <form onSubmit={methods.handleSubmit(handleSubmit)}>
          <div
            style={{
              border: 'solid 1px',
              borderRadius: '10px',
              padding: '20px',
            }}
          >
            <Space style={{ display: 'flex', justifyContent: 'center' }}>
              <Typography.Title level={3}>Вход</Typography.Title>
            </Space>
            {(error as string) && (
              <Space style={{ display: 'flex', justifyContent: 'center' }}>
                <Typography.Text type="danger">Неправильные данные</Typography.Text>
              </Space>
            )}
            <Space.Compact>
              <Controller
                name={'phone.country_code'}
                control={methods.control}
                render={({ field }) => (
                  <Select
                    showSearch
                    style={{ width: '20vh' }}
                    placeholder="Код"
                    options={countries.map((item) => ({
                      key: item.code,
                      label: `+${item.phone}`,
                      value: `+${item.phone}`,
                      code: item.code,
                      name: item.label,
                    }))}
                    disabled={showCode}
                    popupMatchSelectWidth={false}
                    optionLabelProp="label"
                    optionRender={(option) => (
                      <div>
                        <img
                          loading="lazy"
                          width="20"
                          srcSet={`https://flagcdn.com/w40/${option.data.code.toLowerCase()}.png 2x`}
                          src={`https://flagcdn.com/w20/${option.data.code.toLowerCase()}.png`}
                          alt=""
                        />{' '}
                        {option.data.name} ({option.data.code}) {option.data.label}
                      </div>
                    )}
                    filterOption={filterOption}
                    {...field}
                  />
                )}
              />
              <Controller
                name={'phone.number'}
                control={methods.control}
                render={({ field }) => (
                  <Input disabled={showCode} placeholder="Введите номер" {...field} />
                )}
              />
            </Space.Compact>
            {showCode && (
              <>
                <Space style={{ display: 'flex', justifyContent: 'center' }}>
                  <Typography.Paragraph style={{ marginTop: '10px' }}>
                    Введите проверочный код:{' '}
                    <Tooltip title={codeLocal} arrow={false}>
                      <QuestionCircleOutlined />
                    </Tooltip>
                  </Typography.Paragraph>
                </Space>
                <Space style={{ display: 'flex', justifyContent: 'center' }}>
                  <Controller
                    name={'confirmation_code'}
                    control={methods.control}
                    render={({ field }) => <Input.OTP length={4} {...field} />}
                  />
                </Space>
              </>
            )}
            <br />
            <br />
            <Space style={{ display: 'flex', justifyContent: 'center' }}>
              {showCode && (
                <Button loading={isLoading} htmlType="submit">
                  Войти
                </Button>
              )}
              <Button loading={isLoading} disabled={!ready} onClick={() => handleRequestCode()}>
                {ready ? 'Запросить код' : `Подождите ${time} секунд`}
              </Button>
            </Space>
          </div>
        </form>
      </FormProvider>
    </div>
  );
};

export default Login;
