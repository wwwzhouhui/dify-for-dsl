from edgetts_service import router as router_edgetts
from fastapi import FastAPI
import uvicorn
app = FastAPI()

# Include routers from service modules
app.include_router(router_edgetts)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
