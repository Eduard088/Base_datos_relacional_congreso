# app/routers/senado.py
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from db import SessionDep
from models import Senado

router = APIRouter()

@router.post("/senado", response_model=Senado, status_code=status.HTTP_201_CREATED, tags=["senado"])
async def create_senado(data: Senado, session: SessionDep):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

@router.get("/senado/{senado_id}", response_model=Senado, tags=["senado"])
async def read_senado(senado_id: int, session: SessionDep):
    record = session.get(Senado, senado_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record

@router.patch("/senado/{senado_id}", response_model=Senado, tags=["senado"])
async def update_senado(senado_id: int, data: Senado, session: SessionDep):
    record = session.get(Senado, senado_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

@router.delete("/senado/{senado_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["senado"])
async def delete_senado(senado_id: int, session: SessionDep):
    record = session.get(Senado, senado_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(record)
    session.commit()
    return {"detail": "Eliminado"}

@router.get("/senado", response_model=list[Senado], tags=["senado"])
async def list_senado(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Cantidad de registros a mostrar")
):
    records = session.exec(select(Senado).offset(skip).limit(limit)).all()
    return records
