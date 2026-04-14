<script setup>
import { ref } from 'vue'
import {
    Bars3Icon, CubeIcon, InboxArrowDownIcon,
    Cog6ToothIcon, ArrowRightOnRectangleIcon, BoltIcon
} from '@heroicons/vue/24/outline'

defineProps({
    titulo: String
})

const sidebarColapsado = ref(false)
const menuUsuarioAbierto = ref(false)
</script>

<template>
    <div class="flex h-screen bg-slate-50 text-slate-800 font-sans antialiased">

        <aside :class="[
            'bg-white z-20 flex flex-col shadow-[1px_0_15px_rgba(0,0,0,0.03)] transition-all duration-300 ease-in-out relative border-r border-slate-100',
            sidebarColapsado ? 'w-20' : 'w-72'
        ]">
            <div class="h-20 flex items-center px-4 gap-3">
                <button @click="sidebarColapsado = !sidebarColapsado"
                    class="p-2 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-indigo-600 transition-colors focus:outline-none">
                    <Bars3Icon class="w-6 h-6" />
                </button>
                <div v-show="!sidebarColapsado" class="flex items-center gap-2 overflow-hidden">
                    <BoltIcon class="w-7 h-7 text-indigo-600" />
                    <h1 class="text-2xl font-black text-slate-800 tracking-tighter">Volt<span
                            class="text-indigo-600">Stock</span></h1>
                </div>
            </div>

            <nav class="flex-1 px-4 py-6 space-y-1.5">

                <router-link to="/inventario"
                    :class="['w-full rounded-lg transition-all duration-200 flex items-center gap-3.5 text-sm font-semibold group', sidebarColapsado ? 'justify-center p-3' : 'px-4 py-3']"
                    class="text-slate-500 hover:bg-slate-50 hover:text-slate-700"
                    active-class="!text-indigo-700 !bg-indigo-50/80 shadow-sm ring-1 ring-indigo-100 hover:!bg-indigo-50/80 hover:!text-indigo-700">
                    <CubeIcon class="w-5 h-5 transition-colors" />
                    <span v-show="!sidebarColapsado" class="whitespace-nowrap">Inventario Global</span>
                </router-link>

                <router-link to="/cola"
                    :class="['w-full rounded-lg transition-all duration-200 flex items-center gap-3.5 text-sm font-semibold group', sidebarColapsado ? 'justify-center p-3' : 'px-4 py-3']"
                    class="text-slate-500 hover:bg-slate-50 hover:text-slate-700"
                    active-class="!text-indigo-700 !bg-indigo-50/80 shadow-sm ring-1 ring-indigo-100 hover:!bg-indigo-50/80 hover:!text-indigo-700">
                    <InboxArrowDownIcon class="w-5 h-5 transition-colors" />
                    <span v-show="!sidebarColapsado" class="whitespace-nowrap">Cola de Despacho</span>
                </router-link>

                <router-link to="/pila"
                    :class="['w-full rounded-lg transition-all duration-200 flex items-center gap-3.5 text-sm font-semibold group', sidebarColapsado ? 'justify-center p-3' : 'px-4 py-3']"
                    class="text-slate-500 hover:bg-slate-50 hover:text-slate-700"
                    active-class="!text-amber-700 !bg-amber-50/80 shadow-sm ring-1 ring-amber-100">
                    <ArrowUturnUpIcon class="w-5 h-5 transition-colors" />
                    <span v-show="!sidebarColapsado" class="whitespace-nowrap">Pila de Retornos</span>
                </router-link>

            </nav>
            <div v-show="!sidebarColapsado"
                class="p-4 m-4 rounded-xl bg-white border border-slate-200 shadow-sm relative">
                <div class="flex items-center gap-3">
                    <div
                        class="w-9 h-9 rounded-full bg-indigo-100 flex items-center justify-center font-bold text-indigo-700 text-sm">
                        B</div>
                    <div class="flex flex-col flex-1">
                        <span class="text-sm font-bold text-slate-800 leading-none">Bryan</span>
                        <span class="text-[11px] text-slate-500 font-medium mt-1">Administrador</span>
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
                        <button
                            class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-indigo-600 rounded-md flex items-center gap-2 transition-colors">
                            <Cog6ToothIcon class="w-4 h-4" /> Ajustes
                        </button>
                        <div class="h-px bg-slate-100 my-1"></div>
                        <button
                            class="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md flex items-center gap-2 transition-colors">
                            <ArrowRightOnRectangleIcon class="w-4 h-4" /> Cerrar Sesión
                        </button>
                    </div>
                </transition>
            </div>
        </aside>

        <div class="flex-1 flex flex-col min-w-0 relative">

            <header
                class="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10">
                <div>
                    <h2 class="text-xl font-bold text-slate-800 capitalize tracking-tight">{{ titulo }}</h2>
                    <p class="text-[12px] text-slate-500 font-medium mt-0.5">Gestión de Inventario Electrónico</p>
                </div>
                <div class="flex items-center gap-4">
                    <button
                        class="text-sm font-semibold text-slate-500 hover:text-indigo-600 transition-colors px-4 py-2 rounded-lg hover:bg-slate-50">Ingresar</button>
                    <button
                        class="text-sm font-semibold text-indigo-700 bg-indigo-50 border border-indigo-100 hover:bg-indigo-100 px-5 py-2 rounded-lg transition-all shadow-sm">Registrarse</button>
                </div>
            </header>

            <main class="flex-1 overflow-y-auto px-6 pt-6 pb-0 lg:px-10 lg:pt-10 lg:pb-0 custom-scrollbar">
                <div class="w-full min-h-full flex flex-col">

                    <div class="flex-1">
                        <slot></slot>
                    </div>

                    <footer
                        class="mt-12 py-6 border-t border-slate-200 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-slate-500">
                        <div class="flex items-center gap-2">
                            <BoltIcon class="w-4 h-4 text-slate-400" />
                            <span class="font-semibold text-slate-600">VoltStock</span>
                            <span>© 2026 UMG Santa Rosita</span>
                        </div>
                        <div class="flex gap-6 font-medium">
                            <a href="#" class="hover:text-indigo-600 transition-colors">Términos</a>
                            <a href="#" class="hover:text-indigo-600 transition-colors">Privacidad</a>
                            <a href="#" class="hover:text-indigo-600 transition-colors">Contacto</a>
                        </div>
                        <div class="uppercase tracking-widest font-semibold text-[10px]">Proyecto Final - Prog III</div>
                    </footer>
                </div>
            </main>
        </div>
    </div>
</template>

<style>
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
}

.custom-scrollbar:hover::-webkit-scrollbar-thumb {
    background: #94a3b8;
}
</style>