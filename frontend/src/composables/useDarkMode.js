import { ref, watch } from 'vue';

const isDark = ref(localStorage.getItem("dark-mode") === "true");

watch(isDark, (value) => {
    localStorage.setItem("dark-mode", value);
    document.documentElement.classList.toggle("dark", value);
});

export function useDarkMode() {
    return { isDark };
}
