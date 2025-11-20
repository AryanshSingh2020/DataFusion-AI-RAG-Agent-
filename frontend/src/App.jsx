// frontend/src/App.jsx
import React, { useState } from 'react';
import QueryForm from './components/QueryForm';
import ResponseDisplay from './components/ResponseDisplay';
import { postQuery } from './services/api';
import './App.css';

function App() {
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleQuerySubmit = async (query) => {
    setIsLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await postQuery(query);
      setResponse(res.data);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'An unexpected error occurred. Please check the backend console.';
      setError(errorMessage);
      console.error("API Error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Valuefy</h1>
        <h2>Natural Language Data Query Agent</h2>
      </header>
      <main>
        <QueryForm onQuerySubmit={handleQuerySubmit} isLoading={isLoading} />
        <div className="response-area">
          {isLoading && <div className="loader"></div>}
          {error && <div className="error-message">Error: {error}</div>}
          {response && <ResponseDisplay response={response} />}
        </div>
      </main>
      <footer className="App-footer">
        <p>Valuefy RAG Technical Assignment</p>
      </footer>
    </div>
  );
}

export default App;