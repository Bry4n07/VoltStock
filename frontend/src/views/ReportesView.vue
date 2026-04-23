<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { api } from '../services/api'
import { useToast } from '../composables/useToast'
import Paginacion from '../components/pagination.vue'
import { jsPDF } from "jspdf"
import autoTable from 'jspdf-autotable'
import { 
  ChartBarIcon, ArrowPathIcon, UserCircleIcon,
  ArrowUpRightIcon, ArrowDownLeftIcon,
  CalendarDaysIcon, MagnifyingGlassIcon,
  FunnelIcon, ArchiveBoxIcon, DocumentArrowDownIcon
} from '@heroicons/vue/24/outline'

const historial = ref([])
const cargando = ref(true)
const generandoPDF = ref(false) // Nuevo estado para proteger la UI
const { showToast } = useToast()

// Filtros y Paginación
const busquedaGeneral = ref('')
const filtroTipo = ref('')
const fechaFiltro = ref('')
const paginaActual = ref(1)
const itemsPorPagina = 10

const cargarHistorial = async () => {
  cargando.value = true
  try {
    const res = await api('historial/')
    if (res.ok) {
      historial.value = await res.json()
    }
  } catch (err) {
    if (err !== 'Sesión expirada') showToast("Error al cargar la bitácora", "error")
  } finally {
    cargando.value = false
  }
}

// --- LÓGICA DE FILTRADO ---
const historialFiltrado = computed(() => {
  return historial.value.filter(item => {
    const coincideTipo = filtroTipo.value === '' || item.tipo === filtroTipo.value
    const coincideTexto = item.componente_nombre.toLowerCase().includes(busquedaGeneral.value.toLowerCase()) ||
                         item.usuario_nombre.toLowerCase().includes(busquedaGeneral.value.toLowerCase())
    const coincideFecha = fechaFiltro.value === '' || item.fecha.startsWith(fechaFiltro.value)
    return coincideTipo && coincideTexto && coincideFecha
  })
})

const totalPaginas = computed(() => Math.ceil(historialFiltrado.value.length / itemsPorPagina) || 1)
const historialPaginado = computed(() => {
  const inicio = (paginaActual.value - 1) * itemsPorPagina
  return historialFiltrado.value.slice(inicio, inicio + itemsPorPagina)
})

watch([busquedaGeneral, filtroTipo, fechaFiltro], () => { paginaActual.value = 1 })

// --- ESTADÍSTICAS ---
const stats = computed(() => {
  const datos = historialFiltrado.value 
  const salidas = datos.filter(h => h.tipo === 'SALIDA').length
  const entradas = datos.filter(h => h.tipo === 'ENTRADA').length
  
  const conteo = {}
  datos.forEach(h => {
    conteo[h.componente_nombre] = (conteo[h.componente_nombre] || 0) + 1
  })
  const topComponente = Object.keys(conteo).length > 0 
    ? Object.keys(conteo).reduce((a, b) => conteo[a] > conteo[b] ? a : b) 
    : 'N/A'

  return { total: datos.length, salidas, entradas, topComponente }
})

// --- EXPORTAR A PDF (PROTEGIDO) ---
const generarPDF = async () => {
  if (historialFiltrado.value.length === 0) {
    return showToast("No hay datos para exportar", "error")
  }

  let datosAExportar = historialFiltrado.value

  // LÍMITE DE SEGURIDAD PARA EVITAR QUE EL NAVEGADOR EXPLOTE
  if (datosAExportar.length > 1000) {
    showToast("Reporte muy grande. Exportando los últimos 1000 registros por seguridad. Usa filtros para el resto.", "info")
    datosAExportar = datosAExportar.slice(0, 1000)
  }

  generandoPDF.value = true

  // Truco: Hacemos una pausa de 100ms para permitir que Vue dibuje el spinner en el botón antes de que jsPDF bloquee el procesador
  await new Promise(resolve => setTimeout(resolve, 100))

  try {
    const doc = new jsPDF()

    doc.setFontSize(18)
    doc.setTextColor(30, 41, 59) 
    doc.text("Auditoría de Movimientos - VoltStock", 14, 20)

    doc.setFontSize(10)
    doc.setTextColor(100, 116, 139) 
    const fechaHoy = new Date().toLocaleString('es-GT')
    doc.text(`Generado el: ${fechaHoy}`, 14, 28)
    
    if (filtroTipo.value || fechaFiltro.value || busquedaGeneral.value) {
      doc.text(`Filtros aplicados | Fecha: ${fechaFiltro.value || 'Todas'} | Tipo: ${filtroTipo.value || 'Todos'}`, 14, 34)
    }

    const columnas = ["Fecha y Hora", "Responsable", "Operación", "Componente", "Cantidad"]
    const filas = datosAExportar.map(item => [
      new Date(item.fecha).toLocaleString('es-GT', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }),
      item.usuario_nombre,
      item.tipo === 'SALIDA' ? 'Despacho (-)' : 'Reingreso (+)',
      item.componente_nombre,
      item.cantidad.toString()
    ])

    autoTable(doc, {
      startY: 40,
      head: [columnas],
      body: filas,
      theme: 'grid',
      headStyles: { fillColor: [79, 70, 229], textColor: 255 }, // Color Indigo para la tabla
      alternateRowStyles: { fillColor: [248, 250, 252] }, 
      styles: { fontSize: 9, cellPadding: 3 },
    })

    doc.save(`VoltStock_Reporte_${new Date().getTime()}.pdf`)
    showToast("PDF Generado exitosamente", "success")

  } catch (error) {
    showToast("Error al compilar el PDF", "error")
  } finally {
    generandoPDF.value = false
  }
}

const formatearFecha = (fechaISO) => {
  return new Date(fechaISO).toLocaleString('es-GT', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  })
}

onMounted(cargarHistorial)
</script>

<template>
  <div class="w-full bg-slate-50 text-slate-700 font-sans p-3 sm:p-6 min-h-[80vh] flex flex-col items-center animate-fade-in relative pb-10">
    <div class="w-full max-w-[1300px] space-y-6">
      
      <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-5 sm:p-6 rounded-[24px] shadow-sm border border-slate-100">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center shrink-0">
            <ChartBarIcon class="w-6 h-6" />
          </div>
          <div>
            <h1 class="text-xl sm:text-2xl font-black text-slate-800 tracking-tight">Bitácora de Movimientos</h1>
            <p class="text-slate-500 text-xs sm:text-sm font-medium mt-0.5">Auditoría completa del sistema.</p>
          </div>
        </div>
        
        <div class="flex items-center gap-2 w-full sm:w-auto">
          <button @click="generarPDF" :disabled="generandoPDF"
                  class="flex-1 sm:flex-none px-5 py-2.5 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all bg-indigo-600 hover:bg-indigo-700 text-white shadow-md shadow-indigo-200 active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed">
            <ArrowPathIcon v-if="generandoPDF" class="w-5 h-5 animate-spin" />
            <DocumentArrowDownIcon v-else class="w-5 h-5" />
            <span>{{ generandoPDF ? 'Compilando...' : 'Exportar PDF' }}</span>
          </button>
          
          <button @click="cargarHistorial" :disabled="generandoPDF" class="p-2.5 bg-slate-50 border border-slate-200 rounded-xl hover:bg-indigo-50 hover:text-indigo-600 transition-all shadow-sm disabled:opacity-50">
            <ArrowPathIcon :class="['w-5 h-5 text-slate-500', cargando ? 'animate-spin text-indigo-600' : '']" />
          </button>
        </div>
      </header>

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white p-5 rounded-[20px] border border-slate-100 shadow-sm flex flex-col justify-between">
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Registros</p>
          <p class="text-2xl sm:text-3xl font-black text-slate-800">{{ stats.total }}</p>
        </div>
        <div class="bg-white p-5 rounded-[20px] border border-slate-100 shadow-sm border-l-4 border-l-indigo-500">
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Despachos</p>
          <p class="text-2xl sm:text-3xl font-black text-indigo-600">{{ stats.salidas }}</p>
        </div>
        <div class="bg-white p-5 rounded-[20px] border border-slate-100 shadow-sm border-l-4 border-l-emerald-500">
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Retornos</p>
          <p class="text-2xl sm:text-3xl font-black text-emerald-600">{{ stats.entradas }}</p>
        </div>
        <div class="bg-white p-5 rounded-[20px] border border-slate-100 shadow-sm">
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Más Movido</p>
          <p class="text-sm sm:text-lg font-black text-slate-800 truncate">{{ stats.topComponente }}</p>
        </div>
      </div>

      <div class="flex flex-col md:flex-row gap-3 bg-white p-3 rounded-[20px] border border-slate-100 shadow-sm">
        <div class="relative flex-1">
          <MagnifyingGlassIcon class="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
          <input v-model="busquedaGeneral" type="text" placeholder="Buscar componente o usuario..."
            class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-transparent rounded-xl text-sm font-medium outline-none focus:bg-white focus:border-indigo-200 focus:ring-2 focus:ring-indigo-50 transition-all" />
        </div>
        <div class="relative md:w-48">
          <input v-model="fechaFiltro" type="date" 
            class="w-full px-4 py-2 bg-slate-50 border border-transparent rounded-xl text-sm font-medium text-slate-600 outline-none focus:bg-white focus:border-indigo-200 focus:ring-2 focus:ring-indigo-50 transition-all" />
        </div>
        <div class="relative md:w-48">
          <FunnelIcon class="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
          <select v-model="filtroTipo" class="w-full pl-10 pr-8 py-2 bg-slate-50 border border-transparent rounded-xl text-sm font-medium outline-none appearance-none cursor-pointer focus:bg-white focus:border-indigo-200 focus:ring-2 focus:ring-indigo-50 transition-all">
            <option value="">Todo tipo</option>
            <option value="SALIDA">Despachos</option>
            <option value="ENTRADA">Retornos</option>
          </select>
        </div>
      </div>

      <div class="bg-white rounded-[24px] border border-slate-100 shadow-sm overflow-hidden relative">
        <div class="overflow-x-auto">
          <table class="w-full text-left whitespace-nowrap">
            <thead>
              <tr class="bg-slate-50/70 border-b border-slate-100">
                <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Timestamp</th>
                <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Responsable</th>
                <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Operación</th>
                <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Cant.</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="item in historialPaginado" :key="item.id" class="hover:bg-slate-50/50 transition-colors">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-2">
                    <CalendarDaysIcon class="w-4 h-4 text-slate-300" />
                    <span class="text-[11px] font-bold text-slate-500 font-mono">{{ formatearFecha(item.fecha) }}</span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-2">
                    <UserCircleIcon class="w-5 h-5 text-indigo-400" />
                    <span class="text-sm font-bold text-slate-800">{{ item.usuario_nombre }}</span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <div :class="['inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[9px] font-black uppercase tracking-wider', 
                               item.tipo === 'SALIDA' ? 'bg-indigo-50 text-indigo-600' : 'bg-emerald-50 text-emerald-600']">
                    <ArrowUpRightIcon v-if="item.tipo === 'SALIDA'" class="w-3 h-3" />
                    <ArrowDownLeftIcon v-else class="w-3 h-3" />
                    {{ item.tipo === 'SALIDA' ? 'Despacho' : 'Reingreso' }}
                  </div>
                  <div class="flex items-center gap-1.5 mt-1.5 text-[11px] text-slate-500 font-medium">
                    <ArchiveBoxIcon class="w-3.5 h-3.5 opacity-50" />
                    {{ item.componente_nombre }}
                  </div>
                </td>
                <td class="px-6 py-4 text-right">
                  <span :class="['text-sm font-black', item.tipo === 'SALIDA' ? 'text-slate-700' : 'text-emerald-600']">
                    {{ item.tipo === 'SALIDA' ? '-' : '+' }}{{ item.cantidad }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-if="historialFiltrado.length === 0" class="p-16 text-center">
          <p class="text-slate-400 font-bold">No se encontraron movimientos con esos filtros.</p>
        </div>

        <div v-if="historialFiltrado.length > 0" class="px-6 py-4 border-t border-slate-50 flex justify-center bg-white">
          <Paginacion :paginaActual="paginaActual" :totalPaginas="totalPaginas" @cambiarPagina="p => paginaActual = p" />
        </div>

        <div v-if="cargando" class="absolute inset-0 bg-white/60 backdrop-blur-[1px] flex items-center justify-center z-20">
          <div class="animate-spin rounded-full h-8 w-8 border-2 border-indigo-100 border-t-indigo-600"></div>
        </div>
        
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>