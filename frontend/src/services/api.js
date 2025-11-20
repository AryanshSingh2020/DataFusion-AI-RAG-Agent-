// frontend/src/services/api.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Your backend API URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export const postQuery = (question) => {
  return apiClient.post('/query/', { question });
};