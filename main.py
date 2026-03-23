from fastapi import FastAPI,Body,HTTPException

app=FastAPI()
productos =[
    {
     "codigo" : 1,
     "nombre" : "esfero",
     "valor"  : 3500,
     "existencias" :10  
    },
    {
    "codigo" : 2,
    "nombre" : "cuaderno",
    "valor"  : 5000,
    "existencias" :15  
    },
    {
    "codigo" : 3,
    "nombre" : "lapiz",
    "valor"  : 200,
    "existencias" :12  
    }
]

@app.get("/")

def mensaje():
    return "bienvenido a FastAPI ingeniero"


@app.get("/{nombre}/{codigo}")
def mensaje2(nombre:str,codigo:int):
    return f"bienvenido {nombre} codigo {codigo}"

"""""
@app.get("/uno/")
def mensaje3(nombre:str,edad:int):
    return f"nombre {nombre} edad {edad}"
"""

@app.get("/productoall/")
def listProductos():
    return productos

@app.get("/producto/{cod}")
def findProductos(cod:int):
    for prod in productos:
        if prod["codigo"]==cod:
            return prod
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.get("/producto/")
def findProductos2(nom:str):
    for prod in productos:
        if prod["nombre"]==nom:
            return prod
        

@app.post("/producto/")
def createProductos(codigo:int,nombre:str,valor:float,existencia:int):
    
    for prod in productos:
        if prod["codigo"] == codigo:
            raise HTTPException(status_code=400, detail="El producto ya existe")

    if valor <= 0 or existencia <= 0:
        raise HTTPException(status_code=400, detail="Valor y existencias deben ser mayores a cero")
    productos.append({
            "codigo":codigo,
            "nombre":nombre,
            "valor":valor,
            "existencias":existencia
        })
    return productos

@app.post("/producto2/")
def createProductos2(
    cod:int=Body(),
    nom:str=Body(),
    valor:float=Body(),
    existencia:int=Body()
    ):
    productos.append(
        {
            "codigo":cod,
            "nombre":nom,
            "valor":valor,
            "existencias":existencia
        }
    )
    return productos

@app.put("/producto/{cod}")
def updateProductos(
    cod:int,
    nom:str=Body(),
    valor:float=Body(),
    existencia:int=Body()
    ):
        if valor <= 0 or existencia <= 0:
            raise HTTPException(status_code=400, detail="Valor y existencias deben ser mayores a cero")
        for prod in productos:
            if prod["codigo"]==cod:
                prod["nombre"]=nom
                prod["valor"]=valor
                prod["existencias"]=existencia
            return {
                "mensaje": "Producto actualizado",
                "producto": prod
            }
        raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.delete("/producto/{cod}")
def deleteProductos(cod:int):
    for prod in productos:
        if prod["codigo"]==cod:
            productos.remove(prod)
            return {"mensaje": "Producto eliminado", "producto": prod}
    raise HTTPException(status_code=404, detail="Producto no encontrado")
