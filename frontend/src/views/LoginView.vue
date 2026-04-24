<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from '../composables/useToast'
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
  CircleStackIcon,
  CubeIcon,
  ChartBarIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const { toastShow, toastMessage, toastType } = useToast()

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
    setTimeout(() => { errorMsg.value = '' }, 3000)
    return
  }

  isLoading.value = true
  errorMsg.value = ''

  try {
    const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: form.username,
        password: form.password
      })
    })

    const data = await response.json()

    if (response.ok) {
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
      localStorage.setItem('username', form.username)

      try {
        const payloadBase64 = data.access.split('.')[1]
        const payload = JSON.parse(atob(payloadBase64)) 
        
        localStorage.setItem('is_staff', payload.is_staff ? 'true' : 'false')
        localStorage.setItem('is_superuser', payload.is_superuser ? 'true' : 'false')
      } catch (e) {
        console.warn("No se pudo decodificar el rol del token", e)
      }

      router.push('/inventario')
      
    } else {
      errorMsg.value = 'Acceso denegado. Usuario o contraseña incorrectos.'
      setTimeout(() => { errorMsg.value = '' }, 3000)
    }
  } catch (error) {
    console.error('Error de red:', error)
    errorMsg.value = 'Error de conexión. Verifica que el servidor esté activo.'
    setTimeout(() => { errorMsg.value = '' }, 3000)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen w-full flex bg-white font-sans text-slate-800 selection:bg-indigo-100 selection:text-indigo-800">
    
    <div class="hidden lg:flex lg:w-[45%] relative bg-slate-50 border-r border-slate-100 overflow-hidden flex-col justify-center items-center p-12">
      
      <div class="absolute inset-0 bg-[radial-gradient(#e2e8f0_1px,transparent_1px)] [background-size:24px_24px] opacity-50"></div>
      
      <div class="absolute top-0 right-0 -mt-20 -mr-20 w-96 h-96 bg-indigo-200/50 rounded-full blur-[100px]"></div>
      <div class="absolute bottom-0 left-0 -mb-20 -ml-20 w-96 h-96 bg-blue-200/40 rounded-full blur-[100px]"></div>

      <div class="relative z-10 w-full max-w-lg">
        
        <div class="mb-12">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-600 text-xs font-bold uppercase tracking-widest mb-6">
            <BoltIcon class="w-4 h-4" /> VoltStock OS
          </div>
          <h1 class="text-4xl xl:text-5xl font-black text-slate-900 tracking-tight leading-[1.1]">
            El estándar para el <br> <span class="text-indigo-600">control de hardware.</span>
          </h1>
          <p class="mt-6 text-slate-500 font-medium text-base max-w-md leading-relaxed">
            Plataforma centralizada para la gestión de inventario, trazabilidad de componentes y auditoría de laboratorios de ingeniería.
          </p>
        </div>

        <div class="relative w-full h-[280px]">
          
          <div class="absolute top-0 left-0 w-64 bg-white p-5 rounded-2xl shadow-xl shadow-slate-200/50 border border-slate-100 animate-float-slow z-20">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-3">
                <div class="p-2 bg-indigo-50 rounded-lg text-indigo-600"><CubeIcon class="w-5 h-5"/></div>
                <div class="text-sm font-bold text-slate-800">Stock Global</div>
              </div>
              <span class="text-xs font-bold text-emerald-500 bg-emerald-50 px-2 py-1 rounded-md">+12%</span>
            </div>
            <div class="text-3xl font-black text-slate-900 mb-2">2,450</div>
            <div class="w-full bg-slate-100 rounded-full h-1.5">
              <div class="bg-indigo-500 h-1.5 rounded-full" style="width: 75%"></div>
            </div>
          </div>

          <div class="absolute top-20 right-0 w-56 bg-white p-5 rounded-2xl shadow-xl shadow-slate-200/50 border border-slate-100 animate-float-delayed z-10">
            <div class="flex items-center gap-3 mb-3">
              <div class="p-2 bg-emerald-50 rounded-lg text-emerald-600"><ShieldCheckIcon class="w-5 h-5"/></div>
              <div class="text-sm font-bold text-slate-800">Seguridad</div>
            </div>
            <div class="space-y-2">
              <div class="flex items-center gap-2"><div class="w-1.5 h-1.5 bg-emerald-400 rounded-full"></div><span class="text-xs font-medium text-slate-500">Acceso encriptado</span></div>
              <div class="flex items-center gap-2"><div class="w-1.5 h-1.5 bg-emerald-400 rounded-full"></div><span class="text-xs font-medium text-slate-500">Auditoría activa</span></div>
            </div>
          </div>

          <div class="absolute bottom-0 left-16 w-72 bg-white/80 backdrop-blur-md p-5 rounded-2xl shadow-lg shadow-slate-200/40 border border-white z-30">
            <div class="flex items-end gap-2 h-12">
              <div class="w-1/6 bg-indigo-100 rounded-t-sm h-[40%]"></div>
              <div class="w-1/6 bg-indigo-200 rounded-t-sm h-[60%]"></div>
              <div class="w-1/6 bg-indigo-300 rounded-t-sm h-[30%]"></div>
              <div class="w-1/6 bg-indigo-400 rounded-t-sm h-[80%]"></div>
              <div class="w-1/6 bg-indigo-500 rounded-t-sm h-[100%]"></div>
              <div class="w-1/6 bg-indigo-600 rounded-t-sm h-[70%]"></div>
            </div>
          </div>

        </div>

      </div>
    </div>
    <div class="w-full lg:w-[55%] flex flex-col justify-center px-6 sm:px-20 md:px-32 bg-[#fafcfd] relative z-10">
      <div class="w-full max-w-[420px] mx-auto relative z-10 animate-entrance">
        
        <div class="lg:hidden mb-10 flex items-center gap-3">
          <div class="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-md shadow-indigo-200">
            <BoltIcon class="w-6 h-6 text-white" />
          </div>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">VoltStock</h1>
        </div>

        <div class="mb-10 text-center lg:text-left">
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
            <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-widest ml-1 transition-colors group-focus-within:text-indigo-600">
                Usuario
            </label>
            <div class="relative">
              <input 
                v-model="form.username" 
                type="text" 
                placeholder="admin_vstock"
                class="w-full pl-12 pr-4 py-3.5 bg-white border border-slate-200 rounded-xl text-slate-800 placeholder-slate-300 focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all duration-300 font-medium shadow-sm"
              />
              <UserIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 transition-colors group-focus-within:text-indigo-500" />
            </div>
          </div>

          <div class="space-y-2 group">
            <label class="block text-[11px] font-bold text-slate-500 uppercase tracking-widest ml-1 transition-colors group-focus-within:text-indigo-600">
                Contraseña
            </label>
            <div class="relative">
              <input 
                v-model="form.password" 
                :type="showPassword ? 'text' : 'password'" 
                placeholder="••••••••••••"
                class="w-full pl-12 pr-12 py-3.5 bg-white border border-slate-200 rounded-xl text-slate-800 placeholder-slate-300 focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all duration-300 font-medium shadow-sm"
              />
              <LockClosedIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 transition-colors group-focus-within:text-indigo-500" />
              
              <button 
                type="button" 
                @click="showPassword = !showPassword" 
                class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-indigo-600 transition-colors"
              >
                <EyeSlashIcon v-if="showPassword" class="w-5 h-5" />
                <EyeIcon v-else class="w-5 h-5" />
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
            type="submit" 
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

    <transition 
        enter-active-class="transform ease-out duration-300 transition"
        enter-from-class="-translate-y-4 opacity-0 sm:translate-x-4"
        enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0">
        <div v-if="toastShow" class="fixed top-6 right-6 z-[999] pointer-events-none w-full max-w-sm">
            <div class="pointer-events-auto bg-white shadow-2xl rounded-2xl p-4 border" :class="toastType === 'success' ? 'border-emerald-100' : 'border-red-100'">
                <div class="flex items-start gap-3">
                    <div class="shrink-0">
                        <CheckCircleIcon v-if="toastType === 'success'" class="w-6 h-6 text-emerald-500" />
                        <ExclamationCircleIcon v-else class="w-6 h-6 text-red-500" />
                    </div>
                    <div class="flex-1 pt-0.5">
                        <p class="text-sm font-bold text-slate-800">{{ toastType === 'success' ? 'Éxito' : 'Atención' }}</p>
                        <p class="mt-1 text-sm text-slate-500 leading-snug">{{ toastMessage }}</p>
                    </div>
                </div>
            </div>
        </div>
    </transition>

  </div>
</template>

<style scoped>
/* Animación de las tarjetas flotantes en el lado izquierdo */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}
.animate-float-slow {
  animation: float 6s ease-in-out infinite;
}
.animate-float-delayed {
  animation: float 5s ease-in-out infinite;
  animation-delay: 2s;
}

/* Animación de entrada general */
@keyframes entrance {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-entrance {
  animation: entrance 0.5s ease-out forwards;
}

/* Animación de error (Shake horizontal) que tenías original */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-4px); }
  40%, 80% { transform: translateX(4px); }
}
.animate-shake {
  animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
}

/* Fix para el fondo amarillo feo del autocompletado en navegadores web */
input:-webkit-autofill,
input:-webkit-autofill:hover, 
input:-webkit-autofill:focus, 
input:-webkit-autofill:active{
  -webkit-box-shadow: 0 0 0 30px white inset !important; 
  -webkit-text-fill-color: #1e293b !important;
  transition: background-color 5000s ease-in-out 0s;
}

::-webkit-scrollbar {
  width: 0px;
}
</style>