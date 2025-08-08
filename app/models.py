from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey

Base = declarative_base()

class Autor(Base):
    __tablename__ = "Autores"
    autor_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    nacionalidad = Column(String(100))

    libros = relationship("Libro", back_populates="autor")

class Libro(Base):
    __tablename__ = "Libros"
    libro_id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=True)
    autor_id = Column(Integer, ForeignKey("Autores.autor_id"))
    anio_publicacion = Column("año_publicacion", Integer, nullable=True)
    precio = Column(DECIMAL(10,2), nullable=True)

    autor = relationship("Autor", back_populates="libros")
