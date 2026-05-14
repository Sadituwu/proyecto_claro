<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, SwitchButton, Moon, Sunny, WarningFilled } from '@element-plus/icons-vue'
import { useDarkMode } from "@/composables/useDarkMode"
import { ElMessage } from 'element-plus'
import api from '@/services/axios'

const router = useRouter()

const user = JSON.parse(localStorage.getItem('user') || '{}')
const { isDark, toggleDarkMode } = useDarkMode()

const logoutDialogVisible = ref(false)
const isLoggingOut = ref(false)

async function logout() {
  isLoggingOut.value = true

  localStorage.clear()

  ElMessage.success('Sesión cerrada exitosamente')

  isLoggingOut.value = false
  logoutDialogVisible.value = false

  router.push({ name: 'Login' })
}

function showLogoutDialog() {
  logoutDialogVisible.value = true
}

function cancelLogout() {
  logoutDialogVisible.value = false 
}

function handleCommand(command) {
  switch (command) {
    case 'profile':
      router.push({ name: 'UserPerfil' })
      break
    case 'logout':
      showLogoutDialog()
      break
  }
}

</script>

<template>
  <el-header class="flex items-center justify-end gap-4">
    <el-dropdown @command="handleCommand">
      <span class="el-dropdown-link flex items-center cursor-pointer outline-none hover:bg-transparent">
        <el-icon class="mr-1">
          <User />
        </el-icon>
        {{ user.rol }}
      </span>

      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item divided>
            <div class="flex items-center gap-2">
              <el-switch v-model="isDark" inline-prompt :active-icon="Moon" :inactive-icon="Sunny"
                @change="toggleDarkMode" />
              <span>Modo noche</span>
            </div>
          </el-dropdown-item>

          <el-dropdown-item divided command="logout">
            <el-icon class="mr-1">
              <SwitchButton />
            </el-icon>
            Cerrar sesión
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>

    <el-dialog v-model="logoutDialogVisible" width="450px" align-center :close-on-click-modal="false"
      :close-on-press-escape="false">
      <div class="text-center py-4">
        <div class="flex justify-center mb-4">
          <img src="@/assets/sistema/logo-dashboard.png" alt="Logout-claro" class="w-[180px] mx-auto" />
        </div>
        <h2 class="text-xl font-bold mb-2" style="color: var(--el-text-color-primary)">
          ¿Seguro que deseas salir del sistema?
        </h2>
        <p class="text-sm" style="color: var(--el-text-color-secondary)">
          Tu sesión actual se cerrará
        </p>
      </div>

      <template #footer>
        <div class="flex gap-2 justify-center">
          <el-button @click="cancelLogout" :disabled="isLoggingOut" size="large">
            No
          </el-button>
          <el-button type="danger" @click="logout" :loading="isLoggingOut" size="large">
            Sí, cerrar
          </el-button>
        </div>
      </template>
    </el-dialog>
  </el-header>
</template>

<style scoped>
.el-header {
  border-bottom: 2px solid var(--el-menu-border-color);
  padding: 0px 16px;
  font-size: 12px;
  text-align: right;
}
</style>