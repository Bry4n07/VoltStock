<script setup>
import { defineProps, defineEmits } from 'vue'
import { CheckCircleIcon, ClockIcon } from '@heroicons/vue/24/outline'

// Recibimos la "cola" desde App.vue
defineProps({
  pedidos: {
    type: Array,
    required: true
  }
})

// Emitimos un evento cuando queremos despachar el primer elemento
const emit = defineEmits(['despachar'])
</script>

<template>
  <div class="space-y-6 animate-fade-in">
    
    <div class="flex justify-between items-end">
      <div>
        <h3 class="text-2xl font-bold text-slate-800">Cola de Despacho</h3>
        <p class="text-sm text-slate-500 mt-1">Estructura FIFO (First In, First Out). El componente más antiguo se despacha primero.</p>
      </div>
      
      <button 
        @click="emit('despachar')"
        :disabled="pedidos.length === 0"
        :class="[
          'px-6 py-2.5 rounded-xl font-bold text-sm transition-all flex items-center gap-2 shadow-sm',
          pedidos.length === 0 
            ? 'bg-slate-100 text-slate-400 cursor-not-allowed' 
            : 'bg-indigo-600 hover:bg-indigo-700 text-white hover:shadow-md'
        ]"
      >
        <CheckCircleIcon class="w-5 h-5" />
        Despachar Siguiente
      </button>
    </div>

    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm p-8 min-h-[400px]">
      
      <div v-if="pedidos.length === 0" class="h-full flex flex-col items-center justify-center text-center opacity-70 py-20">
        <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-4 border border-slate-100">
          <ClockIcon class="w-10 h-10 text-slate-300" />
        </div>
        <h4 class="text-lg font-bold text-slate-700">La cola está vacía</h4>
        <p class="text-slate-400 max-w-sm mt-2">Ve al Inventario Global y solicita un componente para agregarlo a la cola de despacho.</p>
      </div>

      <div v-else class="space-y-4">
        <div 
          v-for="(pedido, index) in pedidos" 
          :key="pedido.id_temporal"
          :class="[
            'flex items-center justify-between p-5 rounded-xl border transition-all',
            index === 0 ? 'border-indigo-300 bg-indigo-50/30 ring-4 ring-indigo-50' : 'border-slate-200 bg-white hover:border-slate-300'
          ]"
        >
          <div class="flex items-center gap-5">
            <div :class="['w-10 h-10 rounded-lg flex items-center justify-center font-bold text-lg', index === 0 ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200' : 'bg-slate-100 text-slate-500']">
              {{ index + 1 }}
            </div>
            
            <div>
              <h4 class="font-bold text-slate-800">{{ pedido.componente.nombre }}</h4>
              <p class="text-xs text-slate-500 flex items-center gap-1 mt-1">
                <ClockIcon class="w-3.5 h-3.5" /> Solicitado a las {{ pedido.fecha }}
              </p>
            </div>
          </div>

          <span v-if="index === 0" class="bg-indigo-100 text-indigo-700 text-[10px] font-black uppercase tracking-widest px-3 py-1.5 rounded-full">
            Próximo a salir
          </span>
          <span v-else class="text-slate-300 text-sm font-medium">
            En espera
          </span>
        </div>
      </div>

    </div>
  </div>
</template>