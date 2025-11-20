// frontend/src/components/DataTable.jsx
import React from 'react';

function DataTable({ tableData }) {
  if (!tableData || !tableData.rows || tableData.rows.length === 0) {
    return <p>No data to display in the table.</p>;
  }

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            {tableData.headers.map((header, index) => <th key={index}>{header}</th>)}
          </tr>
        </thead>
        <tbody>
          {tableData.rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, cellIndex) => <td key={cellIndex}>{typeof cell === 'boolean' ? cell.toString() : cell}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataTable;