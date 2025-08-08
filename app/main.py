from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .routers.libreria import router as libreria_router

app = FastAPI(
    title="MDAS USS - API",
    description="Servicios de ejemplo para MDAS USS. Incluye CRUD de librería bajo /crudlibreria.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(libreria_router)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    return '''
    <!doctype html>
    <html lang="es">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>MDAS USS — Servicios</title>
        <style>
          body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif; margin: 0; background: #0b1020; color: #e6e9ef;}
          .wrap { max-width: 960px; margin: 0 auto; padding: 56px 20px;}
          .card { background: #141a2f; border: 1px solid #222a46; border-radius: 16px; padding: 28px; box-shadow: 0 10px 30px rgba(0,0,0,.25); }
          h1 { font-size: 28px; margin: 0 0 8px; }
          p.lead { color: #b5c0da; margin: 0 0 18px; }
          a.btn { display: inline-block; padding: 10px 16px; border-radius: 10px; text-decoration: none; font-weight: 600; border: 1px solid #2e3863; }
          a.primary { background: #2e6ee6; border-color: #2e6ee6; color: white; }
          a.secondary { color: #c6d4ff; }
          code { background: #0f1427; padding: 2px 6px; border-radius: 6px; }
          ul { line-height: 1.8; }
        </style>
      </head>
      <body>
        <div class="wrap">
          <div class="card">
            <h1>Bienvenido a <strong>MDAS USS — API</strong></h1>
            <p class="lead">Este servicio expone un CRUD de librería bajo la ruta <code>/crudlibreria</code>.</p>
            <p>
              <a class="btn primary" href="/docs">Ver documentación (Swagger)</a>
              <a class="btn secondary" href="/redoc">ReDoc</a>
            </p>
            <h3>Rutas principales</h3>
            <ul>
              <li><code>GET /</code> — Esta página</li>
              <li><code>GET /crudlibreria/</code> — Índice de endpoints</li>
              <li><code>POST /crudlibreria/crearlibro</code></li>
              <li><code>GET /crudlibreria/buscarlibro?q=texto</code></li>
              <li><code>PUT /crudlibreria/actualizarlibro/{{libro_id}}</code></li>
              <li><code>DELETE /crudlibreria/borrarlibro/{{libro_id}}</code></li>
            </ul>
          </div>
        </div>
      </body>
    </html>
    '''

@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}
