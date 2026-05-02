<script>
export default {
  data() {
    return {
      currentYear: new Date().getFullYear()
    }
  }
}
</script>

<template>
    <el-footer class="h-10">
        <el-row class="h-full justify-end items-center">
          <el-text>Todos los derechos reservados © <strong>{{ currentYear }} BIGDAVI S.A.C.</strong></el-text>
        </el-row>
      </el-footer>
</template>