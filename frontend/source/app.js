import React, { useState } from 'react';
import { extractInsights } from './api';

function App() {
  const [input, setInput] = useState('');
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result = await extractInsights(input);
      setInsights(result);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Paste your text here..."
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Extracting...' : 'Extract Insights'}
        </button>
      </form>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {insights && (
        <div>
          <h2>Key Insights</h2>
          <pre>{JSON.stringify(insights, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;