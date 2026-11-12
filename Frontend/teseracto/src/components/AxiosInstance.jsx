import axios from 'axios'

const baseUrl = 'http://127.0.0.1:8000/'

const AxiosInstance = axios.create({
    baseURL: baseUrl,
    timeout: 5000,
    headers: {
        accept: "application/json"
    }
})

AxiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('Token')
        config.headers.Authorization = token ? `Token ${token}` : ''

        // Si se envía FormData, dejar que el navegador ponga multipart + boundary
        if (config.data instanceof FormData) {
            delete config.headers['Content-Type']
        }
        return config
    }
)

AxiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('Token')
        }
        return Promise.reject(error)
    }
)

export default AxiosInstance