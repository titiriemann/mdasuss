from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from ..database import get_db
from ..models import Autor, Libro
from ..schemas import LibroCreate, LibroUpdate, LibroOut

router = APIRouter(prefix="/crudlibreria", tags=["crudlibreria"])

@router.get("/", summary="Índice CRUD Librería")
def index():
    return {
        "endpoints": {
            "crear": "/crudlibreria/crearlibro",
            "buscar": "/crudlibreria/buscarlibro?q=texto",
            "actualizar": "/crudlibreria/actualizarlibro/{libro_id}",
            "borrar": "/crudlibreria/borrarlibro/{libro_id}",
        }
    }

@router.get("/ping")
def ping():
    return {"status":"ok"}

@router.post("/crearlibro", response_model=LibroOut, summary="Crea autor (si no existe) y libro")
def crear_libro(payload: LibroCreate, db: Session = Depends(get_db)):
    autor = db.query(Autor).filter(
        func.lower(Autor.nombre) == payload.autor_nombre.lower(),
        func.lower(Autor.apellido) == payload.autor_apellido.lower()
    ).first()

    if not autor:
        autor = Autor(
            nombre=payload.autor_nombre,
            apellido=payload.autor_apellido,
            nacionalidad=payload.nacionalidad
        )
        db.add(autor)
        db.flush()

    libro = Libro(
        titulo=payload.titulo,
        autor_id=autor.autor_id,
        anio_publicacion=payload.anio_publicacion,
        precio=payload.precio if payload.precio is not None else None
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)

    return {"id": libro.libro_id, "titulo": libro.titulo, "autor": f"{autor.nombre} {autor.apellido}"}

@router.get("/buscarlibro", response_model=List[LibroOut], summary="Busca por título o autor (LIKE)")
def buscar_libro(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    pattern = f"%{q}%"
    results = (
        db.query(
            Libro.libro_id.label("id"),
            Libro.titulo.label("titulo"),
            func.concat(func.coalesce(Autor.nombre, ""), " ", func.coalesce(Autor.apellido, "")).label("autor")
        )
        .join(Autor, Libro.autor_id == Autor.autor_id, isouter=True)
        .filter(
            or_(
                Libro.titulo.ilike(pattern),
                func.concat(Autor.nombre, " ", Autor.apellido).ilike(pattern),
                Autor.nombre.ilike(pattern),
                Autor.apellido.ilike(pattern),
            )
        )
        .order_by(Libro.libro_id.desc())
        .all()
    )

    return [ {"id": r.id, "titulo": r.titulo, "autor": r.autor.strip()} for r in results ]

@router.put("/actualizarlibro/{libro_id}", response_model=LibroOut, summary="Actualiza título o año por ID")
def actualizar_libro(libro_id: int, payload: LibroUpdate, db: Session = Depends(get_db)):
    libro = db.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    if payload.titulo is None and payload.anio_publicacion is None:
        raise HTTPException(status_code=400, detail="Debe enviar al menos un campo para actualizar (titulo o anio_publicacion)")

    if payload.titulo is not None:
        libro.titulo = payload.titulo
    if payload.anio_publicacion is not None:
        libro.anio_publicacion = payload.anio_publicacion

    db.add(libro)
    db.commit()
    db.refresh(libro)

    autor = db.get(Autor, libro.autor_id) if libro.autor_id else None
    autor_nombre = f"{autor.nombre} {autor.apellido}".strip() if autor else ""

    return {"id": libro.libro_id, "titulo": libro.titulo, "autor": autor_nombre}

@router.delete("/borrarlibro/{libro_id}", summary="Elimina solo el libro (no borra al autor)")
def borrar_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    db.delete(libro)
    db.commit()

    return {"message": f"Libro {libro_id} eliminado"}
