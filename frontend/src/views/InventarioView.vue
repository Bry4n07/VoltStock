<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import Paginacion from '../components/pagination.vue' 
import { useToast } from '../composables/useToast'
import { api } from '../services/api'
import {
  MagnifyingGlassIcon, PlusIcon,
  ExclamationTriangleIcon, CubeIcon,
  TagIcon, CircleStackIcon,
  XMarkIcon, ArrowDownTrayIcon, ArrowUpOnSquareIcon,
  FunnelIcon, AdjustmentsHorizontalIcon,
  CpuChipIcon, CheckBadgeIcon, ExclamationCircleIcon,
  PencilSquareIcon, TrashIcon, MapPinIcon
} from '@heroicons/vue/24/outline'

// Estado
const componentes = ref([])
const categorias = ref([])
const cargando = ref(true)
const busqueda = ref('')
const filtroCategoria = ref('')
const filtroStock = ref('')

// Estado de Modales
const mostrarModal = ref(false)
const mostrarModalEliminar = ref(false)
const idAEliminar = ref(null)

const tipoFormulario = ref('componente')

const mostrarModalTransaccion = ref(false)
const tipoTransaccion = ref('')
const itemSeleccionado = ref(null)
const cantidadTransaccion = ref(1)

const paginaActual = ref(1)
const itemsPorPagina = 8
const { showToast } = useToast()

const rolUsuario = ref(localStorage.getItem('user_rol') || 'auditor')

const nuevoProducto = ref({ id: null, nombre: '', descripcion: '', stock: 0, categoria: '', codigo_interno: '', ubicacion: '' })
const nuevaCatForm = ref({ nombre: '' })

// Computed
const componentesFiltrados = computed(() => {
  return componentes.value.filter(item => {
    const matchNom = item.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
    const matchCat = filtroCategoria.value === '' || item.categoria === parseInt(filtroCategoria.value)
    
    let matchStock = true
    if (filtroStock.value === 'agotado') matchStock = item.stock === 0
    else if (filtroStock.value === 'critico') matchStock = item.stock > 0 && item.stock <= 10
    else if (filtroStock.value === 'optimo') matchStock = item.stock > 10

    return matchNom && matchCat && matchStock
  })
})

const totalPaginas = computed(() => Math.ceil(componentesFiltrados.value.length / itemsPorPagina) || 1)

const componentesPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * itemsPorPagina
  return componentesFiltrados.value.slice(inicio, inicio + itemsPorPagina)
})

const stats = computed(() => ({
  total: componentes.value.length,
  bajo: componentes.value.filter(i => i.stock <= 10 && i.stock > 0).length,
  cats: categorias.value.length,
  agotados: componentes.value.filter(i => i.stock === 0).length
}))

// Watch
watch([busqueda, filtroCategoria, filtroStock], () => { paginaActual.value = 1 })

// Logica de Modales
const manejarEsc = (e) => {
  if (e.key === 'Escape') {
    if (mostrarModal.value) cerrarModal()
    if (mostrarModalTransaccion.value) cerrarModalTransaccion()
    if (mostrarModalEliminar.value) {
      mostrarModalEliminar.value = false
      idAEliminar.value = null
    }
  }
}

const cerrarModal = () => {
  mostrarModal.value = false
  nuevoProducto.value = { id: null, nombre: '', descripcion: '', stock: 0, categoria: '' }
  nuevaCatForm.value = { nombre: '' }
  tipoFormulario.value = 'componente'
}

const abrirModalEditar = (item) => {
  nuevoProducto.value = { ...item }
  tipoFormulario.value = 'editar_componente'
  mostrarModal.value = true
}

const abrirModalTransaccion = (item, tipo) => {
  itemSeleccionado.value = item
  tipoTransaccion.value = tipo
  cantidadTransaccion.value = 1
  mostrarModalTransaccion.value = true
}

const cerrarModalTransaccion = () => {
  mostrarModalTransaccion.value = false
  itemSeleccionado.value = null
  cantidadTransaccion.value = 1
}

const confirmarEliminacion = (id) => {
  idAEliminar.value = id
  mostrarModalEliminar.value = true
}

// API CRUD
const obtenerDatos = async () => {
  cargando.value = true
  try {
    const [resComp, resCat] = await Promise.all([
      api('componentes/'),
      api('categorias/')
    ])
    
    componentes.value = await resComp.json()
    categorias.value = await resCat.json()
  } catch (err) {
    if (err !== 'Sesión expirada') {
      showToast("Error al cargar los datos", "error")
    }
  } finally {
    cargando.value = false
  }
}

const guardarRegistro = async () => {
  let endpoint = ''
  let method = 'POST'
  let body = null

  if (tipoFormulario.value === 'categoria') {
    endpoint = 'categorias/'
    body = nuevaCatForm.value
  } else if (tipoFormulario.value === 'componente') {
    endpoint = 'componentes/'
    body = nuevoProducto.value
  } else if (tipoFormulario.value === 'editar_componente') {
    endpoint = `componentes/${nuevoProducto.value.id}/`
    method = 'PUT'
    body = nuevoProducto.value
  }

  try {
    const res = await api(endpoint, {
      method: method,
      body: JSON.stringify(body)
    })
    
    if (res.ok) { 
      await obtenerDatos()
      cerrarModal()
      showToast(`¡Guardado con éxito!`, "success")
    } else {
      showToast("Verifica los datos", "error")
    }
  } catch (err) { 
    if (err !== 'Sesión expirada') showToast("Error de conexión", "error") 
  }
}

const ejecutarEliminacion = async () => {
  try {
    const res = await api(`componentes/${idAEliminar.value}/`, { method: 'DELETE' })
    if (res.ok) {
      showToast("Componente eliminado", "success")
      await obtenerDatos()
    }
  } catch(err) {
    if (err !== 'Sesión expirada') showToast("Error al Eliminar", "error")
  } finally {
    mostrarModalEliminar.value = false 
    idAEliminar.value = null
  }
}

// Emisore para Pila y Cola
const emit = defineEmits(['solicitar', 'devolver'])

const confirmarTransaccion = async () => {
  try {
    if (tipoTransaccion.value === 'extraer') {
      const res = await api('pedidos/', {
        method: 'POST',
        body: JSON.stringify({
          componente: itemSeleccionado.value.id,
          cantidad: cantidadTransaccion.value
        })
      })
      
      if (res.ok) {
        showToast("Pedido agregado a la cola", "success")
      } else {
        showToast("Error al crear el pedido", "error")
      }

    } else {
      const res = await api('devoluciones/', {
        method: 'POST',
        body: JSON.stringify({
          componente: itemSeleccionado.value.id,
          cantidad: cantidadTransaccion.value,
          motivo: 'Devolución desde inventario'
        })
      })

      if (res.ok) {
        showToast("Devolución agregada a la pila", "success")
      } else {
        showToast("Error al crear la devolución", "error")
      }
    }
  } catch (err) {
    if (err !== 'Sesión expirada') showToast("Error de conexión", "error")
  } finally {
    cerrarModalTransaccion()
  }
}

onMounted(() => {
  obtenerDatos()
  window.addEventListener('keydown', manejarEsc)
})
onUnmounted(() => window.removeEventListener('keydown', manejarEsc))
</script>

<template>
  <div class="w-full bg-white text-slate-700 font-sans p-2 sm:p-6 relative min-h-[80vh]">
    <div class="max-w-[1400px] mx-auto space-y-5 sm:space-y-6">
      
      <header class="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <div class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-indigo-50 text-indigo-600 rounded-md text-[10px] font-bold tracking-[0.1em] uppercase mb-2">
            <CheckBadgeIcon class="w-3.5 h-3.5" /> Sistema Online
          </div>
          <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">Catálogo de Hardware</h1>
          <p class="text-slate-500 mt-1 text-sm font-medium">Gestiona y supervisa el inventario de VoltStock en tiempo real.</p>
        </div>
        
        <button @click="mostrarModal = true; tipoFormulario = 'componente'"
          class="flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-bold shadow-md shadow-indigo-600/20 transition-all active:scale-95 w-full md:w-auto group">
          <PlusIcon class="w-5 h-5 group-hover:rotate-90 transition-transform duration-300" />
          Añadir Registro
        </button>
      </header>

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <div class="relative bg-white p-4 sm:p-5 rounded-[20px] border border-slate-100 shadow-sm flex flex-col justify-between overflow-hidden group hover:shadow-md transition-all duration-300">
          <div class="absolute top-0 right-0 w-16 h-16 sm:w-20 sm:h-20 bg-indigo-50/80 rounded-bl-[100%] transition-transform duration-500 group-hover:scale-110"></div>
          <div class="absolute top-3 right-3 sm:top-4 sm:right-4 text-indigo-500 group-hover:rotate-12 transition-transform duration-300"><CubeIcon class="w-4 h-4 sm:w-5 sm:h-5" /></div>
          <div class="relative z-10 mb-4 sm:mb-6"><h3 class="text-slate-400 font-bold uppercase tracking-widest text-[9px] sm:text-[10px] line-clamp-1">Inventario Total</h3></div>
          <div class="relative z-10">
            <div class="text-2xl sm:text-3xl font-black text-slate-800 mb-1 leading-none">{{ stats.total }}</div>
            <p class="text-[9px] sm:text-[10px] text-slate-500 font-medium line-clamp-1">Registros activos</p>
          </div>
        </div>
        <div class="relative bg-white p-4 sm:p-5 rounded-[20px] border border-slate-100 shadow-sm flex flex-col justify-between overflow-hidden group hover:shadow-md transition-all duration-300">
          <div class="absolute top-0 right-0 w-16 h-16 sm:w-20 sm:h-20 bg-slate-50 rounded-bl-[100%] transition-transform duration-500 group-hover:scale-110"></div>
          <div class="absolute top-3 right-3 sm:top-4 sm:right-4 text-slate-400 group-hover:rotate-12 transition-transform duration-300"><CircleStackIcon class="w-4 h-4 sm:w-5 sm:h-5" /></div>
          <div class="relative z-10 mb-4 sm:mb-6"><h3 class="text-slate-400 font-bold uppercase tracking-widest text-[9px] sm:text-[10px] line-clamp-1">Familias</h3></div>
          <div class="relative z-10">
            <div class="text-2xl sm:text-3xl font-black text-slate-800 mb-1 leading-none">{{ stats.cats }}</div>
            <p class="text-[9px] sm:text-[10px] text-slate-500 font-medium line-clamp-1">Categorías</p>
          </div>
        </div>
        <div class="relative bg-white p-4 sm:p-5 rounded-[20px] border border-slate-100 shadow-sm flex flex-col justify-between overflow-hidden group hover:shadow-md transition-all duration-300">
          <div class="absolute top-0 right-0 w-16 h-16 sm:w-20 sm:h-20 bg-amber-50/80 rounded-bl-[100%] transition-transform duration-500 group-hover:scale-110"></div>
          <div class="absolute top-3 right-3 sm:top-4 sm:right-4 text-amber-500 group-hover:-rotate-12 transition-transform duration-300"><ExclamationTriangleIcon class="w-4 h-4 sm:w-5 sm:h-5" /></div>
          <div class="relative z-10 mb-4 sm:mb-6"><h3 class="text-slate-400 font-bold uppercase tracking-widest text-[9px] sm:text-[10px] line-clamp-1">Stock Crítico</h3></div>
          <div class="relative z-10">
            <div class="text-2xl sm:text-3xl font-black text-amber-500 mb-1 leading-none flex items-center gap-1.5">
              {{ stats.bajo }}
              <span v-if="stats.bajo > 0" class="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
            </div>
            <p class="text-[9px] sm:text-[10px] text-slate-500 font-medium line-clamp-1">Bajo mínimo</p>
          </div>
        </div>
        <div class="relative bg-white p-4 sm:p-5 rounded-[20px] border border-slate-100 shadow-sm flex flex-col justify-between overflow-hidden group hover:shadow-md transition-all duration-300">
          <div class="absolute top-0 right-0 w-16 h-16 sm:w-20 sm:h-20 bg-red-50/80 rounded-bl-[100%] transition-transform duration-500 group-hover:scale-110"></div>
          <div class="absolute top-3 right-3 sm:top-4 sm:right-4 text-red-500 group-hover:rotate-12 transition-transform duration-300"><ExclamationCircleIcon class="w-4 h-4 sm:w-5 sm:h-5" /></div>
          <div class="relative z-10 mb-4 sm:mb-6"><h3 class="text-slate-400 font-bold uppercase tracking-widest text-[9px] sm:text-[10px] line-clamp-1">Agotados</h3></div>
          <div class="relative z-10">
            <div class="text-2xl sm:text-3xl font-black text-red-500 mb-1 leading-none">{{ stats.agotados }}</div>
            <p class="text-[9px] sm:text-[10px] text-slate-500 font-medium line-clamp-1">Requieren stock</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-[24px] border border-slate-100 shadow-sm flex flex-col relative overflow-hidden">
        
        <div class="p-4 border-b border-slate-100 flex flex-col md:flex-row gap-3 relative z-20 bg-white">
          <div class="relative flex-1">
            <MagnifyingGlassIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
            <input v-model="busqueda" type="text" placeholder="Buscar por nombre..."
              class="w-full pl-11 pr-4 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm font-medium text-slate-700 focus:outline-none focus:bg-white focus:ring-2 focus:ring-indigo-100 focus:border-indigo-300 transition-all" />
          </div>
          <div class="flex flex-col sm:flex-row gap-3">
            <div class="relative w-full sm:w-52">
              <FunnelIcon class="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
              <select v-model="filtroCategoria" class="w-full pl-11 pr-8 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm font-medium text-slate-700 focus:outline-none focus:bg-white focus:ring-2 focus:ring-indigo-100 focus:border-indigo-300 cursor-pointer transition-all appearance-none">
                <option value="">Todas las Familias</option>
                <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </div>
            <div class="relative w-full sm:w-44">
              <AdjustmentsHorizontalIcon class="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
              <select v-model="filtroStock" class="w-full pl-11 pr-8 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm font-medium text-slate-700 focus:outline-none focus:bg-white focus:ring-2 focus:ring-indigo-100 focus:border-indigo-300 cursor-pointer transition-all appearance-none">
                <option value="">Estado Stock</option>
                <option value="optimo">Óptimo (+10)</option>
                <option value="critico">Crítico (1-10)</option>
                <option value="agotado">Agotados (0)</option>
              </select>
            </div>
          </div>
        </div>

        <div class="hidden lg:block overflow-x-auto relative z-10 bg-white">
          <table class="w-full text-left">
            <thead>
              <tr class="border-b border-slate-100 bg-slate-50/30">
                <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest w-32">ID.Ref</th>
                <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Componente</th>
                <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Estado Inventario</th>
                <th v-if="rolUsuario === 'admin' || rolUsuario === 'operador'" class="px-6 py-4 text-right text-[10px] font-black text-slate-400 uppercase tracking-widest">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="item in componentesPaginados" :key="item.id" class="hover:bg-slate-50/50 transition-colors group">
                <td class="px-6 py-4 align-middle">
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-slate-100 text-slate-500 rounded-md text-[11px] whitespace-nowrap font-mono font-bold">
                    <TagIcon class="w-3 h-3" /> 
                    {{ item.codigo_interno || 'ID-' + item.id.toString().padStart(4, '0') }}
                  </span>
                </td>
                <td class="px-6 py-4 align-middle">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center shrink-0">
                      <CpuChipIcon class="w-4 h-4 text-slate-400" />
                    </div>
                    <div>
                      <p class="font-bold text-slate-800 text-sm">{{ item.nombre }}</p>
                      <p class="text-[11px] text-slate-400 mt-0.5 line-clamp-1">{{ item.descripcion || 'Sin descripción.' }}</p>
                      <p v-if="item.ubicacion" class="text-[10px] text-indigo-500 font-bold mt-1 flex items-center gap-1"><MapPinIcon class="w-3 h-3" /> {{ item.ubicacion }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 align-middle text-center">
                  <div class="flex justify-center">
                    <div :class="['inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold',
                        item.stock > 10 ? 'bg-emerald-50 text-emerald-700' :
                        item.stock > 0 ? 'bg-amber-50 text-amber-700' : 'bg-red-50 text-red-700']">
                      <div :class="['w-1.5 h-1.5 rounded-full', item.stock > 10 ? 'bg-emerald-500' : item.stock > 0 ? 'bg-amber-500' : 'bg-red-500']"></div>
                      {{ item.stock }} UDS.
                    </div>
                  </div>
                </td>
                <td v-if="rolUsuario === 'admin' || rolUsuario === 'operador'" class="px-6 py-4 text-right whitespace-nowrap">>
                  <div class="flex items-center justify-end gap-2">
                    <button @click="abrirModalTransaccion(item, 'extraer')" :disabled="item.stock === 0"
                      class="p-2 bg-white border border-slate-200 text-indigo-600 hover:bg-indigo-50 hover:border-indigo-200 rounded-lg transition-all disabled:opacity-40 disabled:cursor-not-allowed" title="Extraer">
                      <ArrowUpOnSquareIcon class="w-4 h-4" />
                    </button>
                    <button @click="abrirModalTransaccion(item, 'ingresar')"
                      class="p-2 bg-white border border-slate-200 text-emerald-600 hover:bg-emerald-50 hover:border-emerald-200 rounded-lg transition-all" title="Ingresar/Devolver">
                      <ArrowDownTrayIcon class="w-4 h-4" />
                    </button>
                    <div class="w-px h-6 bg-slate-200 mx-1"></div>
                    <button @click="abrirModalEditar(item)"
                      class="p-2 bg-white border border-slate-200 text-slate-500 hover:bg-slate-50 rounded-lg transition-all" title="Editar">
                      <PencilSquareIcon class="w-4 h-4" />
                    </button>
                    <button @click="confirmarEliminacion(item.id)"
                      class="p-2 bg-white border border-slate-200 text-red-500 hover:bg-red-50 hover:border-red-200 rounded-lg transition-all" title="Eliminar">
                      <TrashIcon class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="lg:hidden p-4 bg-slate-50/50 flex flex-col gap-3.5 relative z-10">
          <div v-for="item in componentesPaginados" :key="item.id" 
              class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm relative overflow-hidden flex flex-col gap-3">
            <div :class="['absolute left-0 top-0 bottom-0 w-1', item.stock > 10 ? 'bg-emerald-400' : item.stock > 0 ? 'bg-amber-400' : 'bg-red-400']"></div>
            <div class="flex items-start justify-between gap-3 pl-1">
              <div class="flex items-start gap-3 flex-1 min-w-0">
                <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center shrink-0 mt-0.5"><CpuChipIcon class="w-4 h-4 text-slate-400" /></div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1">
                    <h4 class="font-bold text-slate-800 text-sm truncate pr-2">{{ item.nombre }}</h4>
                    <div :class="['shrink-0 px-1.5 py-0.5 rounded text-[9px] font-black', item.stock > 10 ? 'bg-emerald-50 text-emerald-700' : item.stock > 0 ? 'bg-amber-50 text-amber-700' : 'bg-red-50 text-red-700']">
                      {{ item.stock }} UD
                    </div>
                  </div>
                  <p class="text-[11px] text-slate-500 mb-2 line-clamp-2 leading-tight">{{ item.descripcion || 'Sin descripción técnica registrada.' }}</p>
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-slate-100 text-slate-500 rounded-md text-xs font-mono font-bold"><TagIcon class="w-3 h-3" /> {{ item.codigo_interno || 'ID-' + item.id.toString().padStart(4, '0') }}</span>
                </div>
              </div>
            </div>
            
            <div v-if="rolUsuario === 'admin' || rolUsuario === 'operador'" class="mt-4 flex justify-end gap-2">
              <button @click="abrirModalTransaccion(item, 'extraer')" :disabled="item.stock === 0" class="flex-1 py-2 bg-indigo-50/80 text-indigo-700 rounded-xl text-[11px] font-bold"><ArrowUpOnSquareIcon class="w-3.5 h-3.5 inline mr-1" /> Extraer</button>
              <button @click="abrirModalTransaccion(item, 'ingresar')" class="flex-1 py-2 bg-emerald-50/80 text-emerald-700 rounded-xl text-[11px] font-bold"><ArrowDownTrayIcon class="w-3.5 h-3.5 inline mr-1" /> Devolver</button>
            </div>
            <div v-if="rolUsuario === 'admin' || rolUsuario === 'operador'" class="mt-4 flex justify-end gap-2">
              <button @click="abrirModalEditar(item)" class="flex-1 py-1.5 border border-slate-200 text-slate-600 rounded-xl text-[11px] font-bold"><PencilSquareIcon class="w-3.5 h-3.5 inline mr-1" /> Editar</button>
              <button @click="confirmarEliminacion(item.id)" class="flex-1 py-1.5 border border-red-100 text-red-600 hover:bg-red-50 rounded-xl text-[11px] font-bold transition-colors"><TrashIcon class="w-3.5 h-3.5 inline mr-1" /> Eliminar</button>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 border-t flex items-center justify-center relative z-10 bg-white rounded-b-[24px]">
          <Paginacion 
              :paginaActual="paginaActual" 
              :totalPaginas="totalPaginas" 
              @cambiarPagina="p => paginaActual = p" 
          />
        </div>
      </div>
    </div>
    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-8" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-8">
      <div v-if="mostrarModal" @mousedown.self="cerrarModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/30 backdrop-blur-sm">
        <div class="bg-white w-full max-w-lg rounded-[24px] shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
          <div class="flex items-center justify-between p-6 border-b border-slate-100">
            <div>
              <h3 class="text-lg font-extrabold text-slate-900">{{ tipoFormulario === 'editar_componente' ? 'Editar Componente' : 'Añadir Registro' }}</h3>
            </div>
            <button @click="cerrarModal" class="p-1.5 text-slate-400 hover:bg-slate-100 rounded-lg"><XMarkIcon class="w-5 h-5" /></button>
          </div>
          <div class="p-6 overflow-y-auto">
            <div v-if="tipoFormulario !== 'editar_componente'" class="flex bg-slate-50 p-1 rounded-xl mb-6 border border-slate-100">
              <button @click="tipoFormulario = 'componente'" :class="['flex-1 py-2 text-xs font-bold rounded-lg', tipoFormulario === 'componente' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500']">Componente</button>
              <button @click="tipoFormulario = 'categoria'" :class="['flex-1 py-2 text-xs font-bold rounded-lg', tipoFormulario === 'categoria' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500']">Familia</button>
            </div>
            <form v-if="tipoFormulario === 'componente' || tipoFormulario === 'editar_componente'" @submit.prevent="guardarRegistro" class="space-y-4">
              <div>
                <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Nombre</label>
                <input v-model="nuevoProducto.nombre" type="text" required class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm outline-none focus:border-indigo-300" />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Descripción</label>
                <input v-model="nuevoProducto.descripcion" type="text" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm outline-none focus:border-indigo-300" />
              </div>
              <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Código Interno (SKU)</label>
                <input v-model="nuevoProducto.codigo_interno" type="text" placeholder="Ej: RES-001" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm outline-none focus:border-indigo-300" />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Ubicación Física</label>
                <input v-model="nuevoProducto.ubicacion" type="text" placeholder="Ej: Estante A" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm outline-none focus:border-indigo-300" />
              </div>
            </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Stock Inicial</label>
                  <input v-model="nuevoProducto.stock" type="number" min="0" :disabled="tipoFormulario === 'editar_componente'" required class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm outline-none disabled:opacity-50" />
                </div>
                <div>
                  <label class="block text-[10px] font-bold text-slate-400 uppercase mb-1.5">Familia</label>
                  <select v-model="nuevoProducto.categoria" required class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm outline-none cursor-pointer">
                    <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                  </select>
                </div>
              </div>
              <div class="pt-4 flex justify-end gap-2">
                <button type="button" @click="cerrarModal" class="px-5 py-2.5 text-sm font-bold text-slate-500 rounded-xl hover:bg-slate-50 transition-colors">Cancelar</button>
                <button type="submit" class="px-6 py-2.5 bg-indigo-600 text-white text-sm font-bold rounded-xl hover:bg-indigo-700 active:scale-95 transition-all">{{ tipoFormulario === 'editar_componente' ? 'Actualizar' : 'Guardar' }}</button>
              </div>
            </form>

            <form v-else @submit.prevent="guardarRegistro" class="space-y-4">
              <div>
                <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1.5">Nombre de la Familia</label>
                <input v-model="nuevaCatForm.nombre" type="text" required placeholder="Ej: Resistencias"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm font-medium outline-none focus:bg-white focus:border-indigo-300 focus:ring-2 focus:ring-indigo-50 transition-all" />
              </div>
              <div class="pt-4 flex justify-end gap-2">
                <button type="button" @click="cerrarModal" class="px-5 py-2.5 text-sm font-bold text-slate-500 hover:bg-slate-50 rounded-xl transition-colors">Cancelar</button>
                <button type="submit" class="px-6 py-2.5 bg-indigo-600 text-white text-sm font-bold rounded-xl shadow-md hover:bg-indigo-700 active:scale-95 transition-all">Crear</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </transition>

    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-8" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-8">
      <div v-if="mostrarModalTransaccion" @mousedown.self="cerrarModalTransaccion" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
        <div class="bg-white w-full max-w-sm rounded-[24px] shadow-2xl overflow-hidden p-6 text-center">
          
          <div class="w-16 h-16 mx-auto rounded-full flex items-center justify-center mb-4"
              :class="tipoTransaccion === 'extraer' ? 'bg-indigo-100 text-indigo-600' : 'bg-emerald-100 text-emerald-600'">
            <ArrowUpOnSquareIcon v-if="tipoTransaccion === 'extraer'" class="w-8 h-8" />
            <ArrowDownTrayIcon v-else class="w-8 h-8" />
          </div>

          <h3 class="text-xl font-black text-slate-800 mb-1">
            {{ tipoTransaccion === 'extraer' ? 'Extraer Componente' : 'Ingresar Devolución' }}
          </h3>
          <p class="text-sm text-slate-500 mb-6">
            {{ itemSeleccionado?.nombre }} <br>
            <span class="text-xs font-bold text-slate-400">(Disponible: {{ itemSeleccionado?.stock }})</span>
          </p>

          <div class="text-left mb-6">
            <label class="block text-[11px] font-bold text-slate-400 uppercase mb-2">Cantidad a {{ tipoTransaccion }}</label>
            <input v-model="cantidadTransaccion" type="number" min="1" :max="tipoTransaccion === 'extraer' ? itemSeleccionado?.stock : 999" 
              class="w-full text-center text-2xl font-black px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 transition-all" />
          </div>

          <div class="flex gap-3">
            <button @click="cerrarModalTransaccion" class="flex-1 py-3 text-sm font-bold text-slate-500 bg-slate-100 hover:bg-slate-200 rounded-xl transition-all">Cancelar</button>
            <button @click="confirmarTransaccion" 
              class="flex-1 py-3 text-white text-sm font-bold rounded-xl transition-all shadow-md active:scale-95"
              :class="tipoTransaccion === 'extraer' ? 'bg-indigo-600 hover:bg-indigo-700 shadow-indigo-600/20' : 'bg-emerald-500 hover:bg-emerald-600 shadow-emerald-500/20'">
              Confirmar
            </button>
          </div>
        </div>
      </div>
    </transition>

    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-8" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-8">
      <div v-if="mostrarModalEliminar" @mousedown.self="mostrarModalEliminar = false" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
        <div class="bg-white w-full max-w-sm rounded-[24px] shadow-2xl overflow-hidden p-6 text-center">
          <div class="w-16 h-16 mx-auto rounded-full bg-red-100 flex items-center justify-center mb-4">
            <TrashIcon class="w-8 h-8 text-red-600" />
          </div>
          <h3 class="text-xl font-black text-slate-800 mb-2">¿Eliminar Componente?</h3>
          <p class="text-sm text-slate-500 mb-6">Esta acción es permanente y no se podrá deshacer. ¿Estás totalmente seguro?</p>
          <div class="flex gap-3">
            <button @click="mostrarModalEliminar = false" class="flex-1 py-3 text-sm font-bold text-slate-500 bg-slate-100 hover:bg-slate-200 rounded-xl transition-all">Cancelar</button>
            <button @click="ejecutarEliminacion" class="flex-1 py-3 text-white text-sm font-bold bg-red-600 hover:bg-red-700 rounded-xl shadow-md shadow-red-600/20 active:scale-95 transition-all">Sí, Eliminar</button>
          </div>
          
        </div>
      </div>
    </transition>
    
  </div>
</template>