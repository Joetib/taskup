import axios from 'axios'
import { createStore } from 'vuex'

export default createStore({
  state: {
    is_loading: false,
    isAuthenticated: false,
    token: '',
    username: '',
    password: '',
    projects: [],
  },
  mutations: {
    updateToken(state, newToken) {
      state.token = newToken
      localStorage.setItem('token', newToken)
      if (newToken !== null && newToken.length > 1) {
        state.isAuthenticated = true
      }
      axios.defaults.headers.common['Authorization'] = "Bearer " + state.token;
    },
    updateUsername(state, newUsername) {
      state.username = newUsername;
    },
    updateisAuthenticated(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated;
    },
    fetchProjects(state) {
      state.is_loading = true
      axios.get('/projects/').then(resp => {
        state.projects = resp.data.all_projects;
        console.log(state.projects)
        state.is_loading = false
      }).catch(e => {
        console.error(e.resp);
        state.is_loading = false
      });
    },
    initializeStore(state) {
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.username = localStorage.getItem('username')
        axios.defaults.headers.common['Authorization'] = "Bearer " + state.token;

      }
    },
    logout(state){
      localStorage.removeItem('token');
      state.token = null
    },
    setIsLoading(state, value){
      state.is_loading = value

    },
  },
  actions: {
  },
  modules: {
  }
})
