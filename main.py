from fastapi import FastAPI

app=FastAPI()
@app.get("/")

def mensaje():
    return "bienvenido a FastAPI ingeniero"


@app.get("/{nombre}/{codigo}")
def mensaje2(nombre:str,codigo:int):
    return f"bienvenido {nombre} codigo {codigo}"


@app.get("/uno/")
def mensaje3(nombre:str,edad:int):
    return f"nombre {nombre} edad {edad}"


