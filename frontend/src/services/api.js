import router from '../router'

const BASE_URL = 'http://127.0.0.1:8000/api'

export const api = async (endpoint, options = {}) => {
    const token = localStorage.getItem('access')

    const defaultHeaders = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    }

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers
        }
    }

    try {
        const response = await fetch(`${BASE_URL}/${endpoint}`, config)

        if (response.status === 401) {
            localStorage.removeItem('access')

            if (router.currentRoute.value.name !== 'login') {
                window.location.href = '/login'
            }
            return Promise.reject('Sesión expirada')
        }

        return response
    } catch (error) {
        console.error('Error en la petición:', error)
        throw error
    }
}