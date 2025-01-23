import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router


application = FastAPI()
application.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@application.get('/', include_in_schema=True)
async def app_start():
    return {"message": "application running!"}

application.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8080, reload=True)