import { useState, useEffect } from 'react'
import { TrendingUp, Leaf, DollarSign, Package } from 'lucide-react'
import { analysisAPI } from '../services/api'

const Dashboard = () => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    loadDashboard()
  }, [])
  
  const loadDashboard = async () => {
    try {
      const response = await analysisAPI.getDashboard()
      setStats(response.data)
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
    }
  }
  
  if (loading) {
    return <div className="text-center py-12">Cargando...</div>
  }
  
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Dashboard de Impacto</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card bg-blue-50 border-2 border-blue-200">
          <div className="flex items-center space-x-3 mb-2">
            <Package className="h-8 w-8 text-blue-600" />
            <div>
              <div className="text-sm font-semibold text-gray-700">Productos</div>
              <div className="text-3xl font-bold text-gray-900">{stats?.total_products || 0}</div>
            </div>
          </div>
        </div>
        
        <div className="card bg-green-50 border-2 border-green-200">
          <div className="flex items-center space-x-3 mb-2">
            <Leaf className="h-8 w-8 text-green-600" />
            <div>
              <div className="text-sm font-semibold text-gray-700">Sostenibilidad Promedio</div>
              <div className="text-3xl font-bold text-green-700">{stats?.average_sustainability?.toFixed(0) || 0}/100</div>
            </div>
          </div>
        </div>
        
        <div className="card bg-purple-50 border-2 border-purple-200">
          <div className="flex items-center space-x-3 mb-2">
            <TrendingUp className="h-8 w-8 text-purple-600" />
            <div>
              <div className="text-sm font-semibold text-gray-700">Huella de Carbono</div>
              <div className="text-3xl font-bold text-purple-700">{stats?.total_carbon_footprint?.toFixed(1) || 0} kg</div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card border-2 border-primary-200">
          <h2 className="text-xl font-bold mb-4 text-gray-900">🏆 Top Productos Sostenibles</h2>
          <div className="space-y-2">
            {stats?.top_sustainable_products?.slice(0, 5).map((product, index) => (
              <div key={product.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold">
                    {index + 1}
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900">{product.name}</div>
                    <div className="text-sm text-gray-700 font-medium">{product.category}</div>
                  </div>
                </div>
                <div className="text-primary-600 font-bold text-lg">{product.score.toFixed(0)}</div>
              </div>
            ))}
          </div>
        </div>
        
        <div className="card border-2 border-primary-200">
          <h2 className="text-xl font-bold mb-4 text-gray-900">📊 Distribución por Categoría</h2>
          <div className="space-y-2">
            {Object.entries(stats?.category_distribution || {}).slice(0, 8).map(([category, count]) => (
              <div key={category} className="flex items-center justify-between p-2 hover:bg-gray-50 rounded">
                <span className="text-gray-800 capitalize font-medium">{category}</span>
                <span className="font-bold text-gray-900 bg-primary-100 px-3 py-1 rounded-full">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
