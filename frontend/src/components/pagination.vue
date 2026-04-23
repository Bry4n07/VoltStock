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

// LÓGICA CORREGIDA: Empezamos a contar desde la página 1
const paginas = computed(() => {
  let pags = []
  for (let i = 1; i <= props.totalPaginas; i++) {
    pags.push(i)
  }
  return pags
})

// FUNCIÓN FALTANTE AGREGADA
const irAnterior = () => {
  if (props.paginaActual > 1) emit('cambiarPagina', props.paginaActual - 1)
}

const irSiguiente = () => {
  if (props.paginaActual < props.totalPaginas) emit('cambiarPagina', props.paginaActual + 1)
}
</script>

<template>
  <div class="flex items-center gap-1.5 sm:gap-2" v-if="totalPaginas > 1">

    <button @click="irAnterior" :disabled="paginaActual === 1"
      class="p-2 sm:p-2.5 rounded-xl bg-white border border-slate-200 text-slate-500 hover:text-indigo-600 hover:border-indigo-300 hover:bg-indigo-50 hover:shadow-sm disabled:opacity-40 disabled:bg-slate-50 disabled:hover:text-slate-500 disabled:hover:border-slate-200 disabled:shadow-none transition-all outline-none focus:ring-2 focus:ring-indigo-100 active:scale-95">
      <ChevronLeftIcon class="w-4 h-4 sm:w-5 sm:h-5" />
    </button>

    <div class="hidden sm:flex items-center gap-1.5">
      <button v-for="pag in paginas" :key="pag" @click="emit('cambiarPagina', pag)"
        :class="['min-w-[36px] h-9 sm:min-w-[40px] sm:h-10 flex items-center justify-center rounded-xl text-xs sm:text-sm font-bold transition-all outline-none focus:ring-2 focus:ring-indigo-100 active:scale-95',
          paginaActual === pag
            ? 'bg-indigo-600 text-white border border-indigo-600 shadow-md shadow-indigo-600/20'
            : 'bg-white text-slate-600 border border-slate-200 hover:border-indigo-300 hover:text-indigo-600 hover:bg-indigo-50 hover:shadow-sm']">
        {{ pag }}
      </button>
    </div>

    <div
      class="sm:hidden flex items-center justify-center min-w-[80px] h-9 bg-slate-50 rounded-xl border border-slate-200 text-xs font-black text-slate-600 tracking-wider">
      {{ paginaActual }} <span class="text-slate-400 mx-1 font-medium">/</span> {{ totalPaginas }}
    </div>

    <button @click="irSiguiente" :disabled="paginaActual === totalPaginas"
      class="p-2 sm:p-2.5 rounded-xl bg-white border border-slate-200 text-slate-500 hover:text-indigo-600 hover:border-indigo-300 hover:bg-indigo-50 hover:shadow-sm disabled:opacity-40 disabled:bg-slate-50 disabled:hover:text-slate-500 disabled:hover:border-slate-200 disabled:shadow-none transition-all outline-none focus:ring-2 focus:ring-indigo-100 active:scale-95">
      <ChevronRightIcon class="w-4 h-4 sm:w-5 sm:h-5" />
    </button>

  </div>
</template>