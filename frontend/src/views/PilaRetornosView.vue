<script setup>
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import { useToast } from '../composables/useToast'
import { api } from '../services/api'
import Paginacion from '../components/pagination.vue'
import {
    Square3Stack3DIcon, ArrowPathIcon, ClockIcon,
    HashtagIcon, ClipboardDocumentListIcon,
    MagnifyingGlassIcon, ArrowLeftEndOnRectangleIcon,
    CheckCircleIcon, LockClosedIcon, ShieldExclamationIcon,
    TrashIcon, XMarkIcon, ExclamationTriangleIcon, CheckBadgeIcon
} from '@heroicons/vue/24/outline'

const devoluciones = ref([])
const despachos = ref([])
const componentes = ref([])
const cargando = ref(true)
const procesando = ref(false)
const mostrarPanel = ref(false)
const { showToast } = useToast()

const despachoSeleccionado = ref(null)
const cantidadARetornar = ref(1)

// Estado del Modal de Eliminación
const modalEliminar = ref({ mostrar: false, id: null })

// --- SISTEMA DE TRACKING DE INTEGRIDAD (Anti-Inflación) ---
// Guardamos en la memoria del navegador lo que ya se procesó para llevar la cuenta
const historicoRetornos = ref(JSON.parse(localStorage.getItem('voltstock_historial_retornos')) || {})

const getCantidadDisponible = (d) => {
    // 1. ¿Cuánto se ha procesado y sumado al inventario?
    const procesado = historicoRetornos.value[d.id] || 0
    // 2. ¿Cuánto está ahorita en la pila esperando?
    const enPila = devoluciones.value
        .filter(dev => dev.motivo?.includes(`[REF:${d.id}]`))
        .reduce((sum, dev) => sum + dev.cantidad, 0)

    // 3. El saldo real
    return d.cantidad - procesado - enPila
}

// --- Paginación PILA ---
const paginaPila = ref(1)
const itemsPorPaginaPila = 6

// --- Paginación y Filtros PANEL ---
const busquedaPanel = ref('')
const fechaPanel = ref('')
const paginaPanel = ref(1)
const itemsPorPaginaPanel = 6

const cargarDatos = async () => {
    cargando.value = true
    try {
        const [resDev, resHist, resComp] = await Promise.all([
            api('devoluciones/'),
            api('historial/'),
            api('componentes/')
        ])
        if (resDev.ok) devoluciones.value = await resDev.json()
        if (resComp.ok) componentes.value = await resComp.json()
        if (resHist.ok) {
            const data = await resHist.json()
            despachos.value = data.filter(h => h.tipo === 'SALIDA')
        }
    } catch (err) {
        if (err !== 'Sesión expirada') showToast("Error al cargar datos", "error")
    } finally {
        cargando.value = false
    }
}

// Computadas de Paginación PILA
const totalPaginasPila = computed(() => Math.ceil(devoluciones.value.length / itemsPorPaginaPila) || 1)
const devolucionesPaginadas = computed(() => {
    const inicio = (paginaPila.value - 1) * itemsPorPaginaPila
    return devoluciones.value.slice(inicio, inicio + itemsPorPaginaPila)
})
watch(devoluciones, () => { if (paginaPila.value > totalPaginasPila.value) paginaPila.value = 1 })

// Lógica LIFO
const reingresarUltimo = async () => {
    if (devoluciones.value.length === 0) return
    const topDev = devoluciones.value[0] // Guardamos qué estamos procesando

    procesando.value = true
    try {
        const res = await api('devoluciones/', { method: 'DELETE' })
        if (res.ok) {
            showToast("Componente sumado al stock.", "success")

            // REGISTRO DE TRACKING: Sumamos al historial local para que el despacho pierda saldo
            const match = topDev.motivo?.match(/\[REF:(\d+)\]/)
            if (match) {
                const id = match[1]
                historicoRetornos.value[id] = (historicoRetornos.value[id] || 0) + topDev.cantidad
                localStorage.setItem('voltstock_historial_retornos', JSON.stringify(historicoRetornos.value))
            }

            await cargarDatos()
        }
    } finally {
        procesando.value = false
    }
}

// Mostrar el Modal bonito
const solicitarEliminacion = (id) => {
    modalEliminar.value = { mostrar: true, id }
}

// Cancelar un retorno (Lo borra sin sumar stock)
const confirmarEliminacion = async () => {
    const id = modalEliminar.value.id
    modalEliminar.value.mostrar = false

    try {
        const res = await api('devoluciones/', {
            method: 'DELETE',
            body: JSON.stringify({ cancelar_id: id })
        })
        if (res.ok) {
            showToast("Retorno cancelado de la pila.", "success")
            await cargarDatos()
        }
    } catch (err) {
        showToast("Error al cancelar", "error")
    }
}

// Paginación PANEL
const despachosFiltrados = computed(() => {
    return despachos.value.filter(d => {
        const coincideTexto = d.componente_nombre.toLowerCase().includes(busquedaPanel.value.toLowerCase()) ||
            d.usuario_nombre.toLowerCase().includes(busquedaPanel.value.toLowerCase())
        const coincideFecha = fechaPanel.value === '' || d.fecha.startsWith(fechaPanel.value)
        return coincideTexto && coincideFecha
    })
})
const totalPaginasPanel = computed(() => Math.ceil(despachosFiltrados.value.length / itemsPorPaginaPanel) || 1)
const despachosPaginados = computed(() => {
    const inicio = (paginaPanel.value - 1) * itemsPorPaginaPanel
    return despachosFiltrados.value.slice(inicio, inicio + itemsPorPaginaPanel)
})
watch([busquedaPanel, fechaPanel], () => { paginaPanel.value = 1 })

const seleccionarDespacho = (despacho) => {
    const disponible = getCantidadDisponible(despacho)
    if (disponible <= 0) return // Bloqueado

    despachoSeleccionado.value = despachoSeleccionado.value?.id === despacho.id ? null : despacho
    cantidadARetornar.value = 1
}

const enviarAPilaDesdeHistorial = async (despacho) => {
    const disponible = getCantidadDisponible(despacho)

    // Validaciones Anti-Errores
    if (cantidadARetornar.value <= 0) {
        return showToast("La cantidad no puede ser 0 o negativa.", "error")
    }
    if (cantidadARetornar.value > disponible) {
        return showToast(`Máximo permitido: ${disponible} unidades.`, "error")
    }

    const comp = componentes.value.find(c => c.nombre === despacho.componente_nombre)
    if (!comp) return showToast("Componente no encontrado.", "error")

    try {
        const res = await api('devoluciones/', {
            method: 'POST',
            body: JSON.stringify({
                componente: comp.id,
                cantidad: cantidadARetornar.value,
                motivo: `[REF:${despacho.id}] Retorno de ${despacho.usuario_nombre}`
            })
        })
        if (res.ok) {
            showToast("Añadido a la Pila de Retornos", "success")
            despachoSeleccionado.value = null
            await cargarDatos()
        }
    } catch (err) {
        showToast("Error al enviar a pila", "error")
    }
}

const formatearFecha = (fechaISO) => {
    return new Date(fechaISO).toLocaleString('es-GT', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })
}

const manejarTeclado = (e) => {
    if (!modalEliminar.value.mostrar) return

    if (e.key === 'Escape') {
        modalEliminar.value.mostrar = false
    }
    if (e.key === 'Enter') {
        confirmarEliminacion()
    }
}

onMounted(() => {
    cargarDatos()
    window.addEventListener('keydown', manejarTeclado) // Escuchar teclado
})

onUnmounted(() => {
    window.removeEventListener('keydown', manejarTeclado) // Limpiar al salir de la vista
})

onMounted(cargarDatos)
</script>

<template>
    <div
        class="w-full bg-slate-50 text-slate-700 font-sans p-2 sm:p-6 min-h-[80vh] flex flex-col items-center animate-fade-in relative">

        <div class="w-full max-w-[1300px] flex flex-col lg:flex-row items-start gap-6 relative">

            <div :class="['transition-all duration-500 ease-in-out w-full', mostrarPanel ? 'lg:w-[60%]' : 'lg:w-full']">

                <header
                    class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-[24px] shadow-sm border border-slate-100 mb-6">
                    <div class="flex items-center gap-4">
                        <div
                            class="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center shrink-0">
                            <Square3Stack3DIcon class="w-6 h-6" />
                        </div>
                        <div>
                            <h1 class="text-2xl font-black text-slate-800 tracking-tight">Pila de Retornos</h1>
                            <p class="text-slate-500 text-sm font-medium mt-0.5">Control LIFO y auditoría.</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <button @click="mostrarPanel = !mostrarPanel"
                            :class="['px-4 py-2.5 rounded-xl font-bold text-sm flex items-center gap-2 transition-all',
                                mostrarPanel ? 'bg-slate-100 text-slate-600 hover:bg-slate-200' : 'bg-emerald-600 text-white shadow-md shadow-emerald-200 hover:bg-emerald-700']">
                            <ClipboardDocumentListIcon class="w-5 h-5" />
                            <span class="hidden sm:inline">{{ mostrarPanel ? 'Ocultar Despachos' : 'Buscar Despachos'
                            }}</span>
                        </button>
                        <button @click="cargarDatos"
                            class="p-2.5 bg-slate-50 rounded-xl hover:bg-emerald-50 text-slate-400 hover:text-emerald-600 transition-all border border-slate-100">
                            <ArrowPathIcon :class="['w-5 h-5', cargando ? 'animate-spin' : '']" />
                        </button>
                    </div>
                </header>

                <div v-if="cargando" class="flex justify-center py-20 bg-white rounded-[24px] border border-slate-100">
                    <div
                        class="animate-spin rounded-full h-12 w-12 border-4 border-emerald-100 border-t-emerald-600 mb-3">
                    </div>
                </div>

                <div v-else-if="devoluciones.length === 0"
                    class="bg-white rounded-[24px] border-2 border-dashed border-slate-200 p-16 text-center shadow-sm">
                    <CheckCircleIcon class="w-14 h-14 text-emerald-300 mx-auto mb-4" />
                    <h3 class="text-xl font-black text-slate-800 mb-2">Pila Vacía</h3>
                    <p class="text-slate-500 text-sm">No hay devoluciones pendientes.</p>
                </div>

                <div v-else class="flex flex-col gap-0 items-center">
                    <transition-group name="pila" tag="div" class="w-full relative flex flex-col">
                        <div v-for="(dev, i) in devolucionesPaginadas" :key="dev.id"
                            :class="['w-full transition-all duration-500 relative', i === 0 && paginaPila === 1 ? 'z-20 scale-100' : 'z-10 -mt-4 opacity-90 scale-[0.98]']">

                            <div
                                :class="['bg-white p-5 rounded-[24px] shadow-lg border flex flex-col sm:flex-row gap-4 sm:items-center justify-between',
                                    i === 0 && paginaPila === 1 ? 'border-emerald-300 ring-4 ring-emerald-50' : 'border-slate-200 shadow-sm']">

                                <div class="flex items-center gap-4">
                                    <div
                                        :class="['w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 font-black text-lg',
                                            i === 0 && paginaPila === 1 ? 'bg-emerald-500 text-white shadow-md shadow-emerald-200' : 'bg-slate-100 text-slate-400']">
                                        {{ i === 0 && paginaPila === 1 ? 'Top' : (paginaPila - 1) * itemsPorPaginaPila +
                                            i + 1 }}
                                    </div>
                                    <div>
                                        <span
                                            class="text-[10px] font-bold text-slate-500 bg-slate-50 border border-slate-100 px-2 py-0.5 rounded uppercase">
                                            RET-{{ dev.id.toString().padStart(4, '0') }}
                                        </span>
                                        <h3 class="text-lg font-extrabold text-slate-800 mt-1">ID: {{ dev.componente }}
                                        </h3>
                                        <p class="text-[11px] text-slate-500 mt-0.5 font-mono">
                                            <ClockIcon class="w-3.5 h-3.5 inline" /> {{
                                                formatearFecha(dev.fecha_devolucion) }}
                                        </p>
                                    </div>
                                </div>

                                <div class="shrink-0 flex flex-col sm:items-end gap-2">
                                    <span
                                        class="font-black text-emerald-600 text-sm bg-emerald-50 px-3 py-1 rounded-lg">+{{
                                            dev.cantidad }} UDS</span>

                                    <div class="flex items-center gap-2 mt-2">
                                        <button @click="solicitarEliminacion(dev.id)"
                                            class="p-2.5 bg-red-50 text-red-500 hover:bg-red-100 hover:text-red-600 rounded-xl transition-colors">
                                            <TrashIcon class="w-5 h-5" />
                                        </button>

                                        <button v-if="i === 0 && paginaPila === 1" @click="reingresarUltimo"
                                            :disabled="procesando"
                                            class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-black rounded-xl shadow-md active:scale-95 transition-all disabled:opacity-70 flex items-center gap-2">
                                            <ArrowPathIcon class="w-5 h-5" /> Reingresar
                                        </button>
                                        <div v-else
                                            class="text-[11px] font-bold text-slate-400 bg-slate-50 px-4 py-2.5 rounded-xl border border-slate-100">
                                            En espera
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </transition-group>

                    <div class="mt-8">
                        <Paginacion :paginaActual="paginaPila" :totalPaginas="totalPaginasPila"
                            @cambiarPagina="p => paginaPila = p" />
                    </div>
                </div>
            </div>

            <div v-show="mostrarPanel"
                class="w-full lg:w-[40%] lg:sticky lg:top-6 bg-white border border-slate-200 rounded-[24px] shadow-sm overflow-hidden animate-slide-in">

                <div class="bg-slate-50 p-4 border-b border-slate-100 flex justify-between items-center">
                    <div class="flex items-center gap-3">
                        <div class="p-2 bg-emerald-100 text-emerald-600 rounded-xl">
                            <ClipboardDocumentListIcon class="w-5 h-5" />
                        </div>
                        <div>
                            <h2 class="text-sm font-black text-slate-800">Historial de Salidas</h2>
                        </div>
                    </div>
                    <button @click="mostrarPanel = false" class="p-1.5 hover:bg-slate-200 rounded-lg text-slate-400">
                        <XMarkIcon class="w-4 h-4" />
                    </button>
                </div>

                <div class="p-4 space-y-4">
                    <div class="flex flex-col gap-2">
                        <div class="relative">
                            <MagnifyingGlassIcon
                                class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                            <input v-model="busquedaPanel" type="text" placeholder="Buscar..."
                                class="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-50" />
                        </div>
                        <input v-model="fechaPanel" type="date"
                            class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-50" />
                    </div>

                    <div class="space-y-2">
                        <div v-for="d in despachosPaginados" :key="d.id"
                            class="border border-slate-100 rounded-xl overflow-hidden shadow-sm relative">
                            <div @click="seleccionarDespacho(d)"
                                :class="['p-3 flex justify-between items-center transition-colors',
                                    getCantidadDisponible(d) <= 0 ? 'bg-slate-50 opacity-60 cursor-not-allowed' :
                                        despachoSeleccionado?.id === d.id ? 'bg-emerald-50 cursor-pointer' : 'bg-white hover:bg-slate-50 cursor-pointer']">

                                <div class="flex-1 pr-2">
                                    <p class="text-[12px] font-bold text-slate-800 line-clamp-1"
                                        :class="{ 'line-through': getCantidadDisponible(d) <= 0 }">{{
                                            d.componente_nombre
                                        }}</p>
                                    <p class="text-[10px] text-slate-500 mt-0.5">{{ d.usuario_nombre }} • {{
                                        formatearFecha(d.fecha) }}</p>
                                </div>
                                <div class="shrink-0 flex flex-col items-end gap-1">
                                    <span
                                        class="text-[10px] font-black text-slate-600 bg-slate-100 px-2 py-1 rounded border">-{{
                                            d.cantidad }}</span>
                                </div>

                                <div v-if="getCantidadDisponible(d) <= 0"
                                    class="absolute inset-0 bg-white/40 flex items-center justify-center backdrop-blur-[1px]">
                                    <span
                                        class="bg-emerald-50 text-emerald-700 text-[10px] font-black uppercase px-3 py-1.5 rounded-full flex items-center gap-1 shadow-sm border border-emerald-100">
                                        <CheckBadgeIcon class="w-4 h-4" /> Completado
                                    </span>
                                </div>
                            </div>

                            <div v-if="despachoSeleccionado?.id === d.id && getCantidadDisponible(d) > 0"
                                class="bg-emerald-50/50 p-3 border-t border-emerald-100 animate-fade-in">

                                <div
                                    class="flex items-center gap-1.5 bg-amber-50 p-2 rounded text-amber-700 text-[10px] font-bold mb-3 border border-amber-100">
                                    <ShieldExclamationIcon class="w-3 h-3 shrink-0" /> Saldo disponible para devolver:
                                    {{ getCantidadDisponible(d) }}
                                </div>

                                <div class="flex items-center gap-2">
                                    <input type="number" v-model="cantidadARetornar" min="1"
                                        :max="getCantidadDisponible(d)"
                                        class="w-16 px-2 py-1.5 border border-emerald-200 rounded-lg text-sm text-center outline-none bg-white font-black focus:ring-2 focus:ring-emerald-400" />
                                    <button @click="enviarAPilaDesdeHistorial(d)"
                                        class="flex-1 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg flex justify-center items-center gap-1 shadow-sm active:scale-95 transition-all">
                                        <ArrowLeftEndOnRectangleIcon class="w-4 h-4" />
                                        <span class="text-[10px] font-black uppercase tracking-widest">A Pila</span>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div v-if="despachosFiltrados.length === 0"
                            class="text-center py-6 bg-slate-50 rounded-xl text-xs text-slate-400 border border-slate-100">
                            No se encontraron salidas.
                        </div>
                    </div>
                    <div class="flex justify-center border-t border-slate-100 pt-3">
                        <Paginacion :paginaActual="paginaPanel" :totalPaginas="totalPaginasPanel"
                            @cambiarPagina="p => paginaPanel = p" />
                    </div>
                </div>
            </div>
        </div>

        <Teleport to="body">
            <div v-if="modalEliminar.mostrar" @click="modalEliminar.mostrar = false"
                class="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">

                <div @click.stop
                    class="bg-white rounded-[28px] p-6 w-full max-w-sm shadow-2xl animate-slide-up border border-slate-100">
                    <div
                        class="w-16 h-16 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                        <ExclamationTriangleIcon class="w-8 h-8" />
                    </div>
                    <h3 class="text-xl font-black text-center text-slate-800 mb-2 tracking-tight">¿Eliminar Retorno?
                    </h3>
                    <p class="text-center text-sm text-slate-500 mb-6 leading-relaxed">
                        Esta acción descartará la tarjeta de la pila. <b>El componente NO se sumará</b> al inventario.
                        <br><span class="text-[10px] text-slate-400 mt-2 block">(Presiona ENTER para confirmar o ESC
                            para cancelar)</span>
                    </p>
                    <div class="flex gap-3">
                        <button @click="modalEliminar.mostrar = false"
                            class="flex-1 py-3 bg-slate-50 hover:bg-slate-100 text-slate-600 font-bold rounded-xl transition-all border border-slate-200">
                            Cancelar
                        </button>
                        <button @click="confirmarEliminacion"
                            class="flex-1 py-3 bg-red-500 hover:bg-red-600 text-white font-bold rounded-xl transition-all shadow-md shadow-red-200 active:scale-95">
                            Sí, Eliminar
                        </button>
                    </div>
                </div>
            </div>
        </Teleport>

    </div>
</template>

<style scoped>
.pila-move,
.pila-enter-active,
.pila-leave-active {
    transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.pila-enter-from,
.pila-leave-to {
    opacity: 0;
    transform: translateY(-30px) scale(0.95);
}

.pila-leave-active {
    position: absolute;
    width: 100%;
}

.animate-fade-in {
    animation: fadeIn 0.2s ease-out forwards;
}

.animate-slide-in {
    animation: slideIn 0.3s ease-out forwards;
    transform-origin: right;
}

.animate-slide-up {
    animation: slideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(20px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.95);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    opacity: 1;
}
</style>