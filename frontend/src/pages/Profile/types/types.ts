type TUser = {
  phone: string;
  referral_code: string;
  used_referral_code: string;
  referrals: TReferral[];
};

type TReferral = {
  phone: string;
};

export type { TUser };
