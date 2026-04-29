import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import { useDarkMode } from './composables/useDarkMode';
import 'element-plus/theme-chalk/dark/css-vars.css';
import 'element-plus/dist/index.css'
import router from './router'
import './style.css'
import App from './App.vue'

const app = createApp(App)
const { isDark } = useDarkMode();
document.documentElement.classList.toggle("dark", isDark.value);
app.use(router)
app.use(ElementPlus)
app.mount('#app')