export interface LoginData {
  email: string;
  password: string;
}

export const login = async (loginData: LoginData): Promise<string> => {
  const response = await fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(loginData),
  });

  if (!response.ok) {
    throw new Error('ログイン失敗');
  }

  const data = await response.json();
  return data.access_token;  // JWTトークンを返す
};
