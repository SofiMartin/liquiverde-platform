import { useState, useEffect, useRef } from 'react'
import { MapPin, Navigation, Store } from 'lucide-react'
import { storesAPI } from '../services/api'

const StoreMap = () => {
  const [stores, setStores] = useState([])
  const [loading, setLoading] = useState(true)
  const mapRef = useRef(null)
  const mapInstanceRef = useRef(null)
  
  useEffect(() => {
    loadStores()
    loadLeaflet()
  }, [])
  
  const loadLeaflet = () => {
    // Cargar CSS de Leaflet
    if (!document.getElementById('leaflet-css')) {
      const link = document.createElement('link')
      link.id = 'leaflet-css'
      link.rel = 'stylesheet'
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
      document.head.appendChild(link)
    }
    
    // Cargar JS de Leaflet
    if (!window.L) {
      const script = document.createElement('script')
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
      script.onload = () => {
        console.log('Leaflet loaded')
      }
      document.head.appendChild(script)
    }
  }
  
  const loadStores = async () => {
    try {
      const response = await storesAPI.list()
      setStores(response.data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }
  
  useEffect(() => {
    if (stores.length > 0 && window.L && mapRef.current && !mapInstanceRef.current) {
      initMap()
    }
  }, [stores])
  
  const initMap = () => {
    // Centro en Santiago, Chile
    const center = [-33.4489, -70.6693]
    
    // Crear mapa
    const map = window.L.map(mapRef.current).setView(center, 12)
    mapInstanceRef.current = map
    
    // Agregar tiles de OpenStreetMap
    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map)
    
    // Agregar marcadores para cada tienda
    stores.forEach(store => {
      const lat = store.location?.latitude || store.location?.coordinates?.[1]
      const lng = store.location?.longitude || store.location?.coordinates?.[0]
      
      if (lat && lng) {
        const marker = window.L.marker([lat, lng]).addTo(map)
        
        const popupContent = `
          <div class="p-2">
            <h3 class="font-bold text-gray-900">${store.name}</h3>
            ${store.chain ? `<p class="text-sm text-gray-600">${store.chain}</p>` : ''}
            <p class="text-sm text-gray-600 mt-1">${store.location?.address || 'Sin dirección'}</p>
            ${store.sustainability_rating ? `
              <p class="text-sm text-primary-600 font-semibold mt-2">
                Sostenibilidad: ${store.sustainability_rating.toFixed(1)}/5
              </p>
            ` : ''}
          </div>
        `
        
        marker.bindPopup(popupContent)
      }
    })
    
    // Ajustar vista para mostrar todos los marcadores
    if (stores.length > 0) {
      const bounds = stores
        .filter(s => s.location?.latitude && s.location?.longitude)
        .map(s => [s.location.latitude, s.location.longitude])
      
      if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50] })
      }
    }
  }
  
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">🗺️ Mapa de Tiendas</h1>
      
      <div className="card">
        <div 
          ref={mapRef} 
          className="rounded-lg h-96 w-full"
          style={{ minHeight: '400px' }}
        />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {stores.map(store => (
          <div key={store.id} className="card hover:shadow-lg transition-shadow">
            <div className="flex items-start space-x-3">
              <Store className="h-6 w-6 text-primary-600 flex-shrink-0" />
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900">{store.name}</h3>
                {store.chain && (
                  <p className="text-sm text-gray-600">{store.chain}</p>
                )}
                <p className="text-sm text-gray-600 mt-1">{store.location.address}</p>
                {store.sustainability_rating && (
                  <div className="mt-2 flex items-center space-x-1">
                    <span className="text-xs text-gray-600">Sostenibilidad:</span>
                    <span className="text-sm font-semibold text-primary-600">
                      {store.sustainability_rating.toFixed(1)}/5
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default StoreMap
