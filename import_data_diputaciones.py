# import_diputaciones.py

import pandas as pd
from sqlmodel import Session, select
from models import Partido, DiputacionFederal
from db import engine

def import_diputaciones(csv_file: str):
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
            
            # --- 2. Insertar registro de DiputacionFederal ---
            registro = DiputacionFederal(
                año = int(row["Año"]),
                partido_id = partido.id,
                votos = int(row["Votos"]),
                proporcion = int(row["Proporcion"]),
                periodo = row["Periodo"],
                legislatura = row["Legislatura"],
                sexo = row["Sexo"],
                curules = int(row["Curules"]),
                financiamiento = int(row["Financiamiento"])
            )
            session.add(registro)
        session.commit()
    print("Datos de diputaciones federales importados exitosamente.")

if __name__ == "__main__":
    csv_file = "/home/barea/Federales/Diputadosfed.csv"
    import_diputaciones(csv_file)