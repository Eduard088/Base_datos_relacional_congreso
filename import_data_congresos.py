# import_congresos.py

import pandas as pd
from sqlmodel import Session, select
from models import Estado, Partido, CongresoLocal
from db import engine

def import_congresos(csv_file: str):
    df = pd.read_csv(csv_file)
    with Session(engine) as session:
        for index, row in df.iterrows():
            # --- 1. Verificar o insertar Estado ---
            id_estado = int(row["ID_estado"])
            nombre_estado = row["Nombre_estado"]
            estado = session.exec(
                select(Estado).where(Estado.id == id_estado)
            ).first()
            if not estado:
                estado = Estado(id=id_estado, nombre=nombre_estado)
                session.add(estado)
                session.commit()
                session.refresh(estado)
            
            # --- 2. Verificar o insertar Partido ---
            partido_nombre = row["Partido"]
            partido = session.exec(
                select(Partido).where(Partido.nombre == partido_nombre)
            ).first()
            if not partido:
                partido = Partido(nombre=partido_nombre)
                session.add(partido)
                session.commit()
                session.refresh(partido)
            
            # --- 3. Insertar registro de CongresoLocal ---
            registro = CongresoLocal(
                año = int(row["Año"]),
                estado_id = id_estado,
                partido_id = partido.id,
                votos = int(row["Votos"]),
                total_votos = int(row["Total_votos"]),
                proporcion = int(row["Proporcion"]),
                sexo = row["Sexo"],
                curules = int(row["Curules"]),
                zona = row["Zona"],
                espectro = row["Espectro"],
                presidencia = row["Presidencia"],
                lista_nominal = int(row["Lista_nominal"]),
                sufragios = row["Sufragios"]
            )
            session.add(registro)
        session.commit()
    print("Datos de congresos locales importados exitosamente.")

if __name__ == "__main__":
    csv_file = "/home/barea/Federales/Elecciones.csv"
    import_congresos(csv_file)
