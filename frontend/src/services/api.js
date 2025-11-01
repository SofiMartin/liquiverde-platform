import axios from 'axios'

// Detectar si estamos en producción o desarrollo
const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
const API_BASE_URL = isProduction 
  ? 'https://liquiverde-platform.onrender.com/api'
  : (import.meta.env.VITE_API_URL || 'http://localhost:8000/api')

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const productsAPI = {
  scanBarcode: (barcode) => api.post(`/products/scan/${barcode}`),
  search: (params) => api.get('/products/search', { params }),
  searchExternal: (params) => api.get('/products/search/external', { params }),
  getById: (id) => api.get(`/products/${id}`),
  create: (product) => api.post('/products/', product),
  findSubstitutes: (productId, params) => api.post(`/products/${productId}/substitutes`, null, { params }),
  compare: (productId1, productId2) => api.post('/products/compare', null, { params: { product_id_1: productId1, product_id_2: productId2 } }),
  list: (limit = 100) => api.get('/products/', { params: { limit } }),
}

export const shoppingListsAPI = {
  create: (shoppingList) => api.post('/shopping-lists/', shoppingList),
  getById: (id) => api.get(`/shopping-lists/${id}`),
  list: (limit = 50) => api.get('/shopping-lists/', { params: { limit } }),
  optimize: (listId, criteria) => api.post(`/shopping-lists/${listId}/optimize`, criteria),
  analyze: (items) => api.post('/shopping-lists/analyze', items),
  quickOptimize: (data) => api.post('/shopping-lists/quick-optimize', data),
}

export const analysisAPI = {
  getDashboard: () => api.get('/analysis/dashboard'),
  calculateImpact: (productIds) => api.get('/analysis/impact', { params: { product_ids: productIds } }),
  getTrends: () => api.get('/analysis/trends'),
  getSavingsReport: (productIds) => api.get('/analysis/savings-report', { params: { product_ids: productIds } }),
}

export const storesAPI = {
  create: (store) => api.post('/stores/', store),
  list: () => api.get('/stores/'),
  getNearby: (params) => api.get('/stores/nearby', { params }),
  searchExternal: (data) => api.post('/stores/search-external', data),
  geocode: (address) => api.post('/stores/geocode', { address }),
  optimizeRoute: (data) => api.post('/stores/optimize-route', data),
  compareRoutes: (data) => api.post('/stores/compare-routes', data),
  getMapData: (params) => api.get('/stores/map-data', { params }),
}

export default api
