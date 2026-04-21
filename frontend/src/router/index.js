import { createRouter, createWebHistory } from 'vue-router'
import InventarioView from '../views/InventarioView.vue'
import ColaPedidosView from '../views/ColaPedidosView.vue'
import PilaRetornosView from '../views/PilaRetornosView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

const routes = [
    {
        path: '/login',
        name: 'login',
        component: LoginView
    },
    {
        path: '/register',
        name: 'register',
        component: RegisterView
    },
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
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes 
})

export default router