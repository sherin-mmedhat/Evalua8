from typing import Union
from fastapi import FastAPI
from entrypoint import Employees
from entrypoint import Kpis

app = FastAPI()

# Include the routers
app.include_router(Employees.router)
app.include_router(Kpis.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}