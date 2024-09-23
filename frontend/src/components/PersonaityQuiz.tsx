// src/components/PersonalityQuiz.tsx
import React, { useState } from 'react';
import { getUmamusume, QuizAnswers, QuizResult } from '../api/umamusumeApi';

const PersonalityQuiz: React.FC = () => {
  const [answers, setAnswers] = useState<QuizAnswers>({
    question1: '',
    question2: '',
  });

  const [result, setResult] = useState<QuizResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAnswers({
      ...answers,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data = await getUmamusume(answers);
      setResult(data);
    } catch (err) {
      setError('診断に失敗しました。再度お試しください。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>ウマ娘性格診断</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>質問1: あなたは外向的ですか？</label>
          <div>
            <input
              type="radio"
              name="question1"
              value="はい"
              onChange={handleChange}
              required
            /> はい
            <input
              type="radio"
              name="question1"
              value="いいえ"
              onChange={handleChange}
              required
            /> いいえ
          </div>
        </div>

        <div>
          <label>質問2: あなたは冷静ですか？</label>
          <div>
            <input
              type="radio"
              name="question2"
              value="はい"
              onChange={handleChange}
              required
            /> はい
            <input
              type="radio"
              name="question2"
              value="いいえ"
              onChange={handleChange}
              required
            /> いいえ
          </div>
        </div>

        {/* 他の質問も同様に追加 */}

        <button type="submit" disabled={loading}>
          {loading ? '診断中...' : '診断する'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && (
        <div>
          <h2>あなたに似ているウマ娘: {result.name}</h2>
          <p>{result.personality}</p>
          <a href={result.url} target="_blank" rel="noopener noreferrer">
            公式サイトで確認する
          </a>
        </div>
      )}
    </div>
  );
};

export default PersonalityQuiz;
