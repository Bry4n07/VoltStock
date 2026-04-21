<script setup>
import { computed } from 'vue';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
    paginaActual: {
        type: Number,
        required: true
    },
    totalPaginas: {
        type: Number,
        required: true
    }
})

const emit = defineEmits(['cambiarPagina'])

const paginas = computed(() => {
    let pags = []
    for (let i = 0; i <= props.totalPaginas; i++) {
        pags.push(i)
    }
    return pags
})

const irSiguiente = () => {
    if (props.paginaActual < props.totalPaginas) emit('cambiarPagina', props.paginaActual + 1)
}
</script>
<template>
    <div class="flex items-center gap-2" v-if="totalPaginas > 1">
    <button 
      @click="irAnterior" 
      :disabled="paginaActual === 1"
      class="p-2 rounded-xl bg-white border border-slate-200 text-slate-400 hover:text-indigo-600 hover:border-indigo-200 disabled:opacity-40 disabled:hover:text-slate-400 disabled:hover:border-slate-200 transition-all shadow-sm">
      <ChevronLeftIcon class="w-4 h-4" />
    </button>

    <div class="hidden sm:flex gap-1">
      <button 
        v-for="pag in paginas" 
        :key="pag"
        @click="emit('cambiarPagina', pag)"
        :class="['w-9 h-9 flex items-center justify-center rounded-xl text-xs font-bold transition-all shadow-sm', 
          paginaActual === pag 
            ? 'bg-indigo-600 text-white border border-indigo-600' 
            : 'bg-white text-slate-500 border border-slate-200 hover:border-indigo-300 hover:text-indigo-600']">
        {{ pag }}
      </button>
    </div>

    <div class="sm:hidden px-4 py-2 bg-slate-50 rounded-xl border border-slate-200 text-xs font-bold text-slate-600">
      {{ paginaActual }} / {{ totalPaginas }}
    </div>

    <button 
      @click="irSiguiente" 
      :disabled="paginaActual === totalPaginas"
      class="p-2 rounded-xl bg-white border border-slate-200 text-slate-400 hover:text-indigo-600 hover:border-indigo-200 disabled:opacity-40 disabled:hover:text-slate-400 disabled:hover:border-slate-200 transition-all shadow-sm">
      <ChevronRightIcon class="w-4 h-4" />
    </button>
  </div>
</template>
