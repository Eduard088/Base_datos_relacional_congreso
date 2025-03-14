# app/routers/estados.py
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Estado

router = APIRouter()

@router.get("/estados", response_model=list[Estado], tags=["estados"])
async def list_estados(session: SessionDep):
    estados = session.exec(select(Estado)).all()
    return estados

@router.post("/estados", response_model=Estado, status_code=status.HTTP_201_CREATED, tags=["estados"])
async def create_estado(estado: Estado, session: SessionDep):
    # Verificar si ya existe un estado con ese id
    existing = session.exec(select(Estado).where(Estado.id == estado.id)).first()
    if existing:
        raise HTTPException(status_code=400, detail="El estado ya existe")
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

@router.patch("/estados/{estado_id}", response_model=Estado, tags=["estados"])
async def update_estado(estado_id: int, estado_data: Estado, session: SessionDep):
    estado = session.get(Estado, estado_id)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    for key, value in estado_data.dict(exclude_unset=True).items():
        setattr(estado, key, value)
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

@router.delete("/estados/{estado_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["estados"])
async def delete_estado(estado_id: int, session: SessionDep):
    estado = session.get(Estado, estado_id)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    session.delete(estado)
    session.commit()
    return {"detail": "Eliminado"}