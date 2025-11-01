import { useState, useEffect } from 'react'
import { Plus, Trash2, Sparkles, Loader2, DollarSign, Leaf } from 'lucide-react'
import { productsAPI, shoppingListsAPI } from '../services/api'

const ShoppingList = () => {
  const [products, setProducts] = useState([])
  const [selectedProducts, setSelectedProducts] = useState([])
  const [maxBudget, setMaxBudget] = useState(50000)
  const [optimizing, setOptimizing] = useState(false)
  const [optimizedResult, setOptimizedResult] = useState(null)
  
  useEffect(() => {
    const controller = new AbortController()
    loadProducts(controller.signal)
    return () => controller.abort()
  }, [])
  
  const loadProducts = async () => {
    try {
      const response = await productsAPI.list(50)
      setProducts(response.data)
    } catch (error) {
      console.error('Error loading products:', error)
    }
  }
  
  const addProduct = (product) => {
    if (!selectedProducts.find(p => p.id === product.id)) {
      setSelectedProducts([...selectedProducts, { ...product, quantity: 1, priority: 3 }])
    }
  }
  
  const removeProduct = (productId) => {
    setSelectedProducts(selectedProducts.filter(p => p.id !== productId))
  }
  
  const updateQuantity = (productId, quantity) => {
    setSelectedProducts(selectedProducts.map(p => 
      p.id === productId ? { ...p, quantity: Math.max(1, quantity) } : p
    ))
  }
  
  const optimizeList = async () => {
    if (selectedProducts.length === 0) return
    
    setOptimizing(true)
    try {
      const response = await shoppingListsAPI.quickOptimize({
        product_ids: selectedProducts.map(p => p.id),
        max_budget: maxBudget,
        prioritize_sustainability: true
      })
      setOptimizedResult(response.data)
    } catch (error) {
      console.error('Error optimizing:', error)
      alert('Error al optimizar la lista. Por favor intenta de nuevo.')
    } finally {
      setOptimizing(false)
    }
  }
  
  const totalCost = selectedProducts.reduce((sum, p) => sum + (p.price * p.quantity), 0)
  
  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Lista de Compras Inteligente</h1>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Product Selection */}
        <div className="space-y-4">
          <div className="card border-2 border-primary-200">
            <h2 className="text-xl font-bold mb-4 text-gray-900">🛒 Productos Disponibles</h2>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {products.map(product => (
                <div key={product.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-primary-50">
                  <div className="flex-1">
                    <div className="font-semibold text-gray-900">{product.name}</div>
                    <div className="text-sm text-gray-700 font-medium">${product.price}</div>
                  </div>
                  <button
                    onClick={() => addProduct(product)}
                    className="btn-primary text-sm py-1 px-3"
                  >
                    <Plus className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Selected Products */}
        <div className="space-y-4">
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Mi Lista ({selectedProducts.length})</h2>
            
            {selectedProducts.length === 0 ? (
              <p className="text-gray-500 text-center py-8">Agrega productos a tu lista</p>
            ) : (
              <div className="space-y-3">
                {selectedProducts.map(product => (
                  <div key={product.id} className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg">
                    <div className="flex-1">
                      <div className="font-medium">{product.name}</div>
                      <div className="text-sm text-gray-600">${product.price} × {product.quantity} = ${(product.price * product.quantity).toFixed(0)}</div>
                    </div>
                    <input
                      type="number"
                      min="1"
                      value={product.quantity}
                      onChange={(e) => updateQuantity(product.id, parseInt(e.target.value))}
                      className="w-16 px-2 py-1 border border-gray-300 rounded"
                    />
                    <button
                      onClick={() => removeProduct(product.id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-5 w-5" />
                    </button>
                  </div>
                ))}
                
                <div className="border-t pt-3 mt-3">
                  <div className="flex justify-between items-center font-semibold">
                    <span>Total:</span>
                    <span className="text-xl">${totalCost.toFixed(0)}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* Optimization */}
          <div className="card">
            <h3 className="font-semibold mb-3 text-gray-900">Optimizar Lista</h3>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Presupuesto Máximo
                </label>
                <input
                  type="number"
                  value={maxBudget}
                  onChange={(e) => setMaxBudget(parseInt(e.target.value))}
                  className="input"
                  min="1000"
                  step="1000"
                />
              </div>
              
              <button
                onClick={optimizeList}
                disabled={optimizing || selectedProducts.length === 0}
                className="btn-primary w-full flex items-center justify-center space-x-2"
              >
                {optimizing ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <Sparkles className="h-5 w-5" />
                )}
                <span>Optimizar Lista</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Optimized Result */}
      {optimizedResult && (
        <div className="card bg-gradient-to-r from-primary-50 to-green-50">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center space-x-2">
            <Sparkles className="h-6 w-6 text-primary-600" />
            <span>Lista Optimizada</span>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-center space-x-2 text-primary-600 mb-1">
                <DollarSign className="h-5 w-5" />
                <span className="text-sm font-medium">Costo Total</span>
              </div>
              <div className="text-2xl font-bold">${optimizedResult.stats.total_cost}</div>
              <div className="text-sm text-gray-600">
                Presupuesto restante: ${optimizedResult.stats.budget_remaining}
              </div>
            </div>
            
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-center space-x-2 text-green-600 mb-1">
                <Leaf className="h-5 w-5" />
                <span className="text-sm font-medium">Sostenibilidad</span>
              </div>
              <div className="text-2xl font-bold">{optimizedResult.stats.average_sustainability}/100</div>
              <div className="text-sm text-gray-600">Puntuación promedio</div>
            </div>
            
            <div className="bg-white rounded-lg p-4">
              <div className="text-sm font-medium text-gray-600 mb-1">Productos</div>
              <div className="text-2xl font-bold">{optimizedResult.stats.items_selected}</div>
              <div className="text-sm text-gray-600">
                {optimizedResult.stats.total_items} unidades totales
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg p-4">
            <h3 className="font-semibold mb-3">Productos Seleccionados</h3>
            <div className="space-y-2">
              {optimizedResult.selected_products.map((item, index) => (
                <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
                  <div>
                    <div className="font-medium">{item.product.name}</div>
                    <div className="text-sm text-gray-600">Cantidad: {item.quantity}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold">${item.subtotal.toFixed(0)}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ShoppingList
