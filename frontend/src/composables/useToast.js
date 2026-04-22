import { ref } from 'vue'

// Estado global (fuera de la función para que se comparta en toda la app)
const toastShow = ref(false)
const toastMessage = ref('')
const toastType = ref('success') // 'success' o 'error'
let timeoutId = null

export function useToast() {
    const showToast = (msg, type = 'success') => {
        // Limpiamos el contador si hay un toast anterior para que no se crucen
        if (timeoutId) clearTimeout(timeoutId)
        
        toastMessage.value = msg
        toastType.value = type
        toastShow.value = true

        // Se oculta solo a los 3.5 segundos
        timeoutId = setTimeout(() => {
            toastShow.value = false
        }, 3500)
    }

    return {
        toastShow,
        toastMessage,
        toastType,
        showToast
    }
}