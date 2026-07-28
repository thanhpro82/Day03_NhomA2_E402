"""
🧪 INTEGRATION TESTS — END-TO-END USER FLOW
"""

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.connection import Base
from src.database.models import User, CandidateProfile, ApprovedMemory, MatchResult, MatchFeedback
from src.services.auth_service import AuthService
from src.services.conversation_service import ConversationService
from src.services.memory_service import MemoryService
from src.services.matching_engine import MatchingEngine
from src.services.explanation_service import ExplanationService
from src.database.seed import SAMPLE_CANDIDATES


class TestUserFlow(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db = Session()

        # Seed 5 candidates
        for c in SAMPLE_CANDIDATES[:5]:
            self.db.add(CandidateProfile(**c))
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_full_user_end_to_end_flow(self):
        """Test toàn bộ luồng người dùng từ Đăng ký -> Chat -> Extract Memory -> Consent -> Profile -> Match -> Feedback"""

        # 1. Đăng ký & Đăng nhập
        ok, user = AuthService.register_user(self.db, "integration@cupid.ai", "password123", "Người dùng Thử nghiệm")
        self.assertTrue(ok)
        self.assertIsNotNone(user.id)

        ok_login, user_logged = AuthService.authenticate_user(self.db, "integration@cupid.ai", "password123")
        self.assertTrue(ok_login)

        # 2. Nhắn tin với Cupid Agent
        conv = ConversationService.get_or_create_conversation(self.db, user.id)
        self.assertIsNotNone(conv.id)

        agent_response = ConversationService.send_message(
            self.db,
            user.id,
            conv.id,
            "Mình khá hướng nội và thích dành cuối tuần ở quán cà phê đọc sách. Mình muốn mối quan hệ nghiêm túc nhưng thích tìm hiểu từ từ."
        )
        self.assertIsNotNone(agent_response)
        self.assertGreater(len(agent_response.content), 0)

        # 3. Trích xuất Memory Candidates
        candidates = MemoryService.extract_memories_from_conversation(self.db, user.id, conv.id)
        self.assertGreater(len(candidates), 0)

        # 4. Phê duyệt Consent (Gán MATCH_USE)
        cand_id = candidates[0].id
        ok_consent, msg_c = MemoryService.process_consent_decision(self.db, user.id, cand_id, "MATCH_USE")
        self.assertTrue(ok_consent)

        # 5. Kiểm tra Profile được cập nhật
        approved_list = self.db.query(ApprovedMemory).filter(ApprovedMemory.owner_id == user.id).all()
        self.assertGreater(len(approved_list), 0)

        # 6. Tìm người phù hợp (Matching Engine)
        match_req, top_matches = MatchingEngine.run_match(self.db, user.id, {"interested_in": ["male"]})
        self.assertGreater(len(top_matches), 0)

        top_m_res, top_cand, top_score_info = top_matches[0]
        self.assertGreater(top_score_info["total_score"], 0)

        # 7. Sinh giải thích minh bạch từ LLM
        explanation = ExplanationService.generate_explanation(self.db, user.id, top_m_res.id)
        self.assertGreater(len(explanation), 0)

        # 8. Gửi phản hồi "Quan tâm"
        feedback = MatchFeedback(match_result_id=top_m_res.id, user_id=user.id, feedback_type="INTERESTED")
        self.db.add(feedback)
        self.db.commit()

        saved_fb = self.db.query(MatchFeedback).filter(MatchFeedback.match_result_id == top_m_res.id).first()
        self.assertEqual(saved_fb.feedback_type, "INTERESTED")


if __name__ == "__main__":
    unittest.main()
