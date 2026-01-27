import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

// pinia에서 persistedstate 플러그인을 사용할 것이다.
const app = createApp(App)

const pinia = app.use(createPinia())
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.mount('#app')
