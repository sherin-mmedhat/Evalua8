from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from entrypoint import Employees
from entrypoint import Kpis
from entrypoint import Feedbacks

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(Employees.router)
app.include_router(Kpis.router)
app.include_router(Feedbacks.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
