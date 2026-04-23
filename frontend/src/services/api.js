import { ref } from 'vue'
// Si usas vue-router importarlo para redireccionar
import router from '../router' 

// Esta variable se puede leer desde CUALQUIER archivo Vue
export const isLoadingGlobal = ref(false)

export const api = async (endpoint, options = {}) => {
  isLoadingGlobal.value = true // Encendemos el loader
  
  const token = localStorage.getItem('token') // O donde guardes tu token
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers
    }
  }

  try {
    // Cambia la URL por la de tu backend de Django
    const response = await fetch(`http://localhost:8000/api/${endpoint}`, config)
    
    // SI EL TOKEN ESTÁ VENCIDO O ES INVÁLIDO
    if (response.status === 401) {
      localStorage.removeItem('token')
      // router.push('/login') // Redirigir al login
      throw new Error('Sesión expirada')
    }
    
    return response
  } catch (error) {
    throw error
  } finally {
    isLoadingGlobal.value = false // Apagamos el loader pase lo que pase
  }
}