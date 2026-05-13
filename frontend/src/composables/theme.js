import { ref, computed } from 'vue';

/**
 * Theme Composable
 * Manages theme switching between light and dark modes
 */
export function useTheme() {
  const theme = ref(localStorage.getItem('theme') || 'light');
  const isDark = computed(() => theme.value === 'dark');
  
  const toggleTheme = () => {
    const newTheme = isDark.value ? 'light' : 'dark';
    theme.value = newTheme;
    localStorage.setItem('theme', newTheme);
  };
  
  const setTheme = (newTheme) => {
    theme.value = newTheme;
    localStorage.setItem('theme', newTheme);
  };
  
  return {
    theme,
    isDark,
    toggleTheme,
    setTheme
  };
}
