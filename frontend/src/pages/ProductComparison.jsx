import { useState, useEffect } from 'react'
import { GitCompare, Search } from 'lucide-react'
import { productsAPI } from '../services/api'

const ProductComparison = () => {
  const [products, setProducts] = useState([])
  const [product1, setProduct1] = useState(null)
  const [product2, setProduct2] = useState(null)
  const [comparison, setComparison] = useState(null)
  
  useEffect(() => {
    loadProducts()
  }, [])
  
  const loadProducts = async () => {
    try {
      const response = await productsAPI.list(50)
      setProducts(response.data)
    } catch (error) {
      console.error('Error:', error)
    }
  }
  
  const compareProducts = async () => {
    if (!product1 || !product2) return
    
    try {
      const response = await productsAPI.compare(product1.id, product2.id)
      setComparison(response.data)
    } catch (error) {
      console.error('Error:', error)
    }
  }
  
  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Comparar Productos</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="font-semibold mb-3 text-gray-900 text-lg">Producto 1</h3>
          <select
            onChange={(e) => setProduct1(products.find(p => p.id === e.target.value))}
            className="input"
          >
            <option value="">Seleccionar producto</option>
            {products.map(p => (
              <option key={p.id} value={p.id}>{p.name} - ${p.price}</option>
            ))}
          </select>
        </div>
        
        <div className="card">
          <h3 className="font-semibold mb-3 text-gray-900 text-lg">Producto 2</h3>
          <select
            onChange={(e) => setProduct2(products.find(p => p.id === e.target.value))}
            className="input"
          >
            <option value="">Seleccionar producto</option>
            {products.map(p => (
              <option key={p.id} value={p.id}>{p.name} - ${p.price}</option>
            ))}
          </select>
        </div>
      </div>
      
      <button
        onClick={compareProducts}
        disabled={!product1 || !product2}
        className="btn-primary w-full flex items-center justify-center space-x-2"
      >
        <GitCompare className="h-5 w-5" />
        <span>Comparar</span>
      </button>
      
      {comparison && (
        <div className="card bg-white border-2 border-primary-200">
          <h2 className="text-2xl font-bold mb-6 text-gray-900">Resultado de Comparación</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h3 className="font-semibold mb-3 text-gray-900 text-lg">{comparison.product1.name}</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-700 font-medium">Precio:</span>
                  <span className="font-bold text-gray-900">${comparison.product1.price}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700 font-medium">Sostenibilidad:</span>
                  <span className="font-bold text-primary-600">{comparison.comparison.product1_scores.overall_score.toFixed(0)}/100</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700 font-medium">Huella CO₂:</span>
                  <span className="font-bold text-gray-900">{comparison.comparison.product1_scores.carbon_footprint.toFixed(2)} kg</span>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h3 className="font-semibold mb-3 text-gray-900 text-lg">{comparison.product2.name}</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-700 font-medium">Precio:</span>
                  <span className="font-bold text-gray-900">${comparison.product2.price}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700 font-medium">Sostenibilidad:</span>
                  <span className="font-bold text-primary-600">{comparison.comparison.product2_scores.overall_score.toFixed(0)}/100</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700 font-medium">Huella CO₂:</span>
                  <span className="font-bold text-gray-900">{comparison.comparison.product2_scores.carbon_footprint.toFixed(2)} kg</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-primary-50 rounded-lg p-4 border-2 border-primary-300">
            <h3 className="font-semibold mb-2 text-gray-900 text-lg">💡 Recomendación</h3>
            <p className="text-gray-800 font-medium">{comparison.comparison.recommendation}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProductComparison
