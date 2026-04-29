<script setup>
import api from '@/services/axios'
import bg from '@/assets/logos-login/fondo-login2.jpg'
import { useRouter, useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import { Message, Lock } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

document.title = 'Iniciar Sesión'

const email = ref('')
const password = ref('')
const isLoggingIn = ref(false)

const router = useRouter()
const route = useRoute()
const url = route.query.url

async function handleLogin() {
  if (isLoggingIn.value) return
  isLoggingIn.value = true

  try {
    const res = await api.post('/login', {
      email: email.value,
      password: password.value
    })

    localStorage.setItem('access_token', res.data.access_token)

    const user = await fetchUser()
    localStorage.setItem('user', JSON.stringify(user))

    router.push({ name: 'Dashboard' })

  } catch (error) {
    const code = error?.response?.data?.code

    if (code === 'email_not_verified') {
      router.push({
        name: 'VerifyEmail',
        query: { email: email.value, onload: true }
      })
      ElMessage.warning('Tu correo aún no ha sido verificado.')
    } else {
      ElMessage.error('Credenciales incorrectas.')
    }
  } finally {
    isLoggingIn.value = false
  }
}

async function fetchUser() {
  try {
    const { data } = await api.get('/me')
    return data
  } catch {
    return null
  }
}

async function confirmEmail() {
  if (!url) return

  try {
    await axios.get(url)
    ElMessage.success('Correo verificado correctamente.')
  } catch {
    ElMessage.error('El enlace expiró o es inválido.')
  }
}

onMounted(() => {
  confirmEmail()
})
</script>

<template>
  <div class="login-layout">

    <!-- IZQUIERDA (IMAGEN) -->
    <div class="login-left" :style="{ backgroundImage: `url(${bg})` }"></div>

    <!-- DERECHA (FORM + FONDO FUTURISTA) -->
    <div class="login-right">

      <div class="login-box">
        <h2 class="title">Bienvenido</h2>
        <p class="subtitle">Accede a tu Modelo IA</p>

        <el-form @submit.prevent="handleLogin" class="login-form">

          <el-input v-model="email" type="email" placeholder="Correo " :prefix-icon="Message"
            size="large" />

          <el-input v-model="password" type="password" placeholder="Contraseña" :prefix-icon="Lock" size="large"
            show-password />

          <el-button type="primary" native-type="submit" size="large" class="login-btn" :loading="isLoggingIn">
            Ingresar
          </el-button>

        </el-form>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* LAYOUT GENERAL */
.login-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
}

/* IZQUIERDA - IMAGEN */
.login-left {
  background: url("./assets/logos-login/fondo-login.jpg") center/cover no-repeat;
}

/* DERECHA - FONDO FUTURISTA */
.login-right {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;

  background: radial-gradient(circle at 20% 20%, #6366f1, transparent 40%),
    radial-gradient(circle at 80% 70%, #9333ea, transparent 40%),
    #0f172a;
}

/* EFECTO GLOW */
.login-right::before {
  content: "";
  position: absolute;
  width: 400px;
  height: 400px;
  background: #6366f1;
  filter: blur(120px);
  opacity: 0.2;
}

/* FORM BOX (GLASS) */
.login-box {
  position: relative;
  z-index: 2;

  width: 100%;
  max-width: 400px;
  padding: 2rem;
  border-radius: 16px;

  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(14px);

  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}

/* TITULOS */
.title {
  
  font-size: 1.8rem;
  font-weight: 600;
  color: #fff;
}

.subtitle {
  font-size: 0.9rem;
  color: #cbd5f5;
  margin-bottom: 1.5rem;
}

/* FORM */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* INPUTS */
:deep(.el-input__wrapper) {
  border-radius: 10px;
}

/* BOTON */
.login-btn {
  margin-top: 10px;
  border-radius: 10px;
  font-weight: 500;
}

/* RESPONSIVE */
@media (max-width: 900px) {
  .login-layout {
    grid-template-columns: 1fr;
  }

  .login-left {
    display: none;
  }
}
</style>