# app/routers/financiamiento_partidos.py
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from db import SessionDep
from models import FinanciamientoPartido

router = APIRouter()

@router.post("/financiamiento/partidos", response_model=FinanciamientoPartido, status_code=status.HTTP_201_CREATED, tags=["financiamiento_partidos"])
async def create_financiamiento_partido(data: FinanciamientoPartido, session: SessionDep):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

@router.get("/financiamiento/partidos/{record_id}", response_model=FinanciamientoPartido, tags=["financiamiento_partidos"])
async def read_financiamiento_partido(record_id: int, session: SessionDep):
    record = session.get(FinanciamientoPartido, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record

@router.patch("/financiamiento/partidos/{record_id}", response_model=FinanciamientoPartido, tags=["financiamiento_partidos"])
async def update_financiamiento_partido(record_id: int, data: FinanciamientoPartido, session: SessionDep):
    record = session.get(FinanciamientoPartido, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

@router.delete("/financiamiento/partidos/{record_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["financiamiento_partidos"])
async def delete_financiamiento_partido(record_id: int, session: SessionDep):
    record = session.get(FinanciamientoPartido, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(record)
    session.commit()
    return {"detail": "Eliminado"}

@router.get("/financiamiento/partidos", response_model=list[FinanciamientoPartido], tags=["financiamiento_partidos"])
async def list_financiamiento_partidos(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Cantidad de registros a mostrar")
):
    records = session.exec(select(FinanciamientoPartido).offset(skip).limit(limit)).all()
    return records