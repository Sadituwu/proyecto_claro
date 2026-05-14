<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/services/axios'
import {
    DataAnalysis,
    User,
    TrendCharts,
    CircleCheckFilled
} from '@element-plus/icons-vue'

const loading = ref(false)
const showModal = ref(false)
const result = ref({})

const form = ref({
    Antiguedad_Mes: '',
    Plan_Precio: '',
    Perfil_Pagador: '',
    Cantidad_Lineas: '',
    Claro_Club: 'si',
    Reclamos_Mes: '',
    Reclamos_Resueltos: '',
    DatosGB_Mes: ''
})

function onlyNumbers(value) {
    return value.replace(/[^0-9.]/g, '')
}

function cerrarModal() {
    showModal.value = false
    form.value = {
        Antiguedad_Mes: '',
        Plan_Precio: '',
        Perfil_Pagador: '',
        Cantidad_Lineas: '',
        Claro_Club: 'si',
        Reclamos_Mes: '',
        Reclamos_Resueltos: '',
        DatosGB_Mes: ''
    }
}

async function enviarFormulario() {
    loading.value = true
    showModal.value = false

    try {
        const { data } = await api.post('/predecir', form.value)

        const isValid =
            data &&
            typeof data === 'object' &&
            data.prediccion !== undefined

        if (!isValid) {
            ElMessage.warning('Debes ingresar todos los campos correctamente')
            return
        }

        result.value = data
        showModal.value = true
        ElMessage.success('Predicción ejecutada correctamente')

    } catch (error) {
        ElMessage.error('Ocurrió un error en la predicción')
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="min-h-screen relative overflow-hidden px-4 py-8 md:px-8" style="background: var(--el-bg-color-page)">

        <!-- Glow background -->
        <div class="absolute top-0 left-0 w-96 h-96 bg-blue-500/20 blur-3xl rounded-full"></div>
        <div class="absolute bottom-0 right-0 w-96 h-96 bg-indigo-500/20 blur-3xl rounded-full"></div>

        <div class="max-w-6xl mx-auto relative z-10">

            <!-- HERO -->
            <div class="rounded-[32px] p-8 md:p-10 mb-8 border backdrop-blur-xl shadow-2xl" style="
          background: linear-gradient(135deg, rgba(59,130,246,.15), rgba(99,102,241,.10));
          border-color: var(--el-border-color-light);
        ">
                <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8">

                    <!-- Left -->
                    <div class="max-w-2xl">
                        <div class="flex items-center gap-4 mb-6">
                            <div class="w-16 h-16 rounded-3xl flex items-center justify-center shadow-lg"
                                style="background: linear-gradient(135deg, var(--el-color-primary), #6366f1)">
                                <el-icon :size="30" color="white">
                                    <DataAnalysis />
                                </el-icon>
                            </div>
                            <div>
                                <h1 class="text-4xl font-black tracking-tight"
                                    style="color: var(--el-text-color-primary)">
                                    Modelo IA Predictivo
                                </h1>
                                <p class="mt-1 text-base" style="color: var(--el-text-color-secondary)">
                                    Analiza patrones y comportamiento de clientes.
                                </p>
                            </div>
                        </div>
                        <p class="leading-relaxed text-[15px] max-w-2xl" style="color: var(--el-text-color-regular)">
                            Completa la información solicitada para que el modelo de inteligencia artificial
                            procese automáticamente el perfil del cliente y genere una predicción avanzada
                            basada en sus indicadores.
                        </p>
                    </div>

                    <!-- Right -->
                    <div class="hidden lg:flex">
                        <div class="w-40 h-40 rounded-full flex items-center justify-center border backdrop-blur-xl"
                            style="
                background: rgba(255,255,255,.05);
                border-color: rgba(255,255,255,.08);
              ">
                            <el-icon :size="70" color="#60a5fa">
                                <TrendCharts />
                            </el-icon>
                        </div>
                    </div>

                </div>
            </div>

            <!-- FORM CARD -->
            <div class="rounded-[32px] p-8 md:p-10 border shadow-2xl backdrop-blur-xl" style="
          background: var(--el-bg-color);
          border-color: var(--el-border-color-light);
        ">

                <!-- GRID -->
                <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

                    <div class="field-card">
                        <label class="field-label">Antigüedad (Meses)</label>
                        <el-input v-model="form.Antiguedad_Mes" placeholder="Ej: 24" size="large"
                            @input="form.Antiguedad_Mes = onlyNumbers(form.Antiguedad_Mes)" />
                    </div>

                    <div class="field-card">
                        <label class="field-label">Plan Precio (S/)</label>
                        <el-input v-model="form.Plan_Precio" placeholder="Ej: 89.90" size="large"
                            @input="form.Plan_Precio = onlyNumbers(form.Plan_Precio)" />
                    </div>

                    <div class="field-card">
                        <label class="field-label">Perfil Pagador</label>
                        <el-select v-model="form.Perfil_Pagador" placeholder="Seleccionar" size="large" class="w-full">
                            <el-option label="Crítico" value="critico" />
                            <el-option label="Regular" value="regular" />
                            <el-option label="Excelente" value="excelente" />
                        </el-select>
                    </div>

                    <div class="field-card">
                        <label class="field-label">Cantidad de Líneas</label>
                        <el-input v-model="form.Cantidad_Lineas" placeholder="Ej: 3" size="large"
                            @input="form.Cantidad_Lineas = onlyNumbers(form.Cantidad_Lineas)" />
                    </div>

                    <div class="field-card">
                        <label class="field-label">Claro Club</label>
                        <el-segmented v-model="form.Claro_Club" :options="[
                            { label: 'Sí', value: 'si' },
                            { label: 'No', value: 'no' }
                        ]" block />
                    </div>

                    <div class="field-card">
                        <label class="field-label">Reclamos por Mes</label>
                        <el-input v-model="form.Reclamos_Mes" placeholder="Ej: 2" size="large"
                            @input="form.Reclamos_Mes = onlyNumbers(form.Reclamos_Mes)" />
                    </div>

                    <div class="field-card">
                        <label class="field-label">Reclamos Resueltos</label>
                        <el-input v-model="form.Reclamos_Resueltos" placeholder="Ej: 1" size="large"
                            @input="form.Reclamos_Resueltos = onlyNumbers(form.Reclamos_Resueltos)" />
                    </div>

                    <div class="field-card">
                        <label class="field-label">Datos GB / Mes</label>
                        <el-input v-model="form.DatosGB_Mes" placeholder="Ej: 45" size="large"
                            @input="form.DatosGB_Mes = onlyNumbers(form.DatosGB_Mes)" />
                    </div>

                </div>

                <!-- INFO -->
                <div class="mt-8 rounded-2xl p-5 border flex items-start gap-4" style="
            background: var(--el-fill-color-light);
            border-color: var(--el-border-color-light);
          ">
                    <div class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
                        style="background: rgba(59,130,246,.15)">
                        <el-icon :size="20" color="#60a5fa">
                            <User />
                        </el-icon>
                    </div>
                    <div>
                        <h3 class="font-semibold mb-1" style="color: var(--el-text-color-primary)">
                            Procesamiento Inteligente
                        </h3>
                        <p class="text-sm leading-relaxed" style="color: var(--el-text-color-secondary)">
                            El modelo evaluará automáticamente el perfil del cliente utilizando variables de
                            consumo, reclamos y comportamiento de pago.
                        </p>
                    </div>
                </div>

                <!-- BUTTON -->
                <div class="mt-10 flex justify-end">
                    <el-button type="primary" size="large" round :loading="loading" @click="enviarFormulario"
                        class="button-ia">
                        <el-icon class="mr-2">
                            <CircleCheckFilled />
                        </el-icon>
                        Ejecutar Predicción
                    </el-button>
                </div>

            </div>
        </div>

        <!-- MODAL RESULTADO -->
        <el-dialog v-model="showModal" width="460px" align-center :show-close="false">
            <div class="modal">

                <div class="modal-icon">
                    <el-icon :size="40" color="white">
                        <TrendCharts />
                    </el-icon>
                </div>

                <h2 class="text-xl font-bold" style="color: var(--el-text-color-primary)">
                    Resultado de Predicción
                </h2>
                <p class="text-sm mt-1 mb-5" style="color: var(--el-text-color-secondary)">
                    Análisis completado por el modelo IA
                </p>

                <div class="result-grid">

                    <div class="result-item">
                        <span class="result-label">ID Cliente</span>
                        <span class="result-value">{{ result.cliente_id ?? '—' }}</span>
                    </div>

                    <div class="result-item">
                        <span class="result-label">Predicción</span>
                        <span class="result-badge"
                            :class="result.prediccion === 'Churn' ? 'badge-danger' : 'badge-success'">
                            {{ result.prediccion ?? '—' }}
                        </span>
                    </div>

                    <div class="result-item">
                        <span class="result-label">Confianza</span>
                        <div class="confidence-bar-wrap">
                            <div class="confidence-bar">
                                <div class="confidence-fill" :style="{ width: result.confianza }"></div>
                            </div>
                            <span class="result-value">{{ result.confianza ?? '—' }}</span>
                        </div>
                    </div>

                    <div class="result-item">
                        <span class="result-label">Estabilidad</span>
                        <span class="result-value highlight">{{ result.estabilidad ?? '—' }}</span>
                    </div>

                </div>

                <el-button type="primary" round @click="cerrarModal" class="btn-entendido">
                    <el-icon class="mr-2">
                        <CircleCheckFilled />
                    </el-icon>
                    Entendido
                </el-button>

            </div>
        </el-dialog>

    </div>
</template>

<style scoped>
.field-card {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.field-label {
    font-size: 14px;
    font-weight: 700;
    color: var(--el-text-color-primary);
}

.button-ia {
    padding-inline: 40px;
    height: 52px;
    font-weight: 700;
    letter-spacing: .3px;
    box-shadow: 0 10px 30px rgba(59, 130, 246, .25);
}

/* MODAL */
.modal {
    text-align: center;
    padding: 8px 0;
}

.modal-icon {
    width: 70px;
    height: 70px;
    border-radius: 20px;
    background: linear-gradient(135deg, var(--el-color-primary), #6366f1);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    box-shadow: 0 10px 30px rgba(59, 130, 246, .3);
}

.result-grid {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 24px;
    text-align: left;
}

.result-item {
    background: var(--el-fill-color-light);
    border: 1px solid var(--el-border-color-light);
    border-radius: 14px;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.result-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--el-text-color-secondary);
}

.result-value {
    font-size: 14px;
    font-weight: 700;
    color: var(--el-text-color-primary);
}

.result-value.highlight {
    color: var(--el-color-primary);
}

.result-badge {
    font-size: 13px;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 20px;
}

.badge-success {
    background: rgba(34, 197, 94, .15);
    color: #16a34a;
}

.badge-danger {
    background: rgba(239, 68, 68, .15);
    color: #dc2626;
}

.confidence-bar-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
}

.confidence-bar {
    width: 100px;
    height: 8px;
    background: var(--el-border-color);
    border-radius: 99px;
    overflow: hidden;
}

.confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--el-color-primary), #6366f1);
    border-radius: 99px;
    transition: width .6s ease;
}

.btn-entendido {
    width: 100%;
    height: 48px;
    font-weight: 700;
}

/* Inputs */
:deep(.el-input__wrapper),
:deep(.el-select__wrapper) {
    border-radius: 16px;
    min-height: 50px;
    padding-inline: 14px;
    transition: all .25s ease;
    background: var(--el-fill-color-blank);
    box-shadow: none !important;
    border: 1px solid var(--el-border-color);
}

:deep(.el-input__wrapper:hover), 
:deep(.el-select__wrapper:hover) {
    border-color: var(--el-color-primary-light-5);
}

:deep(.is-focus) {
    border-color: var(--el-color-primary) !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, .12) !important;
}

:deep(.el-segmented) {
    min-height: 50px;
    border-radius: 16px;
    padding: 6px;
}

:deep(.el-select) {
    width: 100%;
}

* {
    transition: background-color .25s ease, border-color .25s ease, color .25s ease;
}
</style>