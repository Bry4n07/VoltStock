import { ref } from 'vue'
import router from '../router' 

export const isLoadingGlobal = ref(false)

export const api = async (endpoint, options = {}) => {
  isLoadingGlobal.value = true
  
  const token = localStorage.getItem('access') 
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers
    }
  }

  try {
    const response = await fetch(`http://localhost:8000/api/${endpoint}`, config)
    
    if (response.status === 401) {
      localStorage.clear()
      router.push('/login')
      throw new Error('Sesión expirada')
    }
    
    return response
  } catch (error) {
    throw error
  } finally {
    isLoadingGlobal.value = false
  }
}