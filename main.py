from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import json
from routers import institusiRouter, alumniRouter, consumerRouter, tracerRouter, authRouter


app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    authRouter.router,
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    institusiRouter.router,
    prefix="/api/institution",
    tags=["institution"],
)
app.include_router(
    alumniRouter.router,
    prefix='/api/alumni',
    tags=['alumni']
)
app.include_router(
    consumerRouter.router,
    prefix='/api/consumer',
    tags=['consumer']
)
app.include_router(
    tracerRouter.router,
    prefix='/api/tracer',
    tags=['tracer']
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

# uvicorn main:app --reload --port 8000
# php -S localhost:8001 -t public
# pip install fastapi requests  python-multipart
