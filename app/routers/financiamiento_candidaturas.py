# app/routers/financiamiento_candidaturas.py
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from db import SessionDep
from models import FinanciamientoCandidatura

router = APIRouter()

@router.post("/financiamiento/candidaturas", response_model=FinanciamientoCandidatura, status_code=status.HTTP_201_CREATED, tags=["financiamiento_candidaturas"])
async def create_financiamiento_candidatura(data: FinanciamientoCandidatura, session: SessionDep):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

@router.get("/financiamiento/candidaturas/{record_id}", response_model=FinanciamientoCandidatura, tags=["financiamiento_candidaturas"])
async def read_financiamiento_candidatura(record_id: int, session: SessionDep):
    record = session.get(FinanciamientoCandidatura, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record

@router.patch("/financiamiento/candidaturas/{record_id}", response_model=FinanciamientoCandidatura, tags=["financiamiento_candidaturas"])
async def update_financiamiento_candidatura(record_id: int, data: FinanciamientoCandidatura, session: SessionDep):
    record = session.get(FinanciamientoCandidatura, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

@router.delete("/financiamiento/candidaturas/{record_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["financiamiento_candidaturas"])
async def delete_financiamiento_candidatura(record_id: int, session: SessionDep):
    record = session.get(FinanciamientoCandidatura, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(record)
    session.commit()
    return {"detail": "Eliminado"}

@router.get("/financiamiento/candidaturas", response_model=list[FinanciamientoCandidatura], tags=["financiamiento_candidaturas"])
async def list_financiamiento_candidaturas(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Cantidad de registros a mostrar")
):
    records = session.exec(select(FinanciamientoCandidatura).offset(skip).limit(limit)).all()
    return records