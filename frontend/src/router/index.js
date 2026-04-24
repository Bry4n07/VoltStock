import { createRouter, createWebHistory } from 'vue-router'
import InventarioView from '../views/InventarioView.vue'
import ColaPedidosView from '../views/ColaPedidosView.vue'
import PilaRetornosView from '../views/PilaRetornosView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import ReportesView from '../views/ReportesView.vue'

const routes = [
    {
        path: '/login',
        name: 'login',
        component: () => import('../views/LoginView.vue'),
        meta: { title: 'login' },
        beforeEnter: (to, from, next) => {
            const isAuthenticated = localStorage.getItem('access');

            if (isAuthenticated) {
                next('/inventario');
            } else {
                next();
            }
        }
    },
    {
        path: '/register',
        name: 'register',
        component: RegisterView,
        meta: { requiresAuth: true, roles: ['admin'], title: 'register' }
    },
    {
        path: '/dashboard',
        name: 'dashboard',
        component: DashboardView,
        meta: { requiredAuth: true, title: 'dashboard' }
    },
    {
        path: '/',
        redirect: '/dashboard'
    },
    {
        path: '/inventario',
        name: 'inventario',
        component: InventarioView,
        meta: { requiresAuth: true, title: 'inventario' }
    },
    {
        path: '/cola',
        name: 'cola',
        component: ColaPedidosView,
        meta: { requiresAuth: true, roles: ['admin', 'operador'], title: 'Cola' }
    },
    {
        path: '/pila',
        name: 'pila',
        component: PilaRetornosView,
        meta: { requiresAuth: true, roles: ['admin', 'operador'], title: 'pila' }
    },
    {
        path: '/reportes',
        name: 'reportes',
        component: ReportesView,
        meta: { requiresAuth: true, title: 'reportes' }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.afterEach((to) => {
    document.title = to.meta.title || 'VoltStock - Gestión de Laboratorio';
});

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access')
    const rol = localStorage.getItem('user_rol') || 'auditor'

    if (to.meta.requiresAuth && !token) {
        next('/login')
    }
    else if (to.meta.roles && !to.meta.roles.includes(rol)) {
        next('/dashboard')
    }
    else {
        next()
    }
})

export default router