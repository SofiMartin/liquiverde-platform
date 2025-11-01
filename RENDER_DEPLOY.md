# 🎨 Despliegue en Render (100% Gratis)

## 📋 Prerrequisitos

1. ✅ Cuenta en [Render](https://render.com/) (gratis)
2. ✅ Cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (gratis)
3. ✅ Repositorio en GitHub

## 🚀 Paso 1: Preparar MongoDB Atlas

### 1.1 Crear Cluster (si no lo hiciste)
1. Ir a https://www.mongodb.com/cloud/atlas
2. Crear cuenta gratuita
3. Crear cluster **M0 Sandbox** (gratis)

### 1.2 Configurar Acceso
1. **Database Access**:
   - Add New Database User
   - Username: `liquiverde`
   - Password: (genera una segura y guárdala)
   - Privileges: "Read and write to any database"

2. **Network Access**:
   - Add IP Address
   - Allow Access from Anywhere: `0.0.0.0/0`

### 1.3 Obtener Connection String
1. Database → Connect → Connect your application
2. Copiar el string:
   ```
   mongodb+srv://liquiverde:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
3. Reemplazar `<password>` con tu contraseña
4. Agregar el nombre de la base de datos al final:
   ```
   mongodb+srv://liquiverde:TuPassword@cluster0.xxxxx.mongodb.net/liquiverde?retryWrites=true&w=majority
   ```

## 🎨 Paso 2: Desplegar Backend en Render

### 2.1 Crear Web Service para Backend

1. Ir a https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Conectar tu repositorio de GitHub: `SofiMartin/liquiverde-platform`
4. Configurar:

   **Configuración Básica:**
   - **Name**: `liquiverde-backend`
   - **Region**: Oregon (US West) - más cercano
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Environment**: `Docker`
   - **Dockerfile Path**: `backend/Dockerfile`

   **Plan:**
   - Seleccionar **"Free"** (0$/mes)

   **Variables de Entorno:**
   Click "Advanced" → "Add Environment Variable":
   
   ```
   MONGODB_URL = mongodb+srv://liquiverde:TuPassword@cluster0.xxxxx.mongodb.net/liquiverde?retryWrites=true&w=majority
   DATABASE_NAME = liquiverde
   PORT = 8000
   ENVIRONMENT = production
   ```

5. Click **"Create Web Service"**

### 2.2 Esperar el Deploy (5-10 minutos)

Render construirá la imagen Docker y desplegará el backend.

### 2.3 Obtener URL del Backend

Una vez desplegado, verás la URL:
```
https://liquiverde-backend.onrender.com
```

**Probar el backend**:
- API Docs: `https://liquiverde-backend.onrender.com/docs`
- Health: `https://liquiverde-backend.onrender.com/health`

## 🎨 Paso 3: Desplegar Frontend en Render

### 3.1 Crear Static Site para Frontend

1. En Render Dashboard, click **"New +"** → **"Static Site"**
2. Conectar el mismo repositorio: `SofiMartin/liquiverde-platform`
3. Configurar:

   **Configuración Básica:**
   - **Name**: `liquiverde-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

   **Variables de Entorno:**
   ```
   VITE_API_URL = https://liquiverde-backend.onrender.com
   ```
   
   ⚠️ **IMPORTANTE**: Reemplaza con la URL real de tu backend

4. Click **"Create Static Site"**

### 3.2 Esperar el Deploy (3-5 minutos)

### 3.3 Obtener URL del Frontend

Una vez desplegado:
```
https://liquiverde-frontend.onrender.com
```

## 🎯 Paso 4: Cargar Datos Iniciales

### Opción A: Desde la API

Hacer una petición POST a:
```bash
curl -X POST https://liquiverde-backend.onrender.com/api/seed
```

### Opción B: Manualmente

1. Ir a `https://liquiverde-backend.onrender.com/docs`
2. Ejecutar el endpoint de seed

## ✅ Verificar Despliegue

### Backend:
- ✅ Docs: https://liquiverde-backend.onrender.com/docs
- ✅ Health: https://liquiverde-backend.onrender.com/health
- ✅ Dashboard: https://liquiverde-backend.onrender.com/api/analysis/dashboard

### Frontend:
- ✅ Home: https://liquiverde-frontend.onrender.com
- ✅ Scanner: https://liquiverde-frontend.onrender.com/scanner
- ✅ Dashboard: https://liquiverde-frontend.onrender.com/dashboard

## ⚠️ Limitaciones del Plan Gratuito

### Backend (Web Service Free):
- ⏰ **Se duerme después de 15 minutos** de inactividad
- ⏱️ **Primera carga tarda ~30 segundos** (cold start)
- 💾 **512 MB RAM**
- ⏳ **750 horas/mes** de tiempo activo

### Frontend (Static Site):
- ✅ **Siempre activo** (no se duerme)
- ✅ **Ilimitado** en requests
- ✅ **CDN global** incluido

## 🔄 Actualizar Despliegue

Render se actualiza automáticamente con cada push a GitHub:

```bash
git add .
git commit -m "Update"
git push origin main
```

Render detecta el cambio y redespliega automáticamente (5-10 minutos).

## 🐛 Troubleshooting

### Error: "Build failed"
- Verificar que `backend/Dockerfile` existe
- Revisar logs en Render Dashboard

### Error: "Application failed to respond"
- Verificar que PORT=8000 en variables de entorno
- Verificar que el backend expone el puerto correcto

### Error: "MongoDB connection failed"
- Verificar MONGODB_URL en variables de entorno
- Verificar que 0.0.0.0/0 está permitido en MongoDB Atlas
- Verificar que la contraseña no tiene caracteres especiales sin encodear

### Frontend no conecta con Backend
- Verificar que VITE_API_URL apunta a la URL correcta del backend
- Verificar CORS en el backend (debe permitir el dominio del frontend)

### Backend se duerme (cold start)
- Es normal en el plan gratuito
- Primera petición tarda ~30 segundos
- Considera usar un servicio de "keep-alive" o actualizar a plan pagado

## 💰 Costos

- **Backend Free**: $0/mes (con limitaciones)
- **Frontend Static**: $0/mes (sin limitaciones)
- **MongoDB Atlas M0**: $0/mes
- **Total**: **$0/mes** 🎉

## 🚀 Upgrade (Opcional)

Si necesitas eliminar el cold start:

**Backend Starter Plan**: $7/mes
- Sin cold starts
- Siempre activo
- Más RAM y CPU

## 📝 Comandos Útiles

```bash
# Ver logs del backend
# En Render Dashboard → Backend Service → Logs

# Forzar redeploy
# En Render Dashboard → Manual Deploy → Deploy latest commit

# Rollback a versión anterior
# En Render Dashboard → Deploys → Select previous → Rollback
```

## 🎓 Recursos

- [Render Docs](https://render.com/docs)
- [Render Free Tier](https://render.com/docs/free)
- [MongoDB Atlas Free Tier](https://www.mongodb.com/cloud/atlas/pricing)

---

**¡Listo!** Tu aplicación está desplegada en Render 100% gratis 🎉
