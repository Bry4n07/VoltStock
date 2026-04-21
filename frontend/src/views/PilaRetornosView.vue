<script setup>
import { defineProps, defineEmits } from 'vue';
import { ArrowPathIcon, ArchiveBoxIcon } from '@heroicons/vue/24/outline'

defineProps({
    devoluciones: {
        type: Array,
        required: true
    }
})

const emit = defineEmits(['reingresar'])

</script>
<template>
    <div class="space-y-6">
        <div class="flex justify-between items-end">
            <div>
                <h3 class="text-2xl font-bold text-slate-800">Pila de Retorno</h3>
                <p class="text-sm text-slate-500 mt-1">Estructura LIFO (Last In, First Out). El último que entra es el
                    primero que sale.</p>
            </div>
            <button @click="emit('reingresar')" :disabled="devoluciones.length === 0"
                class="px-6 py-2.5 bg-amber-600 text-white rounded-xl font-bold text-sm hover:bg-amber-700 transition-all flex items-center gap-2 shadow-sm disabled:opacity-50 disabled:cursor-not-allowed">
                <ArrowPathIcon class="w-5 h-5" />
                Reingresar Siguiente
            </button>
        </div>

        <div
            class="bg-white border border-slate-200 rounded-2xl shadow-sm p-8 min-h-[300px] flex flex-col items-center justify-center">
            <div v-if="devoluciones.length === 0" class="text-center text-slate-400">
                <ArchiveBoxIcon class="w-12 h-12 mx-auto mb-3 opacity-20" />
                <p>No hay componentes pendientes de reingreso.</p>
            </div>

            <div v-else class="w-full space-y-3">
                <div v-for="(item, index) in [...devoluciones].reverse()" :key="item.id_temporal"
                    class="p-4 border border-slate-100 rounded-lg bg-slate-50 flex justify-between items-center">
                    <div>
                        <p class="font-bold text-slate-700">{{ item.componente.nombre }}</p>
                        <p class="text-xs text-slate-500">Devuelto a las: {{ item.fecha }}</p>
                    </div>
                    <span v-if="index === 0"
                        class="text-[10px] bg-amber-100 text-amber-700 px-2 py-1 rounded-full font-bold uppercase">Cima
                        de la pila</span>
                </div>
            </div>
        </div>
    </div>
</template>
<style></style>