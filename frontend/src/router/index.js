import { createRouter, createWebHistory } from 'vue-router'

/*----  Guest públicas ---*/
import GuestLayout from '@/layout/GuestLayout.vue'

/* --- Vistas públicas --- */
import Home from '@/views/Home.vue'
import Login from '@/views/auth/Login.vue'

/* --- Vistas privadas --- */

import AuthLayout from '@/layout/AuthLayout.vue'
import Dashboard from '@/views/home/Dashboard.vue'
import modeloias from '@/views/modelo/iaclaro.vue'
import registro from '@/views/modelo/tablemodelo.vue'



const routes = [

    {
        path: '/',
        component: GuestLayout,
        meta: { guestOnly: true },
        children: [
            { path: '', name: 'Home', component: Home },
            { path: 'login', name: 'Login', component: Login },

        ]
    },

    {
        path: '/',
        component: AuthLayout,

        children: [
            {
                path: 'dashboard',
                name: 'Dashboard',
                component: Dashboard,
            },
            {
                path: 'modelo',
                name: 'Modelo',
                component: modeloias,
            },
            {
                path: 'modelo',
                name: 'Modelo',
                component: modeloias,
            },
            {
                path: 'registro',
                name: 'Registro',
                component: registro,
            },
        ],
    },


]


const router = createRouter({
    history: createWebHistory(),
    routes
})

/* ----------------- MIDDLEWARE ----------------- */
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token');
    const user = JSON.parse(localStorage.getItem('user'));

    // Si ya está logeado, no acceder a páginas públicas
    if (to.meta.guestOnly && token) {
        return next({ name: 'Dashboard' });
    }

    // Si la ruta privada no tiene token → login
    if (to.meta.requiresAuth && !token) {
        return next({ name: 'Login' });
    }

    // Validación de roles
    if (to.meta.roles && user) {
        const hasRole = to.meta.roles.includes(user.role);
        if (!hasRole) {
            return next({ name: 'NotFound' });
        }
    }

    next();
})

export default router
