from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
from .database import engine, Base, get_db
from .models import User
from .config import settings
import logging

# Настройка логирования
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan для создания таблиц при запуске"""
    logger.info("Starting application...")
    
    try:
        # Создание таблиц
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise
    
    yield
    
    # Очистка при завершении
    logger.info("Shutting down application...")


app = FastAPI(
        title = "FastAPI with PostgreSQL", version = "1.0.0", lifespan = lifespan
        )


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {"message": "FastAPI application connected to PostgreSQL",
            "database_url": settings.DATABASE_URL.replace(settings.POSTGRES_PASSWORD, "***")}


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Проверка здоровья приложения и базы данных"""
    try:
        # Проверяем соединение с БД
        result = await db.execute("SELECT 1")
        db_status = "healthy" if result.scalar() == 1 else "unhealthy"
        
        return {"status": "ok", "database": db_status,
                "database_url": f"postgresql://{settings.POSTGRES_USER}:***@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"}
    except Exception as e:
        raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = f"Database connection failed: {str(e)}"
                )


@app.get("/users")
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Получение списка пользователей"""
    try:
        result = await db.execute(select(User).offset(skip).limit(limit))
        users = result.scalars().all()
        return {"users": users, "count": len(users)}
    except Exception as e:
        raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Failed to fetch users: {str(e)}"
                )


@app.get("/users/count")
async def get_users_count(db: AsyncSession = Depends(get_db)):
    """Получение количества пользователей"""
    try:
        result = await db.execute(select(func.count(User.id)))
        count = result.scalar()
        return {"count": count}
    except Exception as e:
        raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Failed to count users: {str(e)}"
                )


@app.get("/database/info")
async def get_database_info(db: AsyncSession = Depends(get_db)):
    """Получение информации о базе данных"""
    try:
        # Версия PostgreSQL
        result = await db.execute("SELECT version()")
        version = result.scalar()
        
        # Текущая база данных
        result = await db.execute("SELECT current_database()")
        current_db = result.scalar()
        
        # Текущий пользователь
        result = await db.execute("SELECT current_user")
        current_user = result.scalar()
        
        return {"postgresql_version": version, "current_database": current_db, "current_user": current_user,
                "host": settings.POSTGRES_HOST, "port": settings.POSTGRES_PORT}
    except Exception as e:
        raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Failed to get database info: {str(e)}"
                )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host = "0.0.0.0", port = 8000)