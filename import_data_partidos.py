# import_partidos.py

import pandas as pd
from sqlmodel import Session, select
from models import Partido
from db import engine

def import_partidos(csv_file: str):
    df = pd.read_csv(csv_file)
    with Session(engine) as session:
        for index, row in df.iterrows():
            partido_nombre = row["Partido"].strip()
            # Verificar si ya existe (ignorando mayúsculas/minúsculas)
            existing = session.exec(select(Partido).where(Partido.nombre.ilike(partido_nombre))).first()
            if not existing:
                partido = Partido(nombre=partido_nombre)
                session.add(partido)
                session.commit()
                session.refresh(partido)
    print("Datos de partidos importados exitosamente.")

if __name__ == "__main__":
    csv_file = "/home/barea/Federales/Elecciones.csv"
    import_partidos(csv_file)