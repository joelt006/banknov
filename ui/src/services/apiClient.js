import axios from 'axios';
import router from '@/router';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  withCredentials: true,
});

// Attach Bearer token to every request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// On 401 clear stale token and redirect to login
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      router.push('/Login');
    }
    return Promise.reject(error);
  }
);

export default apiClient;
