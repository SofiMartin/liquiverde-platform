import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Scanner from './pages/Scanner'
import ShoppingList from './pages/ShoppingList'
import Dashboard from './pages/Dashboard'
import ProductComparison from './pages/ProductComparison'
import StoreMap from './pages/StoreMap'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/scanner" element={<Scanner />} />
          <Route path="/shopping-list" element={<ShoppingList />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/compare" element={<ProductComparison />} />
          <Route path="/stores" element={<StoreMap />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
