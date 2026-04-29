<script setup>
import Sidebar from '@/components/layout/Sidebar.vue'
import Header from '@/components/layout/Header.vue'
import Footer from '@/components/layout/Footer.vue'
</script>

<template>
  <el-container>
    <Sidebar />

    <el-container class="el-container-vertical bg-[var(--el-bg-color)]">
      <Header />

      <el-main>
        <router-view />
      </el-main>

      <Footer />
    </el-container>
  </el-container>
</template>

<style scoped>
.el-container-vertical {
  flex-direction: column;
  min-height: 100vh;
}
</style>
