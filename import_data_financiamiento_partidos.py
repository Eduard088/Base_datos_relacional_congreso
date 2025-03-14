# import_financiamiento_partidos.py

import pandas as pd
from sqlmodel import Session, select
from models import Partido, FinanciamientoPartido
from db import engine

def import_financiamiento_partidos(csv_file: str):
    df = pd.read_csv(csv_file)
    with Session(engine) as session:
        for index, row in df.iterrows():
            # --- 1. Verificar o insertar Partido ---
            partido_nombre = row["Partido"]
            partido = session.exec(
                select(Partido).where(Partido.nombre == partido_nombre)
            ).first()
            if not partido:
                partido = Partido(nombre=partido_nombre)
                session.add(partido)
                session.commit()
                session.refresh(partido)
            
            # --- 2. Insertar registro de FinanciamientoPartido ---
            registro = FinanciamientoPartido(
                año = int(row["Año"]),
                partido_id = partido.id,
                concepto = row["Concepto"],
                categoria = row["Categoria"],
                monto = int(row["Monto"])
            )
            session.add(registro)
        session.commit()
    print("Datos de financiamiento de partidos importados exitosamente.")

if __name__ == "__main__":
    csv_file = "/home/barea/Federales/financiamiento.csv"
    import_financiamiento_partidos(csv_file)