import { useState, useEffect } from 'react'
import { MapPin, Navigation, Store } from 'lucide-react'
import { storesAPI } from '../services/api'

const StoreMap = () => {
  const [stores, setStores] = useState([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    loadStores()
  }, [])
  
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
  
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Mapa de Tiendas</h1>
      
      <div className="card">
        <div className="bg-gray-100 rounded-lg h-96 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <MapPin className="h-12 w-12 mx-auto mb-2" />
            <p>Mapa interactivo (requiere integración con Leaflet)</p>
          </div>
        </div>
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
