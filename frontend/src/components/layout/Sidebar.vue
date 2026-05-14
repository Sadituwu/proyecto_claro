<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElButton, ElIcon } from 'element-plus'
import { DArrowLeft, DArrowRight } from '@element-plus/icons-vue'
import { menuItems } from '@/router/menu.js'

const route = useRoute()

const activeMenu = ref('')

const isCollapsed = ref(JSON.parse(localStorage.getItem('sidebarCollapsed')) || false)

const drawerVisible = ref(false)

const isMobile = ref(window.innerWidth <= 768)

const updateIsMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

window.addEventListener('resize', updateIsMobile) 

const user = JSON.parse(localStorage.getItem('user') || '{}')

const filteredMenu = computed(() => {
  return menuItems.filter(item => item.roles.includes(user?.rol) || 'guest')
})

const findActiveMenu = (currentPath) => {
  for (const item of filteredMenu.value) {
    if (item.children) {
      for (const child of item.children) {
        if (child.routeName === currentPath) {
          return child.routeName
        }
        if (child.matchRoutes?.some(matchRoute => currentPath.includes(matchRoute))) {
          return child.routeName
        }
      }
    } else {
      if (item.routeName === currentPath) {
        return item.routeName
      }
      if (item.matchRoutes?.some(matchRoute => currentPath.includes(matchRoute))) {
        return item.routeName
      }
    }
  }
  return currentPath
}

watch(() => route.path, (newPath) => {
  activeMenu.value = findActiveMenu(newPath)
  localStorage.setItem('activeMenu', activeMenu.value)
}, { immediate: true })

watch(isCollapsed, (newVal) => {
  localStorage.setItem('sidebarCollapsed', JSON.stringify(newVal))
})

onMounted(() => {
  activeMenu.value = findActiveMenu(route.path)
})
</script>

<template>
  <el-aside v-if="!isMobile" :width="isCollapsed ? '64px' : '230px'"
    class="transition-all duration-300 bg-[var(--el-bg-color)]">
    <div class="p-3 flex items-center gap-3">
      <div v-show="!isCollapsed" class="flex-1 text-center">
        <router-link to="/dashboard">
          <img src="@/assets/sistema/logo-dashboard.png" alt="Logo-CLaro" class="w-[180px] mx-auto" />
        </router-link>
      </div>
      <el-button @click="isCollapsed = !isCollapsed" :class="isCollapsed ? 'rotate-180' : ''" :icon="DArrowLeft" />
    </div>
    <div>
      <el-menu :router="true" :default-active="activeMenu" :collapse="isCollapsed" class="border-none sidebar-menu"
        style="background-color: var(--el-bg-color); color: var(--el-text-color-regular);"
        active-text-color="var(--el-color-primary)" @select="activeMenu = $event">
        <template v-for="item in filteredMenu" :key="item.title">
          <el-sub-menu v-if="item.children" :index="item.title">
            <template #title>
              <el-icon>
                <component :is="item.icon" />
              </el-icon>
              <span>{{ item.title }}</span>
            </template>
            <el-menu-item v-for="child in item.children" :key="child.routeName" :index="child.routeName">
              <el-icon>
                <component :is="child.icon" />
              </el-icon>
              {{ child.title }}
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item v-else :index="item.routeName">
            <el-icon>
              <component :is="item.icon" />
            </el-icon>
            <span>{{ item.title }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </div>
  </el-aside>
  <!-- ------ MÓVIL ------ -->
  <el-drawer v-else v-model="drawerVisible" :with-header="false" size="230px" direction="ltr">
    <div class="p-3 flex items-center gap-3">
      <div class="flex-1 text-center">
        <router-link to="/dashboard" @click="drawerVisible = false">
          <img src="" alt="SENATI Logo" class="w-[180px] mx-auto" />
        </router-link>
      </div>
      <el-button @click="drawerVisible = false" :icon="DArrowLeft" />
    </div>
    <el-menu :router="true" :default-active="activeMenu" class="border-none sidebar-menu"
      style="background-color: var(--el-bg-color); color: var(--el-text-color-regular);"
      active-text-color="var(--el-color-primary)" @select="(key) => { activeMenu = key; drawerVisible = false }">
      <template v-for="item in filteredMenu" :key="item.title">
        <!-- SUBMENU EN MÓVIL -->
        <el-sub-menu v-if="item.children" :index="item.title">
          <template #title>
            <el-icon>
              <component :is="item.icon" />
            </el-icon>
            <span>{{ item.title }}</span>
          </template>
          <el-menu-item v-for="child in item.children" :key="child.routeName" :index="child.routeName">
            <el-icon>
              <component :is="child.icon" />
            </el-icon>
            <span>{{ child.title }}</span>
          </el-menu-item>
        </el-sub-menu>
        <!-- ITEM NORMAL -->
        <el-menu-item v-else :index="item.routeName">
          <el-icon>
            <component :is="item.icon" />
          </el-icon>
          <span>{{ item.title }}</span>
        </el-menu-item>
      </template>
    </el-menu>
  </el-drawer>
  <el-button v-if="isMobile" class="fixed top-4 left-4 z-50" @click="drawerVisible = true" :icon="DArrowRight" />
</template>

<style scoped>
.el-menu {
  border-right: none;
  height: 100%;
  overflow: hidden;
}

.el-aside {
  border-right: 2px solid var(--el-menu-border-color);
}

.sidebar-menu {
  overflow-y: auto;
}

.el-menu--collapse {
  overflow: hidden !important;
}
</style>