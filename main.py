from fastapi import FastAPI, Body, HTTPException
import json
import os

app = FastAPI()
ARCHIVO = "productos.json"

# Cargar JSON
def cargar_productos():
    if not os.path.exists(ARCHIVO):
        return []

    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return []

# Guardar JSON
def guardar_productos(productos):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, indent=4, ensure_ascii=False)

# Generar código automático
def generar_codigo(productos):
    if not productos:
        return 1
    return max(prod["codigo"] for prod in productos) + 1

# Ruta base
@app.get("/")
def mensaje():
    return {"mensaje": "API de productos funcionando"}

# Listar todos
@app.get("/productoall/")
def listProductos():
    return cargar_productos()

# Buscar por código
@app.get("/producto/{cod}")
def buscar_codigo(cod: int):
    productos = cargar_productos()
    for prod in productos:
        if prod["codigo"] == cod:
            return prod
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Buscar por nombre
@app.get("/producto/nombre/{nom}")
def buscar_nombre(nom: str):
    productos = cargar_productos()
    for prod in productos:
        if prod["nombre"].lower() == nom.lower():
            return prod
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Crear producto
@app.post("/producto/")
def createProductos(
    nombre: str = Body(...),
    valor: float = Body(...),
    existencias: int = Body(...)
):
    productos = cargar_productos()

    nombre = nombre.strip()

    if not nombre:
        raise HTTPException(status_code=400, detail="Nombre vacío")

    if valor <= 0 or existencias <= 0:
        raise HTTPException(status_code=400, detail="Valores deben ser mayores a 0")

    codigo = generar_codigo(productos)

    nuevo = {
        "codigo": codigo,
        "nombre": nombre,
        "valor": valor,
        "existencias": existencias
    }

    productos.append(nuevo)
    guardar_productos(productos)

    return {
        "mensaje": "Producto creado",
        "producto": nuevo
    }

# Actualizar producto
@app.put("/producto/{cod}")
def updateProductos(
    cod: int,
    nombre: str = Body(...),
    valor: float = Body(...),
    existencias: int = Body(...)
):
    productos = cargar_productos()

    nombre = nombre.strip()

    if not nombre:
        raise HTTPException(status_code=400, detail="Nombre vacío")

    if valor <= 0 or existencias <= 0:
        raise HTTPException(status_code=400, detail="Valores deben ser mayores a 0")

    for prod in productos:
        if prod["codigo"] == cod:
            prod["nombre"] = nombre
            prod["valor"] = valor
            prod["existencias"] = existencias

            guardar_productos(productos)

            return {
                "mensaje": "Producto actualizado",
                "producto": prod
            }

    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Eliminar producto
@app.delete("/producto/{cod}")
def deleteProductos(cod: int):
    productos = cargar_productos()

    for prod in productos:
        if prod["codigo"] == cod:
            productos.remove(prod)
            guardar_productos(productos)

            return {
                "mensaje": "Producto eliminado",
                "producto": prod
            }

    raise HTTPException(status_code=404, detail="Producto no encontrado")
