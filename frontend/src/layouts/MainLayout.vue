<script setup>
import { ref, onMounted, onUnmounted, reactive, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { api } from '../services/api'
import {
    Bars3Icon, CubeIcon, InboxArrowDownIcon,
    Cog6ToothIcon, ArrowRightOnRectangleIcon, BoltIcon,
    ArrowUturnUpIcon, UserPlusIcon, XMarkIcon, BellIcon, ShieldCheckIcon,
    LockClosedIcon, EyeIcon, EyeSlashIcon,
    CheckCircleIcon, ExclamationCircleIcon, ChartBarIcon, DocumentChartBarIcon, HomeIcon, ArchiveBoxIcon, QueueListIcon,
    Square3Stack3DIcon
} from '@heroicons/vue/24/outline'

import { useToast } from '../composables/useToast'

const router = useRouter()
const route = useRoute()
const { toastShow, toastMessage, toastType, showToast } = useToast()

defineProps({ titulo: String })
const sidebarColapsado = ref(localStorage.getItem('sidebar_estado') === 'true')
const sidebarMobileAbierto = ref(false)
const menuUsuarioAbierto = ref(false)
const modalAjustesAbierto = ref(false)
const showPassword = ref(false)
const pwdForm = reactive({ actual: '', nueva: '', confirmar: '' })

// Estado de Sesión y Roles
const isAuthenticated = ref(false)
const username = ref('Cargando...')
const rolUsuario = ref('auditor')
// Formateador visual del rol para el perfil
const nombreRolVisual = computed(() => {
    if (rolUsuario.value === 'admin') return 'Administrador'
    if (rolUsuario.value === 'tecnico') return 'Técnico de Laboratorio'
    return 'Auditor (Lectura)'
})

watch(() => route.path, () => { sidebarMobileAbierto.value = false })

const handleKeydown = (e) => {
    if (e.key === 'Escape' && modalAjustesAbierto.value) {
        cerrarModal()
    }
}

//Sidebar
watch(sidebarColapsado, (nuevoEstado) => {
    localStorage.setItem('sidebar_estado', nuevoEstado)
})

const cargarPerfilUsuario = async () => {
    try {
        const res = await api('auth/me/')
        if (res.ok) {
            const data = await res.json()
            username.value = data.first_name || data.username || 'Usuario'
            rolUsuario.value = data.rol || 'auditor'

            localStorage.setItem('user_rol', rolUsuario.value)
            localStorage.setItem('user_name', username.value)
        }
    } catch (error) {
        console.error("Error al sincronizar el perfil.")
    }
}

onMounted(() => {
    window.addEventListener('keydown', handleKeydown)
    const token = localStorage.getItem('access')
    if (token) {
        isAuthenticated.value = true
        username.value = localStorage.getItem('user_name') || 'Usuario'
        rolUsuario.value = localStorage.getItem('user_rol') || 'auditor'
        cargarPerfilUsuario() 
    } else {
        router.push('/login')
    }
})

onUnmounted(() => { window.removeEventListener('keydown', handleKeydown) })

const cerrarSesion = (mensajeAdicional = null) => {
    localStorage.clear()
    isAuthenticated.value = false
    modalAjustesAbierto.value = false
    if (mensajeAdicional) showToast(mensajeAdicional, 'error')
    router.push('/login')
}

const abrirAjustes = () => {
    menuUsuarioAbierto.value = false
    modalAjustesAbierto.value = true
}

const cerrarModal = () => {
    modalAjustesAbierto.value = false
    pwdForm.actual = ''
    pwdForm.nueva = ''
    pwdForm.confirmar = ''
    showPassword.value = false
}

const cambiarPassword = async () => {
    if (pwdForm.nueva !== pwdForm.confirmar) {
        showToast("Las contraseñas nuevas no coinciden.", "error")
        return
    }

    const token = localStorage.getItem('access');
    if (!token) return cerrarSesion("Sesión caducada.");

    try {
        const response = await fetch('http://127.0.0.1:8000/api/auth/change-password/', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({ old_password: pwdForm.actual, new_password: pwdForm.nueva })
        });

        if (response.status === 401) return cerrarSesion("Tu sesión expiró.");

        if (response.ok) {
            showToast("¡Contraseña actualizada!", "success");
            cerrarModal();
        } else {
            const data = await response.json();
            showToast(data.old_password ? data.old_password[0] : "Error al actualizar.", "error");
        }
    } catch (error) {
        showToast("Error de conexión.", "error");
    }
}
</script>

<template>
    <div class="flex h-screen bg-slate-50 text-slate-800 font-sans antialiased relative overflow-hidden">

        <transition enter-active-class="transition-opacity ease-linear duration-300" enter-from-class="opacity-0"
            enter-to-class="opacity-100" leave-active-class="transition-opacity ease-linear duration-300"
            leave-from-class="opacity-100" leave-to-class="opacity-0">
            <div v-show="sidebarMobileAbierto"
                class="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-40 lg:hidden cursor-pointer"
                @click="sidebarMobileAbierto = false"></div>
        </transition>

        <aside :class="[
            'bg-white z-50 flex flex-col shadow-[1px_0_15px_rgba(0,0,0,0.03)] transition-all duration-300 ease-in-out absolute lg:relative h-full border-r border-slate-100',
            sidebarColapsado ? 'lg:w-20' : 'lg:w-72',
            sidebarMobileAbierto ? 'w-72 translate-x-0' : '-translate-x-full lg:translate-x-0'
        ]">
            <div class="h-20 flex items-center px-4 gap-3 shrink-0">
                <button @click="sidebarColapsado = !sidebarColapsado"
                    class="hidden lg:block p-2 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-indigo-600 transition-colors focus:outline-none">
                    <Bars3Icon class="w-6 h-6" />
                </button>
                <div v-show="!sidebarColapsado || sidebarMobileAbierto"
                    class="flex items-center gap-2 overflow-hidden px-2 lg:px-0">
                    <BoltIcon class="w-7 h-7 text-indigo-600 shrink-0" />
                    <h1 class="text-2xl font-black text-slate-800 tracking-tighter">Volt<span
                            class="text-indigo-600">Stock</span></h1>
                </div>
            </div>

            <nav class="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto custom-scrollbar">
                
                <router-link to="/dashboard"
                    :class="['w-full rounded-lg transition-all duration-200 flex items-center gap-3.5 text-sm font-semibold group', sidebarColapsado ? 'justify-center p-3' : 'px-4 py-3']"
                    class="text-slate-500 hover:bg-slate-50 hover:text-slate-700"
                    active-class="!text-indigo-700 !bg-indigo-50/80 shadow-sm ring-1 ring-indigo-100">
                    <ChartBarIcon class="w-5 h-5 transition-colors" />
                    <span v-show="!sidebarColapsado" class="whitespace-nowrap">Dashboard</span>
                </router-link>
                
                <router-link to="/inventario"
                    :class="['w-full rounded-lg transition-all duration-200 flex items-center gap-3.5 text-sm font-semibold group', sidebarColapsado && !sidebarMobileAbierto ? 'justify-center p-3' : 'px-4 py-3']"
                    class="text-slate-500 hover:bg-slate-50 hover:text-slate-700"
                    active-class="!text-indigo-700 !bg-indigo-50/80 shadow-sm ring-1 ring-indigo-100">
                    <CubeIcon class="w-5 h-5" />
                    <span v-show="!sidebarColapsado || sidebarMobileAbierto" class="whitespace-nowrap">Inventario Global</span>
                </router-link>

                <router-link v-if="rolUsuario === 'admin' || rolUsuario === 'tecnico'" to="/cola"
                    :class="['w-full rounded-lg transition-all duration-200 flex items-center gap-3.5 text-sm font-semibold group', sidebarColapsado && !sidebarMobileAbierto ? 'justify-center p-3' : 'px-4 py-3']"
                    class="text-slate-500 hover:bg-slate-50 hover:text-slate-700"
                    active-class="!text-indigo-700 !bg-indigo-50/80 shadow-sm ring-1 ring-indigo-100">
                    <InboxArrowDownIcon class="w-5 h-5" />
                    <span v-show="!sidebarColapsado || sidebarMobileAbierto" class="whitespace-nowrap">Cola de Despacho</span>
                </router-link>

                <router-link v-if="rolUsuario === 'admin' || rolUsuario === 'tecnico'" to="/pila"
                    :class="['w-full rounded-lg transition-all duration-200 flex items-center gap-3.5 text-sm font-semibold group', sidebarColapsado && !sidebarMobileAbierto ? 'justify-center p-3' : 'px-4 py-3']"
                    class="text-slate-500 hover:bg-slate-50 hover:text-slate-700"
                    active-class="!text-indigo-700 !bg-indigo-50/80 shadow-sm ring-1 ring-indigo-100">
                    <ArrowUturnUpIcon class="w-5 h-5" />
                    <span v-show="!sidebarColapsado || sidebarMobileAbierto" class="whitespace-nowrap">Pila de Retornos</span>
                </router-link>

                <router-link to="/reportes"
                    :class="['w-full rounded-lg transition-all duration-200 flex items-center gap-3.5 text-sm font-semibold group', sidebarColapsado ? 'justify-center p-3' : 'px-4 py-3']"
                    class="text-slate-500 hover:bg-slate-50 hover:text-slate-700"
                    active-class="!text-indigo-700 !bg-indigo-50/80 shadow-sm ring-1 ring-indigo-100">
                    <DocumentChartBarIcon class="w-5 h-5 transition-colors" />
                    <span v-show="!sidebarColapsado" class="whitespace-nowrap">Reportes</span>
                </router-link>

                <div v-if="rolUsuario === 'admin'">
                    <div v-show="!sidebarColapsado || sidebarMobileAbierto"
                        class="mt-8 mb-2 px-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">
                        Administración</div>
                    <router-link to="/register"
                        :class="['w-full rounded-lg transition-all duration-200 flex items-center gap-3.5 text-sm font-semibold group', sidebarColapsado && !sidebarMobileAbierto ? 'justify-center p-3 mt-8' : 'px-4 py-3']"
                        class="text-slate-500 hover:bg-slate-50 hover:text-slate-700"
                        active-class="!text-indigo-700 !bg-indigo-50/80 shadow-sm ring-1 ring-indigo-100">
                        <UserPlusIcon class="w-5 h-5" />
                        <span v-show="!sidebarColapsado || sidebarMobileAbierto" class="whitespace-nowrap">Alta de Personal</span>
                    </router-link>
                </div>
            </nav>

            <div v-show="(!sidebarColapsado || sidebarMobileAbierto) && isAuthenticated"
                class="p-4 m-4 rounded-xl bg-white border border-slate-200 shadow-sm relative shrink-0">
                <div class="flex items-center gap-3">
                    <div
                        class="w-9 h-9 rounded-full bg-indigo-100 flex items-center justify-center font-bold text-indigo-700 text-sm uppercase">
                        {{ username.charAt(0) }}</div>
                    <div class="flex flex-col flex-1 overflow-hidden">
                        <span class="text-sm font-bold text-slate-800 leading-none truncate">{{ username }}</span>
                        <span class="text-[10px] text-slate-500 font-bold mt-1 truncate">{{ nombreRolVisual }}</span>
                    </div>
                    <button @click="menuUsuarioAbierto = !menuUsuarioAbierto"
                        class="p-1.5 rounded-md text-slate-400 hover:bg-slate-50 hover:text-slate-700 transition-all">
                        <Cog6ToothIcon class="w-5 h-5" />
                    </button>
                </div>

                <transition enter-active-class="transition ease-out duration-100"
                    enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
                    leave-active-class="transition ease-in duration-75"
                    leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                    <div v-show="menuUsuarioAbierto"
                        class="absolute bottom-[4.5rem] right-0 left-0 bg-white border border-slate-200 rounded-lg shadow-lg p-1.5 z-50">
                        <button @click="abrirAjustes"
                            class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-indigo-600 rounded-md flex items-center gap-2 transition-colors">
                            <Cog6ToothIcon class="w-4 h-4" /> Ajustes
                        </button>
                        <div class="h-px bg-slate-100 my-1"></div>
                        <button @click="cerrarSesion()"
                            class="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md flex items-center gap-2 transition-colors">
                            <ArrowRightOnRectangleIcon class="w-4 h-4" /> Cerrar Sesión
                        </button>
                    </div>
                </transition>
            </div>
        </aside>

        <div class="flex-1 flex flex-col min-w-0 relative">
            <header
                class="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center px-4 lg:px-8 sticky top-0 z-10">
                <button @click="sidebarMobileAbierto = true"
                    class="lg:hidden p-2 mr-3 text-slate-500 hover:bg-slate-100 rounded-lg transition-colors">
                    <Bars3Icon class="w-6 h-6" />
                </button>
                <div>
                    <h2 class="text-xl font-bold text-slate-800 capitalize tracking-tight">{{ titulo }}</h2>
                    <p class="text-[12px] text-slate-500 font-medium mt-0.5 hidden sm:block">Gestión de Inventario
                        Electrónico</p>
                </div>
            </header>

            <main class="flex-1 overflow-y-auto px-4 pt-6 pb-0 lg:px-10 lg:pt-10 custom-scrollbar">
                <div class="w-full min-h-full flex flex-col">
                    <div class="flex-1">
                        <slot></slot>
                    </div>

                    <footer
                        class="mt-12 py-8 border-t border-slate-200 flex flex-col md:flex-row justify-between items-center gap-6 text-xs text-slate-500 bg-white md:bg-transparent -mx-4 px-4 md:mx-0 md:px-0 shadow-[0_-1px_15px_rgba(0,0,0,0.02)] md:shadow-none">
                        <div class="flex flex-col md:flex-row items-center gap-2 md:gap-3 text-center md:text-left">
                            <div class="flex items-center gap-2">
                                <BoltIcon class="w-5 h-5 text-indigo-400" />
                                <span class="font-bold text-slate-700 text-sm">VoltStock</span>
                            </div>
                            <span class="hidden md:block text-slate-300">|</span>
                            <span>© 2026 UMG Santa Rosita</span>
                        </div>
                        <div class="flex gap-6 font-medium">
                            <a href="#" class="hover:text-indigo-600 transition-colors">Términos</a>
                            <a href="#" class="hover:text-indigo-600 transition-colors">Privacidad</a>
                            <a href="#" class="hover:text-indigo-600 transition-colors">Contacto</a>
                        </div>
                        <div
                            class="uppercase tracking-[0.2em] font-bold text-[9px] text-slate-400 bg-slate-50 md:bg-transparent px-4 py-2 rounded-full">
                            Proyecto Final - Prog III</div>
                    </footer>
                </div>
            </main>
        </div>

        <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0"
            enter-to-class="opacity-100" leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100" leave-to-class="opacity-0">
            <div v-if="modalAjustesAbierto" class="fixed inset-0 z-[100] flex items-center justify-center px-4">
                <div class="absolute inset-0 bg-slate-900/20 backdrop-blur-sm cursor-pointer" @click="cerrarModal">
                </div>
                <div
                    class="relative bg-white w-full max-w-md rounded-3xl shadow-2xl overflow-hidden border border-slate-100 flex flex-col max-h-[90vh]">
                    <div
                        class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50 shrink-0">
                        <div class="flex items-center gap-3">
                            <div class="p-2 bg-indigo-100 text-indigo-600 rounded-xl">
                                <Cog6ToothIcon class="w-5 h-5" />
                            </div>
                            <h3 class="text-lg font-bold text-slate-800">Ajustes de Cuenta</h3>
                        </div>
                        <button @click="cerrarModal"
                            class="text-slate-400 hover:text-slate-600 p-2 rounded-full transition-colors focus:outline-none">
                            <XMarkIcon class="w-5 h-5" />
                        </button>
                    </div>

                    <div class="p-6 space-y-6 overflow-y-auto custom-scrollbar">
                        <div>
                            <span
                                class="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-3">Información
                                del Perfil</span>
                            <div class="bg-slate-50 border border-slate-100 rounded-2xl p-4 flex items-center gap-4">
                                <div
                                    class="w-12 h-12 rounded-full bg-indigo-600 flex items-center justify-center font-bold text-white text-xl uppercase shadow-sm">
                                    {{ username.charAt(0) }}</div>
                                <div>
                                    <div class="font-bold text-slate-800 text-lg leading-tight">{{ username }}</div>
                                    <div class="text-[11px] font-black uppercase tracking-wider flex items-center gap-1 mt-1"
                                        :class="rolUsuario === 'admin' ? 'text-rose-500' : rolUsuario === 'tecnico' ? 'text-emerald-500' : 'text-indigo-500'">
                                        <ShieldCheckIcon class="w-4 h-4" /> {{ nombreRolVisual }}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="h-px w-full bg-slate-100"></div>

                        <div>
                            <span
                                class="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-4">Preferencias</span>
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-3">
                                    <BellIcon class="w-5 h-5 text-slate-400" />
                                    <div>
                                        <div class="text-sm font-bold text-slate-700">Notificaciones</div>
                                        <div class="text-xs text-slate-500">Alertas de stock crítico</div>
                                    </div>
                                </div>
                                <label class="relative inline-flex items-center cursor-pointer">
                                    <input type="checkbox" value="" class="sr-only peer" checked>
                                    <div
                                        class="w-11 h-6 bg-slate-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:bg-indigo-600 after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border after:rounded-full after:h-5 after:w-5 after:transition-all">
                                    </div>
                                </label>
                            </div>
                        </div>

                        <div class="h-px w-full bg-slate-100"></div>

                        <div>
                            <div class="flex items-center justify-between mb-4">
                                <span
                                    class="text-[10px] font-black text-slate-400 uppercase tracking-widest block">Seguridad</span>
                                <button type="button" @click="showPassword = !showPassword"
                                    class="text-[10px] font-bold text-indigo-600 uppercase tracking-wider flex items-center gap-1">
                                    <component :is="showPassword ? EyeSlashIcon : EyeIcon" class="w-3.5 h-3.5" /> {{
                                        showPassword ? 'Ocultar' : 'Ver' }}
                                </button>
                            </div>
                            <form @submit.prevent="cambiarPassword" class="space-y-3">
                                <div class="relative group">
                                    <LockClosedIcon
                                        class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500" />
                                    <input v-model="pwdForm.actual" :type="showPassword ? 'text' : 'password'"
                                        placeholder="Contraseña Actual" required
                                        class="w-full pl-9 pr-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all" />
                                </div>
                                <div class="grid grid-cols-2 gap-3">
                                    <div class="relative group">
                                        <LockClosedIcon
                                            class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500" />
                                        <input v-model="pwdForm.nueva" :type="showPassword ? 'text' : 'password'"
                                            placeholder="Nueva" required
                                            class="w-full pl-9 pr-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all" />
                                    </div>
                                    <div class="relative group">
                                        <LockClosedIcon
                                            class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500" />
                                        <input v-model="pwdForm.confirmar" :type="showPassword ? 'text' : 'password'"
                                            placeholder="Confirmar" required
                                            class="w-full pl-9 pr-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all" />
                                    </div>
                                </div>
                                <button type="submit"
                                    class="w-full mt-2 py-2.5 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 text-xs font-bold uppercase rounded-xl transition-colors">Actualizar
                                    Contraseña</button>
                            </form>
                        </div>
                    </div>

                    <div class="px-6 py-4 bg-slate-50/80 border-t border-slate-100 flex justify-end shrink-0">
                        <button @click="cerrarModal"
                            class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-bold rounded-xl transition-colors shadow-md shadow-indigo-200">Cerrar</button>
                    </div>
                </div>
            </div>
        </transition>

        <transition enter-active-class="transform ease-out duration-300 transition"
            enter-from-class="-translate-y-4 opacity-0 sm:translate-x-4"
            enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
            leave-active-class="transition ease-in duration-200" leave-from-class="opacity-100"
            leave-to-class="opacity-0">
            <div v-if="toastShow" class="fixed top-6 right-6 z-[999] pointer-events-none w-full max-w-sm">
                <div class="pointer-events-auto bg-white shadow-2xl rounded-2xl p-4 border"
                    :class="toastType === 'success' ? 'border-emerald-100' : 'border-red-100'">
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