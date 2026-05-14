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

async function handleLogin() {
  if (isLoggingIn.value) return

  isLoggingIn.value = true

  try {
    const res = await api.post('/login', {
      username: email.value,
      password: password.value
    })

    console.log(res.data)

    localStorage.setItem('user', JSON.stringify(res.data))

    router.push({ name: 'Modelo' })

  } catch (error) {
    console.error(error)

    ElMessage.error('Credenciales incorrectas.')
  } finally {
    isLoggingIn.value = false
  }
}

</script>

<template>
  <div class="login-wrap">
    <div class="login-img" :style="{ backgroundImage: `url(${bg})` }">
      <div class="login-img__overlay">
        <h1>Inteligencia al<br><span>servicio tuyo</span></h1>
        <p>Accede a modelos de IA de última generación.</p>
      </div>
    </div>
    <!-- Panel formulario -->
    <div class="login-panel">
      <el-card class="login-card" shadow="never">
        <div class="login-card__header">
          <el-avatar :size="48" class="login-avatar">
            <el-icon :size="24">
              <Lock />
            </el-icon>
          </el-avatar>
          <h2 class="el-text is-bold" style="font-size: 1.4rem">Bienvenidos a todos</h2>
          <p class="el-text el-text--info" style="font-size: 0.85rem">Accede a tu modelo IA</p>
        </div>
        <el-form @submit.prevent="handleLogin" class="login-form">
          <el-form-item>
            <el-input v-model="email" placeholder="Correo electrónico" :prefix-icon="Message" size="large" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="password" type="password" placeholder="Contraseña" :prefix-icon="Lock" size="large"
              show-password />
          </el-form-item>
          <el-button type="primary" native-type="submit" size="large" :loading="isLoggingIn"
            style="width: 100%; border-radius: 10px">
            Ingresar
          </el-button>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.login-wrap {
  display: flex;
  min-height: 100vh;
}

/* ── Imagen ── */
.login-img {
  display: none;
  flex: 1;
  background: center / cover no-repeat;
  position: relative;
}

@media (min-width: 900px) {
  .login-img {
    display: block;
  }
}

.login-img__overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 3rem;
  background: linear-gradient(to top, rgba(15, 23, 42, .85) 30%, transparent);
  color: #fff;
}

.login-img__overlay h1 {
  font-size: clamp(1.8rem, 3vw, 2.8rem);
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: .75rem;
}

.login-img__overlay h1 span {
  color: #a5b4fc;
}

.login-img__overlay p {
  color: rgba(255, 255, 255, .6);
  font-size: .9rem;
}

/* ── Panel ── */
.login-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
}

/* ── Card ── */
.login-card {
  width: 100%;
  max-width: 400px;
  border-radius: 16px !important;
}

.login-card__header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: .5rem;
  margin-bottom: 1.75rem;
  text-align: center;
}

.login-avatar {
  background-color: var(--el-color-primary) !important;
  color: #fff !important;
  margin-bottom: .5rem;
}

/* ── Form ── */
.login-form .el-form-item {
  margin-bottom: 1rem;
}
</style>