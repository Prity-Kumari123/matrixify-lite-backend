from fastapi import FastAPI
from app.api.import_products import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Matrixify-Lite Import Engine")

app.include_router(router, prefix="/import")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "running"}
