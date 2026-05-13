import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { store } from './store';
import { useTheme } from './composables/theme';

/**
 * Main Vue Application
 * Integrates all Phase 6 components
 */
const app = createApp(App).use(router).use(store).use(useTheme);

// Mount app
app.mount('#app');

// Global error handling
app.config.errorHandler((error) => {
  console.error('Application Error:', error);
});

// Global success handling
app.config.warnHandler((warning) => {
  console.warn('Application Warning:', warning);
});

export default app;
