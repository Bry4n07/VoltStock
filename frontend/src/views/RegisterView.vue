<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { 
  UserIcon, 
  IdentificationIcon, 
  LockClosedIcon, 
  EyeIcon, 
  EyeSlashIcon,
  ShieldCheckIcon,
  UserPlusIcon,
  ChevronDownIcon
} from '@heroicons/vue/24/outline'
import { SparklesIcon } from '@heroicons/vue/24/solid'

const router = useRouter()
const isLoading = ref(false)
const showPassword = ref(false)

const form = reactive({
  nombre: '',
  username: '',
  rol: 'operador',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) {
    alert("Las contraseñas no coinciden.")
    return
  }
  isLoading.value = true
  setTimeout(() => {
    isLoading.value = false
    alert(`Usuario ${form.username} creado exitosamente`)
    router.push('/inventario')
  }, 1500)
}
</script>

<template>
  <div class="w-full animate-fade-in pb-10">
    
    <div class="mb-8">
      <div class="flex items-center gap-4">
        <div class="p-3 bg-indigo-600 rounded-2xl shadow-lg shadow-indigo-200 text-white">
          <UserPlusIcon class="w-7 h-7" />
        </div>
        <div>
          <h2 class="text-3xl font-black text-slate-800 tracking-tight">Alta de Personal</h2>
          <p class="text-slate-500 font-medium mt-0.5">Configuración de nuevos accesos al sistema VoltStock</p>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200 overflow-hidden flex flex-col lg:flex-row min-h-[650px]">
      
      <div class="lg:w-[38%] bg-slate-50/50 p-10 lg:p-14 border-b lg:border-b-0 lg:border-r border-slate-200 flex flex-col">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white border border-slate-200 text-indigo-600 text-[11px] font-bold tracking-widest uppercase mb-10 shadow-sm w-fit">
          <SparklesIcon class="w-4 h-4" />
          Seguridad de Nivel
        </div>
        
        <div class="flex-1">
          <h3 class="text-2xl font-extrabold text-slate-800 mb-4 italic">Privilegios del Rol</h3>
          <p class="text-slate-600 leading-relaxed mb-10">
            Cada rol otorga una capa de responsabilidad distinta dentro de la gestión electrónica de VoltStock. Asegúrese de asignar el perfil correcto.
          </p>
          
          <div class="space-y-6">
            <transition name="list" mode="out-in">
              <div :key="form.rol" class="space-y-4">
                <div v-if="form.rol === 'operador'" class="group p-6 bg-white rounded-3xl border border-slate-100 shadow-md shadow-slate-200/50">
                  <div class="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <CheckBadgeIcon class="w-6 h-6" v-if="false" /> <span class="font-bold text-lg">OP</span>
                  </div>
                  <span class="block text-xs font-black text-indigo-600 uppercase tracking-tighter mb-2">Acceso Estándar</span>
                  <p class="text-sm text-slate-500 leading-snug">Habilitado para lectura de inventario, despacho de ítems y recepción de devoluciones.</p>
                </div>

                <div v-if="form.rol === 'supervisor'" class="group p-6 bg-white rounded-3xl border border-slate-100 shadow-md shadow-slate-200/50">
                  <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <span class="font-bold text-lg">SV</span>
                  </div>
                  <span class="block text-xs font-black text-amber-600 uppercase tracking-tighter mb-2">Control de Turno</span>
                  <p class="text-sm text-slate-500 leading-snug">Incluye funciones de operador más auditoría de stock crítico y validación de reportes.</p>
                </div>

                <div v-if="form.rol === 'admin'" class="group p-6 bg-white rounded-3xl border border-slate-100 shadow-md shadow-slate-200/50">
                  <div class="w-10 h-10 rounded-xl bg-rose-100 text-rose-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <span class="font-bold text-lg">AD</span>
                  </div>
                  <span class="block text-xs font-black text-rose-600 uppercase tracking-tighter mb-2">Administración Total</span>
                  <p class="text-sm text-slate-500 leading-snug">Acceso irrestricto a la configuración de hardware, base de datos y gestión de personal.</p>
                </div>
              </div>
            </transition>
          </div>
        </div>

        <div class="mt-auto pt-10 text-[11px] text-slate-400 font-medium">
          Sistema de Registro Certificado VoltStock v2.0
        </div>
      </div>

      <div class="lg:w-[62%] p-10 lg:p-16 flex flex-col justify-center">
        <form @submit.prevent="handleRegister" class="max-w-2xl mx-auto w-full space-y-8">
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-8">
            <div class="space-y-2 group">
              <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-[0.15em] ml-1">Nombre Completo</label>
              <div class="relative">
                <input v-model="form.nombre" type="text" required placeholder="Ej. Carlos Mendoza" 
                  class="w-full pl-12 pr-4 py-4 bg-slate-50 border-none rounded-2xl focus:bg-white focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all text-sm font-semibold text-slate-800 shadow-inner" />
                <UserIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-indigo-500 transition-colors" />
              </div>
            </div>

            <div class="space-y-2 group">
              <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-[0.15em] ml-1">Asignar Rol</label>
              <div class="relative">
                <select v-model="form.rol" 
                  class="w-full pl-12 pr-10 py-4 bg-slate-50 border-none rounded-2xl focus:bg-white focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all text-sm font-bold text-slate-700 appearance-none cursor-pointer shadow-inner">
                  <option value="operador">Operador de Inventario</option>
                  <option value="supervisor">Supervisor de Turno</option>
                  <option value="admin">Administrador General</option>
                </select>
                <ShieldCheckIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-indigo-500 transition-colors" />
                <ChevronDownIcon class="w-4 h-4 absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
              </div>
            </div>

            <div class="space-y-2 group">
              <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-[0.15em] ml-1">ID de Usuario</label>
              <div class="relative">
                <input v-model="form.username" type="text" required placeholder="usuario_lab" 
                  class="w-full pl-12 pr-4 py-4 bg-slate-50 border-none rounded-2xl focus:bg-white focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all text-sm font-semibold text-slate-800 shadow-inner" />
                <IdentificationIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-indigo-500 transition-colors" />
              </div>
            </div>

            <div class="flex items-center text-[12px] text-slate-400 px-2 leading-tight">
              Este ID será el identificador único para el acceso a terminales.
            </div>
          </div>

          <div class="h-px bg-slate-100 w-full"></div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-8">
            <div class="space-y-2 group">
              <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-[0.15em] ml-1">Contraseña</label>
              <div class="relative">
                <input v-model="form.password" :type="showPassword ? 'text' : 'password'" required placeholder="••••••••" 
                  class="w-full pl-12 pr-4 py-4 bg-slate-50 border-none rounded-2xl focus:bg-white focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all text-sm font-semibold text-slate-800 shadow-inner" />
                <LockClosedIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-indigo-500 transition-colors" />
              </div>
            </div>

            <div class="space-y-2 group">
              <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-[0.15em] ml-1">Confirmar</label>
              <div class="relative">
                <input v-model="form.confirmPassword" :type="showPassword ? 'text' : 'password'" required placeholder="••••••••" 
                  class="w-full pl-12 pr-4 py-4 bg-slate-50 border-none rounded-2xl focus:bg-white focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all text-sm font-semibold text-slate-800 shadow-inner" />
                <ShieldCheckIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-indigo-500 transition-colors" />
              </div>
            </div>
          </div>

          <div class="flex items-center justify-between px-2 pt-2">
            <button type="button" @click="showPassword = !showPassword" class="text-xs font-extrabold text-indigo-600 hover:text-indigo-700 transition-colors uppercase tracking-widest flex items-center gap-2">
              <component :is="showPassword ? EyeSlashIcon : EyeIcon" class="w-4 h-4" />
              {{ showPassword ? 'Ocultar Claves' : 'Ver Claves' }}
            </button>
          </div>

          <div class="pt-10 flex flex-col sm:flex-row items-center justify-end gap-4">
            <button type="button" @click="router.push('/inventario')"
              class="w-full sm:w-auto px-8 py-4 rounded-2xl text-sm font-bold text-slate-500 hover:bg-slate-100 transition-all">
              Volver al Inventario
            </button>
            <button type="submit" :disabled="isLoading"
              class="w-full sm:w-auto px-12 py-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl text-sm font-bold shadow-xl shadow-indigo-200 transition-all active:scale-[0.98] flex items-center justify-center gap-3 disabled:opacity-70">
              <span v-if="!isLoading">Crear Usuario Nuevo</span>
              <svg v-else class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            </button>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Transición suave para el cambio de rol */
.list-enter-active, .list-leave-active {
  transition: all 0.3s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateX(-10px);
}
.list-leave-to {
  opacity: 0;
  transform: translateX(10px);
}

select {
  background-image: none;
}

input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0px 1000px #f8fafc inset !important;
  -webkit-text-fill-color: #1e293b !important;
}
</style>