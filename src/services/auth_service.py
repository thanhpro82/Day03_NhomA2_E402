"""
🔐 AUTHENTICATION & SESSION SERVICE — CUPID AGENT 💘
Quản lý đăng ký, đăng nhập và bảo mật phân quyền dữ liệu cá nhân.
"""

import hashlib
from sqlalchemy.orm import Session
from src.database.models import User
from src.services.audit_service import AuditService


class AuthService:
    """Service xác thực tài khoản & bảo mật session"""

    @staticmethod
    def register_user(db: Session, email: str, password: str, display_name: str = None) -> tuple[bool, User or str]:
        """Đăng ký tài khoản người dùng mới bằng email và mật khẩu"""
        email_clean = email.strip().lower()
        if not email_clean or "@" not in email_clean:
            return False, "Email không hợp lệ."

        if len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự."

        existing = db.query(User).filter(User.email == email_clean).first()
        if existing:
            return False, "Email này đã được sử dụng."

        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        user = User(
            email=email_clean,
            password_hash=pwd_hash,
            display_name=display_name or email_clean.split("@")[0].capitalize()
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        AuditService.log_event(db, actor_id=user.id, action="REGISTER_USER", decision="ALLOW")
        return True, user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> tuple[bool, User or str]:
        """Đăng nhập xác thực email và mật khẩu"""
        email_clean = email.strip().lower()
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()

        user = db.query(User).filter(User.email == email_clean, User.password_hash == pwd_hash).first()
        if not user:
            AuditService.log_event(db, actor_id=email_clean, action="LOGIN_FAILED", decision="DENIED")
            return False, "Email hoặc mật khẩu không chính xác."

        AuditService.log_event(db, actor_id=user.id, action="LOGIN_SUCCESS", decision="ALLOW")
        return True, user

    @staticmethod
    def verify_owner_access(authenticated_user_id: str, target_owner_id: str) -> bool:
        """
        NGUYÊN TẮC BẢO MẬT CỐT LÕI:
        Không sử dụng user ID do frontend gửi để truy vấn dữ liệu nếu khác với authenticated_user_id.
        """
        return authenticated_user_id == target_owner_id
