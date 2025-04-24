/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

import axios from 'axios'
axios.defaults.baseURL = import.meta.env.VITE_API_ROOT;
axios.defaults.withCredentials = true;

import { showApiErrorMessage } from '@/stores/messages';
axios.interceptors.response.use((response) => {
    return response;
  }, (error) => {
    error.message = showApiErrorMessage(error);
    throw error
});

const app = createApp(App)

registerPlugins(app)

app.mount('#app')
