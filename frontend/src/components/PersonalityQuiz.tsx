import React, { useState } from 'react';

const PersonalityQuiz: React.FC = () => {
  const [question1, setQuestion1] = useState('');
  const [question2, setQuestion2] = useState('');
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const token = localStorage.getItem('token');  // 保存したトークンを取得

    if (!token) {
      setError('No token found. Please login first.');
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/getUmamusume`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,  // トークンをヘッダーに含める
        },
        body: JSON.stringify({
          question1: question1,
          question2: question2,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError('Failed to get the result. Please try again.');
    }
  };

  return (
    <div>
      <h2>Personality Quiz</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Question 1:
            <input
              type="text"
              value={question1}
              onChange={(e) => setQuestion1(e.target.value)}
            />
          </label>
        </div>
        <div>
          <label>
            Question 2:
            <input
              type="text"
              value={question2}
              onChange={(e) => setQuestion2(e.target.value)}
            />
          </label>
        </div>
        <button type="submit">Submit</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {result && (
        <div>
          <h3>Recommended Umamusume:</h3>
          <p>Name: {result.name}</p>
          <p>Personality: {result.personality}</p>
          <p>
            <a href={result.url} target="_blank" rel="noopener noreferrer">
              Official Profile
            </a>
          </p>
        </div>
      )}
    </div>
  );
};

export default PersonalityQuiz;
