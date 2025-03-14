# app/routers/partidos.py
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Partido

router = APIRouter()

@router.get("/partidos", response_model=list[Partido], tags=["partidos"])
async def list_partidos(session: SessionDep):
    partidos = session.exec(select(Partido)).all()
    return partidos

@router.post("/partidos", response_model=Partido, status_code=status.HTTP_201_CREATED, tags=["partidos"])
async def create_partido(partido: Partido, session: SessionDep):
    # Normalizar el nombre (eliminar espacios adicionales)
    partido.nombre = partido.nombre.strip()
    # Verificar si ya existe (ignorando mayúsculas/minúsculas)
    existing = session.exec(select(Partido).where(Partido.nombre.ilike(partido.nombre))).first()
    if existing:
        raise HTTPException(status_code=400, detail="El partido ya existe")
    session.add(partido)
    session.commit()
    session.refresh(partido)
    return partido

@router.patch("/partidos/{partido_id}", response_model=Partido, tags=["partidos"])
async def update_partido(partido_id: int, partido_data: Partido, session: SessionDep):
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    for key, value in partido_data.dict(exclude_unset=True).items():
        setattr(partido, key, value)
    session.add(partido)
    session.commit()
    session.refresh(partido)
    return partido

@router.delete("/partidos/{partido_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["partidos"])
async def delete_partido(partido_id: int, session: SessionDep):
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    session.delete(partido)
    session.commit()
    return {"detail": "Eliminado"}