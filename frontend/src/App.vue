<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import MainLayout from './layouts/MainLayout.vue'

const route = useRoute()

// --- 1. LÓGICA DE RUTAS (LA QUE FALTABA) ---
// Esta variable es la que decide si se muestra el Sidebar o no
const esRutaAutenticacion = computed(() => {
  return route.path === '/login'
})

const tituloFormateado = computed(() => {
  if (route.name == 'inventario') return 'Inventario Global'
  if (route.name == 'cola') return 'Cola de Despacho'
  if (route.name == 'pila') return 'Pila de Retornos'
  return 'VoltStock'
})

// --- 2. ESTADO GLOBAL ---
const colaPedidos = ref([])
const pilaDevoluciones = ref([])

// --- 3. TUS FUNCIONES DE SIEMPRE ---
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
  
</template>
  