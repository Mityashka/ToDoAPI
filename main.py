import uvicorn
from fastapi import FastAPI
from script import app

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
