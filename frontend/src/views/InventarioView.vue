<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import Paginacion from '../components/pagination.vue' 
import { useToast } from '../composables/useToast' 
import {
  MagnifyingGlassIcon, PlusIcon,
  ExclamationTriangleIcon, CubeIcon,
  TagIcon, CircleStackIcon,
  XMarkIcon, ArrowDownTrayIcon, ArrowUpOnSquareIcon,
  FunnelIcon, AdjustmentsHorizontalIcon,
  CpuChipIcon, CheckBadgeIcon, ExclamationCircleIcon
} from '@heroicons/vue/24/outline'

// --- ESTADO ---
const componentes = ref([])
const categorias = ref([])
const cargando = ref(true)
const busqueda = ref('')
const filtroCategoria = ref('')
const filtroStock = ref('')
const mostrarModal = ref(false)
const tipoFormulario = ref('componente')

const paginaActual = ref(1)
const itemsPorPagina = 8
const { showToast } = useToast()

const nuevoProducto = ref({ nombre: '', descripcion: '', stock: 0, categoria: '' })
const nuevaCatForm = ref({ nombre: '' })

// --- COMPUTED ---
const componentesFiltrados = computed(() => {
  return componentes.value.filter(item => {
    const matchNom = item.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
    const matchCat = filtroCategoria.value === '' || item.categoria === parseInt(filtroCategoria.value)
    
    let matchStock = true
    if (filtroStock.value === 'agotado') matchStock = item.stock === 0
    else if (filtroStock.value === 'critico') matchStock = item.stock > 0 && item.stock < 5
    else if (filtroStock.value === 'optimo') matchStock = item.stock >= 5

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
  bajo: componentes.value.filter(i => i.stock < 5 && i.stock > 0).length,
  cats: categorias.value.length,
  agotados: componentes.value.filter(i => i.stock === 0).length
}))

watch([busqueda, filtroCategoria, filtroStock], () => { paginaActual.value = 1 })

// --- LÓGICA ---
const manejarEsc = (e) => {
  if (e.key === 'Escape' && mostrarModal.value) {
    const elActivo = document.activeElement
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(elActivo.tagName)) elActivo.blur()
    else cerrarModal()
  }
}

const cerrarModal = () => {
  mostrarModal.value = false
  nuevoProducto.value = { nombre: '', descripcion: '', stock: 0, categoria: '' }
  nuevaCatForm.value = { nombre: '' }
  tipoFormulario.value = 'componente'
}

const obtenerDatos = async () => {
  try {
    const [resComp, resCat] = await Promise.all([
      fetch('http://127.0.0.1:8000/api/componentes/'),
      fetch('http://127.0.0.1:8000/api/categorias/')
    ])
    componentes.value = await resComp.json()
    categorias.value = await resCat.json()
  } catch (err) { 
    showToast("Error al cargar los datos", "error")
  } finally { cargando.value = false }
}

const guardarRegistro = async () => {
  const url = tipoFormulario.value === 'componente' ? 'componentes/' : 'categorias/'
  const body = tipoFormulario.value === 'componente' ? nuevoProducto.value : nuevaCatForm.value

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/${url}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    
    if (res.ok) { 
      await obtenerDatos()
      cerrarModal()
      showToast(`¡Guardado con éxito!`, "success")
    } else {
      showToast("Verifica los datos", "error")
    }
  } catch (err) { showToast("Error de conexión", "error") }
}

const emit = defineEmits(['solicitar', 'devolver'])

onMounted(() => {
  obtenerDatos()
  window.addEventListener('keydown', manejarEsc)
})
onUnmounted(() => window.removeEventListener('keydown', manejarEsc))
</script>

<template>
  <div class="w-full bg-white text-slate-700 font-sans p-2 sm:p-6">
    <div class="max-w-[1400px] mx-auto space-y-5 sm:space-y-6">
      
      <header class="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <div class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-indigo-50 text-indigo-600 rounded-md text-[10px] font-bold tracking-[0.1em] uppercase mb-2">
            <CheckBadgeIcon class="w-3.5 h-3.5" /> Sistema Online
          </div>
          <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">Catálogo de Hardware</h1>
          <p class="text-slate-500 mt-1 text-sm font-medium">Gestiona y supervisa el inventario de VoltStock en tiempo real.</p>
        </div>
        
        <button @click="mostrarModal = true"
          class="flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-bold shadow-md shadow-indigo-600/20 transition-all active:scale-95 w-full md:w-auto group">
          <PlusIcon class="w-5 h-5 group-hover:rotate-90 transition-transform duration-300" />
          Añadir Registro
        </button>
      </header>

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        
        <div class="relative bg-white p-4 sm:p-5 rounded-[20px] border border-slate-100 shadow-sm flex flex-col justify-between overflow-hidden group hover:shadow-md transition-all duration-300">
          <div class="absolute top-0 right-0 w-16 h-16 sm:w-20 sm:h-20 bg-indigo-50/80 rounded-bl-[100%] transition-transform duration-500 group-hover:scale-110"></div>
          <div class="absolute top-3 right-3 sm:top-4 sm:right-4 text-indigo-500 group-hover:rotate-12 transition-transform duration-300">
            <CubeIcon class="w-4 h-4 sm:w-5 sm:h-5" />
          </div>
          
          <div class="relative z-10 mb-4 sm:mb-6">
            <h3 class="text-slate-400 font-bold uppercase tracking-widest text-[9px] sm:text-[10px] line-clamp-1">Inventario Total</h3>
          </div>
          <div class="relative z-10">
            <div class="text-2xl sm:text-3xl font-black text-slate-800 mb-1 leading-none">{{ stats.total }}</div>
            <p class="text-[9px] sm:text-[10px] text-slate-500 font-medium line-clamp-1">Registros activos</p>
          </div>
        </div>

        <div class="relative bg-white p-4 sm:p-5 rounded-[20px] border border-slate-100 shadow-sm flex flex-col justify-between overflow-hidden group hover:shadow-md transition-all duration-300">
          <div class="absolute top-0 right-0 w-16 h-16 sm:w-20 sm:h-20 bg-slate-50 rounded-bl-[100%] transition-transform duration-500 group-hover:scale-110"></div>
          <div class="absolute top-3 right-3 sm:top-4 sm:right-4 text-slate-400 group-hover:rotate-12 transition-transform duration-300">
            <CircleStackIcon class="w-4 h-4 sm:w-5 sm:h-5" />
          </div>

          <div class="relative z-10 mb-4 sm:mb-6">
            <h3 class="text-slate-400 font-bold uppercase tracking-widest text-[9px] sm:text-[10px] line-clamp-1">Familias</h3>
          </div>
          <div class="relative z-10">
            <div class="text-2xl sm:text-3xl font-black text-slate-800 mb-1 leading-none">{{ stats.cats }}</div>
            <p class="text-[9px] sm:text-[10px] text-slate-500 font-medium line-clamp-1">Categorías</p>
          </div>
        </div>

        <div class="relative bg-white p-4 sm:p-5 rounded-[20px] border border-slate-100 shadow-sm flex flex-col justify-between overflow-hidden group hover:shadow-md transition-all duration-300">
          <div class="absolute top-0 right-0 w-16 h-16 sm:w-20 sm:h-20 bg-amber-50/80 rounded-bl-[100%] transition-transform duration-500 group-hover:scale-110"></div>
          <div class="absolute top-3 right-3 sm:top-4 sm:right-4 text-amber-500 group-hover:-rotate-12 transition-transform duration-300">
            <ExclamationTriangleIcon class="w-4 h-4 sm:w-5 sm:h-5" />
          </div>

          <div class="relative z-10 mb-4 sm:mb-6">
            <h3 class="text-slate-400 font-bold uppercase tracking-widest text-[9px] sm:text-[10px] line-clamp-1">Stock Crítico</h3>
          </div>
          <div class="relative z-10">
            <div class="text-2xl sm:text-3xl font-black text-amber-500 mb-1 leading-none flex items-center gap-1.5">
              {{ stats.bajo }}
              <span v-if="stats.bajo > 0" class="relative flex h-2 w-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
              </span>
            </div>
            <p class="text-[9px] sm:text-[10px] text-slate-500 font-medium line-clamp-1">Bajo mínimo</p>
          </div>
        </div>

        <div class="relative bg-white p-4 sm:p-5 rounded-[20px] border border-slate-100 shadow-sm flex flex-col justify-between overflow-hidden group hover:shadow-md transition-all duration-300">
          <div class="absolute top-0 right-0 w-16 h-16 sm:w-20 sm:h-20 bg-red-50/80 rounded-bl-[100%] transition-transform duration-500 group-hover:scale-110"></div>
          <div class="absolute top-3 right-3 sm:top-4 sm:right-4 text-red-500 group-hover:rotate-12 transition-transform duration-300">
            <ExclamationCircleIcon class="w-4 h-4 sm:w-5 sm:h-5" />
          </div>

          <div class="relative z-10 mb-4 sm:mb-6">
            <h3 class="text-slate-400 font-bold uppercase tracking-widest text-[9px] sm:text-[10px] line-clamp-1">Agotados</h3>
          </div>
          <div class="relative z-10">
            <div class="text-2xl sm:text-3xl font-black text-red-500 mb-1 leading-none">{{ stats.agotados }}</div>
            <p class="text-[9px] sm:text-[10px] text-slate-500 font-medium line-clamp-1">Requieren stock</p>
          </div>
        </div>

      </div>

      <div class="bg-white rounded-[24px] border border-slate-100 shadow-sm flex flex-col">
        
        <div class="p-4 border-b border-slate-100 flex flex-col md:flex-row gap-3">
          <div class="relative flex-1">
            <MagnifyingGlassIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
            <input v-model="busqueda" type="text" placeholder="Buscar por nombre o ID de componente..."
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
                <option value="optimo">Óptimo (+5)</option>
                <option value="critico">Crítico (1-4)</option>
                <option value="agotado">Agotados (0)</option>
              </select>
            </div>
          </div>
        </div>

        <div class="hidden lg:block overflow-x-auto rounded-b-[24px]">
          <table class="w-full text-left">
            <thead>
              <tr class="border-b border-slate-100 bg-slate-50/30">
                <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest w-32">ID.Ref</th>
                <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Componente</th>
                <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Estado Inventario</th>
                <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="item in componentesPaginados" :key="item.id" class="hover:bg-slate-50/50 transition-colors group">
                <td class="px-6 py-4 align-middle">
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-slate-100 text-slate-500 rounded-md text-xs font-mono font-bold group-hover:bg-indigo-50 group-hover:text-indigo-600 transition-colors">
                    <TagIcon class="w-3 h-3" /> {{ item.id.toString().padStart(4, '0') }}
                  </span>
                </td>
                <td class="px-6 py-4 align-middle">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center shrink-0">
                      <CpuChipIcon class="w-4 h-4 text-slate-400" />
                    </div>
                    <div>
                      <p class="font-bold text-slate-800 text-sm">{{ item.nombre }}</p>
                      <p class="text-[11px] text-slate-400 mt-0.5 line-clamp-1">{{ item.descripcion || 'Sin descripción técnica.' }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 align-middle text-center">
                  <div class="flex justify-center">
                    <div :class="[
                        'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold',
                        item.stock > 5 ? 'bg-emerald-50 text-emerald-700' :
                        item.stock > 0 ? 'bg-amber-50 text-amber-700' : 'bg-red-50 text-red-700'
                      ]">
                      <div :class="['w-1.5 h-1.5 rounded-full', item.stock > 5 ? 'bg-emerald-500' : item.stock > 0 ? 'bg-amber-500' : 'bg-red-500']"></div>
                      {{ item.stock }} UDS.
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 align-middle">
                  <div class="flex items-center justify-end gap-2">
                    <button @click="emit('solicitar', item)" :disabled="item.stock === 0"
                      class="p-2 bg-white border border-slate-200 text-indigo-600 hover:bg-indigo-50 hover:border-indigo-200 rounded-lg transition-all disabled:opacity-40 disabled:cursor-not-allowed" title="Extraer">
                      <ArrowUpOnSquareIcon class="w-4 h-4" />
                    </button>
                    <button @click="emit('devolver', item)"
                      class="p-2 bg-white border border-slate-200 text-slate-500 hover:bg-slate-50 rounded-lg transition-all" title="Ingresar">
                      <ArrowDownTrayIcon class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="componentesPaginados.length === 0">
                <td colspan="4" class="px-6 py-12 text-center">
                  <div class="flex flex-col items-center justify-center">
                    <MagnifyingGlassIcon class="w-8 h-8 text-slate-300 mb-3" />
                    <p class="text-sm font-bold text-slate-600">No se encontraron componentes</p>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="lg:hidden p-4 bg-slate-50/50 flex flex-col gap-3.5">
          <div v-for="item in componentesPaginados" :key="item.id" 
               class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm relative overflow-hidden flex flex-col gap-3">
            
            <div :class="['absolute left-0 top-0 bottom-0 w-1', item.stock > 5 ? 'bg-emerald-400' : item.stock > 0 ? 'bg-amber-400' : 'bg-red-400']"></div>

            <div class="flex items-start justify-between gap-3 pl-1">
              <div class="flex items-start gap-3 flex-1 min-w-0">
                <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center shrink-0 mt-0.5">
                  <CpuChipIcon class="w-4 h-4 text-slate-400" />
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1">
                    <h4 class="font-bold text-slate-800 text-sm truncate pr-2">{{ item.nombre }}</h4>
                    <div :class="['shrink-0 px-1.5 py-0.5 rounded text-[9px] font-black', item.stock > 5 ? 'bg-emerald-50 text-emerald-700' : item.stock > 0 ? 'bg-amber-50 text-amber-700' : 'bg-red-50 text-red-700']">
                      {{ item.stock }} UD
                    </div>
                  </div>
                  <span class="inline-flex items-center gap-1 text-[10px] text-slate-400 font-mono">
                    <TagIcon class="w-3 h-3" /> ID-{{ item.id.toString().padStart(4, '0') }}
                  </span>
                </div>
              </div>
            </div>
            
            <div class="flex gap-2 pl-12">
              <button @click="emit('solicitar', item)" :disabled="item.stock === 0"
                class="flex-1 flex items-center justify-center gap-1.5 py-2 bg-indigo-50/80 text-indigo-700 hover:bg-indigo-100 rounded-xl text-[11px] font-bold disabled:opacity-40 transition-all">
                <ArrowUpOnSquareIcon class="w-3.5 h-3.5" /> Extraer
              </button>
              <button @click="emit('devolver', item)"
                class="flex-1 flex items-center justify-center gap-1.5 py-2 bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 rounded-xl text-[11px] font-bold transition-all">
                <ArrowDownTrayIcon class="w-3.5 h-3.5" /> Ingresar
              </button>
            </div>
          </div>
          
          <div v-if="componentesPaginados.length === 0" class="p-8 text-center bg-white rounded-2xl border border-slate-100">
            <p class="text-sm font-bold text-slate-500">No se encontraron componentes.</p>
          </div>
        </div>

        <div class="px-6 py-4 bg-white border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4 rounded-b-[24px]">
          <p class="text-xs font-medium text-slate-500">
            Mostrando <span class="text-slate-800 font-bold">{{ componentesPaginados.length }}</span> de {{ componentesFiltrados.length }}
          </p>
          <Paginacion :paginaActual="paginaActual" :totalPaginas="totalPaginas" @cambiarPagina="p => paginaActual = p" />
        </div>
      </div>
    </div>

    <transition 
      enter-active-class="transition-all duration-300 ease-out" 
      enter-from-class="opacity-0 translate-y-8" 
      enter-to-class="opacity-100 translate-y-0" 
      leave-active-class="transition-all duration-200 ease-in" 
      leave-from-class="opacity-100 translate-y-0" 
      leave-to-class="opacity-0 translate-y-8">
      <div v-if="mostrarModal" @mousedown.self="cerrarModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/30 backdrop-blur-sm">
        
        <div class="bg-white w-full max-w-lg rounded-[24px] shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
          
          <div class="flex items-center justify-between p-6 border-b border-slate-100">
            <div>
              <h3 class="text-lg font-extrabold text-slate-900">Añadir Registro</h3>
              <p class="text-xs text-slate-500 mt-0.5">Ingresa los datos al sistema.</p>
            </div>
            <button @click="cerrarModal" class="p-1.5 text-slate-400 hover:text-slate-700 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors"><XMarkIcon class="w-5 h-5" /></button>
          </div>

          <div class="p-6 overflow-y-auto">
            <div class="flex bg-slate-50 p-1 rounded-xl mb-6 border border-slate-100">
              <button @click="tipoFormulario = 'componente'" :class="['flex-1 py-2 text-xs font-bold rounded-lg transition-all', tipoFormulario === 'componente' ? 'bg-white shadow-sm text-indigo-600 border border-slate-200/50' : 'text-slate-500 hover:text-slate-700']">Componente</button>
              <button @click="tipoFormulario = 'categoria'" :class="['flex-1 py-2 text-xs font-bold rounded-lg transition-all', tipoFormulario === 'categoria' ? 'bg-white shadow-sm text-indigo-600 border border-slate-200/50' : 'text-slate-500 hover:text-slate-700']">Familia</button>
            </div>

            <form v-if="tipoFormulario === 'componente'" @submit.prevent="guardarRegistro" class="space-y-4">
              <div>
                <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1.5">Nombre Comercial</label>
                <input v-model="nuevoProducto.nombre" type="text" required placeholder="Ej. Diodo LED Rojo"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm font-medium outline-none focus:bg-white focus:border-indigo-300 focus:ring-2 focus:ring-indigo-50 transition-all" />
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1.5">Stock</label>
                  <input v-model="nuevoProducto.stock" type="number" min="0" required
                    class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm font-medium outline-none focus:bg-white focus:border-indigo-300 focus:ring-2 focus:ring-indigo-50 transition-all" />
                </div>
                <div>
                  <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1.5">Familia</label>
                  <select v-model="nuevoProducto.categoria" required
                    class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200/60 rounded-xl text-sm font-medium outline-none focus:bg-white focus:border-indigo-300 focus:ring-2 focus:ring-indigo-50 transition-all appearance-none cursor-pointer">
                    <option value="" disabled>Seleccionar...</option>
                    <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                  </select>
                </div>
              </div>

              <div class="pt-4 flex justify-end gap-2">
                <button type="button" @click="cerrarModal" class="px-5 py-2.5 text-sm font-bold text-slate-500 hover:bg-slate-50 rounded-xl transition-colors">Cancelar</button>
                <button type="submit" class="px-6 py-2.5 bg-indigo-600 text-white text-sm font-bold rounded-xl shadow-md hover:bg-indigo-700 active:scale-95 transition-all">Guardar</button>
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
  </div>
</template>