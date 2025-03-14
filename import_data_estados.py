import pandas as pd
from sqlmodel import Session, select
from models import Estado
from db import engine

def import_estados(csv_file: str):
    df = pd.read_csv(csv_file)
    with Session(engine) as session:
        for index, row in df.iterrows():
            id_estado = int(row["ID_estado"])
            nombre_estado = row["Nombre_estado"].strip()
            # Verificar si el estado ya existe
            existing = session.exec(select(Estado).where(Estado.id == id_estado)).first()
            if not existing:
                estado = Estado(id=id_estado, nombre=nombre_estado)
                session.add(estado)
                session.commit()
                session.refresh(estado)
    print("Datos de estados importados exitosamente.")

if __name__ == "__main__":
    csv_file = "/home/barea/Federales/Elecciones.csv"  
    import_estados(csv_file)