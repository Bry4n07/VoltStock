<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from '../services/api'
import { useToast } from '../composables/useToast'
import { useRouter } from 'vue-router'
import { 
  ArchiveBoxIcon, ExclamationTriangleIcon, 
  QueueListIcon, Square3Stack3DIcon, ClockIcon, 
  ArrowUpRightIcon, ArrowDownLeftIcon, CheckCircleIcon,
  ChartBarIcon, ChevronRightIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const { showToast } = useToast()

const cargando = ref(true)
const nombreUsuario = ref('')
const stats = ref({
  totalComponentes: 0,
  stockGlobal: 0,
  pedidosPendientes: 0,
  retornosPendientes: 0
})

const alertasStock = ref([])
const actividadReciente = ref([])

// Saludo dinámico según la hora
const saludo = computed(() => {
  const hora = new Date().getHours()
  if (hora >= 5 && hora < 12) return 'Buenos días'
  if (hora >= 12 && hora < 18) return 'Buenas tardes'
  return 'Buenas noches'
})

const fechaActual = computed(() => {
  return new Date().toLocaleDateString('es-GT', { 
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
  })
})

const cargarDashboard = async () => {
  cargando.value = true
  try {
    // 1. Intentar obtener el nombre del usuario (Desde LocalStorage o API)
    // Ajusta la ruta 'auth/me/' a la que uses en tu backend de Django
    const localName = localStorage.getItem('user_name')
    if (localName) {
      nombreUsuario.value = localName
    } else {
      try {
        const resUser = await api('auth/me/') // Endpoint ficticio/común de usuario
        if (resUser.ok) {
          const userData = await resUser.json()
          nombreUsuario.value = userData.first_name || userData.username || 'Ingeniero'
          localStorage.setItem('user_name', nombreUsuario.value) // Guardar para la próxima
        }
      } catch (e) { /* Silencioso si no existe el endpoint aún */ }
    }

    // 2. Cargar las métricas
    const [resComp, resPed, resDev, resHist] = await Promise.all([
      api('componentes/'),
      api('pedidos/'),
      api('devoluciones/'),
      api('historial/')
    ])

    if (resComp.ok) {
      const componentes = await resComp.json()
      stats.value.totalComponentes = componentes.length
      stats.value.stockGlobal = componentes.reduce((acc, curr) => acc + curr.stock, 0)
      
      alertasStock.value = componentes
        .filter(c => c.stock < 10)
        .sort((a, b) => a.stock - b.stock)
        .slice(0, 5) 
    }

    if (resPed.ok) {
      const pedidos = await resPed.json()
      stats.value.pedidosPendientes = pedidos.length
    }

    if (resDev.ok) {
      const devoluciones = await resDev.json()
      stats.value.retornosPendientes = devoluciones.length
    }

    if (resHist.ok) {
      const historial = await resHist.json()
      actividadReciente.value = historial.slice(0, 6)
    }

  } catch (err) {
    if (err !== 'Sesión expirada') showToast("Error al sincronizar dashboard", "error")
  } finally {
    cargando.value = false
  }
}

const formatearHora = (fechaISO) => {
  return new Date(fechaISO).toLocaleTimeString('es-GT', { hour: '2-digit', minute: '2-digit' })
}

const navegarA = (ruta) => {
  router.push(ruta)
}

onMounted(cargarDashboard)
</script>

<template>
  <div class="w-full bg-slate-50/50 text-slate-700 font-sans p-3 sm:p-6 min-h-[85vh] animate-fade-in relative pb-10">
    
    <div class="max-w-[1400px] mx-auto space-y-6">
      
      <header class="flex flex-col md:flex-row md:items-center justify-between gap-6 bg-white p-6 sm:p-8 rounded-[32px] shadow-sm border border-slate-100">
        
        <div>
          <h1 class="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
            {{ saludo }}, <span class="text-indigo-600 capitalize">{{ nombreUsuario }}</span>
          </h1>
          <p class="text-slate-500 text-sm font-medium mt-1.5 flex items-center gap-2">
            <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ fechaActual }}
          </p>
        </div>
        

        <button @click="cargarDashboard" class="p-3.5 bg-slate-50 hover:bg-indigo-50 border border-slate-100 hover:border-indigo-100 rounded-2xl transition-all group shadow-sm flex-shrink-0">
          <ArrowPathIcon class="w-6 h-6 text-slate-400 group-hover:text-indigo-600 transition-colors" />
        </button>

      </header>

      <div class="space-y-6">
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          <div @click="navegarA('/inventario')" class="bg-white p-6 rounded-[24px] border border-slate-100 shadow-sm hover:shadow-md transition-shadow cursor-pointer group">
            <div class="flex justify-between items-start mb-4">
              <div class="p-3 bg-indigo-50 text-indigo-600 rounded-2xl group-hover:scale-110 transition-transform">
                <ArchiveBoxIcon class="w-6 h-6" />
              </div>
              <span class="text-[10px] font-black text-indigo-400 uppercase tracking-widest">Catálogo</span>
            </div>
            <h3 class="text-3xl font-black text-slate-800">{{ stats.totalComponentes }}</h3>
            <p class="text-sm text-slate-500 font-medium mt-1">Componentes registrados</p>
          </div>

          <div class="bg-white p-6 rounded-[24px] border border-slate-100 shadow-sm">
            <div class="flex justify-between items-start mb-4">
              <div class="p-3 bg-emerald-50 text-emerald-600 rounded-2xl">
                <ChartBarIcon class="w-6 h-6" />
              </div>
              <span class="text-[10px] font-black text-emerald-400 uppercase tracking-widest">Volumen</span>
            </div>
            <h3 class="text-3xl font-black text-slate-800">{{ stats.stockGlobal }}</h3>
            <p class="text-sm text-slate-500 font-medium mt-1">Unidades físicas en bodega</p>
          </div>

          <div @click="navegarA('/cola')" class="bg-white p-6 rounded-[24px] border border-slate-100 shadow-sm hover:shadow-md transition-shadow cursor-pointer group relative overflow-hidden">
            <div v-if="stats.pedidosPendientes > 0" class="absolute top-0 right-0 w-2 h-full bg-amber-400"></div>
            <div class="flex justify-between items-start mb-4">
              <div class="p-3 bg-amber-50 text-amber-600 rounded-2xl group-hover:scale-110 transition-transform">
                <QueueListIcon class="w-6 h-6" />
              </div>
              <span class="text-[10px] font-black text-amber-400 uppercase tracking-widest">FIFO</span>
            </div>
            <h3 class="text-3xl font-black text-slate-800">{{ stats.pedidosPendientes }}</h3>
            <p class="text-sm text-slate-500 font-medium mt-1">Entregas pendientes</p>
          </div>

          <div @click="navegarA('/pila')" class="bg-white p-6 rounded-[24px] border border-slate-100 shadow-sm hover:shadow-md transition-shadow cursor-pointer group relative overflow-hidden">
            <div v-if="stats.retornosPendientes > 0" class="absolute top-0 right-0 w-2 h-full bg-emerald-400"></div>
            <div class="flex justify-between items-start mb-4">
              <div class="p-3 bg-emerald-50 text-emerald-600 rounded-2xl group-hover:scale-110 transition-transform">
                <Square3Stack3DIcon class="w-6 h-6" />
              </div>
              <span class="text-[10px] font-black text-emerald-400 uppercase tracking-widest">LIFO</span>
            </div>
            <h3 class="text-3xl font-black text-slate-800">{{ stats.retornosPendientes }}</h3>
            <p class="text-sm text-slate-500 font-medium mt-1">Retornos por auditar</p>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 bg-white rounded-[28px] border border-slate-100 shadow-sm p-6 sm:p-8">
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center gap-3">
                <div class="p-2 bg-red-50 text-red-500 rounded-xl"><ExclamationTriangleIcon class="w-6 h-6" /></div>
                <div>
                  <h2 class="text-lg font-black text-slate-800">Alertas de Stock Crítico</h2>
                  <p class="text-xs text-slate-500 font-medium">Componentes con menos de 10 unidades.</p>
                </div>
              </div>
              <button @click="navegarA('/inventario')" class="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
                Ver Inventario <ChevronRightIcon class="w-3 h-3" />
              </button>
            </div>

            <div v-if="alertasStock.length === 0" class="bg-emerald-50/50 border border-emerald-100 rounded-[20px] p-8 text-center">
              <CheckCircleIcon class="w-12 h-12 text-emerald-400 mx-auto mb-3" />
              <h3 class="text-slate-700 font-bold">Laboratorio Abastecido</h3>
              <p class="text-slate-500 text-xs mt-1">Ningún componente está en niveles críticos actualmente.</p>
            </div>

            <div v-else class="space-y-3">
              <div v-for="alerta in alertasStock" :key="alerta.id" class="flex items-center justify-between p-4 bg-slate-50/80 rounded-2xl border border-slate-100 hover:border-red-200 transition-colors">
                <div class="flex items-center gap-4">
                  <div class="w-2 h-10 rounded-full" :class="alerta.stock <= 3 ? 'bg-red-500' : 'bg-amber-400'"></div>
                  <div>
                    <h4 class="text-sm font-bold text-slate-800">{{ alerta.nombre }}</h4>
                    <p class="text-xs text-slate-500 font-mono mt-0.5">{{ alerta.codigo_interno || 'Sin SKU' }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <span class="text-lg font-black" :class="alerta.stock <= 3 ? 'text-red-600' : 'text-amber-600'">{{ alerta.stock }}</span>
                  <span class="text-[10px] text-slate-400 font-bold ml-1 uppercase">Restantes</span>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-[28px] border border-slate-100 shadow-sm p-6 sm:p-8">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-lg font-black text-slate-800">Actividad Reciente</h2>
              <button @click="navegarA('/reportes')" class="p-1.5 hover:bg-slate-50 rounded-lg transition-colors">
                <ArrowUpRightIcon class="w-4 h-4 text-slate-400" />
              </button>
            </div>

            <div v-if="actividadReciente.length === 0" class="text-center py-10">
              <ClockIcon class="w-10 h-10 text-slate-200 mx-auto mb-2" />
              <p class="text-sm font-medium text-slate-400">Sin movimientos recientes.</p>
            </div>

            <div v-else class="relative before:absolute before:inset-0 before:ml-[1.1rem] before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 before:to-transparent">
              <div v-for="mov in actividadReciente" :key="mov.id" class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active mb-5">
                <div :class="['flex items-center justify-center w-8 h-8 rounded-full border-4 border-white shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-sm relative z-10',
                              mov.tipo === 'SALIDA' ? 'bg-indigo-500' : 'bg-emerald-500']">
                  <ArrowUpRightIcon v-if="mov.tipo === 'SALIDA'" class="w-3 h-3 text-white" />
                  <ArrowDownLeftIcon v-else class="w-3 h-3 text-white" />
                </div>
                
                <div class="w-[calc(100%-3rem)] md:w-[calc(50%-2rem)] bg-slate-50 p-3 rounded-xl border border-slate-100 hover:shadow-md transition-shadow">
                  <div class="flex justify-between items-start mb-1">
                    <span class="text-[10px] font-black text-slate-400">{{ formatearHora(mov.fecha) }}</span>
                    <span :class="['text-[10px] font-black px-1.5 py-0.5 rounded', 
                                  mov.tipo === 'SALIDA' ? 'bg-indigo-100 text-indigo-700' : 'bg-emerald-100 text-emerald-700']">
                      {{ mov.tipo === 'SALIDA' ? '-' : '+' }}{{ mov.cantidad }}
                    </span>
                  </div>
                  <p class="text-xs font-bold text-slate-800 line-clamp-1">{{ mov.componente_nombre }}</p>
                  <p class="text-[9px] text-slate-500 mt-1 italic">{{ mov.usuario_nombre }}</p>
                </div>
              </div>
            </div>
            
            <button @click="navegarA('/reportes')" class="w-full mt-4 py-2.5 bg-slate-50 hover:bg-slate-100 text-slate-600 text-xs font-black rounded-xl transition-colors">
              Ver Bitácora Completa
            </button>
          </div>
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