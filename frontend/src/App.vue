<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { isLoadingGlobal } from './services/api'
import MainLayout from './layouts/MainLayout.vue'

const route = useRoute()

// Logica de Rutas
const esRutaAutenticacion = computed(() => {
  return route.path === '/login'
})

const tituloFormateado = computed(() => {
  if (route.name == 'inventario') return 'Inventario Global'
  if (route.name == 'cola') return 'Cola de Despacho'
  if (route.name == 'pila') return 'Pila de Retornos'
  if (route.name == 'reportes') return 'Reportes'
  if (route.name == 'register') return 'Registro de personal'
  return 'VoltStock'
})

// Estado Global
const colaPedidos = ref([])
const pilaDevoluciones = ref([])

const manejarSolicitud = (componente) => {
  colaPedidos.value.push({
    id_temporal: Date.now(),
    componente: componente,
    fecha: new Date().toLocaleTimeString()
  })
}

const manejarDespacho = () => {
  if (colaPedidos.value.length > 0) {
    const despacho = colaPedidos.value.shift()
    alert(`¡Se Despachó el componente: ${despacho.componente.nombre}!`)
  }
}

const manejarDevolucion = (componente) => {
  pilaDevoluciones.value.push({
    id_temporal: Date.now(),
    componente: componente,
    fecha: new Date().toLocaleDateString()
  })
}

const manejarReingreso = () => {
  if (pilaDevoluciones.value.length > 0) {
    const reingreso = pilaDevoluciones.value.pop()
    alert(`¡Reingresado a bodega: ${reingreso.componente.nombre}!`)
  }
} 
</script>

<template>
  
  <div v-if="esRutaAutenticacion">
    <router-view />
  </div>

  <MainLayout v-else :titulo="tituloFormateado">
    <router-view v-slot="{ Component }">
      <component 
        :is="Component" 
        :pedidos="colaPedidos" 
        :devoluciones="pilaDevoluciones" 
        @solicitar="manejarSolicitud"
        @despachar="manejarDespacho" 
        @devolver="manejarDevolucion" 
        @reingresar="manejarReingreso" 
      />
    </router-view>
    
  </MainLayout>
  
  <Teleport to="body">
    <transition name="fade">
      <div v-if="isLoadingGlobal" class="fixed inset-0 z-[999999] flex items-center justify-center bg-slate-100/50 backdrop-blur-md">
        
        <div class="flex flex-col items-center">
          
          <div class="relative w-24 h-32 flex flex-col items-center justify-end mb-4">
            
            <div class="w-14 h-14 bg-gradient-to-tr from-indigo-500 to-emerald-400 rounded-2xl shadow-[0_10px_20px_rgba(99,102,241,0.4)] flex items-center justify-center animate-squish relative overflow-hidden z-10">
               <svg class="w-7 h-7 text-white animate-pulse" fill="currentColor" viewBox="0 0 24 24"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
               <div class="absolute top-0 left-0 w-full h-1/2 bg-white/20 rounded-b-full"></div>
            </div>
            
            <div class="w-10 h-2 bg-indigo-900/10 rounded-full blur-[2px] animate-sombra mt-1"></div>
          </div>

          <div class="bg-white/90 border border-slate-100 px-6 py-3 rounded-full shadow-lg shadow-slate-200/50 flex items-center gap-3">
            <span class="text-indigo-600 font-black tracking-widest text-[11px] uppercase">Cargando</span>
            <div class="flex gap-1.5">
              <span class="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style="animation-delay: 0s"></span>
              <span class="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style="animation-delay: 0.15s"></span>
              <span class="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style="animation-delay: 0.3s"></span>
            </div>
          </div>

        </div>

      </div>
    </transition>
  </Teleport>
</template>
<style>
/* Animación suave para aparecer y desaparecer */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* El secreto del efecto Cute: Squash & Stretch */
@keyframes squish {
  0%, 100% {
    /* En el suelo: Aplastado y gordito */
    transform: translateY(0) scaleY(0.7) scaleX(1.2);
    border-radius: 20px;
  }
  15% {
    /* Empieza a saltar: Se estira hacia arriba */
    transform: translateY(-15px) scaleY(1.1) scaleX(0.9);
  }
  50% {
    /* En el aire (punto más alto): Estirado y relajado */
    transform: translateY(-50px) scaleY(1.05) scaleX(0.95);
    border-radius: 12px;
  }
  85% {
    /* Cayendo: Se estira por la gravedad */
    transform: translateY(-15px) scaleY(1.1) scaleX(0.9);
  }
}

/* La sombra debe achicarse cuando el cubo está lejos del suelo */
@keyframes shadow-scale {
  0%, 100% {
    transform: scaleX(1.4);
    opacity: 0.8;
  }
  50% {
    transform: scaleX(0.4);
    opacity: 0.2;
  }
}

/* Aplicamos la animación infinita en bucle de 0.8 segundos */
.animate-squish {
  animation: squish 0.8s cubic-bezier(0.28, 0.84, 0.42, 1) infinite;
}
.animate-sombra {
  animation: shadow-scale 0.8s cubic-bezier(0.28, 0.84, 0.42, 1) infinite;
}
</style>