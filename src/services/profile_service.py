"""
📋 RELATIONSHIP PROFILE SERVICE — CUPID AGENT 💘
Quản lý trang "Cupid hiểu gì về bạn" và CRUD thuộc tính hồ sơ cá nhân.
"""

from sqlalchemy.orm import Session
from src.database.models import ApprovedMemory, ConsentRecord
from src.services.audit_service import AuditService
from src.config import CATEGORY_LABELS_VI


class ProfileService:
    """Service quản lý hồ sơ hiểu biết của Cupid về người dùng"""

    @staticmethod
    def get_user_profile_grouped(db: Session, user_id: str) -> dict:
        """
        Lấy thông tin hồ sơ người dùng nhóm theo 10 hạng mục chuẩn product spec:
        1. Mục tiêu mối quan hệ
        2. Giá trị sống
        3. Phong cách giao tiếp
        4. Phong cách sống
        5. Sở thích & Xu hướng xã hội
        6. Ranh giới cá nhân
        7. Dealbreaker
        8. Tốc độ phát triển mối quan hệ
        9. Những dữ liệu còn thiếu
        10. Độ tin cậy từng thuộc tính
        """
        memories = db.query(ApprovedMemory).filter(ApprovedMemory.owner_id == user_id).all()

        grouped = {
            "relationship_goal": [],
            "core_value": [],
            "communication_style": [],
            "lifestyle": [],
            "social_preference": [],
            "relationship_pace": [],
            "affection_preference": [],
            "conflict_style": [],
            "personal_boundary": [],
            "dealbreaker": [],
            "interest": [],
            "other": []
        }

        found_categories = set()
        for m in memories:
            found_categories.add(m.category)
            if m.category in grouped:
                grouped[m.category].append(m)
            else:
                grouped["other"].append(m)

        # 9. Xác định những dữ liệu còn thiếu (Missing Dimensions)
        essential_categories = ["relationship_goal", "core_value", "communication_style", "relationship_pace", "dealbreaker"]
        missing_categories = [cat for cat in essential_categories if cat not in found_categories]

        return {
            "grouped_memories": grouped,
            "total_count": len(memories),
            "missing_categories": missing_categories,
            "missing_labels": [CATEGORY_LABELS_VI.get(c, c) for c in missing_categories]
        }

    @staticmethod
    def add_custom_memory(db: Session, user_id: str, category: str, human_readable_value: str, visibility: str = "MATCH_USE") -> ApprovedMemory:
        """Cho phép người dùng tự thêm thuộc tính mới vào hồ sơ"""
        memory = ApprovedMemory(
            owner_id=user_id,
            category=category,
            key=f"user_added_{category}",
            value=human_readable_value,
            human_readable_value=human_readable_value,
            confidence=1.0,
            stability="stable",
            sensitivity="normal",
            visibility=visibility,
            user_confirmed=True
        )
        db.add(memory)
        db.commit()
        db.refresh(memory)

        AuditService.log_event(db, actor_id=user_id, action="ADD_PROFILE_MEMORY", resource_id=memory.id, decision="ALLOW")
        return memory

    @staticmethod
    def update_memory_visibility(db: Session, user_id: str, memory_id: str, new_visibility: str) -> tuple[bool, str]:
        """Cập nhật quyền sử dụng dữ liệu của memory"""
        memory = db.query(ApprovedMemory).filter(
            ApprovedMemory.id == memory_id,
            ApprovedMemory.owner_id == user_id
        ).first()

        if not memory:
            return False, "Không tìm thấy thuộc tính hoặc không có quyền sở hữu."

        prev = memory.visibility
        memory.visibility = new_visibility

        # Ghi nhật ký thay đổi quyền
        consent = ConsentRecord(
            user_id=user_id,
            memory_id=memory_id,
            previous_visibility=prev,
            new_visibility=new_visibility
        )
        db.add(consent)
        db.commit()

        AuditService.log_event(db, actor_id=user_id, action="UPDATE_MEMORY_VISIBILITY", resource_id=memory_id, decision="ALLOW", details=f"{prev} -> {new_visibility}")
        return True, f"Đã chuyển quyền riêng tư sang {new_visibility}"

    @staticmethod
    def flag_misunderstanding(db: Session, user_id: str, memory_id: str) -> tuple[bool, str]:
        """Đánh dấu Cupid đã hiểu sai và loại bỏ memory này khỏi profile"""
        memory = db.query(ApprovedMemory).filter(
            ApprovedMemory.id == memory_id,
            ApprovedMemory.owner_id == user_id
        ).first()

        if not memory:
            return False, "Không tìm thấy thuộc tính."

        db.delete(memory)
        db.commit()

        AuditService.log_event(db, actor_id=user_id, action="FLAG_MISUNDERSTANDING", resource_id=memory_id, decision="ALLOW")
        return True, "Đã đánh dấu Cupid hiểu sai và loại bỏ khỏi hồ sơ của bạn."

    @staticmethod
    def delete_memory(db: Session, user_id: str, memory_id: str) -> tuple[bool, str]:
        """Xóa hoàn toàn một memory khỏi hồ sơ"""
        return ProfileService.flag_misunderstanding(db, user_id, memory_id)
