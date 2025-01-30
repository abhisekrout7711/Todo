import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import router


application = FastAPI()
application.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# application.openapi = lambda: {
#     **application.openapi(),
#     "components": {
#         "securitySchemes": {
#             "bearerAuth": {
#                 "type": "http",
#                 "scheme": "bearer",
#                 "bearerFormat": "JWT",
#             }
#         }
#     },
# }

@application.get('/', include_in_schema=True)
async def app_start():
    return {"message": "application running!"}

application.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("backend.app.main:application", host="0.0.0.0", port=8080, reload=True)