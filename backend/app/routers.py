from fastapi import APIRouter
from backend.app.auth import router as auth_router
from backend.app.task import router as task_router
from backend.app.tag import router as tag_router


router = APIRouter(prefix="/api")
router.include_router(auth_router, prefix="/user", tags=["user"])
router.include_router(task_router, prefix="/task", tags=["task"])
router.include_router(tag_router, prefix="/tag", tags=["tag"])