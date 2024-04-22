type TRequest = {
  confirmation_code?: number;
  token?: string;
};

type TLoginData = {
  phone: string;
  send_code?: boolean;
  confirmation_code?: number;
};

export type { TRequest, TLoginData };
