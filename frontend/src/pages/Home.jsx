import { Link } from 'react-router-dom'
import { ScanBarcode, ShoppingCart, BarChart3, MapPin, Leaf, TrendingDown, Globe } from 'lucide-react'

const Home = () => {
  const features = [
    {
      icon: ScanBarcode,
      title: 'Escanear Productos',
      description: 'Escanea códigos de barras para obtener información de sostenibilidad al instante',
      link: '/scanner',
      color: 'bg-blue-500'
    },
    {
      icon: ShoppingCart,
      title: 'Listas Inteligentes',
      description: 'Crea y optimiza listas de compras basadas en presupuesto y sostenibilidad',
      link: '/shopping-list',
      color: 'bg-green-500'
    },
    {
      icon: BarChart3,
      title: 'Dashboard de Impacto',
      description: 'Visualiza tu impacto ambiental y ahorros en tiempo real',
      link: '/dashboard',
      color: 'bg-purple-500'
    },
    {
      icon: MapPin,
      title: 'Mapa de Tiendas',
      description: 'Encuentra tiendas cercanas y optimiza tu ruta de compras',
      link: '/stores',
      color: 'bg-red-500'
    },
  ]
  
  const stats = [
    { label: 'Productos Analizados', value: '15+', icon: Leaf },
    { label: 'Ahorro Promedio', value: '15%', icon: TrendingDown },
    { label: 'CO₂ Reducido', value: '2.5kg', icon: Globe },
  ]
  
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center space-y-6">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-primary-100 rounded-full">
          <Leaf className="h-10 w-10 text-primary-600" />
        </div>
        
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900">
          Compra Inteligente,
          <span className="text-primary-600"> Vive Sostenible</span>
        </h1>
        
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          LiquiVerde te ayuda a ahorrar dinero mientras tomas decisiones de compra más sostenibles.
          Optimiza tu presupuesto y reduce tu impacto ambiental.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/scanner" className="btn-primary inline-flex items-center justify-center space-x-2">
            <ScanBarcode className="h-5 w-5" />
            <span>Escanear Producto</span>
          </Link>
          
          <Link to="/shopping-list" className="btn-secondary inline-flex items-center justify-center space-x-2">
            <ShoppingCart className="h-5 w-5" />
            <span>Crear Lista</span>
          </Link>
        </div>
      </section>
      
      {/* Stats Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon
          return (
            <div key={index} className="card text-center">
              <Icon className="h-8 w-8 text-primary-600 mx-auto mb-3" />
              <div className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</div>
              <div className="text-sm text-gray-600">{stat.label}</div>
            </div>
          )
        })}
      </section>
      
      {/* Features Grid */}
      <section className="space-y-6">
        <h2 className="text-3xl font-bold text-gray-900 text-center">
          Funcionalidades Principales
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <Link
                key={index}
                to={feature.link}
                className="card hover:shadow-lg transition-shadow duration-200 group"
              >
                <div className={`inline-flex items-center justify-center w-12 h-12 ${feature.color} rounded-lg mb-4 group-hover:scale-110 transition-transform`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </Link>
            )
          })}
        </div>
      </section>
      
      {/* How It Works */}
      <section className="card bg-gradient-to-r from-primary-50 to-green-50">
        <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">
          ¿Cómo Funciona?
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
              1
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Escanea o Busca</h3>
            <p className="text-gray-600 text-sm">
              Escanea productos o busca en nuestro catálogo para ver información de sostenibilidad
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
              2
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Optimiza tu Lista</h3>
            <p className="text-gray-600 text-sm">
              Nuestro algoritmo optimiza tu lista de compras según presupuesto y sostenibilidad
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
              3
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Ahorra y Cuida el Planeta</h3>
            <p className="text-gray-600 text-sm">
              Visualiza tu impacto y ahorra dinero mientras reduces tu huella de carbono
            </p>
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="card bg-primary-600 text-white text-center">
        <h2 className="text-3xl font-bold mb-4">
          ¿Listo para Empezar?
        </h2>
        <p className="text-lg mb-6 opacity-90">
          Comienza a hacer compras más inteligentes y sostenibles hoy mismo
        </p>
        <Link to="/scanner" className="inline-block bg-white text-primary-600 font-semibold py-3 px-8 rounded-lg hover:bg-gray-100 transition-colors">
          Escanear Mi Primer Producto
        </Link>
      </section>
    </div>
  )
}

export default Home
