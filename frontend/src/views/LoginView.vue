<script setup>
import { ref, reactive } from 'vue'
import { 
  UserIcon, 
  LockClosedIcon, 
  EyeIcon, 
  EyeSlashIcon,
  ExclamationCircleIcon,
  BoltIcon,
  ArrowRightIcon,
  CpuChipIcon,
  ShieldCheckIcon,
  CircleStackIcon
} from '@heroicons/vue/24/outline'

const form = reactive({
  username: '',
  password: '',
  remember: false
})

const showPassword = ref(false)
const isLoading = ref(false)
const errorMsg = ref('')

const handleLogin = async () => {
  if (!form.username || !form.password) {
    errorMsg.value = 'Se requieren credenciales para el acceso.'
    return
  }

  isLoading.value = true
  errorMsg.value = ''

  try {
    await new Promise(resolve => setTimeout(resolve, 1800))
    errorMsg.value = 'Acceso denegado. Usuario o contraseña incorrectos.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen w-full flex bg-white font-sans text-slate-600 selection:bg-indigo-100 selection:text-indigo-700 overflow-hidden">
    
    <div class="hidden lg:flex lg:w-[45%] relative items-center justify-center bg-white border-r border-slate-100">
      <div class="relative z-10 max-w-md px-12">
        <div class="mb-12 flex items-center gap-4">
          <div class="w-14 h-14 bg-indigo-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-200">
            <BoltIcon class="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 class="text-3xl font-black text-slate-900 tracking-tighter leading-none">
              VOLT<span class="text-indigo-600">STOCK</span>
            </h1>
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-[0.3em]">Hardware Management</span>
          </div>
        </div>

        <h2 class="text-5xl font-extrabold text-slate-900 leading-[1.1] mb-6 tracking-tight">
          Gestiona tu <br/>
          <span class="text-indigo-600">inventario pro.</span>
        </h2>
        
        <p class="text-slate-500 text-base mb-12 font-medium leading-relaxed">
          Control de alta precisión para laboratorios de ingeniería y entornos de producción de hardware.
        </p>

        <div class="bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-[0_20px_50px_rgba(0,0,0,0.03)] relative">
          <div class="absolute top-4 right-4 opacity-5">
            <CpuChipIcon class="w-20 h-20 text-indigo-900" />
          </div>

          <div class="mb-8">
            <span class="text-[10px] font-black text-indigo-600 uppercase tracking-widest block mb-2">Mainframe Status</span>
            <div class="flex items-center gap-2">
                <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                <span class="text-sm font-bold text-slate-800 tracking-tight">Node_01 Active</span>
            </div>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div class="p-4 bg-slate-50/50 rounded-2xl">
                <span class="text-[9px] font-bold text-slate-400 uppercase">Load Factor</span>
                <div class="text-xl font-black text-slate-800 mt-1">72.4%</div>
            </div>
            <div class="p-4 bg-slate-50/50 rounded-2xl">
                <span class="text-[9px] font-bold text-slate-400 uppercase">Temp Core</span>
                <div class="text-xl font-black text-emerald-600 mt-1">34°C</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="w-full lg:w-[55%] flex flex-col justify-center px-6 sm:px-20 md:px-32 bg-[#fafcfd] relative">
      
      <div class="absolute inset-0 pointer-events-none opacity-[0.03] flex items-center justify-center overflow-hidden">
        <CpuChipIcon class="w-[800px] h-[800px] text-slate-900 rotate-12 transform scale-150" />
      </div>

      <div class="w-full max-w-[420px] mx-auto relative z-10 animate-entrance">
        
        <div class="mb-10 text-center lg:text-center">
          <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-100/50 mb-5 text-indigo-600">
            <ShieldCheckIcon class="w-4 h-4" />
            <span class="text-[9px] font-bold uppercase tracking-widest">Acceso Restringido</span>
          </div>
          <h2 class="text-3xl font-black text-slate-900 mb-2 tracking-tight">Autenticación del Sistema</h2>
          <p class="text-slate-500 font-medium text-sm">Ingrese sus credenciales de seguridad para continuar.</p>
        </div>

        <transition name="shake">
          <div v-if="errorMsg" class="mb-6 p-4 rounded-xl bg-red-50 border border-red-100 flex items-center gap-3 text-red-600 text-sm font-semibold animate-shake">
            <ExclamationCircleIcon class="w-5 h-5 shrink-0 text-red-500" />
            {{ errorMsg }}
          </div>
        </transition>

        <form @submit.prevent="handleLogin" class="space-y-6">
          
          <div class="space-y-2 group">
            <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-widest ml-1 group-focus-within:text-indigo-600 transition-colors">
                Usuario
            </label>
            <div class="relative">
              <input v-model="form.username" type="text" placeholder="admin_vstock"
                class="w-full pl-12 pr-4 py-3.5 bg-white border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-300 font-medium text-slate-800 shadow-sm"
              />
              <UserIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors" />
            </div>
          </div>

          <div class="space-y-2 group">
            <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-widest ml-1 group-focus-within:text-indigo-600 transition-colors">
                Contraseña
            </label>
            <div class="relative">
              <input v-model="form.password" :type="showPassword ? 'text' : 'password'" placeholder="••••••••••••"
                class="w-full pl-12 pr-12 py-3.5 bg-white border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-300 font-medium text-slate-800 shadow-sm"
              />
              <LockClosedIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors" />
              <button type="button" @click="showPassword = !showPassword" class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-indigo-600 transition-colors">
                <EyeIcon v-if="!showPassword" class="w-5 h-5" />
                <EyeSlashIcon v-else class="w-5 h-5" />
              </button>
            </div>
          </div>

          <div class="flex items-center justify-between pt-2 pb-2">
            <div class="flex items-center gap-3 cursor-pointer" @click="form.remember = !form.remember">
              <div 
                class="w-10 h-6 flex items-center rounded-full p-1 transition-colors duration-300 ease-in-out"
                :class="form.remember ? 'bg-indigo-600' : 'bg-slate-200'"
              >
                <div 
                  class="bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300 ease-in-out"
                  :class="form.remember ? 'translate-x-4' : 'translate-x-0'"
                ></div>
              </div>
              <span class="text-xs font-bold text-slate-600 select-none">Mantener sesión activa</span>
            </div>
            
            <a href="#" class="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors">¿Olvidó su contraseña?</a>
          </div>

          <button 
            :disabled="isLoading" 
            class="group relative w-full py-4 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-700 hover:to-violet-700 text-white rounded-xl font-bold text-xs uppercase tracking-widest shadow-lg shadow-indigo-200 transition-all duration-300 active:scale-[0.98] disabled:opacity-70"
          >
            <div class="flex items-center justify-center gap-3">
              <template v-if="!isLoading">
                <span>Ejecutar Inicio de Sesión</span>
                <ArrowRightIcon class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </template>
              <template v-else>
                <div class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                <span>Enviando credenciales...</span>
              </template>
            </div>
          </button>
        </form>

        <div class="mt-12 text-center">
          <p class="text-xs font-medium text-slate-400">
            ¿Problemas de acceso? <a href="#" class="text-slate-600 font-bold hover:text-indigo-600 transition-colors">Contacta a soporte</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes entrance {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-entrance {
  animation: entrance 0.5s ease-out forwards;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-4px); }
  40%, 80% { transform: translateX(4px); }
}
.animate-shake {
  animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
}

input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0px 1000px white inset;
  -webkit-text-fill-color: #1e293b;
}

::-webkit-scrollbar {
  width: 0px;
}
</style>