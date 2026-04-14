<script setup>
import { ref, onMounted } from 'vue'

// --- ESTADO Y DATOS ---
const componentes = ref([])
const cargando = ref(true)

// --- LÓGICA CON MYSQL ---
const obtenerComponentes = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/componentes/')
    componentes.value = await res.json()
  } catch (err) {
    console.error("Error al conectar con la API:", err)
  } finally {
    cargando.value = false
  }
}

// Emisores de eventos para avisarle a App.vue que queremos mover algo
const emit = defineEmits(['solicitar', 'devolver'])

onMounted(obtenerComponentes)
</script>

<template>
  <div class="space-y-6 animate-fade-in">
    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      
      <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center">
        <div>
          <h3 class="text-lg font-bold text-slate-800">Catálogo de Componentes</h3>
          <p class="text-xs text-slate-500 mt-1">Administra el stock disponible en la base de datos.</p>
        </div>
        <span class="bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider ring-1 ring-indigo-100">
          {{ componentes.length }} Artículos
        </span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead class="bg-slate-50/50 text-slate-500 text-[10px] uppercase tracking-widest font-semibold border-b border-slate-100">
            <tr>
              <th class="px-6 py-4">Componente</th>
              <th class="px-6 py-4 text-center">Stock Disponible</th>
              <th class="px-6 py-4 text-right">Acciones de Flujo</th>
            </tr>
          </thead>
          
          <tbody class="divide-y divide-slate-50">
            <tr v-if="cargando">
              <td colspan="3" class="px-6 py-12 text-center text-slate-400 font-medium">Cargando componentes desde MySQL...</td>
            </tr>
            <tr v-else-if="componentes.length === 0">
              <td colspan="3" class="px-6 py-12 text-center text-slate-400 font-medium">No hay componentes registrados en el sistema.</td>
            </tr>
            <tr v-for="item in componentes" :key="item.id" class="hover:bg-slate-50 transition-colors group">
              <td class="px-6 py-4">
                <p class="font-bold text-slate-800 group-hover:text-indigo-600 transition-colors">{{ item.nombre }}</p>
                <p class="text-xs text-slate-500 mt-0.5 line-clamp-1">{{ item.descripcion }}</p>
              </td>
              <td class="px-6 py-4 text-center">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-emerald-50 text-emerald-700 ring-1 ring-inset ring-emerald-600/20">
                  {{ item.stock }} UNIDADES
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex justify-end gap-2">
                  <button @click="emit('solicitar', item)" class="bg-white text-blue-600 hover:bg-blue-50 border border-blue-200 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all shadow-sm hover:shadow">
                    Solicitar
                  </button>
                  <button @click="emit('devolver', item)" class="bg-white text-amber-600 hover:bg-amber-50 border border-amber-200 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all shadow-sm hover:shadow">
                    Devolver
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>