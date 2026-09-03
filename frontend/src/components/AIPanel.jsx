/**
 * AIPanel — simple assistant for querying current city state.
 */

import { useState } from 'react';
import { api } from '../api/client';

const QUICK_QUESTIONS = [
  'What is happening right now?',
  'Why is the risk high?',
  'What should we do?',
  'Which roads are affected?',
];

export default function AIPanel() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleAsk(q) {
    const query = q || question;
    if (!query.trim()) return;

    setLoading(true);
    setAnswer('');
    try {
      const res = await api.askAI(query);
      setAnswer(res.answer);
    } catch {
      setAnswer('Unable to reach the AI service.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="panel ai-panel">
      <h2 className="panel-title">UrbanShield Assistant</h2>
      <div className="ai-quick">
        {QUICK_QUESTIONS.map(q => (
          <button
            key={q}
            className="btn btn-quick"
            onClick={() => { setQuestion(q); handleAsk(q); }}
          >
            {q}
          </button>
        ))}
      </div>
      <div className="ai-input-row">
        <input
          type="text"
          className="ai-input"
          placeholder="Ask about the current situation..."
          value={question}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleAsk()}
        />
        <button
          className="btn btn-ask"
          onClick={() => handleAsk()}
          disabled={loading || !question.trim()}
        >
          {loading ? '...' : 'Ask'}
        </button>
      </div>
      {answer && (
        <div className="ai-response">
          <pre className="ai-response-text">{answer}</pre>
        </div>
      )}
    </div>
  );
}
