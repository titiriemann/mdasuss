# MDAS USS — FastAPI CRUD Librería

CRUD en FastAPI para tablas **Autores** y **Libros** (MySQL). Incluye página de bienvenida en `/` y
subrutas en `/crudlibreria` (creación de autor si no existe, búsqueda LIKE por libro/autor, update por ID y borrado de libro).

## Estructura

```
app/
  main.py           # app principal y landing
  database.py       # conexión MySQL vía SQLAlchemy + PyMySQL
  models.py         # ORM (mapea 'año_publicacion' -> anio_publicacion)
  schemas.py        # Pydantic v2
  routers/
    libreria.py     # Endpoints /crudlibreria/*
requirements.txt
Dockerfile
.env                # credenciales (ya configuradas)
```

> Nota: El campo **año_publicacion** de MySQL se mapea como `anio_publicacion` en Python.

## Variables de entorno

Se leen desde `.env`:

```
DB_HOST=151.106.97.118
DB_USER=u549055514_ALUMNOS
DB_PASSWORD=xxxxxxxxxxxxxx
DB_NAME=u549055514_2024_MDAS_USS
```

## Cómo correr localmente

```bash
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8023
```

- Swagger: http://localhost:8023/docs
- ReDoc:   http://localhost:8023/redoc

## Endpoints (prefijo `/crudlibreria`)

- `POST  /crudlibreria/crearlibro`
  ```json
  {
    "titulo": "El Quijote",
    "autor_nombre": "Miguel",
    "autor_apellido": "de Cervantes",
    "nacionalidad": "Española",
    "anio_publicacion": 1605,
    "precio": 10.50
  }
  ```

- `GET   /crudlibreria/buscarlibro?q=quij`
- `PUT   /crudlibreria/actualizarlibro/{libro_id}` con body:
  ```json
  { "titulo": "Nuevo título", "anio_publicacion": 2024 }
  ```
- `DELETE /crudlibreria/borrarlibro/{libro_id}`

## Deploy con Docker (recomendado)

```bash
docker build -t mdasuss-crudlibreria:latest .
docker run -d --name mdasuss-crudlibreria -p 8023:8023 --env-file .env mdasuss-crudlibreria:latest
```

Luego apunta tu reverse-proxy/Nginx a `http://localhost:8023` para el dominio `https://mdasuss.semilla42.com`.

### Nginx (ejemplo con path `/`)

```nginx
server {
  server_name mdasuss.semilla42.com;
  listen 80;
  location / {
    proxy_pass http://127.0.0.1:8023;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

> Como los endpoints están en `/crudlibreria/*`, no necesitas reglas especiales de subpath: accede a `https://mdasuss.semilla42.com/crudlibreria/...`

## Deploy con Coolify/Portainer

- Crea una nueva app tipo Dockerfile apuntando a este repo.
- Configura las variables de entorno (o carga `.env`).
- Publica el puerto 8023.
- Asigna el dominio `mdasuss.semilla42.com` (root) o el que corresponda.

---

Hecho con ❤️ para la asignatura MDAS USS.
