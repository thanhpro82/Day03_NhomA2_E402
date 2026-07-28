"""
🧠 MEMORY EXTRACTION & CONSENT SERVICE — CUPID AGENT 💘
Phân tích trích xuất Memory Candidates & quản lý quyền riêng tư Consent của người dùng.
"""

from sqlalchemy.orm import Session
from src.database.models import MemoryCandidate, ApprovedMemory, Message, ConsentRecord, generate_uuid
from src.services.llm_provider import get_llm_provider
from src.services.audit_service import AuditService
from src.config import MEMORY_CATEGORIES, VISIBILITY_OPTIONS


class MemoryService:
    """Service trích xuất và phê duyệt ghi nhớ"""

    @staticmethod
    def extract_memories_from_conversation(db: Session, user_id: str, conversation_id: str) -> list:
        """
        Phân tích cuộc trò chuyện và tạo danh sách MemoryCandidate ở trạng thái PENDING.
        """
        messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()
        if not messages:
            return []

        conv_text = "\n".join([f"{m.sender_type.upper()}: {m.content}" for m in messages])

        provider = get_llm_provider()
        raw_candidates = provider.extract_memories(conv_text)

        created_candidates = []
        for raw in raw_candidates:
            category = raw.get("category", "interest")
            if category not in MEMORY_CATEGORIES:
                category = "interest"

            candidate = MemoryCandidate(
                id=generate_uuid(),
                user_id=user_id,
                conversation_id=conversation_id,
                category=category,
                key=raw.get("key", "extracted_trait"),
                value=raw.get("value", ""),
                human_readable_value=raw.get("human_readable_value", raw.get("value", "")),
                confidence=raw.get("confidence", 0.85),
                stability=raw.get("stability", "stable"),
                sensitivity=raw.get("sensitivity", "normal"),
                recommended_usage=raw.get("recommended_usage", "match_profile"),
                status="PENDING"
            )
            db.add(candidate)
            created_candidates.append(candidate)

        db.commit()
        AuditService.log_event(db, actor_id=user_id, action="EXTRACT_MEMORIES", resource_id=conversation_id, decision="ALLOW")
        return created_candidates

    @staticmethod
    def get_pending_candidates(db: Session, user_id: str) -> list:
        """Lấy tất cả memory candidate đang chờ duyệt của user"""
        return db.query(MemoryCandidate).filter(
            MemoryCandidate.user_id == user_id,
            MemoryCandidate.status == "PENDING"
        ).all()

    @staticmethod
    def process_consent_decision(db: Session, user_id: str, candidate_id: str, decision: str) -> tuple[bool, str]:
        """
        Người dùng quyết định gán quyền cho candidate:
        - PRIVATE_ONLY
        - MATCH_USE
        - SHAREABLE
        - DO_NOT_SAVE
        """
        if decision not in VISIBILITY_OPTIONS:
            return False, f"Quyết định không hợp lệ. Phải thuộc: {VISIBILITY_OPTIONS}"

        candidate = db.query(MemoryCandidate).filter(
            MemoryCandidate.id == candidate_id,
            MemoryCandidate.user_id == user_id
        ).first()

        if not candidate:
            return False, "Không tìm thấy memory candidate hoặc không có quyền truy cập."

        if decision == "DO_NOT_SAVE":
            candidate.status = "REJECTED"
            db.commit()
            AuditService.log_event(db, actor_id=user_id, action="CONSENT_REJECT_MEMORY", resource_id=candidate_id, decision="ALLOW")
            return True, "Đã loại bỏ memory, không lưu vào hệ thống."

        # Lưu vào ApprovedMemory
        candidate.status = "APPROVED"
        approved_id = generate_uuid()

        approved = ApprovedMemory(
            id=approved_id,
            owner_id=user_id,
            category=candidate.category,
            key=candidate.key,
            value=candidate.value,
            human_readable_value=candidate.human_readable_value,
            confidence=candidate.confidence,
            stability=candidate.stability,
            sensitivity=candidate.sensitivity,
            visibility=decision,
            source_conversation_id=candidate.conversation_id,
            user_confirmed=True
        )
        db.add(approved)

        # Ghi nhật ký ConsentRecord
        consent_log = ConsentRecord(
            user_id=user_id,
            memory_id=approved_id,
            previous_visibility=None,
            new_visibility=decision
        )
        db.add(consent_log)

        db.commit()
        AuditService.log_event(db, actor_id=user_id, action="CONSENT_APPROVE_MEMORY", resource_id=approved_id, decision="ALLOW", details=decision)
        return True, f"Đã lưu memory thành công với quyền: {decision}"
