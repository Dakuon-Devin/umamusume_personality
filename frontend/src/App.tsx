import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import PersonalityQuiz from './components/PersonalityQuiz';

const App: React.FC = () => {
  const [token, setToken] = useState<string | null>(null);

  return (
    <div>
      {!token ? (
        <LoginForm onLogin={(newToken: string) => setToken(newToken)} />
      ) : (
        <PersonalityQuiz token={token} />
      )}
    </div>
  );
};

export default App;
