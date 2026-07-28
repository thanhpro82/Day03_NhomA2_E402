"""
🗄️ DATABASE CONNECTION & SESSION MANAGEMENT
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import DATABASE_URL

# Cấu hình SQLite Engine
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency helper lấy database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Khởi tạo tất cả bảng cơ sở dữ liệu nếu chưa tồn tại"""
    import src.database.models  # Ensure models are registered
    Base.metadata.create_all(bind=engine)
