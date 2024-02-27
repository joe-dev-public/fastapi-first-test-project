from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

my_origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=my_origins,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
