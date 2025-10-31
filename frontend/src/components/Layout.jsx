import { Link, useLocation } from 'react-router-dom'
import { Home, ScanBarcode, ShoppingCart, BarChart3, GitCompare, MapPin, Leaf } from 'lucide-react'

const Layout = ({ children }) => {
  const location = useLocation()
  
  const navigation = [
    { name: 'Inicio', path: '/', icon: Home },
    { name: 'Escanear', path: '/scanner', icon: ScanBarcode },
    { name: 'Lista de Compras', path: '/shopping-list', icon: ShoppingCart },
    { name: 'Dashboard', path: '/dashboard', icon: BarChart3 },
    { name: 'Comparar', path: '/compare', icon: GitCompare },
    { name: 'Tiendas', path: '/stores', icon: MapPin },
  ]
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <Leaf className="h-8 w-8 text-primary-600" />
              <span className="text-2xl font-bold text-gray-900">
                Liqui<span className="text-primary-600">Verde</span>
              </span>
            </Link>
            
            <nav className="hidden md:flex space-x-1">
              {navigation.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-primary-100 text-primary-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span className="font-medium">{item.name}</span>
                  </Link>
                )
              })}
            </nav>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      
      {/* Mobile Navigation */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
        <div className="grid grid-cols-6 gap-1">
          {navigation.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex flex-col items-center justify-center py-2 ${
                  isActive ? 'text-primary-600' : 'text-gray-600'
                }`}
              >
                <Icon className="h-6 w-6" />
                <span className="text-xs mt-1">{item.name.split(' ')[0]}</span>
              </Link>
            )
          })}
        </div>
      </nav>
      
      {/* Bottom padding for mobile nav */}
      <div className="h-20 md:hidden"></div>
    </div>
  )
}

export default Layout
