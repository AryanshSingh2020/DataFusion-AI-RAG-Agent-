// frontend/src/components/charts/ChartRenderer.jsx
import React from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF', '#FF4560'];

function ChartRenderer({ chartData }) {
  if (!chartData || !chartData.data) return <p>No chart data available.</p>;

  switch (chartData.type) {
    case 'pie':
      return (
        <ResponsiveContainer width="100%" height={350}>
          <PieChart>
            <Pie data={chartData.data} cx="50%" cy="50%" labelLine={false} outerRadius={120} fill="#8884d8" dataKey="value" nameKey="name" label>
              {chartData.data.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      );

    case 'bar':
      return (
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={chartData.data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      );

    // Add case for 'line' chart here for portfolio growth queries

    default:
      return <p>Unsupported chart type: {chartData.type}</p>;
  }
}

export default ChartRenderer;