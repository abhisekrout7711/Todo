from fastapi import APIRouter
from backend.app.auth import router as auth_router
from backend.app.tasks import router as task_router


router = APIRouter(prefix="/api")
router.include_router(auth_router, prefix="/user", tags=["user"])
router.include_router(task_router, prefix="/task", tags=["task"])