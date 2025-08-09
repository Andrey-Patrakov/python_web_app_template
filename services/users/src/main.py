import uvicorn
from fastapi import FastAPI
from src.api.routers import all_routers
from src.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
