import { createRouter, createWebHistory } from "vue-router";

// Import all components
import Login from "./components/Login.vue";
import Dashboard from "./components/Dashboard.vue";
import FarmerDashboard from "./components/FarmerDashboard.vue";
import OfficerDashboard from "./components/OfficerDashboard.vue";
import AdminDashboard from "./components/AdminDashboard.vue";
import Marketplace from "./components/Marketplace.vue";
import PriceTrends from "./components/PriceTrends.vue";
import DemandInsights from "./components/DemandInsights.vue";
import CropRecommendations from "./components/CropRecommendations.vue";
import PriceComparison from "./components/PriceComparison.vue";
import Notifications from "./components/Notifications.vue";
import Profile from "./components/Profile.vue";

const routes = [
  { path: "/", redirect: "/dashboard" },
  { path: "/login", component: Login },

  { path: "/dashboard", component: Dashboard },
  { path: "/farmer-dashboard", component: FarmerDashboard },
  { path: "/officer-dashboard", component: OfficerDashboard },
  { path: "/admin-dashboard", component: AdminDashboard },

  { path: "/marketplace", component: Marketplace },
  { path: "/price-trends", component: PriceTrends },
  { path: "/demand", component: DemandInsights },
  { path: "/recommendations", component: CropRecommendations },
  { path: "/price-comparison", component: PriceComparison },
  { path: "/notifications", component: Notifications },
  { path: "/profile", component: Profile },

  // Catch-all redirect to dashboard
  { path: "/:pathMatch(.*)*", redirect: "/dashboard" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
