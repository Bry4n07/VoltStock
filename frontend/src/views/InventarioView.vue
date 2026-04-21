<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import Paginacion from '../components/pagination.vue' 
import {
  MagnifyingGlassIcon, PlusIcon,
  ExclamationTriangleIcon, CubeIcon,
  TagIcon, CircleStackIcon,
  ChevronLeftIcon, ChevronRightIcon,
  XMarkIcon,
  HashtagIcon
} from '@heroicons/vue/24/outline'

// --- ESTADO ---
const componentes = ref([])
const categorias = ref([])
const cargando = ref(true)
const busqueda = ref('')
const filtroCategoria = ref('')
const mostrarModal = ref(false)
const tipoFormulario = ref('componente')

const paginaActual = ref(1)
const itemsPorPagina = 8

// Modelos
const nuevoProducto = ref({ nombre: '', descripcion: '', stock: 0, categoria: '' })
const nuevaCatForm = ref({ nombre: '' })

// --- COMPUTED (Solo UNA vez) ---
const componentesFiltrados = computed(() => {
  return componentes.value.filter(item => {
    const matchNom = item.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
    const matchCat = filtroCategoria.value === '' || item.categoria === parseInt(filtroCategoria.value)
    return matchNom && matchCat
  })
})

const totalPaginas = computed (() => {
  return Math.ceil(componentesFiltrados.value.length / itemsPorPagina) || 1 
})

const componentesPaginados = computed (() => {
  const inicio = (paginaActual.value - 1) * itemsPorPagina
  const fin = inicio + itemsPorPagina
  return componentesFiltrados.value.slice(inicio, fin)
})

const stats = computed(() => ({
  total: componentes.value.length,
  bajo: componentes.value.filter(i => i.stock < 5 && i.stock > 0).length,
  cats: categorias.value.length,
  agotados: componentes.value.filter(i => i.stock === 0).length
}))

watch([busqueda, filtroCategoria], () => {
  paginaActual.value = 1
})

// --- LÓGICA DE CIERRE ---
const manejarEsc = (e) => {
  if (e.key === 'Escape' && mostrarModal.value) {
    const elActivo = document.activeElement
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(elActivo.tagName)) {
      elActivo.blur()
    } else {
      cerrarModal()
    }
  }
}

const cerrarModal = () => {
  mostrarModal.value = false
  nuevoProducto.value = { nombre: '', descripcion: '', stock: 0, categoria: '' }
  nuevaCatForm.value = { nombre: '' }
}

// --- DATOS API ---
const obtenerDatos = async () => {
  try {
    const [resComp, resCat] = await Promise.all([
      fetch('http://127.0.0.1:8000/api/componentes/'),
      fetch('http://127.0.0.1:8000/api/categorias/')
    ])
    componentes.value = await resComp.json()
    categorias.value = await resCat.json()
  } catch (err) { console.error("Error API:", err) } finally { cargando.value = false }
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
    if (res.ok) { await obtenerDatos(); cerrarModal() }
  } catch (err) { alert("Error al guardar en el servidor") }
}

const emit = defineEmits(['solicitar', 'devolver'])

onMounted(() => {
  obtenerDatos()
  window.addEventListener('keydown', manejarEsc)
})
onUnmounted(() => window.removeEventListener('keydown', manejarEsc))
</script>

<template>
  <div class="w-full max-w-[1600px] mx-auto space-y-6 pb-12 px-4 sm:px-6 lg:px-8">

    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mt-2">
      <div>
        <h1 class="text-3xl font-extrabold text-slate-800 tracking-tight">Inventario Global</h1>
        <p class="text-sm text-slate-500 mt-1">Gestión de referencias, existencias y flujo de hardware.</p>
      </div>
      <button @click="mostrarModal = true"
        class="w-full md:w-auto flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-semibold shadow-md shadow-indigo-200 transition-all active:scale-95 text-sm">
        <PlusIcon class="w-5 h-5" />
        Nuevo Registro
      </button>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
        <div class="p-3 bg-indigo-50 rounded-xl text-indigo-600">
          <CubeIcon class="w-6 h-6" />
        </div>
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Items</p>
          <h3 class="text-2xl font-black text-slate-800 leading-none mt-1">{{ stats.total }}</h3>
        </div>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
        <div class="p-3 bg-amber-50 rounded-xl text-amber-600">
          <ExclamationTriangleIcon class="w-6 h-6" />
        </div>
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Stock Crítico</p>
          <h3 class="text-2xl font-black text-slate-800 leading-none mt-1">{{ stats.bajo }}</h3>
        </div>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
        <div class="p-3 bg-red-50 rounded-xl text-red-600">
          <TagIcon class="w-6 h-6" />
        </div>
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Agotados</p>
          <h3 class="text-2xl font-black text-slate-800 leading-none mt-1">{{ stats.agotados }}</h3>
        </div>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
        <div class="p-3 bg-emerald-50 rounded-xl text-emerald-600">
          <CircleStackIcon class="w-6 h-6" />
        </div>
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Familias</p>
          <h3 class="text-2xl font-black text-slate-800 leading-none mt-1">{{ stats.cats }}</h3>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">

      <div class="flex flex-col md:flex-row gap-0 border-b border-slate-200 bg-slate-50/50">
        <div class="relative flex-1 border-b md:border-b-0 md:border-r border-slate-200">
          <MagnifyingGlassIcon class="w-5 h-5 absolute left-5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input v-model="busqueda" type="text" placeholder="Buscar por código, nombre o descripción..."
            class="w-full pl-12 pr-6 py-4 bg-transparent border-none text-sm font-medium text-slate-700 outline-none placeholder-slate-400 focus:bg-white transition-colors" />
        </div>
        <select v-model="filtroCategoria"
          class="w-full md:w-64 px-6 py-4 bg-transparent border-none text-sm font-semibold text-slate-600 outline-none hover:bg-slate-100 cursor-pointer transition-colors">
          <option value="">Todas las Familias</option>
          <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
        </select>
      </div>

      <div class="hidden md:block overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="text-[11px] uppercase font-bold text-slate-400 tracking-wider bg-white">
              <th class="px-6 py-4 border-b border-slate-100 w-24">Ref / ID</th>
              <th class="px-6 py-4 border-b border-slate-100">Especificaciones</th>
              <th class="px-6 py-4 border-b border-slate-100 text-center">Disponibilidad</th>
              <th class="px-6 py-4 border-b border-slate-100 text-right">Acciones Operativas</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="(item, index) in componentesPaginados" :key="item.id">
              <td class="px-6 py-4">
                <div
                  class="inline-flex items-center gap-1 px-2 py-1 bg-slate-100 text-slate-600 rounded text-xs font-mono font-bold">
                  <HashtagIcon class="w-3 h-3 text-slate-400" />
                  {{ item.id.toString().padStart(4, '0') }}
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="flex flex-col">
                  <span class="font-bold text-slate-800 text-sm">{{ item.nombre }}</span>
                  <span class="text-xs text-slate-500 mt-0.5 truncate max-w-xs xl:max-w-md">{{ item.descripcion ||
                    'Sindescripción técnica' }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-center">
                <span
                  :class="['inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold border',
                    item.stock > 5 ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                      item.stock > 0 ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-red-50 text-red-700 border-red-200']">
                  <div
                    :class="['w-1.5 h-1.5 rounded-full', item.stock > 5 ? 'bg-emerald-500' : item.stock > 0 ? 'bg-amber-500' : 'bg-red-500']">
                  </div>
                  {{ item.stock }} UNID
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex justify-end gap-2">
                  <button @click="emit('solicitar', item)" :disabled="item.stock === 0"
                    class="px-3 py-1.5 bg-white border border-indigo-200 text-indigo-600 hover:bg-indigo-50 text-xs font-bold rounded-lg disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-sm">
                    Solicitar
                  </button>
                  <button @click="emit('devolver', item)"
                    class="px-3 py-1.5 bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 text-xs font-bold rounded-lg transition-colors shadow-sm">
                    Retornar
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="md:hidden bg-slate-50 p-4 space-y-4">
        <div v-for="(item, index) in componentesPaginados" :key="item.id" class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
          <div class="p-4 border-b border-slate-100 flex justify-between items-start gap-3">
            <div>
              <span
                class="inline-block px-2 py-0.5 bg-slate-100 text-slate-500 text-[10px] font-mono font-bold rounded mb-1">
                REF-{{ item.id.toString().padStart(4, '0') }}
              </span>
              <h4 class="font-bold text-slate-800 text-base leading-tight">{{ item.nombre }}</h4>
            </div>
            <div
              :class="['shrink-0 flex flex-col items-center justify-center w-12 h-12 rounded-xl border',
                item.stock > 5 ? 'bg-emerald-50 border-emerald-100 text-emerald-700' :
                  item.stock > 0 ? 'bg-amber-50 border-amber-100 text-amber-700' : 'bg-red-50 border-red-100 text-red-700']">
              <span class="text-sm font-black">{{ item.stock }}</span>
              <span class="text-[8px] font-bold uppercase">Unid</span>
            </div>
          </div>

          <div class="p-4 bg-slate-50/50 flex-1">
            <p class="text-xs text-slate-500 leading-relaxed">{{ item.descripcion || 'Sin información detallada componente en la base de datos.' }} </p>
          </div>

          <div class="p-3 border-t border-slate-100 flex gap-2 bg-white">
            <button @click="emit('solicitar', item)" :disabled="item.stock === 0"
              class="flex-1 py-2.5 bg-indigo-50 text-indigo-700 border border-indigo-100 text-xs font-bold rounded-lg disabled:opacity-40 shadow-sm active:scale-95 transition-transform">
              Solicitar
            </button>
            <button @click="emit('devolver', item)"
              class="flex-1 py-2.5 bg-white text-slate-600 border border-slate-200 text-xs font-bold rounded-lg shadow-sm active:scale-95 transition-transform hover:bg-slate-50">
              Retornar
            </button>
          </div>
        </div>
      </div>

      <div class="px-6 py-4 bg-white border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
  <p class="text-xs font-medium text-slate-500">
    Mostrando <span class="font-bold text-slate-800">{{ componentesPaginados.length }}</span> de {{ componentesFiltrados.length }} registros
  </p>
  
  <Paginacion 
    :paginaActual="paginaActual" 
    :totalPaginas="totalPaginas" 
    @cambiarPagina="nuevaPagina => paginaActual = nuevaPagina" 
  />
</div>
    </div>

    <div v-if="mostrarModal" @mousedown.self="cerrarModal"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/30 backdrop-blur-sm transition-opacity">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg flex flex-col overflow-hidden relative">

        <button @click="cerrarModal"
          class="absolute top-4 right-4 p-1 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-md transition-colors">
          <XMarkIcon class="w-6 h-6" />
        </button>

        <div class="px-6 pt-6 pb-4 border-b border-slate-100">
          <h3 class="text-xl font-bold text-slate-800">Crear Nuevo Registro</h3>
          <p class="text-sm text-slate-500 mt-1">Añade componentes o familias a la base de datos.</p>
        </div>

        <div class="flex bg-slate-50 p-1.5 mx-6 mt-6 rounded-lg border border-slate-200">
          <button @click="tipoFormulario = 'componente'"
            :class="['flex-1 py-2 text-xs font-bold rounded-md transition-colors',
              tipoFormulario === 'componente' ? 'bg-white shadow-sm text-indigo-700 border border-slate-200' : 'text-slate-500 hover:text-slate-700']">
            Componente
          </button>
          <button @click="tipoFormulario = 'categoria'"
            :class="['flex-1 py-2 text-xs font-bold rounded-md transition-colors',
              tipoFormulario === 'categoria' ? 'bg-white shadow-sm text-indigo-700 border border-slate-200' : 'text-slate-500 hover:text-slate-700']">
            Familia / Categoría
          </button>
        </div>

        <div class="p-6">
          <form v-if="tipoFormulario === 'componente'" @submit.prevent="guardarRegistro" class="space-y-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Nombre Comercial</label>
              <input v-model="nuevoProducto.nombre" type="text" required placeholder="Ej: Arduino Nano"
                class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all" />
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Descripción Técnica</label>
              <textarea v-model="nuevoProducto.descripcion" placeholder="Especificaciones, pines, voltaje..."
                class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all h-24 resize-none"></textarea>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-slate-700 mb-1">Stock Inicial</label>
                <input v-model="nuevoProducto.stock" type="number" min="0" required
                  class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none transition-all" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-700 mb-1">Categoría</label>
                <select v-model="nuevoProducto.categoria" required
                  class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none transition-all">
                  <option value="" disabled>Seleccione...</option>
                  <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                </select>
              </div>
            </div>

            <div class="pt-4 flex justify-end gap-2">
              <button type="button" @click="cerrarModal"
                class="px-5 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors">Cancelar</button>
              <button type="submit"
                class="px-5 py-2.5 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors">Guardar
                Componente</button>
            </div>
          </form>

          <form v-else @submit.prevent="guardarRegistro" class="space-y-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 mb-1">Nombre de la Familia</label>
              <input v-model="nuevaCatForm.nombre" type="text" required placeholder="Ej: Microcontroladores"
                class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all" />
            </div>
            <div class="pt-4 flex justify-end gap-2">
              <button type="button" @click="cerrarModal"
                class="px-5 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors">Cancelar</button>
              <button type="submit"
                class="px-5 py-2.5 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 shadow-sm transition-colors">Crear
                Categoría</button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>