from fastapi import FastAPI
from core.db import engine, Base
from api.v1.roles.router import router as role_router
from api.v1.auth.router import router as auth_router
from api.v1.users.router import router as user_router
from api.v1.actions.router import router as action_router
from api.v1.type_device.router import router as type_device_router
from api.v1.status_device.router import router as status_device_router
from api.v1.devices.router import router as device_router
from api.v1.action_logs.router import router as action_log_router

def create_app():
    app = FastAPI()
    Base.metadata.create_all(bind=engine)
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
    app.include_router(action_router, prefix="/api/v1/actions", tags=["Actions"])
    app.include_router(role_router, prefix="/api/v1/roles", tags=["Roles"])
    app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(device_router, prefix="/api/v1/devices", tags=["Devices"])
    app.include_router(type_device_router, prefix="/api/v1/type_devices", tags=["Type Devices"])
    app.include_router(status_device_router, prefix="/api/v1/status_devices", tags=["Status Devices"])
    app.include_router(action_log_router, prefix="/api/v1/action_logs", tags=["Action Logs"])
    
    return app


app = create_app()

