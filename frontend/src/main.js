import { createApp } from 'vue'
import { inject } from '@vercel/analytics'
import App from './App.vue'

// Inject Vercel Analytics
inject()

createApp(App).mount('#app')
