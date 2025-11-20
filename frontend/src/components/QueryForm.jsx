// frontend/src/components/QueryForm.jsx
import React, { useState } from 'react';

function QueryForm({ onQuerySubmit, isLoading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    onQuerySubmit(query);
  };

  return (
    <form onSubmit={handleSubmit} className="query-form">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="e.g., Who are the top 5 clients by portfolio value?"
        disabled={isLoading}
      />
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Analyzing...' : 'Ask'}
      </button>
    </form>
  );
}

export default QueryForm;