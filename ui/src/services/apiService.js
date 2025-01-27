// src/services/apiService.js
import apiClient from './apiClient';

// export const getUserInfo = async () => {
//   return await apiClient.get('/accounts/user/');
  
// };

export const getBalance = async () => {
  return await apiClient.get('/transactions/balance/');
};

export const loginUser = async (credentials) => {
  return await apiClient.post('/accounts/login/', credentials);
};

