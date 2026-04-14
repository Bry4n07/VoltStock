
<script setup>
import { ref, computed} from 'vue'
import {useRoute} from 'vue-router'
import MainLayout from './layouts/MainLayout.vue';

const route = useRoute()

const tituloFormateado = computed(() => {
  if (route.name === 'inventario') return 'Inventario Global'
  if (route.name === 'cola') return 'Cola de Despacho'
  return 'VoltStock'
})

const colaPedidos = ref([])
//const pilaDevoluciones = ref([])

const manejaSolicitud = (componente) => {
  colaPedidos.value.push({
    id_temporal: Date.now(),
    componente: componente,
    fecha: new Date().toLocaleTimesString()
  })
  alert('${componente.nombre} agregado a la cola de despacho.')
}
const manejarDespacho = () => {
  if (colaPedidos.value.leght > 0) {
    const despacho = colaPedidos.value.shift()
    aler('¡Se despachó el componente: ${despacho.componente.nombre}!')
  }
}
</script>
<template>
  <MainLayout>
    <router-view
    :pedidos="colaPedidos"
    @solicitar="manejarSolicitud"
    @despachar="manejarDespacho"
    ></router-view>  
  </MainLayout>
</template>
<style>
</style>