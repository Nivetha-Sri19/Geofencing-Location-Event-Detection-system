from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from app.api.v1.router import router
from app.core.config import settings
from app.core.database import get_session_factory,dispose_engine
from app.core.exceptions import AppException,app_exception_handler
from app.core.security import hash_password
from app.models.user import User
from app.models.enums import UserRole
async def bootstrap_admin():
    if not settings.bootstrap_admin_enabled: return
    async with get_session_factory()() as db:
        existing=await db.scalar(select(User).where(User.username==settings.bootstrap_admin_username))
        if not existing:
            db.add(User(username=settings.bootstrap_admin_username,email=settings.bootstrap_admin_email,password_hash=hash_password(settings.bootstrap_admin_password),role=UserRole.ADMIN))
            await db.commit()
@asynccontextmanager
async def lifespan(app:FastAPI):
    await bootstrap_admin(); yield; await dispose_engine()
app=FastAPI(title=settings.app_name,version=settings.app_version,description='Enterprise geofencing and location event detection backend.',lifespan=lifespan)
app.add_exception_handler(AppException,app_exception_handler)
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origin_list,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(router,prefix=settings.api_v1_prefix)
@app.get('/health',tags=['System'])
async def health(): return {'status':'ok','service':settings.app_name,'version':settings.app_version}
