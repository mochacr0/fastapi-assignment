import uvicorn
from fastapi import FastAPI

from app.routers.main import app_router

app = FastAPI()
app.include_router(app_router)


@app.get("/health-check", status_code=200, tags=["Health Check"])
async def get_health_check():
    return {"status": "OK"}


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
