# app/routers/diputaciones.py
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from db import SessionDep
from models import DiputacionFederal

router = APIRouter()

@router.post("/diputaciones", response_model=DiputacionFederal, status_code=status.HTTP_201_CREATED, tags=["diputaciones"])
async def create_diputacion(data: DiputacionFederal, session: SessionDep):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

@router.get("/diputaciones/{diputacion_id}", response_model=DiputacionFederal, tags=["diputaciones"])
async def read_diputacion(diputacion_id: int, session: SessionDep):
    record = session.get(DiputacionFederal, diputacion_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record

@router.patch("/diputaciones/{diputacion_id}", response_model=DiputacionFederal, tags=["diputaciones"])
async def update_diputacion(diputacion_id: int, data: DiputacionFederal, session: SessionDep):
    record = session.get(DiputacionFederal, diputacion_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

@router.delete("/diputaciones/{diputacion_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["diputaciones"])
async def delete_diputacion(diputacion_id: int, session: SessionDep):
    record = session.get(DiputacionFederal, diputacion_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(record)
    session.commit()
    return {"detail": "Eliminado"}

@router.get("/diputaciones", response_model=list[DiputacionFederal], tags=["diputaciones"])
async def list_diputaciones(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Cantidad de registros a mostrar")
):
    records = session.exec(select(DiputacionFederal).offset(skip).limit(limit)).all()
    return records