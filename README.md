# 🚀 Flask API REST v2.0.0

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-orange)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **API REST profesional con CRUD completo, validación Marshmallow, SQLAlchemy y manejo robusto de errores**

Transformamos un simple endpoint `/ping` en una API de nivel empresarial con base de datos SQLite, validación de datos y respuestas JSON estandarizadas.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Endpoints](#-endpoints)
- [Ejemplos con curl](#-ejemplos-con-curl)
- [Manejo de Errores](#-manejo-de-errores)
- [Testing](#-testing)

---

## ✨ Características

| Característica | Descripción |
|----------------|-------------|
| 🔧 **CRUD Completo** | Create, Read, Update, Delete para entidades Producto |
| 🗄️ **Base de Datos** | SQLite con SQLAlchemy ORM |
| ✅ **Validación** | Marshmallow para validación y serialización |
| 📄 **Paginación** | Paginación automática con metadatos |
| 🔍 **Búsqueda** | Búsqueda por nombre y filtrado por categoría |
| 🛡️ **Errores HTTP** | Respuestas estandarizadas (400, 404, 422, 500) |
| 📊 **Estadísticas** | Endpoint de métricas del inventario |
| 🏗️ **Blueprints** | Arquitectura modular y escalable |

---

## 🛠️ Tecnologías

- **Flask 3.0.3** - Framework web ligero
- **SQLAlchemy 2.0** - ORM para base de datos
- **Flask-Marshmallow** - Validación y serialización
- **Marshmallow-SQLAlchemy** - Integración ORM
- **SQLite** - Base de datos embebida

---

## 📦 Instalación

### Requisitos

- Python 3.8+
- pip

### Pasos

```bash
# Clonar el repositorio
git clone https://github.com/JohananCruz19/simple_api_flask.git
cd simple_api_flask

# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python run.py
```

La API estará disponible en `http://localhost:5000`

---

## 🏗️ Estructura del Proyecto

```
simple_api_flask/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   └── product.py       # Product model
│   ├── schemas/             # Marshmallow schemas
│   │   ├── __init__.py
│   │   └── product_schema.py
│   └── api/                 # API blueprints
│       ├── __init__.py
│       ├── health.py        # Health check endpoints
│       └── products.py      # Product CRUD endpoints
├── config.py                # Configuration classes
├── run.py                   # Application entry point
├── requirements.txt
└── README.md
```

---

## 🌐 Endpoints

### Health Check

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/ping` | Simple ping/pong |
| GET | `/api/v1/health` | Health check completo |
| GET | `/api/v1/ready` | Readiness check (Docker/K8s) |

### Productos (CRUD)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/products` | Listar productos (con paginación) |
| GET | `/api/v1/products/<id>` | Obtener producto por ID |
| POST | `/api/v1/products` | Crear nuevo producto |
| PUT | `/api/v1/products/<id>` | Actualizar producto |
| DELETE | `/api/v1/products/<id>` | Eliminar producto (soft delete) |
| POST | `/api/v1/products/<id>/restore` | Restaurar producto eliminado |
| GET | `/api/v1/products/stats` | Estadísticas del inventario |

### Query Parameters (GET /products)

| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `page` | int | Número de página | 1 |
| `per_page` | int | Items por página (max 100) | 10 |
| `category` | string | Filtrar por categoría | - |
| `search` | string | Buscar por nombre | - |
| `sort_by` | string | Campo de ordenamiento (name, price, created_at, stock) | created_at |
| `sort_order` | string | Orden (asc, desc) | desc |

---

## 📝 Ejemplos con curl

### Health Check

```bash
# Ping simple
curl -X GET http://localhost:5000/api/v1/ping

# Respuesta:
# {"data": {"message": "pong", "version": "2.0.0"}, "meta": {"endpoint": "health.ping", "version": "2.0.0"}, "success": true}

# Health check completo
curl -X GET http://localhost:5000/api/v1/health
```

### Crear Producto (POST)

```bash
curl -X POST http://localhost:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Dell XPS 13",
    "description": "Laptop ultradelgada con pantalla InfinityEdge",
    "price": 1299.99,
    "stock": 25,
    "sku": "LAP-DEL-001",
    "category": "tecnologia"
  }'

# Respuesta exitosa (201):
# {
#   "data": {
#     "message": "Product created successfully",
#     "product": {
#       "category": "tecnologia",
#       "created_at": "2026-03-17T20:30:00",
#       "description": "Laptop ultradelgada con pantalla InfinityEdge",
#       "id": 1,
#       "is_active": true,
#       "name": "Laptop Dell XPS 13",
#       "price": 1299.99,
#       "sku": "LAP-DEL-001",
#       "stock": 25,
#       "updated_at": "2026-03-17T20:30:00"
#     }
#   },
#   "meta": {"endpoint": "products.create_product", "version": "2.0.0"},
#   "success": true
# }
```

### Listar Productos (GET)

```bash
# Listar todos (paginado)
curl -X GET http://localhost:5000/api/v1/products

# Con filtros y paginación
curl -X GET "http://localhost:5000/api/v1/products?page=1&per_page=5&category=tecnologia&sort_by=price&sort_order=desc"

# Buscar por nombre
curl -X GET "http://localhost:5000/api/v1/products?search=laptop"

# Respuesta:
# {
#   "data": {
#     "items": [...],
#     "pagination": {
#       "has_next": false,
#       "has_prev": false,
#       "page": 1,
#       "per_page": 10,
#       "total_items": 1,
#       "total_pages": 1
#     }
#   },
#   "meta": {"endpoint": "products.get_products", "version": "2.0.0"},
#   "success": true
# }
```

### Obtener Producto por ID (GET)

```bash
curl -X GET http://localhost:5000/api/v1/products/1

# Respuesta:
# {
#   "data": {
#     "category": "tecnologia",
#     "created_at": "2026-03-17T20:30:00",
#     "description": "Laptop ultradelgada...",
#     "id": 1,
#     "is_active": true,
#     "name": "Laptop Dell XPS 13",
#     "price": 1299.99,
#     "sku": "LAP-DEL-001",
#     "stock": 25,
#     "updated_at": "2026-03-17T20:30:00"
#   },
#   "meta": {"endpoint": "products.get_product", "version": "2.0.0"},
#   "success": true
# }
```

### Actualizar Producto (PUT)

```bash
curl -X PUT http://localhost:5000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 1199.99,
    "stock": 20
  }'

# Respuesta:
# {
#   "data": {
#     "message": "Product updated successfully",
#     "product": {...}
#   },
#   "meta": {...},
#   "success": true
# }
```

### Eliminar Producto (DELETE) - Soft Delete

```bash
curl -X DELETE http://localhost:5000/api/v1/products/1

# Respuesta:
# {
#   "data": {
#     "message": "Product deleted successfully",
#     "product_id": 1
#   },
#   "meta": {...},
#   "success": true
# }
```

### Restaurar Producto (POST)

```bash
curl -X POST http://localhost:5000/api/v1/products/1/restore

# Respuesta:
# {
#   "data": {
#     "message": "Product restored successfully",
#     "product": {...}
#   },
#   "meta": {...},
#   "success": true
# }
```

### Estadísticas

```bash
curl -X GET http://localhost:5000/api/v1/products/stats

# Respuesta:
# {
#   "data": {
#     "categories": [
#       {"count": 15, "name": "tecnologia"},
#       {"count": 8, "name": "hogar"}
#     ],
#     "total_inventory_value": 45678.50,
#     "total_products": 23,
#     "total_stock": 145
#   },
#   "meta": {...},
#   "success": true
# }
```

---

## ⚠️ Manejo de Errores

Todas las respuestas de error siguen el mismo formato estandarizado:

```json
{
  "success": false,
  "data": null,
  "meta": {
    "endpoint": "products.get_product",
    "version": "2.0.0"
  },
  "error": {
    "code": 404,
    "message": "Product not found",
    "details": "Product with ID 999 does not exist"
  }
}
```

### Códigos de Error

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| **400** | Bad Request | Body JSON inválido |
| **404** | Not Found | Producto no existe |
| **405** | Method Not Allowed | Método HTTP no permitido |
| **409** | Conflict | SKU duplicado |
| **422** | Unprocessable Entity | Error de validación |
| **500** | Internal Server Error | Error del servidor |

### Ejemplo Error 422 (Validación)

```bash
curl -X POST http://localhost:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "A",
    "price": -50
  }'

# Respuesta:
# {
#   "success": false,
#   "error": {
#     "code": 422,
#     "message": "Validation error",
#     "details": {
#       "name": ["Length must be between 2 and 100."],
#       "price": ["Price must be >= 0"],
#       "sku": ["Missing data for required field."]
#     }
#   }
# }
```

---

## 🧪 Testing

```bash
# Ejecutar tests con pytest
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Verbose
pytest -v
```

---

## 🚀 Despliegue

### Usando Gunicorn (Producción)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "run:app"
```

### Docker (Próximamente)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

---

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

---

## 🙏 Créditos

Desarrollado con:
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Marshmallow](https://marshmallow.readthedocs.io/)

---

<div align="center">

**¿Preguntas?** Abre un [issue](https://github.com/JohananCruz19/simple_api_flask/issues)

⭐ **Star si te fue útil!**

</div>