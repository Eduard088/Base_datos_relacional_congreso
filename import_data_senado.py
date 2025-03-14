# import_senado.py

import pandas as pd
from sqlmodel import Session, select
from models import Partido, Senado
from db import engine

def import_senado(csv_file: str):
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
            
            # --- 2. Insertar registro de Senado ---
            registro = Senado(
                año = int(row["Año"]),
                partido_id = partido.id,
                votos = int(row["Votos"]),
                proporcion = int(row["Proporcion"]),
                sexo = row["Sexo"],
                curules = int(row["Curules"]),
                financiamiento = int(row["Financiamiento"]),
                periodo = row["Periodo"],
                legislatura = row["Legislatura"]
            )
            session.add(registro)
        session.commit()
    print("Datos del Senado importados exitosamente.")

if __name__ == "__main__":
    csv_file = "/home/barea/Federales/Senado.csv"  
    import_senado(csv_file)
