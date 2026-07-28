"""
💡 EXPLAINABLE RECOMMENDATION SERVICE — CUPID AGENT 💘
Tạo phần giải thích gợi ý tự nhiên từ kết quả Matching Engine có cấu trúc.
BẢO MẬT: KHÔNG ĐỌC RAW CHAT CỦA NGƯỜI DÙNG HOẶC ỨNG VIÊN.
"""

from sqlalchemy.orm import Session
from src.database.models import MatchResult, CandidateProfile
from src.services.llm_provider import get_llm_provider
from src.services.audit_service import AuditService


class ExplanationService:
    """Service tạo giải thích ghép đôi minh bạch"""

    @staticmethod
    def generate_explanation(db: Session, user_id: str, match_result_id: str) -> str:
        """Lấy thông tin MatchResult và tạo văn bản giải thích tự nhiên từ LLM"""
        match_res = db.query(MatchResult).filter(
            MatchResult.id == match_result_id,
            MatchResult.user_id == user_id
        ).first()

        if not match_res:
            return "Không tìm thấy kết quả ghép đôi."

        candidate = db.query(CandidateProfile).filter(CandidateProfile.id == match_res.candidate_id).first()
        if not candidate:
            return "Không tìm thấy thông tin ứng viên."

        candidate_info = {
            "display_name": candidate.display_name,
            "age": candidate.age,
            "gender": candidate.gender,
            "city": candidate.city,
            "occupation": candidate.occupation,
            "shareable_intro": candidate.shareable_intro,
            "core_values": candidate.core_values,
            "lifestyle": candidate.lifestyle,
            "boundaries": candidate.boundaries
        }

        match_data = {
            "total_score": match_res.total_score,
            "confidence": match_res.confidence,
            "matched_dimensions": match_res.matched_dimensions,
            "differences": match_res.differences,
            "missing_dimensions": match_res.missing_dimensions
        }

        provider = get_llm_provider()
        explanation = provider.explain_match(match_data, candidate_info)

        # Lưu giải thích vào DB
        match_res.explanation_text = explanation
        db.commit()

        AuditService.log_event(db, actor_id=user_id, action="GENERATE_MATCH_EXPLANATION", resource_id=match_result_id, decision="ALLOW")
        return explanation
