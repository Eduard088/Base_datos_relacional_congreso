# models.py
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum

# ---------------------------
# Dimensiones
# ---------------------------

class Estado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Corresponde a "ID_estado"
    nombre: str  # "Nombre_estado"

class Partido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str

# ---------------------------
# Hechos (Fact Tables)
# ---------------------------

# 1. Congresos Locales  
# Variables: Año, ID_estado, (se usa la dimensión Estado), Partido, Votos, Total_votos, Proporcion, Sexo,  
# Curules, Zona, Espectro, Presidencia, Lista_nominal, Sufragios
class CongresoLocal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    año: int
    estado_id: int = Field(foreign_key="estado.id")  # Relación con la dimensión Estado
    partido_id: int = Field(foreign_key="partido.id")  # Relación con la dimensión Partido
    votos: int
    total_votos: int
    proporcion: int
    sexo: str            # Se espera, por ejemplo, "Hombre" o "Mujer" (no se crea enum, pero se podría)
    curules: int
    zona: str
    espectro: str
    presidencia: str
    lista_nominal: int
    sufragios: str

# 2. Diputaciones Federales  
# Variables: Partido, Votos, Proporcion, Año, Periodo, Legislatura, Sexo, Curules, Financiamiento
class DiputacionFederal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    año: int
    partido_id: int = Field(foreign_key="partido.id")
    votos: int
    proporcion: int
    periodo: str
    legislatura: str
    sexo: str
    curules: int
    financiamiento: int

# 3. Senado  
# Variables: Partido, Votos, Proporcion, Sexo, Curules, Año, Financiamiento, Periodo, Legislatura
class Senado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    año: int
    partido_id: int = Field(foreign_key="partido.id")
    votos: int
    proporcion: int
    sexo: str
    curules: int
    financiamiento: int
    periodo: str
    legislatura: str

# 4. Financiamiento Público de Partidos Políticos  
# Variables: Año, Partido, Concepto, Categoria, Monto
class FinanciamientoPartido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    año: int
    partido_id: int = Field(foreign_key="partido.id")
    concepto: str
    categoria: str
    monto: int

# 5. Financiamiento Público de Candidaturas Independientes  
# Variables: Año, Partido, Concepto, Monto
class FinanciamientoCandidatura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    año: int
    partido_id: int = Field(foreign_key="partido.id")
    concepto: str
    monto: int
