import { createRouter, createWebHistory} from 'vue-router'
import InventarioView from '../views/InventarioView.vue'
import ColaPedidosView from '../views/ColaPedidosView.vue'
import PilaRetornosView from '../views/PilaRetornosView.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/inventario'
        },
        {
            path: '/inventario',
            name: 'inventario',
            component: InventarioView
        },
        {
            path: '/cola',
            name: 'cola',
            component: ColaPedidosView
        },
        {
            path: '/pila',
            name: 'pila',
            component: PilaRetornosView
        },
    ]
})

export default router