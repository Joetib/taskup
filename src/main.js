import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

if (process.env.NODE_ENV === "development"){
    axios.defaults.baseURL = 'http://localhost:5000/'
} else {
    axios.defaults.baseURL = 'https://joetib.pythonanywhere.com/'
}
console.log(axios.defaults.baseURL)

createApp(App).use(store).use(router, axios).mount('#app')
