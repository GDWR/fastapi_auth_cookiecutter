from .admin import router as admin_router
from .auth import router as auth_router
from .user import router as user_router

all_routers = [
    admin_router,
    auth_router,
    user_router,
]
