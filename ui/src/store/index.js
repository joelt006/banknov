import { createStore } from 'vuex';
import apiClient from '../services/apiClient'; 


export default createStore({
  state: {
    user: null,
    token: null,
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await apiClient.post('/accounts/login/', credentials);
        const token = response.data.token;
        commit('setToken', token);

        const userInfo = await apiClient.get('/accounts/user/');
        commit('setUser', userInfo.data);

        return token;
      } catch (error) {
        console.error('Login failed', error);
        throw error;
      }
    },
    logout({ commit }) {
      commit('setUser', null);
      commit('setToken', null);
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
    getUser: (state) => state.user,
  },
});
