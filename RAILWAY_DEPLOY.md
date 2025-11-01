# 🚂 Despliegue en Railway

Guía paso a paso para desplegar LiquiVerde Platform en Railway.

## 📋 Prerrequisitos

- Cuenta en [Railway.app](https://railway.app/)
- Cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (gratis)
- Repositorio en GitHub

## 🚀 Pasos de Despliegue

### 1. Preparar MongoDB Atlas

1. Ir a https://www.mongodb.com/cloud/atlas
2. Crear cuenta gratuita
3. Crear un nuevo cluster (M0 Free)
4. En "Database Access", crear un usuario:
   - Username: `liquiverde`
   - Password: (generar una segura)
5. En "Network Access", agregar: `0.0.0.0/0` (permitir desde cualquier IP)
6. Obtener connection string:
   - Click en "Connect" → "Connect your application"
   - Copiar el string: `mongodb+srv://liquiverde:<password>@cluster0.xxxxx.mongodb.net/`

### 2. Desplegar en Railway

#### Opción A: Desde GitHub (Recomendado)

1. Ir a https://railway.app/
2. Click en "Start a New Project"
3. Seleccionar "Deploy from GitHub repo"
4. Autorizar Railway a acceder a tu GitHub
5. Seleccionar el repositorio: `SofiMartin/liquiverde-platform`
6. Railway detectará automáticamente el `docker-compose.yml`

#### Opción B: Servicios Separados

**Backend:**
1. New Project → Deploy from GitHub
2. Seleccionar repositorio
3. Root Directory: `/backend`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Frontend:**
1. Add Service → Deploy from GitHub
2. Seleccionar mismo repositorio
3. Root Directory: `/frontend`
4. Build Command: `npm install && npm run build`
5. Start Command: `npm run preview -- --port $PORT --host 0.0.0.0`

**MongoDB:**
1. Add Service → Database → Add MongoDB
2. Railway creará una instancia automáticamente

### 3. Configurar Variables de Entorno

En el servicio **Backend**, agregar:

```env
MONGODB_URL=mongodb+srv://liquiverde:<password>@cluster0.xxxxx.mongodb.net/
DATABASE_NAME=liquiverde
PORT=8000
ENVIRONMENT=production
```

En el servicio **Frontend**, agregar:

```env
VITE_API_URL=https://tu-backend.railway.app
```

### 4. Obtener URLs

Después del despliegue:
- Backend: `https://liquiverde-backend.up.railway.app`
- Frontend: `https://liquiverde-frontend.up.railway.app`

### 5. Cargar Datos Iniciales

Ejecutar el seeder desde Railway CLI:

```bash
railway run python -m app.services.seed_data
```

O hacer una petición POST a:
```
https://tu-backend.railway.app/api/seed
```

## 🔧 Configuración Adicional

### Dominio Personalizado

1. En Railway, ir a Settings del servicio
2. Click en "Generate Domain" o "Custom Domain"
3. Agregar tu dominio personalizado

### Monitoreo

Railway proporciona:
- Logs en tiempo real
- Métricas de uso
- Alertas de errores

## 📊 Costos

- **Free Tier**: $5 de crédito mensual
- Suficiente para:
  - Backend: ~$3/mes
  - Frontend: ~$1/mes
  - Total: ~$4/mes (dentro del free tier)

## 🐛 Troubleshooting

### Error: "Application failed to respond"
- Verificar que el PORT esté configurado correctamente
- Revisar logs: `railway logs`

### Error: "MongoDB connection failed"
- Verificar connection string
- Verificar que la IP esté permitida en MongoDB Atlas

### Error: "Build failed"
- Verificar que todas las dependencias estén en requirements.txt
- Revisar logs de build

## 📝 Comandos Útiles

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Ver logs
railway logs

# Ejecutar comandos
railway run <comando>

# Abrir dashboard
railway open
```

## 🔄 Actualizar Despliegue

Railway se actualiza automáticamente con cada push a GitHub:

```bash
git add .
git commit -m "Update"
git push origin main
```

Railway detectará el cambio y redesplegar automáticamente.

## ✅ Verificar Despliegue

1. Frontend: Abrir URL del frontend
2. Backend: Visitar `https://tu-backend.railway.app/docs`
3. Health Check: `https://tu-backend.railway.app/health`

---

**¡Listo!** Tu aplicación está desplegada en Railway 🎉
