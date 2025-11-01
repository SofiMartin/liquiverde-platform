import { useState } from 'react'
import { ScanBarcode, Search, Loader2, AlertCircle, CheckCircle2, Leaf } from 'lucide-react'
import { productsAPI } from '../services/api'

const Scanner = () => {
  const [barcode, setBarcode] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [product, setProduct] = useState(null)
  const [error, setError] = useState(null)
  const [searchResults, setSearchResults] = useState([])
  
  const handleScan = async (e) => {
    e.preventDefault()
    if (!barcode.trim()) return
    
    setLoading(true)
    setError(null)
    setProduct(null)
    
    try {
      const response = await productsAPI.scanBarcode(barcode)
      setProduct(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Producto no encontrado')
    } finally {
      setLoading(false)
    }
  }
  
  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return
    
    setLoading(true)
    setError(null)
    setSearchResults([])
    
    try {
      const response = await productsAPI.search({ query: searchQuery, limit: 10 })
      setSearchResults(response.data)
      
      if (response.data.length === 0) {
        setError('No se encontraron productos')
      }
    } catch (err) {
      setError('Error al buscar productos')
    } finally {
      setLoading(false)
    }
  }
  
  const selectProduct = (selectedProduct) => {
    setProduct(selectedProduct)
    setSearchResults([])
    setSearchQuery('')
  }
  
  const getSustainabilityColor = (score) => {
    if (score >= 70) return 'text-green-600 bg-green-100'
    if (score >= 50) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }
  
  const getSustainabilityLabel = (score) => {
    if (score >= 70) return 'Excelente'
    if (score >= 50) return 'Bueno'
    return 'Mejorable'
  }
  
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-900">Escanear Producto</h1>
        <p className="text-gray-600">Escanea un código de barras o busca un producto</p>
      </div>
      
      {/* Scanner Form */}
      <div className="card">
        <form onSubmit={handleScan} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Código de Barras
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={barcode}
                onChange={(e) => setBarcode(e.target.value)}
                placeholder="Ej: 7804123456789"
                className="input flex-1"
              />
              <button
                type="submit"
                disabled={loading}
                className="btn-primary flex items-center space-x-2"
              >
                {loading ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <ScanBarcode className="h-5 w-5" />
                )}
                <span>Escanear</span>
              </button>
            </div>
          </div>
        </form>
      </div>
      
      {/* Search Form */}
      <div className="card">
        <form onSubmit={handleSearch} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Buscar Producto
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Ej: Leche orgánica"
                className="input flex-1"
              />
              <button
                type="submit"
                disabled={loading}
                className="btn-primary flex items-center space-x-2"
              >
                {loading ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <Search className="h-5 w-5" />
                )}
                <span>Buscar</span>
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* Available Barcodes */}
      <div className="card bg-blue-50 border-2 border-blue-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center space-x-2">
          <ScanBarcode className="h-5 w-5 text-blue-600" />
          <span>Códigos de Barras Disponibles</span>
        </h3>
        <p className="text-sm text-gray-700 mb-4">Prueba escaneando estos códigos para ver productos de ejemplo:</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="bg-white rounded-lg p-3 border border-blue-100">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium text-gray-900">Lentejas Orgánicas</p>
                <p className="text-sm text-gray-600">Código: <code className="bg-gray-100 px-2 py-1 rounded">7804123456797</code></p>
              </div>
              <button onClick={() => setBarcode('7804123456797')} className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                Usar
              </button>
            </div>
          </div>
          <div className="bg-white rounded-lg p-3 border border-blue-100">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium text-gray-900">Arroz Integral Orgánico</p>
                <p className="text-sm text-gray-600">Código: <code className="bg-gray-100 px-2 py-1 rounded">7804123456796</code></p>
              </div>
              <button onClick={() => setBarcode('7804123456796')} className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                Usar
              </button>
            </div>
          </div>
          <div className="bg-white rounded-lg p-3 border border-blue-100">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium text-gray-900">Pasta Integral</p>
                <p className="text-sm text-gray-600">Código: <code className="bg-gray-100 px-2 py-1 rounded">7804123456803</code></p>
              </div>
              <button onClick={() => setBarcode('7804123456803')} className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                Usar
              </button>
            </div>
          </div>
          <div className="bg-white rounded-lg p-3 border border-blue-100">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium text-gray-900">Pechuga de Pollo Orgánica</p>
                <p className="text-sm text-gray-600">Código: <code className="bg-gray-100 px-2 py-1 rounded">7804123456789</code></p>
              </div>
              <button onClick={() => setBarcode('7804123456789')} className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                Usar
              </button>
            </div>
          </div>
          <div className="bg-white rounded-lg p-3 border border-blue-100">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium text-gray-900">Manzanas Orgánicas</p>
                <p className="text-sm text-gray-600">Código: <code className="bg-gray-100 px-2 py-1 rounded">7804123456793</code></p>
              </div>
              <button onClick={() => setBarcode('7804123456793')} className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                Usar
              </button>
            </div>
          </div>
          <div className="bg-white rounded-lg p-3 border border-blue-100">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium text-gray-900">Leche Descremada Orgánica</p>
                <p className="text-sm text-gray-600">Código: <code className="bg-gray-100 px-2 py-1 rounded">7804123456791</code></p>
              </div>
              <button onClick={() => setBarcode('7804123456791')} className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                Usar
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3">
          <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-red-900">Error</h3>
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      )}
      
      {/* Search Results */}
      {searchResults.length > 0 && (
        <div className="card space-y-3">
          <h3 className="font-semibold text-gray-900">Resultados de Búsqueda</h3>
          <div className="space-y-2">
            {searchResults.map((result) => (
              <button
                key={result.id}
                onClick={() => selectProduct(result)}
                className="w-full text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-gray-900">{result.name}</div>
                    <div className="text-sm text-gray-600">{result.brand} - {result.category}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold text-gray-900">${result.price}</div>
                    {result.sustainability_score && (
                      <div className="text-xs text-gray-600">
                        Score: {result.sustainability_score.overall_score.toFixed(0)}
                      </div>
                    )}
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
      
      {/* Product Details */}
      {product && (
        <div className="card space-y-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">{product.name}</h2>
              <div className="flex flex-wrap gap-2 text-sm text-gray-600">
                {product.brand && <span>Marca: {product.brand}</span>}
                <span>•</span>
                <span>Categoría: {product.category}</span>
                {product.origin_country && (
                  <>
                    <span>•</span>
                    <span>Origen: {product.origin_country}</span>
                  </>
                )}
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-primary-600">${product.price}</div>
              <div className="text-sm text-gray-600">por {product.unit}</div>
            </div>
          </div>
          
          {product.description && (
            <p className="text-gray-700">{product.description}</p>
          )}
          
          {/* Sustainability Score */}
          {product.sustainability_score && (
            <div className="space-y-4">
              <h3 className="font-semibold text-gray-900 flex items-center space-x-2">
                <Leaf className="h-5 w-5 text-primary-600" />
                <span>Puntuación de Sostenibilidad</span>
              </h3>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className={`text-2xl font-bold rounded-lg py-2 ${getSustainabilityColor(product.sustainability_score.overall_score)}`}>
                    {product.sustainability_score.overall_score.toFixed(0)}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">General</div>
                  <div className="text-xs text-gray-500">
                    {getSustainabilityLabel(product.sustainability_score.overall_score)}
                  </div>
                </div>
                
                <div className="text-center">
                  <div className={`text-2xl font-bold rounded-lg py-2 ${getSustainabilityColor(product.sustainability_score.economic_score)}`}>
                    {product.sustainability_score.economic_score.toFixed(0)}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Económico</div>
                </div>
                
                <div className="text-center">
                  <div className={`text-2xl font-bold rounded-lg py-2 ${getSustainabilityColor(product.sustainability_score.environmental_score)}`}>
                    {product.sustainability_score.environmental_score.toFixed(0)}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Ambiental</div>
                </div>
                
                <div className="text-center">
                  <div className={`text-2xl font-bold rounded-lg py-2 ${getSustainabilityColor(product.sustainability_score.social_score)}`}>
                    {product.sustainability_score.social_score.toFixed(0)}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Social</div>
                </div>
              </div>
              
              {product.sustainability_score.carbon_footprint && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-blue-900">Huella de Carbono</span>
                    <span className="text-lg font-bold text-blue-900">
                      {product.sustainability_score.carbon_footprint.toFixed(2)} kg CO₂
                    </span>
                  </div>
                </div>
              )}
            </div>
          )}
          
          {/* Labels */}
          {product.labels && product.labels.length > 0 && (
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Certificaciones</h3>
              <div className="flex flex-wrap gap-2">
                {product.labels.map((label, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800"
                  >
                    <CheckCircle2 className="h-4 w-4 mr-1" />
                    {label}
                  </span>
                ))}
              </div>
            </div>
          )}
          
          {/* Nutritional Info */}
          {product.nutritional_info && (
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Información Nutricional (por 100g/ml)</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {product.nutritional_info.energy_kcal && (
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600">Energía</div>
                    <div className="font-semibold">{product.nutritional_info.energy_kcal} kcal</div>
                  </div>
                )}
                {product.nutritional_info.proteins && (
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600">Proteínas</div>
                    <div className="font-semibold">{product.nutritional_info.proteins}g</div>
                  </div>
                )}
                {product.nutritional_info.carbohydrates && (
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600">Carbohidratos</div>
                    <div className="font-semibold">{product.nutritional_info.carbohydrates}g</div>
                  </div>
                )}
                {product.nutritional_info.fats && (
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600">Grasas</div>
                    <div className="font-semibold">{product.nutritional_info.fats}g</div>
                  </div>
                )}
                {product.nutritional_info.fiber && (
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600">Fibra</div>
                    <div className="font-semibold">{product.nutritional_info.fiber}g</div>
                  </div>
                )}
                {product.nutritional_info.sodium && (
                  <div className="bg-gray-50 rounded-lg p-3">
                    <div className="text-sm text-gray-600">Sodio</div>
                    <div className="font-semibold">{(product.nutritional_info.sodium * 1000).toFixed(0)}mg</div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Scanner
