import axios from 'axios';
import router from '@/router';

const adminApiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  withCredentials: true,
});

adminApiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('adminToken');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

adminApiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      localStorage.removeItem('adminToken');
      localStorage.removeItem('adminUsername');
      router.push('/AdminLogin');
    }
    return Promise.reject(error);
  }
);

export default adminApiClient;
