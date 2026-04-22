<template>
  <div class="space-y-8 animate-fade-in">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-black text-slate-800 tracking-tight">Panel de Control</h1>
        <p class="text-sm text-slate-500 font-medium">Estado actual del laboratorio VoltStock</p>
      </div>
      <div class="text-right">
        <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">Última sincronización</span>
        <p class="text-sm font-bold text-indigo-600">Hace 2 minutos</p>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white p-6 rounded-[2rem] border border-slate-100 shadow-sm">
        <div class="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4">
          <CircleStackIcon class="w-6 h-6" />
        </div>
        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Componentes</span>
        <div class="text-3xl font-black text-slate-800 mt-1">1,284</div>
      </div>

      <div class="bg-white p-6 rounded-[2rem] border border-slate-100 shadow-sm">
        <div class="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center mb-4">
          <ExclamationTriangleIcon class="w-6 h-6" />
        </div>
        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Stock Crítico</span>
        <div class="text-3xl font-black text-rose-600 mt-1">12</div>
      </div>

      <div class="bg-white p-6 rounded-[2rem] border border-slate-100 shadow-sm">
        <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
          <ArrowPathIcon class="w-6 h-6" />
        </div>
        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">En Préstamo</span>
        <div class="text-3xl font-black text-slate-800 mt-1">45</div>
      </div>

      <div class="bg-white p-6 rounded-[2rem] border border-slate-100 shadow-sm">
        <div class="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center mb-4">
          <UserGroupIcon class="w-6 h-6" />
        </div>
        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Usuarios Activos</span>
        <div class="text-3xl font-black text-slate-800 mt-1">8</div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2 bg-white rounded-[2.5rem] border border-slate-100 p-8 shadow-sm">
        <h3 class="text-lg font-black text-slate-800 mb-6">Actividad Reciente</h3>
        <div class="space-y-6">
          <div v-for="i in 3" :key="i" class="flex items-center gap-4 p-4 rounded-2xl bg-slate-50/50 border border-slate-50">
            <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-sm">
              <BoltIcon class="w-5 h-5 text-indigo-500" />
            </div>
            <div class="flex-1">
                <p class="text-sm font-bold text-slate-700">Despacho de Arduino Nano</p>
                <p class="text-xs text-slate-500">Realizado por encargado_lab1</p>
            </div>
            <div class="text-right text-xs font-bold text-slate-400 uppercase">14:20 PM</div>
          </div>
        </div>
      </div>

      <div class="bg-indigo-600 rounded-[2.5rem] p-8 text-white shadow-xl shadow-indigo-100 relative overflow-hidden">
        <div class="relative z-10">
          <h3 class="text-xl font-bold mb-2">Reporte de Turno</h3>
          <p class="text-indigo-100 text-sm leading-relaxed mb-8">Genera un resumen rápido de las entradas y salidas de las últimas 8 horas.</p>
          <button class="w-full py-4 bg-white text-indigo-600 rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-indigo-50 transition-colors">Descargar PDF</button>
        </div>
        <BoltIcon class="absolute -bottom-10 -right-10 w-48 h-48 text-indigo-500 opacity-20" />
      </div>
    </div>
  </div>
</template>