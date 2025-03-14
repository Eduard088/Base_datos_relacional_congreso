# app/routers/congresos.py
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from db import SessionDep
from models import CongresoLocal

router = APIRouter()

@router.post("/congresos", response_model=CongresoLocal, status_code=status.HTTP_201_CREATED, tags=["congresos"])
async def create_congreso(congreso: CongresoLocal, session: SessionDep):
    session.add(congreso)
    session.commit()
    session.refresh(congreso)
    return congreso

@router.get("/congresos/{congreso_id}", response_model=CongresoLocal, tags=["congresos"])
async def read_congreso(congreso_id: int, session: SessionDep):
    record = session.get(CongresoLocal, congreso_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record

@router.patch("/congresos/{congreso_id}", response_model=CongresoLocal, tags=["congresos"])
async def update_congreso(congreso_id: int, data: CongresoLocal, session: SessionDep):
    record = session.get(CongresoLocal, congreso_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

@router.delete("/congresos/{congreso_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["congresos"])
async def delete_congreso(congreso_id: int, session: SessionDep):
    record = session.get(CongresoLocal, congreso_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(record)
    session.commit()
    return {"detail": "Eliminado"}

@router.get("/congresos", response_model=list[CongresoLocal], tags=["congresos"])
async def list_congresos(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Cantidad de registros a mostrar")
):
    records = session.exec(select(CongresoLocal).offset(skip).limit(limit)).all()
    return records
