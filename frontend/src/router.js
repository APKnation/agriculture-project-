import { createRouter, createWebHistory } from 'vue-router';
import Login from './components/Login.vue';
import Dashboard from './components/Dashboard.vue'; 

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },
  
  { 
    path: '/dashboard', 
    name: 'Dashboard', 
    component: Dashboard, 
    meta: { requiresAuth: true } 
  },

  // FIXED: Moved these inside the routes array correctly
  { 
    path: '/price-comparison', 
    name: 'PricesComparison',
    component: () => import('./components/PriceComparison.vue'), 
    meta: { requiresAuth: true } 
  },
  { 
    path: '/notifications', 
    name: 'Notifications',
    component: () => import('./components/Notifications.vue'), 
    meta: { requiresAuth: true } 
  },
  {
  path: '/create-profile',
  name: 'CreateProfile',
  component: () => import('./components/CreateProfile.vue'),
  meta: { requiresAuth: false } // Change this to false so new users can see it!
},
  { 
    path: '/profile', 
    name: 'Profile',
    component: () => import('./components/Profile.vue'), 
    meta: { requiresAuth: true } 
  },

  // ROLE-SPECIFIC PAGES
  { 
    path: '/farmer-dashboard', 
    component: () => import('./components/FarmerDashboard.vue'), 
    meta: { requiresAuth: true, role: 'farmer' } 
  },
  { 
    path: '/admin-dashboard', 
    component: () => import('./components/AdminDashboard.vue'), 
    meta: { requiresAuth: true, role: 'admin' } 
  },
  { 
    path: '/officer-dashboard', 
    component: () => import('./components/OfficerDashboard.vue'), 
    meta: { requiresAuth: true, role: 'officer' } 
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Guard Logic
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('role')?.toLowerCase().trim();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !token) {
    return next('/login');
  }

  if (to.path === '/login' && token) {
    return next('/dashboard');
  }

  if (to.meta.role && to.meta.role !== userRole) {
    console.warn("Unauthorized. Redirecting...");
    return next('/dashboard'); 
  }

  next();
});

export default router;