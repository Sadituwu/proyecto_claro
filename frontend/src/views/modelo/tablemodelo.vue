<script setup>
import { ref, onMounted, watch } from 'vue'
import { Search, DataAnalysis } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '@/services/axios'
import { debounce } from 'lodash-es'

/* =========================
   STATE
========================= */
const registros = ref([])
const loading = ref(false)

const search = ref('')
const perfilFiltro = ref('')
const sortOrder = ref('desc')

const currentPage = ref(1)
const pageSize = ref(10)

const total = ref(0)

/* =========================
   API
========================= */
async function obtenerClientes() {
    loading.value = true

    try {
        const response = await api.get('/clientes', {
            params: {
                page: currentPage.value,
                limit: pageSize.value,
                search: search.value.trim(),
                perfil: perfilFiltro.value,
                sort: sortOrder.value
            }
        })

        const data = response.data?.data

        registros.value = Array.isArray(data) ? data : []
        total.value = response.data?.total ?? 0

    } catch (error) {
        console.error(error)
        ElMessage.error('Error al cargar registros')
        registros.value = []
    } finally {
        loading.value = false
    }
}

/* =========================
   DEBOUNCE (SEARCH)
========================= */
const fetchDebounced = debounce(() => {
    currentPage.value = 1
    obtenerClientes()
}, 400)

/* =========================
   INIT
========================= */
onMounted(obtenerClientes)

/* =========================
   WATCHES CORRECTOS
========================= */
watch([search, perfilFiltro, sortOrder], () => {
    fetchDebounced()
})

watch([currentPage, pageSize], obtenerClientes)

/* =========================
   PERFIL TAG
========================= */
function getPerfilTag(type) {
    switch (type) {
        case 'bueno':
        case 'excelente': return 'success'
        case 'regular': return 'warning'
        case 'critico': return 'danger'
        default: return 'info'
    }
}
</script>

<template>
    <div class="min-h-screen p-4 md:p-8" style="background: var(--el-bg-color-page)">

        <div class="max-w-7xl mx-auto">

            <!-- HEADER -->
            <div class="rounded-[30px] p-6 md:p-8 mb-6 border shadow-xl"
                style="background: var(--el-bg-color); border-color: var(--el-border-color-light);">

                <div class="flex flex-col lg:flex-row gap-6 lg:items-center lg:justify-between">

                    <div class="flex items-center gap-4">

                        <div class="w-16 h-16 rounded-3xl flex items-center justify-center"
                            style="background: linear-gradient(135deg,var(--el-color-primary),#6366f1);">

                            <el-icon :size="30" color="white">
                                <DataAnalysis />
                            </el-icon>

                        </div>

                        <div>
                            <h1 class="text-3xl font-black">
                                Tabla de Modelos IA
                            </h1>

                            <p class="mt-1 text-gray-500">
                                Visualización inteligente de registros predictivos.
                            </p>
                        </div>

                    </div>

                    <!-- SEARCH -->
                    <div class="w-full lg:w-[340px]">

                        <el-input
                            v-model="search"
                            size="large"
                            placeholder="Buscar clientes..."
                            clearable
                        >
                            <template #prefix>
                                <el-icon>
                                    <Search />
                                </el-icon>
                            </template>
                        </el-input>

                    </div>

                </div>

            </div>

            <!-- FILTERS -->
            <div class="rounded-[28px] p-5 mb-6 border shadow-lg"
                style="background: var(--el-bg-color); border-color: var(--el-border-color-light);">

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">

                    <!-- PERFIL -->
                    <div>
                        <label class="filter-label">Perfil Pagador</label>

                        <el-select v-model="perfilFiltro" clearable class="w-full">
                            <el-option label="Excelente" value="excelente" />
                            <el-option label="Regular" value="regular" />
                            <el-option label="Crítico" value="critico" />
                        </el-select>
                    </div>

                    <!-- SORT -->
                    <div>
                        <label class="filter-label">Ordenar por Precio</label>

                        <el-select v-model="sortOrder" class="w-full">
                            <el-option label="Mayor a menor" value="desc" />
                            <el-option label="Menor a mayor" value="asc" />
                        </el-select>
                    </div>

                    <!-- TOTAL -->
                    <div class="rounded-2xl flex items-center justify-center border"
                        style="background: var(--el-fill-color-light);">

                        <div class="text-center">
                            <div class="text-3xl font-black text-blue-500">
                                {{ total }}
                            </div>
                            <div class="text-sm text-gray-500">
                                Registros encontrados
                            </div>
                        </div>

                    </div>

                </div>

            </div>

            <!-- TABLE -->
            <div class="rounded-[28px] overflow-hidden border shadow-xl"
                style="background: var(--el-bg-color); border-color: var(--el-border-color-light);">

                <el-table
                    :data="registros"
                    stripe
                    v-loading="loading"
                >

                    <el-table-column prop="Cliente" label="Cliente" />
                    <el-table-column prop="Antiguedad_Mes" label="Antigüedad" />
                    <el-table-column prop="Plan_Precio" label="Plan S/" />

                    <el-table-column label="Perfil">
                        <template #default="scope">
                            <el-tag :type="getPerfilTag(scope.row.Perfil_Pagador)">
                                {{ scope.row.Perfil_Pagador }}
                            </el-tag>
                        </template>
                    </el-table-column>

                    <el-table-column prop="Cantidad_Lineas" label="Líneas" />
                    <el-table-column prop="Claro_Club" label="Club" />
                    <el-table-column prop="Reclamos_Mes" label="Reclamos" />
                    <el-table-column prop="Reclamos_Resueltos" label="Resueltos" />
                    <el-table-column prop="DatosGB_Mes" label="GB" />

                    <el-table-column prop="Reclamo_Frecuente" label="Reclamo frecuente" />
                    <el-table-column prop="Razon_Abandono" label="Predicción" />

                </el-table>

            </div>

            <!-- PAGINATION -->
            <div class="mt-6 flex justify-center">

                <el-pagination
                    v-model:current-page="currentPage"
                    v-model:page-size="pageSize"
                    :total="total"
                    :page-sizes="[10, 20, 50]"
                    layout="total, sizes, prev, pager, next"
                />

            </div>

        </div>
    </div>
</template>
<style scoped>
.filter-label {
    display: block;
    margin-bottom: 10px;
    font-size: 14px;
    font-weight: 700;
    color: var(--el-text-color-primary);
}

/* MOBILE CARD */
.mobile-card {
    border-radius: 28px;
    padding: 22px;
    border: 1px solid var(--el-border-color-light);
    background: var(--el-bg-color);
    box-shadow:
        0 10px 30px rgba(0, 0, 0, .06);
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 14px;
    border-radius: 18px;
    background: var(--el-fill-color-light);
}

.info-item span {
    font-size: 12px;
    color: var(--el-text-color-secondary);
}

.info-item strong {
    font-size: 15px;
    color: var(--el-text-color-primary);
}

/* ELEMENT PLUS */
:deep(.el-input__wrapper),
:deep(.el-select__wrapper) {
    min-height: 50px;
    border-radius: 16px;
    border: 1px solid var(--el-border-color);
    background: var(--el-fill-color-blank);
    box-shadow: none !important;
}

:deep(.el-input__wrapper:hover),
:deep(.el-select__wrapper:hover) {
    border-color: var(--el-color-primary-light-5);
}

:deep(.is-focus) {
    border-color: var(--el-color-primary) !important;
    box-shadow:
        0 0 0 4px rgba(59, 130, 246, .12) !important;
}

/* TABLE */
:deep(.el-table) {
    background: transparent !important;
    color: var(--el-text-color-primary);
}

:deep(.el-table tr),
:deep(.el-table th.el-table__cell),
:deep(.el-table td.el-table__cell) {
    background: transparent !important;
}

:deep(.el-table__header-wrapper th) {
    font-weight: 700;
    color: var(--el-text-color-primary);
}

:deep(.el-pagination button),
:deep(.el-pager li) {
    border-radius: 12px !important;
}

/* TRANSITIONS */
* {
    transition:
        background-color .25s ease,
        border-color .25s ease,
        color .25s ease;
}
</style>