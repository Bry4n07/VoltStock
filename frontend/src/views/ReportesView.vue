<template>
  <div class="max-w-4xl mx-auto space-y-8 animate-fade-in">
    <div class="text-center space-y-2">
      <h1 class="text-3xl font-black text-slate-800">Centro de Reportes</h1>
      <p class="text-slate-500 font-medium">Exporta la información de VoltStock para auditorías o inventarios físicos.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-sm group hover:border-indigo-200 transition-all">
        <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
          <TableCellsIcon class="w-6 h-6" />
        </div>
        <h4 class="text-xl font-black text-slate-800 mb-2">Inventario de Existencias</h4>
        <p class="text-sm text-slate-500 mb-8 leading-relaxed">Listado completo de componentes con su ubicación, cantidad actual y valor estimado.</p>
        <div class="flex gap-3">
          <button class="flex-1 py-3 bg-slate-50 text-slate-600 rounded-xl font-bold text-xs uppercase hover:bg-slate-100 transition-colors">Excel</button>
          <button class="flex-1 py-3 bg-indigo-600 text-white rounded-xl font-bold text-xs uppercase hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-100">PDF</button>
        </div>
      </div>

      <div class="bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-sm group hover:border-amber-200 transition-all">
        <div class="w-12 h-12 bg-amber-50 text-amber-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
          <ArrowPathIcon class="w-6 h-6" />
        </div>
        <h4 class="text-xl font-black text-slate-800 mb-2">Historial de Movimientos</h4>
        <p class="text-sm text-slate-500 mb-8 leading-relaxed">Bitácora detallada de quién sacó qué componente y cuándo fue devuelto al laboratorio.</p>
        <div class="flex gap-3">
          <button class="flex-1 py-3 bg-slate-50 text-slate-600 rounded-xl font-bold text-xs uppercase hover:bg-slate-100 transition-colors">Excel</button>
          <button class="flex-1 py-3 bg-amber-600 text-white rounded-xl font-bold text-xs uppercase hover:bg-amber-700 transition-colors shadow-lg shadow-amber-100">PDF</button>
        </div>
      </div>
    </div>
  </div>
</template>