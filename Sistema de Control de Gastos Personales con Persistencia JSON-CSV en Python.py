# ===================================================================
# DESCRIPCIÓN GENERAL DEL PROGRAMA
# Este es un sistema completo para llevar el control de tus finanzas personales:
# - Registrar ingresos y gastos
# - Calcular saldo actual
# - Ver resumen por categorías de gasto
# - Guardar y cargar datos en archivos JSON y CSV
# - Totalmente validado y con buena estructura (POO)
# ===================================================================

import json
import csv
from typing import List, Dict


# ===================================================================
# CLASE 1: Movimiento - Representa un ingreso o gasto individual
# ===================================================================
class Movimiento:
    """
    Representa un movimiento financiero (ingreso o gasto).
    Ejemplos: salario, alquiler, supermercado, Netflix, etc.
    """

    def __init__(self, tipo: str, categoria: str, monto: float):
        # Validación: solo permite "ingreso" o "gasto"
        if tipo not in ("ingreso", "gasto"):
            raise ValueError("El tipo debe ser 'ingreso' o 'gasto'")
        # Validación: no permite montos negativos o cero
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        self.tipo = tipo          # "ingreso" o "gasto"
        self.categoria = categoria  # Ej: "salario", "alimentación", "transporte"
        self.monto = monto        # Valor en dinero (ej: 2500.50)

    # Convierte el objeto en diccionario (necesario para guardar en JSON/CSV)
    def to_dict(self) -> Dict:
        """Convierte el movimiento en diccionario (para JSON o CSV)."""
        return {"tipo": self.tipo, "categoria": self.categoria, "monto": self.monto}


# ===================================================================
# CLASE 2: ControlGastos - El cerebro del sistema
# ===================================================================
class ControlGastos:
    """
    Sistema principal para registrar y analizar movimientos financieros.
    Es como una pequeña app de finanzas personales.
    """

    def __init__(self):
        self.movimientos: List[Movimiento] = []  # Lista que guarda todos los movimientos

    # ==================== OPERACIONES BÁSICAS ====================
    def agregar_movimiento(self, tipo: str, categoria: str, monto: float) -> None:
        """Agrega un nuevo ingreso o gasto al sistema."""
        movimiento = Movimiento(tipo, categoria, monto)  # Crea el movimiento con validaciones
        self.movimientos.append(movimiento)             # Lo guarda en la lista

    def calcular_saldo(self) -> float:
        """Calcula cuánto dinero te queda: ingresos totales - gastos totales."""
        ingresos = sum(m.monto for m in self.movimientos if m.tipo == "ingreso")
        gastos = sum(m.monto for m in self.movimientos if m.tipo == "gasto")
        return ingresos - gastos

    def resumen_por_categoria(self) -> Dict[str, float]:
        """Muestra cuánto gastaste en cada categoría (alimentación, transporte, etc.)."""
        resumen: Dict[str, float] = {}
        for m in self.movimientos:
            if m.tipo == "gasto":
                # Si la categoría ya existe, suma. Si no, crea con 0 y suma
                resumen[m.categoria] = resumen.get(m.categoria, 0) + m.monto
        return resumen

    # ==================== GUARDAR EN ARCHIVOS ====================
    def guardar_json(self, archivo: str = "movimientos.json") -> None:
        """Guarda todos los movimientos en un archivo JSON (formato universal)."""
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in self.movimientos], f, indent=4)
        print(f"Datos guardados en {archivo}")

    def cargar_json(self, archivo: str = "movimientos.json") -> None:
        """Carga movimientos desde un archivo JSON."""
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.movimientos = [Movimiento(**item) for item in data]
            print(f"Datos cargados desde {archivo}")
        except FileNotFoundError:
            print("No se encontró el archivo JSON. Iniciando con lista vacía.")
            self.movimientos = []

    def guardar_csv(self, archivo: str = "movimientos.csv") -> None:
        """Guarda los movimientos en formato CSV (se abre en Excel)."""
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["tipo", "categoria", "monto"])
            writer.writeheader()
            for m in self.movimientos:
                writer.writerow(m.to_dict())
        print(f"Datos guardados en {archivo}")

    def cargar_csv(self, archivo: str = "movimientos.csv") -> None:
        """Carga movimientos desde un archivo CSV."""
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.movimientos = [Movimiento(row["tipo"], row["categoria"], float(row["monto"])) for row in reader]
            print(f"Datos cargados desde {archivo}")
        except FileNotFoundError:
            print("No se encontró el archivo CSV. Iniciando con lista vacía.")
            self.movimientos = []


# ===================================================================
# EJEMPLO DE USO REAL (prueba del sistema)
# ===================================================================
if __name__ == "__main__":
    # Creamos un nuevo sistema de control de gastos
    sistema = ControlGastos()

    # Registramos algunos movimientos de ejemplo
    sistema.agregar_movimiento("ingreso", "salario", 2500)
    sistema.agregar_movimiento("gasto", "alimentación", 300)
    sistema.agregar_movimiento("gasto", "transporte", 150)
    sistema.agregar_movimiento("gasto", "ocio", 200)

    # Mostramos el saldo actual
    print(f"Saldo actual: ${sistema.calcular_saldo():,.2f}")

    # Mostramos cuánto se gastó en cada categoría
    print("\nResumen de gastos por categoría:")
    for categoria, total in sistema.resumen_por_categoria().items():
        print(f" - {categoria}: ${total:,.2f}")

    # Guardamos los datos en archivos
    sistema.guardar_json("movimientos.json")
    sistema.guardar_csv("movimientos.csv")

    # Probamos cargar desde JSON
    print("\n--- Probando cargar desde archivo ---")
    nuevo_sistema = ControlGastos()
    nuevo_sistema.cargar_json("movimientos.json")
    print(f"Saldo después de cargar desde JSON: ${nuevo_sistema.calcular_saldo():,.2f}")