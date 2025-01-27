// src/services/apiClient.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Your backend API base URL
  withCredentials: true, // Include cookies with every request
});

export default apiClient;
