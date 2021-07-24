from fastapi import FastAPI
import json
from routers import institusiRouter,alumniRouter


app = FastAPI()

app.include_router(
    institusiRouter.router,
    prefix="/institution",
    tags=["institution"],
)
app.include_router(
    alumniRouter.router,
    prefix='/alumni',
    tags=['alumni']
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# uvicorn main:app --reload --port 8000
# php -S localhost:8001 -t public 
    