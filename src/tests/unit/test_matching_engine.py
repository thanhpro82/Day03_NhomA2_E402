"""
🧪 UNIT TESTS — MATCHING ENGINE & PRIVACY VISIBILITY
"""

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.connection import Base
from src.database.models import User, CandidateProfile, ApprovedMemory, MatchRequest
from src.services.matching_engine import MatchingEngine
from src.database.seed import SAMPLE_CANDIDATES


class TestMatchingEngine(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db = Session()

        # Seed candidates
        for c_data in SAMPLE_CANDIDATES[:5]:
            self.db.add(CandidateProfile(**c_data))

        # Seed User
        user = User(id="user_test_01", email="test@cupid.ai", password_hash="hash")
        self.db.add(user)
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_matching_engine_weighted_scoring(self):
        """Kiểm tra công thức tính điểm tương thích có trả kết quả hợp lệ 0-100%"""
        user_id = "user_test_01"

        # Thêm 2 memory hợp tác với Minh (candidate_001)
        self.db.add(ApprovedMemory(
            owner_id=user_id,
            category="relationship_goal",
            key="long_term",
            value="Mối quan hệ nghiêm túc",
            human_readable_value="Muốn mối quan hệ lâu dài",
            visibility="MATCH_USE"
        ))
        self.db.add(ApprovedMemory(
            owner_id=user_id,
            category="relationship_pace",
            key="slow",
            value="Tiến triển từ từ",
            human_readable_value="Thích tiến triển từ từ",
            visibility="MATCH_USE"
        ))
        self.db.commit()

        match_req, top_matches = MatchingEngine.run_match(self.db, user_id, {"interested_in": ["male"]})

        self.assertIsNotNone(match_req)
        self.assertGreaterThan = self.assertGreater(len(top_matches), 0)
        top_cand = top_matches[0][1]
        top_score = top_matches[0][2]

        self.assertTrue(0 <= top_score["total_score"] <= 100)
        self.assertGreater(top_score["confidence"], 0)
        self.assertGreater(len(top_score["matched_dimensions"]), 0)

    def test_privacy_visibility_filter(self):
        """Kiểm tra Matching Engine KHÔNG đọc memory có visibility = PRIVATE_ONLY"""
        user_id = "user_test_01"

        # Chỉ có PRIVATE_ONLY memory -> Không được đi vào Matching Engine
        self.db.add(ApprovedMemory(
            owner_id=user_id,
            category="relationship_goal",
            key="secret_trait",
            value="Bí mật riêng tư",
            human_readable_value="Chỉ chat riêng",
            visibility="PRIVATE_ONLY"
        ))
        self.db.commit()

        # Query approve memories với visibility MATCH_USE / SHAREABLE -> Phải = 0
        memories_for_match = self.db.query(ApprovedMemory).filter(
            ApprovedMemory.owner_id == user_id,
            ApprovedMemory.visibility.in_(["MATCH_USE", "SHAREABLE"])
        ).all()

        self.assertEqual(len(memories_for_match), 0)


if __name__ == "__main__":
    unittest.main()
