<script setup>
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import { useToast } from '../composables/useToast'
import { api } from '../services/api'
import Paginacion from '../components/pagination.vue'
import { 
  QueueListIcon, CheckCircleIcon, ClockIcon, 
  HashtagIcon, ArchiveBoxIcon, TrashIcon,
  ExclamationTriangleIcon, ArrowRightEndOnRectangleIcon,
  MagnifyingGlassIcon, PlusCircleIcon, XMarkIcon,
  CubeIcon, ViewfinderCircleIcon
} from '@heroicons/vue/24/outline'

const pedidos = ref([])
const componentes = ref([]) 
const cargando = ref(true)
const procesando = ref(false)
const mostrarPanel = ref(false)
const { showToast } = useToast()

// Estado Modal Eliminación
const modalEliminar = ref({ mostrar: false, id: null })

// --- PANEL DE CREACIÓN RÁPIDA ---
const busquedaComponente = ref('')
const componenteSeleccionado = ref(null)
const cantidadAPedir = ref(1)

// --- Paginación COLA ---
const paginaCola = ref(1)
const itemsPorPaginaCola = 6

// --- Paginación PANEL ---
const paginaPanel = ref(1)
const itemsPorPaginaPanel = 5

const cargarDatos = async () => {
  cargando.value = true
  try {
    const [resPed, resComp] = await Promise.all([
      api('pedidos/'),
      api('componentes/')
    ])
    if (resPed.ok) pedidos.value = await resPed.json()
    if (resComp.ok) componentes.value = await resComp.json()
  } catch (err) {
    if (err !== 'Sesión expirada') showToast("Error al cargar datos", "error")
  } finally {
    cargando.value = false
  }
}

// --- LÓGICA FIFO (Cola) ---
const totalPaginasCola = computed(() => Math.ceil(pedidos.value.length / itemsPorPaginaCola) || 1)
const pedidosPaginados = computed(() => {
  const inicio = (paginaCola.value - 1) * itemsPorPaginaCola
  return pedidos.value.slice(inicio, inicio + itemsPorPaginaCola)
})
watch(pedidos, () => { if (paginaCola.value > totalPaginasCola.value) paginaCola.value = 1 })

const despacharSiguiente = async () => {
  if (pedidos.value.length === 0) return
  procesando.value = true
  try {
    const res = await api('pedidos/', { method: 'DELETE' })
    if (res.ok) {
      showToast("Pedido despachado. Stock actualizado.", "success")
      await cargarDatos()
    } else {
      const data = await res.json()
      showToast(data.error || "Stock insuficiente", "error")
    }
  } catch (err) {
    showToast("Error en el servidor", "error")
  } finally {
    procesando.value = false
  }
}

// --- CANCELACIÓN SEGURA ---
const solicitarEliminacion = (id) => modalEliminar.value = { mostrar: true, id }
const confirmarEliminacion = async () => {
  const id = modalEliminar.value.id
  modalEliminar.value.mostrar = false
  try {
    const res = await api('pedidos/', {
      method: 'DELETE',
      body: JSON.stringify({ cancelar_id: id })
    })
    if (res.ok) {
      showToast("Pedido cancelado de la cola.", "success")
      await cargarDatos()
    }
  } catch (err) {
    showToast("Error al cancelar", "error")
  }
}

const manejarTeclado = (e) => {
  if (!modalEliminar.value.mostrar) return
  if (e.key === 'Escape') modalEliminar.value.mostrar = false
  if (e.key === 'Enter') confirmarEliminacion()
}

// --- LÓGICA DEL BUSCADOR RÁPIDO (Panel) ---
const componentesFiltrados = computed(() => {
  return componentes.value.filter(c => 
    c.nombre.toLowerCase().includes(busquedaComponente.value.toLowerCase()) ||
    (c.codigo_interno && c.codigo_interno.toLowerCase().includes(busquedaComponente.value.toLowerCase()))
  )
})

const totalPaginasPanel = computed(() => Math.ceil(componentesFiltrados.value.length / itemsPorPaginaPanel) || 1)
const componentesPaginados = computed(() => {
  const inicio = (paginaPanel.value - 1) * itemsPorPaginaPanel
  return componentesFiltrados.value.slice(inicio, inicio + itemsPorPaginaPanel)
})
watch(busquedaComponente, () => { paginaPanel.value = 1 })

const seleccionarComponente = (comp) => {
  if (comp.stock <= 0) return // No dejar seleccionar si no hay stock
  componenteSeleccionado.value = componenteSeleccionado.value?.id === comp.id ? null : comp
  cantidadAPedir.value = 1
}

const agregarAColaRapido = async (comp) => {
  if (cantidadAPedir.value <= 0) return showToast("La cantidad debe ser mayor a 0", "error")
  if (cantidadAPedir.value > comp.stock) return showToast("No hay suficiente stock", "error")

  try {
    const res = await api('pedidos/', {
      method: 'POST',
      body: JSON.stringify({
        componente: comp.id,
        cantidad: cantidadAPedir.value
      })
    })
    if (res.ok) {
      showToast("Añadido a la Cola de Despacho", "success")
      componenteSeleccionado.value = null
      await cargarDatos()
    }
  } catch (err) {
    showToast("Error al crear el pedido", "error")
  }
}

const getStockActual = (componenteId) => {
  const comp = componentes.value.find(c => c.id === componenteId)
  return comp ? comp.stock : 0
}

const formatearFecha = (fechaISO) => {
  return new Date(fechaISO).toLocaleString('es-GT', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  cargarDatos()
  window.addEventListener('keydown', manejarTeclado)
})
onUnmounted(() => window.removeEventListener('keydown', manejarTeclado))
</script>

<template>
  <div class="w-full bg-slate-50 text-slate-700 font-sans p-3 sm:p-6 min-h-[80vh] flex flex-col items-center animate-fade-in relative">
    
    <div class="w-full max-w-[1300px] flex flex-col lg:flex-row items-start gap-6 relative">
      
      <div :class="['transition-all duration-500 ease-in-out w-full', mostrarPanel ? 'lg:w-[60%]' : 'lg:w-full']">
        
        <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 sm:p-6 rounded-[20px] sm:rounded-[24px] shadow-sm border border-slate-100 mb-6">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center shrink-0">
              <QueueListIcon class="w-6 h-6" />
            </div>
            <div>
              <h1 class="text-xl sm:text-2xl font-black text-slate-800 tracking-tight">Cola de Despacho</h1>
              <p class="text-slate-500 text-xs sm:text-sm font-medium mt-0.5">Lógica FIFO (First In, First Out).</p>
            </div>
          </div>
          <div class="flex items-center gap-2 w-full sm:w-auto">
            <button @click="mostrarPanel = !mostrarPanel" 
                    :class="['flex-1 sm:flex-none px-4 py-2.5 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all', mostrarPanel ? 'bg-slate-100 text-slate-600 hover:bg-slate-200' : 'bg-indigo-600 text-white shadow-md shadow-indigo-200 hover:bg-indigo-700']">
              <PlusCircleIcon class="w-5 h-5" />
              <span>{{ mostrarPanel ? 'Cerrar Buscador' : 'Nuevo Pedido' }}</span>
            </button>
          </div>
        </header>

        <div v-if="pedidos.length === 0" class="bg-white rounded-[24px] border-2 border-dashed border-slate-200 p-10 sm:p-16 text-center shadow-sm">
          <CheckCircleIcon class="w-14 h-14 text-indigo-300 mx-auto mb-4" />
          <h3 class="text-lg sm:text-xl font-black text-slate-800 mb-2">Cola Vacía</h3>
          <p class="text-slate-500 text-sm">No hay entregas pendientes. Usa el panel para crear una rápida.</p>
        </div>

        <div v-else class="flex flex-col gap-0 items-center">
          <transition-group name="cola" tag="div" class="w-full relative flex flex-col space-y-3 sm:space-y-4">
            <div v-for="(pedido, index) in pedidosPaginados" :key="pedido.id" 
                :class="['w-full bg-white p-4 sm:p-5 rounded-[20px] sm:rounded-[24px] shadow-sm border transition-all duration-500 flex flex-col sm:flex-row gap-4 sm:items-center justify-between',
                          index === 0 && paginaCola === 1 ? 'border-indigo-300 ring-4 ring-indigo-50 shadow-lg scale-100' : 'border-slate-200 opacity-95 scale-[0.98]']">
              
              <div class="flex items-start sm:items-center gap-3 sm:gap-4">
                <div :class="['w-12 h-12 sm:w-14 sm:h-14 rounded-2xl flex items-center justify-center shrink-0 font-black text-base sm:text-lg',
                              index === 0 && paginaCola === 1 ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200' : 'bg-slate-100 text-slate-400']">
                  {{ index === 0 && paginaCola === 1 ? '1º' : (paginaCola - 1) * itemsPorPaginaCola + index + 1 }}
                </div>
                <div class="min-w-0 flex-1">
                  <div class="flex flex-wrap items-center gap-2 mb-1.5">
                    <span class="text-[9px] sm:text-[10px] font-bold text-slate-500 bg-slate-50 border border-slate-100 px-2 py-0.5 rounded uppercase whitespace-nowrap">
                      PED-{{ pedido.id.toString().padStart(4, '0') }}
                    </span>
                    <span class="text-[9px] sm:text-[10px] text-slate-500 flex items-center gap-1 font-mono whitespace-nowrap">
                      <ClockIcon class="w-3 h-3" /> {{ formatearFecha(pedido.fecha_solicitud) }}
                    </span>
                  </div>
                  <h3 class="text-sm sm:text-base font-extrabold text-slate-800 line-clamp-2">ID Comp: {{ pedido.componente }}</h3>
                  
                  <p :class="['text-[10px] sm:text-[11px] font-bold mt-1.5 flex items-center gap-1', 
                              getStockActual(pedido.componente) >= pedido.cantidad ? 'text-emerald-500' : 'text-red-500']">
                     <ArchiveBoxIcon class="w-3.5 h-3.5" />
                     Bodega: {{ getStockActual(pedido.componente) }} uds
                  </p>
                </div>
              </div>

              <div class="shrink-0 flex flex-col sm:items-end gap-3 w-full sm:w-auto mt-2 sm:mt-0 border-t sm:border-t-0 border-slate-100 pt-3 sm:pt-0">
                <div class="flex items-center justify-between sm:justify-end w-full gap-4">
                  <span class="font-black text-indigo-700 text-xs sm:text-sm bg-indigo-50 px-3 py-1.5 rounded-lg">-{{ pedido.cantidad }} uds</span>
                  
                  <div class="flex items-center gap-2">
                    <button @click="solicitarEliminacion(pedido.id)" class="p-2.5 bg-red-50 text-red-500 hover:bg-red-100 hover:text-red-600 rounded-xl transition-colors">
                      <TrashIcon class="w-5 h-5" />
                    </button>

                    <button v-if="index === 0 && paginaCola === 1" @click="despacharSiguiente" :disabled="procesando"
                      class="px-4 sm:px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs sm:text-sm font-black rounded-xl shadow-md active:scale-95 transition-all disabled:opacity-70 flex items-center gap-2">
                      <ArrowRightEndOnRectangleIcon class="w-5 h-5" /> Despachar
                    </button>
                    <div v-else class="text-[10px] sm:text-[11px] font-bold text-slate-400 bg-slate-50 px-3 sm:px-4 py-2.5 rounded-xl border border-slate-100 whitespace-nowrap">
                      En espera
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </transition-group>
          
          <div class="mt-8 w-full flex justify-center overflow-x-auto">
            <Paginacion :paginaActual="paginaCola" :totalPaginas="totalPaginasCola" @cambiarPagina="p => paginaCola = p" />
          </div>
        </div>
      </div>

      <div v-show="mostrarPanel" class="w-full lg:w-[40%] lg:sticky lg:top-6 bg-white border border-slate-200 rounded-[24px] shadow-sm overflow-hidden animate-slide-in">
        
        <div class="bg-indigo-600 p-5 border-b border-indigo-700 flex justify-between items-center text-white">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-white/20 rounded-xl"><ViewfinderCircleIcon class="w-5 h-5" /></div>
            <div>
              <h2 class="text-sm font-black">Buscador Rápido</h2>
              <p class="text-[10px] text-indigo-200 font-medium opacity-80">Añade a la cola al instante</p>
            </div>
          </div>
          <button @click="mostrarPanel = false" class="p-1.5 hover:bg-white/10 rounded-lg transition-colors">
            <XMarkIcon class="w-5 h-5" />
          </button>
        </div>

        <div class="p-4 space-y-4">
          <div class="relative">
            <MagnifyingGlassIcon class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input v-model="busquedaComponente" type="text" placeholder="Buscar componente..." 
                   class="w-full pl-9 pr-3 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-50 transition-all" />
          </div>

          <div class="space-y-2">
            <div v-for="c in componentesPaginados" :key="c.id" class="border border-slate-100 rounded-xl overflow-hidden relative">
              <div @click="seleccionarComponente(c)" 
                   :class="['p-3 flex justify-between items-center transition-colors',
                            c.stock <= 0 ? 'bg-slate-50 opacity-60 cursor-not-allowed' : 
                            componenteSeleccionado?.id === c.id ? 'bg-indigo-50 cursor-pointer' : 'bg-white hover:bg-slate-50 cursor-pointer']">
                
                <div class="flex-1 pr-2">
                  <p class="text-xs font-bold text-slate-800 line-clamp-1">{{ c.nombre }}</p>
                  <p class="text-[10px] text-slate-500 mt-0.5 font-mono">Stock: {{ c.stock }} uds</p>
                </div>
                
                <div v-if="c.stock <= 0" class="absolute inset-0 bg-white/40 flex items-center justify-center backdrop-blur-[1px]">
                  <span class="bg-red-50 text-red-600 text-[10px] font-black uppercase px-3 py-1 rounded-full border border-red-100">
                    Agotado
                  </span>
                </div>
              </div>

              <div v-if="componenteSeleccionado?.id === c.id && c.stock > 0" 
                   class="bg-indigo-50/50 p-3 border-t border-indigo-100 animate-fade-in flex flex-col gap-3">
                
                <div class="flex items-center gap-2">
                  <input type="number" v-model="cantidadAPedir" min="1" :max="c.stock" 
                         class="w-16 px-2 py-2 border border-indigo-200 rounded-xl text-sm text-center outline-none bg-white font-black focus:ring-2 focus:ring-indigo-400" />
                  <button @click="agregarAColaRapido(c)" 
                          class="flex-1 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl flex justify-center items-center gap-2 shadow-sm active:scale-95 transition-all">
                    <PlusCircleIcon class="w-4 h-4" />
                    <span class="text-[11px] font-black uppercase tracking-widest">Crear Pedido</span>
                  </button>
                </div>
              </div>
            </div>
            
            <div v-if="componentesFiltrados.length === 0" class="text-center py-8 bg-slate-50 rounded-xl text-xs text-slate-400 border border-slate-100">
              No se encontraron componentes.
            </div>
          </div>
          
          <div class="flex justify-center border-t border-slate-100 pt-3">
             <Paginacion :paginaActual="paginaPanel" :totalPaginas="totalPaginasPanel" @cambiarPagina="p => paginaPanel = p" />
          </div>
        </div>
      </div>
    </div>

    <Teleport to="body">
      <div v-if="modalEliminar.mostrar" @click="modalEliminar.mostrar = false" 
           class="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
        
        <div @click.stop class="bg-white rounded-[28px] p-6 w-full max-w-sm shadow-2xl animate-slide-up border border-slate-100 mx-4">
          <div class="w-16 h-16 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <ExclamationTriangleIcon class="w-8 h-8" />
          </div>
          <h3 class="text-xl font-black text-center text-slate-800 mb-2 tracking-tight">¿Cancelar Pedido?</h3>
          <p class="text-center text-sm text-slate-500 mb-6 leading-relaxed">
            Esta acción eliminará el pedido de la cola. <b>El stock del inventario NO se verá afectado</b>.
            <br><span class="text-[10px] text-slate-400 mt-2 hidden sm:block">(Presiona ENTER para confirmar o ESC para cancelar)</span>
          </p>
          <div class="flex flex-col sm:flex-row gap-3">
            <button @click="modalEliminar.mostrar = false" class="w-full sm:flex-1 py-3 bg-slate-50 hover:bg-slate-100 text-slate-600 font-bold rounded-xl transition-all border border-slate-200">
              Cerrar
            </button>
            <button @click="confirmarEliminacion" class="w-full sm:flex-1 py-3 bg-red-500 hover:bg-red-600 text-white font-bold rounded-xl transition-all shadow-md shadow-red-200 active:scale-95">
              Sí, Cancelar
            </button>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<style scoped>
.cola-move, .cola-enter-active, .cola-leave-active { transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1); }
.cola-enter-from, .cola-leave-to { opacity: 0; transform: translateX(-30px) scale(0.95); }
.cola-leave-active { position: absolute; width: 100%; }

.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
.animate-slide-in { animation: slideIn 0.3s ease-out forwards; transform-origin: right; }
.animate-slide-up { animation: slideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideIn { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }

input[type="number"]::-webkit-inner-spin-button, input[type="number"]::-webkit-outer-spin-button { opacity: 1; }
</style>