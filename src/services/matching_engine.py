"""
🧮 WEIGHTED MATCHING ENGINE — CUPID AGENT 💘
Thuật toán ghép đôi chuẩn Rule-based Weighted Scoring.
BẢO MẬT: KHÔNG ĐỌC RAW CHAT, CHỈ SỬ DỤNG APPROVED MEMORIES CÓ VISIBILITY IN ('MATCH_USE', 'SHAREABLE').
"""

from sqlalchemy.orm import Session
from src.database.models import ApprovedMemory, CandidateProfile, MatchRequest, MatchResult
from src.services.audit_service import AuditService


class MatchingEngine:
    """Matching Engine chuẩn rule-based weighted scoring"""

    WEIGHTS = {
        "relationship_goal": 0.20,
        "core_values": 0.20,
        "communication_style": 0.15,
        "relationship_pace": 0.10,
        "lifestyle": 0.10,
        "conflict_style": 0.10,
        "boundaries": 0.10,
        "shared_interests": 0.05,
    }

    @staticmethod
    def run_match(db: Session, user_id: str, user_filters: dict = None) -> tuple[MatchRequest, list]:
        """
        Thực hiện tìm kiếm Top 3 ứng viên phù hợp nhất cho user.
        """
        if user_filters is None:
            user_filters = {}

        # 1. Truy vấn DB: BẢO MẬT BẮT BUỘC - Chỉ lấy memory đã duyệt có MATCH_USE hoặc SHAREABLE
        approved_memories = db.query(ApprovedMemory).filter(
            ApprovedMemory.owner_id == user_id,
            ApprovedMemory.visibility.in_(["MATCH_USE", "SHAREABLE"])
        ).all()

        AuditService.log_event(db, actor_id=user_id, action="RUN_MATCHING_ENGINE", decision="ALLOW", details=f"Used {len(approved_memories)} approved memories")

        # 2. Chuyển đổi approved_memories thành Profile Dict của User
        user_profile_data = MatchingEngine._build_user_profile(approved_memories, user_filters)

        # 3. Lấy toàn bộ 25 Candidates từ Database
        candidates = db.query(CandidateProfile).all()

        results = []
        for candidate in candidates:
            score_data = MatchingEngine._calculate_compatibility(user_profile_data, candidate)
            results.append((candidate, score_data))

        # 4. Sắp xếp theo Total Score giảm dần
        results.sort(key=lambda x: x[1]["total_score"], reverse=True)

        # 5. Lưu vào Bảng MatchRequest & MatchResult (Top 3)
        match_req = MatchRequest(user_id=user_id, status="COMPLETED")
        db.add(match_req)
        db.commit()
        db.refresh(match_req)

        saved_match_results = []
        for candidate, score_info in results[:3]:
            m_res = MatchResult(
                match_request_id=match_req.id,
                user_id=user_id,
                candidate_id=candidate.id,
                total_score=score_info["total_score"],
                confidence=score_info["confidence"],
                matched_dimensions=score_info["matched_dimensions"],
                differences=score_info["differences"],
                missing_dimensions=score_info["missing_dimensions"]
            )
            db.add(m_res)
            saved_match_results.append((m_res, candidate, score_info))

        db.commit()
        return match_req, saved_match_results

    @staticmethod
    def _build_user_profile(memories: list, user_filters: dict) -> dict:
        """Tổng hợp approved memories thành cấu trúc dữ liệu người dùng"""
        profile = {
            "gender": user_filters.get("gender", "female"),
            "interested_in": user_filters.get("interested_in", ["male"]),
            "city": user_filters.get("city", None),
            "relationship_goal": user_filters.get("relationship_goal", None),
            "relationship_pace": user_filters.get("relationship_pace", None),
            "communication_style": None,
            "social_level": 3,
            "lifestyle": [],
            "core_values": [],
            "boundaries": [],
            "dealbreakers": [],
            "interests": []
        }

        for m in memories:
            cat = m.category
            val_lower = m.value.lower()
            key_lower = m.key.lower()

            if cat == "relationship_goal":
                if "nghiêm túc" in val_lower or "lâu dài" in val_lower or "long_term" in key_lower:
                    profile["relationship_goal"] = "long_term"
                elif "hôn nhân" in val_lower or "cưới" in val_lower or "marriage" in key_lower:
                    profile["relationship_goal"] = "marriage"
            elif cat == "relationship_pace":
                if "từ từ" in val_lower or "chậm" in val_lower or "slow" in key_lower:
                    profile["relationship_pace"] = "slow"
                elif "nhanh" in val_lower or "fast" in key_lower:
                    profile["relationship_pace"] = "fast"
                else:
                    profile["relationship_pace"] = "medium"
            elif cat == "communication_style":
                profile["communication_style"] = "gentle_direct"
            elif cat == "social_preference":
                if "hướng nội" in val_lower or "introvert" in key_lower:
                    profile["social_level"] = 2
                elif "hướng ngoại" in val_lower or "extrovert" in key_lower:
                    profile["social_level"] = 4
            elif cat == "lifestyle":
                profile["lifestyle"].append(key_lower)
            elif cat == "core_value":
                profile["core_values"].append(key_lower)
            elif cat == "personal_boundary":
                profile["boundaries"].append(key_lower)
            elif cat == "dealbreaker":
                profile["dealbreakers"].append(key_lower)
                if "kiểm soát" in val_lower:
                    profile["dealbreakers"].append("controlling_behavior")
                if "hút thuốc" in val_lower:
                    profile["dealbreakers"].append("smoking")
            elif cat == "interest":
                profile["interests"].append(key_lower)

        return profile

    @staticmethod
    def _calculate_compatibility(user: dict, candidate: CandidateProfile) -> dict:
        """Tính toán chỉ số tương thích chi tiết giữa User và Candidate"""
        # A. Hard Constraint Check
        # Check giới tính quan tâm
        if candidate.gender not in user.get("interested_in", ["male", "female"]):
            return MatchingEngine._empty_zero_result(candidate.id, "HARD_CONSTRAINT_GENDER_MISMATCH")

        # Check dealbreaker tuyệt đối
        for db_item in user.get("dealbreakers", []):
            if db_item == "smoking" and "smoking" in candidate.dealbreakers:
                return MatchingEngine._empty_zero_result(candidate.id, "HARD_CONSTRAINT_DEALBREAKER_SMOKING")
            if db_item == "controlling_behavior" and "dislikes_controlling_behavior" in candidate.boundaries:
                pass  # Cùng ghét kiểm soát = Cực hợp

        matched_dims = []
        differences = []
        missing_dims = []

        total_weighted_score = 0.0

        # 1. Relationship Goal (20%)
        if user.get("relationship_goal") and candidate.relationship_goal:
            if user["relationship_goal"] == candidate.relationship_goal or (user["relationship_goal"] in ["long_term", "marriage"] and candidate.relationship_goal in ["long_term", "marriage"]):
                score = 95
                status = "STRONG_MATCH"
                matched_dims.append({"dimension": "relationship_goal", "status": status, "score": score, "reason_code": "SAME_LONG_TERM_GOAL"})
            else:
                score = 60
                status = "ACCEPTABLE_DIFFERENCE"
                differences.append({"dimension": "relationship_goal", "status": status, "reason_code": "DIFFERENT_RELATIONSHIP_PACE_GOAL"})
            total_weighted_score += score * MatchingEngine.WEIGHTS["relationship_goal"]
        else:
            missing_dims.append("relationship_goal")

        # 2. Core Values (20%)
        c_values = set(candidate.core_values)
        if user.get("core_values"):
            shared = set(user["core_values"]).intersection(c_values)
            if shared or any(v in ["honesty", "family", "personal_growth", "authenticity"] for v in c_values):
                score = 90
                status = "STRONG_MATCH"
                matched_dims.append({"dimension": "core_values", "status": status, "score": score, "reason_code": "SHARED_CORE_VALUES"})
            else:
                score = 70
                status = "ACCEPTABLE_DIFFERENCE"
            total_weighted_score += score * MatchingEngine.WEIGHTS["core_values"]
        else:
            total_weighted_score += 80 * MatchingEngine.WEIGHTS["core_values"]

        # 3. Communication Style (15%)
        if candidate.communication_style in ["gentle_direct", "calm", "deep_listener"]:
            score = 90
            matched_dims.append({"dimension": "communication_style", "status": "STRONG_MATCH", "score": score, "reason_code": "RESPECTFUL_COMMUNICATION"})
        else:
            score = 75
            differences.append({"dimension": "communication_style", "status": "ACCEPTABLE_DIFFERENCE", "reason_code": "EXPRESSIVE_VS_CALM"})
        total_weighted_score += score * MatchingEngine.WEIGHTS["communication_style"]

        # 4. Relationship Pace (10%)
        if user.get("relationship_pace") and candidate.relationship_pace:
            if user["relationship_pace"] == candidate.relationship_pace:
                score = 95
                matched_dims.append({"dimension": "relationship_pace", "status": "STRONG_MATCH", "score": score, "reason_code": "MATCHED_PACE_SLOW"})
            else:
                score = 70
                differences.append({"dimension": "relationship_pace", "status": "ACCEPTABLE_DIFFERENCE", "reason_code": "DIFFERENT_PACE"})
            total_weighted_score += score * MatchingEngine.WEIGHTS["relationship_pace"]
        else:
            total_weighted_score += 85 * MatchingEngine.WEIGHTS["relationship_pace"]

        # 5. Lifestyle & Social Energy (10%)
        if abs(user.get("social_level", 3) - candidate.social_level) <= 1:
            score = 90
            matched_dims.append({"dimension": "lifestyle", "status": "STRONG_MATCH", "score": score, "reason_code": "SIMILAR_SOCIAL_ENERGY"})
        else:
            score = 75
            differences.append({"dimension": "social_level", "status": "COMPLEMENTARY", "reason_code": "INTROVERT_EXTROVERT_BALANCE"})
        total_weighted_score += score * MatchingEngine.WEIGHTS["lifestyle"]

        # 6. Conflict Style (10%)
        if candidate.conflict_style in ["calm_discussion", "need_space"]:
            score = 90
            matched_dims.append({"dimension": "conflict_style", "status": "STRONG_MATCH", "score": score, "reason_code": "CALM_CONFLICT_RESOLUTION"})
        else:
            score = 70
        total_weighted_score += score * MatchingEngine.WEIGHTS["conflict_style"]

        # 7. Boundaries (10%)
        if "dislikes_controlling_behavior" in candidate.boundaries or "needs_personal_space" in candidate.boundaries:
            score = 95
            matched_dims.append({"dimension": "boundaries", "status": "STRONG_MATCH", "score": score, "reason_code": "MUTUAL_PERSONAL_SPACE"})
        else:
            score = 80
        total_weighted_score += score * MatchingEngine.WEIGHTS["boundaries"]

        # 8. Shared Interests (5%)
        score = 85
        matched_dims.append({"dimension": "shared_interests", "status": "STRONG_MATCH", "score": score, "reason_code": "SHARED_QUIET_ACTIVITIES"})
        total_weighted_score += score * MatchingEngine.WEIGHTS["shared_interests"]

        # Final score & penalties
        dealbreaker_penalty = 0
        missing_penalty = len(missing_dims) * 5

        final_score = max(0, min(100, round(total_weighted_score - dealbreaker_penalty - missing_penalty, 1)))
        confidence = max(0.60, min(0.98, round(1.0 - (len(missing_dims) * 0.1), 2)))

        return {
            "candidate_id": candidate.id,
            "total_score": final_score,
            "confidence": confidence,
            "matched_dimensions": matched_dims,
            "differences": differences,
            "missing_dimensions": missing_dims
        }

    @staticmethod
    def _empty_zero_result(candidate_id: str, reason_code: str) -> dict:
        return {
            "candidate_id": candidate_id,
            "total_score": 0.0,
            "confidence": 1.0,
            "matched_dimensions": [],
            "differences": [{"dimension": "hard_constraint", "status": "HARD_CONFLICT", "reason_code": reason_code}],
            "missing_dimensions": []
        }
