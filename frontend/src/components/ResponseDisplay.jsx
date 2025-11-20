// frontend/src/components/ResponseDisplay.jsx
import React from 'react';
import DataTable from './DataTable';
import ChartRenderer from './charts/ChartRenderer';

function ResponseDisplay({ response }) {
  if (!response) return null;

  switch (response.type) {
    case 'text':
      return <div className="response-text">{response.content.answer}</div>;
    case 'table':
      return <DataTable tableData={response.content} />;
    case 'chart':
      return <ChartRenderer chartData={response.content} />;
    default:
      return <p>Received an unknown response format.</p>;
  }
}

export default ResponseDisplay;