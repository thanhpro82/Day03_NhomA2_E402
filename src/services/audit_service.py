"""
📜 AUDIT LOGGING SERVICE — CUPID AGENT 💘
Ghi nhận lịch sử truy vết bảo mật theo đúng chuẩn (KHÔNG lưu nội dung trò chuyện hay mật khẩu).
"""

from sqlalchemy.orm import Session
from src.database.models import AuditLog


class AuditService:
    """Service ghi nhật ký truy vết bảo mật"""

    @staticmethod
    def log_event(db: Session, actor_id: str, action: str, resource_id: str = None, decision: str = "ALLOW", details: str = None):
        """
        Ghi nhật ký audit chuẩn cấu trúc:
        {
          "actor_id": "user_id",
          "action": "READ_OWN_MEMORY",
          "resource_id": "memory_id",
          "decision": "ALLOW",
          "timestamp": "..."
        }
        """
        try:
            audit = AuditLog(
                actor_id=actor_id,
                action=action,
                resource_id=resource_id,
                decision=decision,
                details=details
            )
            db.add(audit)
            db.commit()
        except Exception as e:
            print(f"⚠️ Failed to write audit log: {e}")
            db.rollback()
