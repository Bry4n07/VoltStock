<script setup>
import { ref, reactive, onMounted, computed, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  UserIcon, IdentificationIcon, LockClosedIcon, 
  EyeIcon, EyeSlashIcon, ShieldCheckIcon,
  UserPlusIcon, ChevronDownIcon, CheckBadgeIcon, ExclamationTriangleIcon, BriefcaseIcon, BookOpenIcon,
  UsersIcon, PencilSquareIcon, NoSymbolIcon, CheckCircleIcon, XMarkIcon
} from '@heroicons/vue/24/outline'
import { SparklesIcon } from '@heroicons/vue/24/solid'
import { useToast } from '../composables/useToast'
import { api } from '../services/api'
import Pagination from '../components/pagination.vue'

const router = useRouter()
const { showToast } = useToast()
const isLoading = ref(false)
const showPassword = ref(false)

const activeTab = ref('registro')

// Logica de Registro
const form = reactive({ nombre: '', username: '', rol: 'operador', password: '', confirmPassword: '' })

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) return showToast("Las contraseñas no coinciden.", "error")
  isLoading.value = true

  let is_staff_envio = form.rol === 'admin' || form.rol === 'operador'
  let is_superuser_envio = form.rol === 'admin'

  try {
    const response = await api('auth/register/', {
      method: 'POST',
      body: JSON.stringify({ username: form.username, password: form.password, first_name: form.nombre, is_staff: is_staff_envio, is_superuser: is_superuser_envio })
    });

    if (response.status === 201) { 
      showToast(`¡Usuario ${form.username} registrado!`, "success");
      form.nombre = ''; form.username = ''; form.password = ''; form.confirmPassword = ''; form.rol = 'operador';
      cargarUsuarios();
      activeTab.value = 'directorio';
    } else {
      const dataError = await response.json();
      showToast(`Error: ${dataError.username ? dataError.username[0] : 'Verifica los datos'}`, "error");
    }
  } catch (error) { showToast("Error de servidor.", "error"); } 
  finally { isLoading.value = false; }
}

// Logica de directorio y paginación
const usuarios = ref([])
const modalEdit = ref(false)
const usuarioAEditar = ref(null)
const editForm = reactive({ rol: '', password: '' })

// Paginación Reactiva
const paginaActual = ref(1)
const itemsPorPagina = 5

const totalPaginas = computed(() => Math.ceil(usuarios.value.length / itemsPorPagina))

const usuariosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * itemsPorPagina
  const fin = inicio + itemsPorPagina
  return usuarios.value.slice(inicio, fin)
})

const cambiarPagina = (nuevaPagina) => {
  paginaActual.value = nuevaPagina
}

onMounted(() => {
  const rolActual = localStorage.getItem('user_rol')
  if (rolActual !== 'admin') {
    showToast("Acceso denegado. Solo administradores.", "error")
    router.push('/dashboard')
  } else {
    cargarUsuarios()
  }
})

const cargarUsuarios = async () => {
  try {
    const res = await api('auth/users/')
    if (res.ok) usuarios.value = await res.json()
  } catch (error) { console.error("Error al cargar directorio") }
}

const getRolVisual = (user) => {
  if (user.is_superuser) return { nombre: 'Admin Global', color: 'bg-indigo-100 text-indigo-700 border-indigo-200' }
  if (user.is_staff) return { nombre: 'Operador', color: 'bg-emerald-100 text-emerald-700 border-emerald-200' }
  return { nombre: 'Auditor', color: 'bg-amber-100 text-amber-700 border-amber-200' }
}

const toggleEstado = async (user) => {
  try {
    const res = await api(`auth/users/${user.id}/`, {
      method: 'PUT',
      body: JSON.stringify({ is_active: !user.is_active })
    })
    if (res.ok) {
      user.is_active = !user.is_active
      showToast(user.is_active ? 'Usuario habilitado' : 'Usuario deshabilitado', 'success')
    } else { showToast("No se pudo cambiar el estado", "error") }
  } catch (error) { showToast("Error de conexión.", "error") }
}

// Logica de modal
const abrirModal = (user) => {
  usuarioAEditar.value = user
  editForm.rol = user.is_superuser ? 'admin' : (user.is_staff ? 'operador' : 'auditor')
  editForm.password = ''
  modalEdit.value = true
}

const guardarEdicion = async () => {
  try {
    const payload = { rol: editForm.rol }
    if (editForm.password.trim() !== '') payload.password = editForm.password

    const res = await api(`auth/users/${usuarioAEditar.value.id}/`, {
      method: 'PUT',
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      showToast("Actualización exitosa", "success")
      modalEdit.value = false
      cargarUsuarios()
    } else { showToast("Error al actualizar.", "error") }
  } catch (error) { showToast("Error de conexión.", "error") }
}

const handleKeydown = (e) => {
  if (e.key === 'Escape' && modalEdit.value) {
    const elementoActivo = document.activeElement
    if (elementoActivo.tagName === 'INPUT' || elementoActivo.tagName === 'SELECT') {
      elementoActivo.blur()
    } else {
      modalEdit.value = false
    }
  }
}

watch(modalEdit, (isOpen) => {
  if (isOpen) window.addEventListener('keydown', handleKeydown)
  else window.removeEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="w-full animate-fade-in pb-10">
    
    <div class="mb-8 flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div class="flex items-center gap-4">
        <div class="p-3 bg-indigo-600 rounded-2xl shadow-lg shadow-indigo-200 text-white">
          <UserPlusIcon v-if="activeTab === 'registro'" class="w-7 h-7" />
          <UsersIcon v-else class="w-7 h-7" />
        </div>
        <div>
          <h2 class="text-3xl font-black text-slate-800 tracking-tight">Gestión de Personal</h2>
          <p class="text-slate-500 font-medium mt-0.5">Control de accesos al sistema VoltStock</p>
        </div>
      </div>
      <div class="flex bg-slate-200/50 p-1 rounded-xl w-full sm:w-auto">
        <button @click="activeTab = 'registro'" :class="['flex-1 sm:px-6 py-2.5 rounded-lg text-sm font-bold transition-all', activeTab === 'registro' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700']">
          Nuevo Ingreso
        </button>
        <button @click="activeTab = 'directorio'" :class="['flex-1 sm:px-6 py-2.5 rounded-lg text-sm font-bold transition-all', activeTab === 'directorio' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700']">
          Directorio
        </button>
      </div>
    </div>

    <div v-if="activeTab === 'registro'" class="bg-white rounded-[2.5rem] shadow-sm border border-slate-200 overflow-hidden flex flex-col lg:flex-row min-h-[650px] animate-fade-in">
      <div class="lg:w-[38%] bg-slate-50/50 p-10 lg:p-14 border-b lg:border-b-0 lg:border-r border-slate-200 flex flex-col relative overflow-hidden">
        <div class="absolute -right-20 -bottom-20 w-64 h-64 bg-indigo-50 rounded-full blur-3xl opacity-60 pointer-events-none"></div>
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white border border-slate-200 text-indigo-600 text-[11px] font-bold tracking-widest uppercase mb-10 shadow-sm w-fit relative z-10">
          <SparklesIcon class="w-4 h-4" /> Nivel de Acceso
        </div>
        <div class="flex-1 relative z-10">
          <h3 class="text-2xl font-extrabold text-slate-800 mb-4 tracking-tight">Privilegios Asignados</h3>
          <p class="text-sm text-slate-500 leading-relaxed mb-8">Revisa las capacidades del rol que estás a punto de crear.</p>
          <transition name="fade-slide" mode="out-in">
            <div v-if="form.rol === 'operador'" key="op" class="p-6 bg-white rounded-3xl border border-slate-100 shadow-lg shadow-slate-200/40 relative">
              <div class="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-600 flex items-center justify-center mb-5"><BriefcaseIcon class="w-6 h-6" /></div>
              <h4 class="text-lg font-black text-slate-800 mb-2">Operador de Inventario</h4>
              <p class="text-sm text-slate-600 leading-relaxed mb-4">El perfil estándar para el trabajo diario. Permite gestionar las salidas y entradas de material.</p>
            </div>
            <div v-else-if="form.rol === 'auditor'" key="au" class="p-6 bg-white rounded-3xl border border-slate-100 shadow-lg shadow-slate-200/40 relative">
              <div class="w-12 h-12 rounded-2xl bg-amber-100 text-amber-600 flex items-center justify-center mb-5"><BookOpenIcon class="w-6 h-6" /></div>
              <h4 class="text-lg font-black text-slate-800 mb-2">Auditor (Lectura)</h4>
              <p class="text-sm text-slate-600 leading-relaxed mb-4">Perfil restringido, ideal para profesores o supervisores. Solo lectura de inventario y reportes.</p>
            </div>
            <div v-else-if="form.rol === 'admin'" key="ad" class="p-6 bg-indigo-600 rounded-3xl border border-indigo-500 shadow-xl shadow-indigo-200 text-white relative">
              <div class="w-12 h-12 rounded-2xl bg-indigo-500/50 flex items-center justify-center mb-5"><ShieldCheckIcon class="w-6 h-6" /></div>
              <h4 class="text-lg font-black mb-2">Administrador</h4>
              <p class="text-sm text-indigo-100 leading-relaxed mb-4">Control total sobre el sistema VoltStock. Otorgar con extrema precaución.</p>
            </div>
          </transition>
        </div>
      </div>
      <div class="lg:w-[62%] p-10 lg:p-16 flex flex-col justify-center">
        <form @submit.prevent="handleRegister" class="max-w-2xl mx-auto w-full space-y-8">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-8">
            <div class="space-y-2 group">
              <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-[0.15em] ml-1">Nombre Completo</label>
              <div class="relative">
                <input v-model="form.nombre" type="text" required placeholder="Ej. Juan Carlos" class="w-full pl-12 pr-4 py-4 bg-slate-50 border-none rounded-2xl focus:bg-white focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all text-sm font-semibold text-slate-800 shadow-inner" />
                <UserIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-indigo-500 transition-colors" />
              </div>
            </div>
            <div class="space-y-2 group">
              <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-[0.15em] ml-1">Seleccionar Rol</label>
              <div class="relative">
                <select v-model="form.rol" class="w-full pl-12 pr-10 py-4 bg-slate-50 border-none rounded-2xl focus:bg-white focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all text-sm font-bold text-slate-700 appearance-none cursor-pointer shadow-inner">
                  <option value="operador">Operador de Inventario</option>
                  <option value="auditor">Auditor (Lectura)</option>
                  <option value="admin">Administrador</option>
                </select>
                <ShieldCheckIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-indigo-500 transition-colors" />
                <ChevronDownIcon class="w-4 h-4 absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
              </div>
            </div>
            <div class="space-y-2 group">
              <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-[0.15em] ml-1">ID de Usuario</label>
              <div class="relative">
                <input v-model="form.username" type="text" required placeholder="usuario_lab" class="w-full pl-12 pr-4 py-4 bg-slate-50 border-none rounded-2xl focus:bg-white focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all text-sm font-semibold text-slate-800 shadow-inner" />
                <IdentificationIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-indigo-500 transition-colors" />
              </div>
            </div>
          </div>
          <div class="h-px bg-slate-100 w-full"></div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-8">
            <div class="space-y-2 group">
              <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-[0.15em] ml-1">Contraseña Inicial</label>
              <div class="relative">
                <input v-model="form.password" :type="showPassword ? 'text' : 'password'" required placeholder="••••••••" class="w-full pl-12 pr-4 py-4 bg-slate-50 border-none rounded-2xl focus:bg-white focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all text-sm font-semibold text-slate-800 shadow-inner" />
                <LockClosedIcon class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-indigo-500 transition-colors" />
              </div>
            </div>
            <div class="space-y-2 group">
              <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-[0.15em] ml-1">Confirmar Contraseña</label>
              <div class="relative">
                <input v-model="form.confirmPassword" :type="showPassword ? 'text' : 'password'" required placeholder="••••••••" class="w-full pl-12 pr-4 py-4 bg-slate-50 border-none rounded-2xl focus:bg-white focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all text-sm font-semibold text-slate-800 shadow-inner" />
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
            <button type="button" @click="router.push('/dashboard')" class="w-full sm:w-auto px-8 py-4 rounded-2xl text-sm font-bold text-slate-500 hover:bg-slate-100 transition-all">
              Cancelar
            </button>
            <button type="submit" :disabled="isLoading" class="w-full sm:w-auto px-12 py-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl text-sm font-bold shadow-xl shadow-indigo-200 transition-all active:scale-[0.98] flex items-center justify-center gap-3 disabled:opacity-70">
              <span v-if="!isLoading">Crear Usuario</span>
              <svg v-else class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="activeTab === 'directorio'" class="bg-white rounded-[2rem] shadow-sm border border-slate-200 overflow-hidden animate-fade-in flex flex-col min-h-[500px]">
      
      <div class="hidden md:block overflow-x-auto rounded-t-3xl flex-1">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50/80 border-b border-slate-100">
              <th class="px-8 py-6 text-[10px] font-black text-slate-400 uppercase tracking-widest">Identidad</th>
              <th class="px-6 py-6 text-[10px] font-black text-slate-400 uppercase tracking-widest">Rol Asignado</th>
              <th class="px-6 py-6 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Acceso</th>
              <th class="px-8 py-6 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Opciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="user in usuariosPaginados" :key="user.id" class="hover:bg-slate-50/50 transition-colors group">
              <td class="px-8 py-5">
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 rounded-2xl bg-indigo-50 flex items-center justify-center font-black text-indigo-600 shadow-sm border border-indigo-100/50">
                    {{ user.username.charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <div class="font-extrabold text-slate-800 text-sm">{{ user.first_name || 'Sin Nombre' }}</div>
                    <div class="text-xs text-slate-400 font-bold mt-0.5">@{{ user.username }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-5">
                <span :class="['px-3 py-1.5 text-[10px] font-black uppercase tracking-widest rounded-lg border', getRolVisual(user).color]">
                  {{ getRolVisual(user).nombre }}
                </span>
              </td>
              <td class="px-6 py-5 text-center">
                <div class="flex flex-col items-center gap-1.5">
                  <button @click="toggleEstado(user)" :class="['relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none shadow-inner border border-black/5', user.is_active ? 'bg-emerald-500' : 'bg-slate-200']">
                    <span :class="['inline-block h-4 w-4 transform rounded-full bg-white transition-transform shadow-sm', user.is_active ? 'translate-x-6' : 'translate-x-1']"></span>
                  </button>
                  <span class="text-[9px] font-black uppercase tracking-wider" :class="user.is_active ? 'text-emerald-600' : 'text-slate-400'">
                    {{ user.is_active ? 'Activo' : 'Suspendido' }}
                  </span>
                </div>
              </td>
              <td class="px-8 py-5 text-right">
                <button @click="abrirModal(user)" class="p-2.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-xl transition-all inline-flex items-center gap-2">
                  <PencilSquareIcon class="w-5 h-5" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="md:hidden flex-1 p-4 space-y-4 bg-slate-50/50">
        <div v-for="user in usuariosPaginados" :key="user.id + '-mobile'" class="bg-white border border-slate-200 p-5 rounded-2xl shadow-sm flex flex-col gap-4">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-full bg-indigo-50 flex items-center justify-center font-black text-indigo-600 border border-indigo-100">
              {{ user.username.charAt(0).toUpperCase() }}
            </div>
            <div class="flex-1">
              <div class="font-extrabold text-slate-800 text-sm">{{ user.first_name || 'Sin Nombre' }}</div>
              <div class="text-xs text-slate-400 font-bold">@{{ user.username }}</div>
            </div>
            <button @click="abrirModal(user)" class="p-2 bg-slate-50 text-slate-500 rounded-xl border border-slate-100">
              <PencilSquareIcon class="w-5 h-5" />
            </button>
          </div>
          <div class="flex items-center justify-between pt-3 border-t border-slate-50">
            <span :class="['px-3 py-1.5 text-[10px] font-black uppercase tracking-widest rounded-lg border', getRolVisual(user).color]">
              {{ getRolVisual(user).nombre }}
            </span>
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-black uppercase tracking-wider text-slate-500">Acceso:</span>
              <button @click="toggleEstado(user)" :class="['relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none shadow-inner border border-black/5', user.is_active ? 'bg-emerald-500' : 'bg-slate-200']">
                <span :class="['inline-block h-4 w-4 transform rounded-full bg-white transition-transform shadow-sm', user.is_active ? 'translate-x-6' : 'translate-x-1']"></span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="usuarios.length > 0" class="p-6 border-t border-slate-100 bg-white mt-auto flex justify-center">
        <Pagination x
          :pagina-actual="paginaActual" 
          :total-paginas="totalPaginas" 
          @cambiar-pagina="cambiarPagina" 
        />
      </div>

      <div v-if="usuarios.length === 0" class="py-20 flex flex-col items-center justify-center text-center">
        <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4">
          <UsersIcon class="w-8 h-8 text-slate-300" />
        </div>
        <p class="text-sm font-bold text-slate-500">Cargando directorio o no hay usuarios registrados.</p>
      </div>
    </div>

    <Teleport to="body">
      <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition ease-in duration-150" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
        <div v-if="modalEdit" class="fixed inset-0 z-[999999] flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
          <form @submit.prevent="guardarEdicion" class="bg-white rounded-[2rem] shadow-2xl w-full max-w-sm overflow-hidden border border-slate-100">
            
            <div class="px-8 py-6 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
              <div>
                <h3 class="font-black text-slate-800 text-lg">Editar Usuario</h3>
                <p class="text-xs text-slate-500 font-medium">@{{ usuarioAEditar?.username }}</p>
              </div>
              <button type="button" @click="modalEdit = false" class="text-slate-400 hover:text-slate-600 bg-white p-2 rounded-full shadow-sm">
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>
            
            <div class="p-8 space-y-6">
              <div class="space-y-2">
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Modificar Rol</label>
                <select v-model="editForm.rol" class="w-full p-3.5 bg-slate-50 rounded-2xl outline-none text-sm font-bold border border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all">
                  <option value="operador">Operador de Inventario</option>
                  <option value="auditor">Auditor (Lectura)</option>
                  <option value="admin">Administrador Global</option>
                </select>
              </div>

              <div class="space-y-2">
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Forzar Nueva Contraseña</label>
                <input v-model="editForm.password" type="text" placeholder="Dejar vacío para no cambiar" class="w-full p-3.5 bg-slate-50 rounded-2xl outline-none text-sm font-medium border border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all" />
              </div>

              <button type="submit" class="w-full py-4 mt-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl text-sm font-bold shadow-xl shadow-indigo-200 transition-all flex items-center justify-center gap-2 active:scale-95">
                <CheckCircleIcon class="w-5 h-5" /> Aplicar Cambios
              </button>
            </div>

          </form>
        </div>
      </transition>
    </Teleport>

  </div>
</template>

<style scoped>
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.fade-slide-enter-from { opacity: 0; transform: translateY(10px) scale(0.98); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-10px) scale(0.98); }
select { background-image: none; }
input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0px 1000px #f8fafc inset !important;
  -webkit-text-fill-color: #1e293b !important;
}
</style>