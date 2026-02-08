import { createRouter, createWebHistory } from "vue-router";

// Import all components
import Login from "./components/Login.vue";
import Register from "./components/Register.vue";
import Dashboard from "./components/Dashboard.vue";
import FarmerDashboard from "./components/FarmerDashboard.vue";
import OfficerDashboard from "./components/OfficerDashboard.vue";
import AdminDashboard from "./components/AdminDashboard.vue";
import Marketplace from "./components/Marketplace.vue";
import PriceTrends from "./components/PriceTrends.vue";
import DemandInsights from "./components/DemandInsights.vue";
import PriceComparison from "./components/PriceComparison.vue";
import Notifications from "./components/Notifications.vue";
import Profile from "./components/Profile.vue";
import CropManagement from "./components/CropManagement.vue";

// New advanced components
import AdvancedAnalytics from "./components/AdvancedAnalytics.vue";
import WeatherDashboard from "./components/WeatherDashboard.vue";

const routes = [
  // Root path - redirect based on authentication
  { path: "/", redirect: to => {
    const token = localStorage.getItem("token");
    if (token) {
      return "/dashboard";
    } else {
      return "/login";
    }
  }},
  
  { path: "/login", component: Login },
  { path: "/register", component: Register },

  // Common dashboard (accessible to all logged-in users)
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true } },

  // Role-specific dashboards
  {
    path: "/farmer-dashboard",
    component: FarmerDashboard,
    meta: { requiresAuth: true, role: "farmer" },
  },
  {
    path: "/officer-dashboard",
    component: OfficerDashboard,
    meta: { requiresAuth: true, role: "officer" },
  },
  {
    path: "/admin-dashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" },
  },

  // Shared features
  {
    path: "/marketplace",
    component: Marketplace,
    meta: { requiresAuth: true },
  },
  {
    path: "/price-trends",
    component: PriceTrends,
    meta: { requiresAuth: true },
  },
  { path: "/demand", component: DemandInsights, meta: { requiresAuth: true } },
  
  {
    path: "/price-comparison",
    component: PriceComparison,
    meta: { requiresAuth: true },
  },
  {
    path: "/notifications",
    component: Notifications,
    meta: { requiresAuth: true },
  },
  { path: "/profile", component: Profile, meta: { requiresAuth: true } },
  { path: "/crops", component: CropManagement, meta: { requiresAuth: true } },

  // New advanced features
  {
    path: "/analytics",
    component: AdvancedAnalytics,
    meta: { requiresAuth: true, role: ["officer", "admin"] },
  },
  {
    path: "/weather",
    component: WeatherDashboard,
    meta: { requiresAuth: true, role: ["farmer", "officer"] },
  },

  // Legacy routes for backward compatibility
  {
    path: "/recommendations",
    component: WeatherDashboard, // Redirect to weather dashboard for now
    meta: { requiresAuth: true, role: "farmer" },
  },
  {
    path: "/reports",
    component: AdvancedAnalytics, // Redirect to analytics for officers
    meta: { requiresAuth: true, role: "officer" },
  },
  {
    path: "/admin-panel",
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" },
  },

  // Catch-all redirect to login (more robust)
  { path: "/:pathMatch(.*)*", redirect: "/login" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const userRole = localStorage.getItem("role");
  
  console.log('🛡️ Router Guard - Checking auth for:', to.path);
  console.log('🔑 Token present:', !!token);
  console.log('👤 User role:', userRole);
  console.log('🔒 Requires auth:', to.meta.requiresAuth);

  if (to.meta.requiresAuth && !token) {
    console.log('❌ No token found, redirecting to login');
    // Not logged in → redirect to login
    return next("/login");
  }

  if (to.meta.role) {
    // Handle role requirements
    const requiredRoles = Array.isArray(to.meta.role) ? to.meta.role : [to.meta.role];
    
    if (!userRole || !requiredRoles.includes(userRole)) {
      // Role mismatch → redirect to appropriate dashboard
      if (userRole === 'farmer') {
        return next("/farmer-dashboard");
      } else if (userRole === 'officer') {
        return next("/officer-dashboard");
      } else if (userRole === 'admin') {
        return next("/admin-dashboard");
      } else {
        return next("/dashboard");
      }
    }
  }

  next();
});

export default router;
