from typing import Union
from fastapi import FastAPI
from entrypoint import Employees

app = FastAPI()

# Include the routers
app.include_router(Employees.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}