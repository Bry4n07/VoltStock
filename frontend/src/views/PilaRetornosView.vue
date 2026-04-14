<script setup>
import { defineProps, defineEmits } from 'vue';
import {ArrowPathIcon, ArchiveBoxIcon} from '@heroicons/vue/24/outline'

const props = defineProps({
    devoluciones: {
        type: Array,
        required: true
    }
})

const emit = defineEmits(['reingresar'])

</script>
<template>
    <div class="space-y-6 animate-fade-in"> 
        <div class="flex justify-between items-end">
            <div>
                <h3 class="text-2xl font-bold text-slate-800"> Pila de Retorno </h3>
                <p class="text-sm text-slate-500 mt-1"> Estructura LIFO (last In, Fisrt Out) </p>
            </div>
            <button @click="emit('reingresar')" :disabled="devoluciones.length === 0" _class="['px-6 py-2.5 rounded-xl font-bold text-sm transition-all flex items-center gap-2 shadow-sm']"> </button>
        </div>
    </div>
</template>
<style>
</style>