"""
🌱 DATABASE SEED SCRIPT — CUPID AGENT 💘
Khởi tạo 25 hồ sơ ứng viên giả lập mẫu đa dạng (không dựa trên người thật) và tài khoản demo user.
"""

from sqlalchemy.orm import Session
from src.database.connection import SessionLocal, init_db
from src.database.models import CandidateProfile, User, ApprovedMemory
import hashlib

# Danh sách 25 Candidate Mẫu theo chuẩn Yêu cầu E
SAMPLE_CANDIDATES = [
    # 1. Minh - Nam 24 - Hà Nội
    {
        "id": "candidate_001",
        "display_name": "Minh",
        "age": 24,
        "gender": "male",
        "interested_in": ["female"],
        "city": "Hà Nội",
        "occupation": "Kỹ sư phần mềm",
        "relationship_goal": "long_term",
        "relationship_pace": "slow",
        "communication_style": "gentle_direct",
        "social_level": 2,
        "lifestyle": ["reading", "coffee", "running"],
        "core_values": ["personal_growth", "honesty", "family"],
        "affection_preferences": ["quality_time", "acts_of_service"],
        "conflict_style": "calm_discussion",
        "boundaries": ["needs_personal_space", "dislikes_controlling_behavior"],
        "dealbreakers": ["dishonesty", "aggressive_communication"],
        "wants_children": "undecided",
        "marriage_timeline": "3_to_5_years",
        "shareable_intro": "Thích những cuộc trò chuyện sâu, chạy bộ và dành thời gian ở quán cà phê yên tĩnh."
    },
    # 2. Linh - Nữ 23 - Hà Nội
    {
        "id": "candidate_002",
        "display_name": "Linh",
        "age": 23,
        "gender": "female",
        "interested_in": ["male"],
        "city": "Hà Nội",
        "occupation": "Nhà thiết kế đồ họa",
        "relationship_goal": "long_term",
        "relationship_pace": "slow",
        "communication_style": "gentle_direct",
        "social_level": 2,
        "lifestyle": ["reading", "painting", "cats", "meditation"],
        "core_values": ["authenticity", "empathy", "family"],
        "affection_preferences": ["quality_time", "words_of_affirmation"],
        "conflict_style": "calm_discussion",
        "boundaries": ["needs_personal_space", "dislikes_loud_noise"],
        "dealbreakers": ["dishonesty", "smoking"],
        "wants_children": "yes",
        "marriage_timeline": "3_to_5_years",
        "shareable_intro": "Thích vẽ tranh, yêu mèo, chuộng những cuộc hẹn góc phố thanh bình."
    },
    # 3. Nam - Nam 26 - TP.HCM
    {
        "id": "candidate_003",
        "display_name": "Nam",
        "age": 26,
        "gender": "male",
        "interested_in": ["female"],
        "city": "TP.HCM",
        "occupation": "Quản lý Sản phẩm (Product Manager)",
        "relationship_goal": "long_term",
        "relationship_pace": "medium",
        "communication_style": "humorous",
        "social_level": 4,
        "lifestyle": ["travel", "photography", "cooking", "cats"],
        "core_values": ["freedom", "creativity", "emotional_connection"],
        "affection_preferences": ["physical_touch", "quality_time"],
        "conflict_style": "calm_discussion",
        "boundaries": ["dislikes_controlling_behavior"],
        "dealbreakers": ["smoking", "excessive_control"],
        "wants_children": "yes",
        "marriage_timeline": "2_to_3_years",
        "shareable_intro": "Yêu du lịch nhiếp ảnh, thích nấu ăn cuối tuần và trò chuyện hài hước."
    },
    # 4. Trang - Nữ 22 - Hà Nội
    {
        "id": "candidate_004",
        "display_name": "Trang",
        "age": 22,
        "gender": "female",
        "interested_in": ["male"],
        "city": "Hà Nội",
        "occupation": "Chuyên viên Truyền thông",
        "relationship_goal": "casual_to_serious",
        "relationship_pace": "medium",
        "communication_style": "expressive",
        "social_level": 5,
        "lifestyle": ["concerts", "travel", "foodie", "dogs"],
        "core_values": ["joy", "new_experiences", "friendship"],
        "affection_preferences": ["words_of_affirmation", "receiving_gifts"],
        "conflict_style": "express_immediately",
        "boundaries": ["respect_hobbies"],
        "dealbreakers": ["patriarchal_attitude", "overly_serious"],
        "wants_children": "undecided",
        "marriage_timeline": "someday",
        "shareable_intro": "Sôi nổi, thích đi nghe nhạc live, ăn uống trải nghiệm và nuôi cún."
    },
    # 5. Long - Nam 28 - Hà Nội
    {
        "id": "candidate_005",
        "display_name": "Long",
        "age": 28,
        "gender": "male",
        "interested_in": ["female"],
        "city": "Hà Nội",
        "occupation": "Co-founder Startup",
        "relationship_goal": "marriage",
        "relationship_pace": "slow",
        "communication_style": "logical_direct",
        "social_level": 4,
        "lifestyle": ["podcasts", "chess", "gym", "startup"],
        "core_values": ["innovation", "intellect", "ambition"],
        "affection_preferences": ["words_of_affirmation", "acts_of_service"],
        "conflict_style": "calm_discussion",
        "boundaries": ["needs_focus_time"],
        "dealbreakers": ["conservatism", "lack_of_logic"],
        "wants_children": "yes",
        "marriage_timeline": "1_to_2_years",
        "shareable_intro": "Đam mê công nghệ, thích đánh cờ vua, nghe podcast và hướng tới hôn nhân bền vững."
    },
    # 6. Hoa - Nữ 25 - Hà Nội
    {
        "id": "candidate_006",
        "display_name": "Hoa",
        "age": 25,
        "gender": "female",
        "interested_in": ["male"],
        "city": "Hà Nội",
        "occupation": "Bác sĩ Thú y",
        "relationship_goal": "long_term",
        "relationship_pace": "medium",
        "communication_style": "gentle_direct",
        "social_level": 3,
        "lifestyle": ["baking", "yoga", "gardening", "cats"],
        "core_values": ["family", "stability", "care", "loyalty"],
        "affection_preferences": ["acts_of_service", "quality_time"],
        "conflict_style": "calm_discussion",
        "boundaries": ["mutual_respect"],
        "dealbreakers": ["apathy", "carelessness"],
        "wants_children": "yes",
        "marriage_timeline": "2_to_3_years",
        "shareable_intro": "Dậy sớm làm bánh, tập yoga và quan tâm chăm sóc gia đình."
    },
    # 7. Khang - Nam 25 - TP.HCM
    {
        "id": "candidate_007",
        "display_name": "Khang",
        "age": 25,
        "gender": "male",
        "interested_in": ["female"],
        "city": "TP.HCM",
        "occupation": "Kỹ sư Cơ khí",
        "relationship_goal": "long_term",
        "relationship_pace": "slow",
        "communication_style": "calm",
        "social_level": 2,
        "lifestyle": ["motorbikes", "gaming", "fishing", "camping"],
        "core_values": ["realism", "independence", "simplicity"],
        "affection_preferences": ["physical_touch", "acts_of_service"],
        "conflict_style": "need_space",
        "boundaries": ["needs_personal_space"],
        "dealbreakers": ["drama", "excessive_demands"],
        "wants_children": "undecided",
        "marriage_timeline": "3_to_5_years",
        "shareable_intro": "Đi phượt cắm trại, ít nói nhưng chu đáo và thích tự tay làm đồ gỗ."
    },
    # 8. Thảo - Nữ 24 - TP.HCM
    {
        "id": "candidate_008",
        "display_name": "Thảo",
        "age": 24,
        "gender": "female",
        "interested_in": ["male"],
        "city": "TP.HCM",
        "occupation": "Lập trình viên AI",
        "relationship_goal": "long_term",
        "relationship_pace": "slow",
        "communication_style": "logical_direct",
        "social_level": 2,
        "lifestyle": ["coding", "manga", "gaming", "coffee"],
        "core_values": ["intellect", "truth", "free_thought"],
        "affection_preferences": ["quality_time"],
        "conflict_style": "calm_discussion",
        "boundaries": ["respect_intellectual_space"],
        "dealbreakers": ["illogical_behavior", "overly_emotional"],
        "wants_children": "no",
        "marriage_timeline": "not_priority",
        "shareable_intro": "Thích phân tích dữ liệu, đọc manga và đàm đạo tri thức ở quán cà phê đêm."
    },
    # 9. Đức - Nam 27 - Đà Nẵng
    {
        "id": "candidate_009",
        "display_name": "Đức",
        "age": 27,
        "gender": "male",
        "interested_in": ["female"],
        "city": "Đà Nẵng",
        "occupation": "Kiến trúc sư",
        "relationship_goal": "marriage",
        "relationship_pace": "slow",
        "communication_style": "gentle_direct",
        "social_level": 2,
        "lifestyle": ["chess", "reading", "astronomy", "quiet_coffee"],
        "core_values": ["knowledge", "depth", "independence"],
        "affection_preferences": ["quality_time"],
        "conflict_style": "calm_discussion",
        "boundaries": ["needs_quiet_time"],
        "dealbreakers": ["superficiality", "lack_of_goals"],
        "wants_children": "yes",
        "marriage_timeline": "1_to_2_years",
        "shareable_intro": "Hướng nội, mê thiên văn học, cờ vua và xây dựng mái ấm gia đình sâu sắc."
    },
    # 10. Mai - Nữ 24 - Đà Nẵng
    {
        "id": "candidate_010",
        "display_name": "Mai",
        "age": 24,
        "gender": "female",
        "interested_in": ["male"],
        "city": "Đà Nẵng",
        "occupation": "Giáo viên Tiếng Anh",
        "relationship_goal": "long_term",
        "relationship_pace": "medium",
        "communication_style": "expressive",
        "social_level": 4,
        "lifestyle": ["volunteering", "dancing", "travel", "blogging"],
        "core_values": ["connection", "empathy", "personal_growth"],
        "affection_preferences": ["words_of_affirmation", "quality_time"],
        "conflict_style": "calm_discussion",
        "boundaries": ["respect_volunteer_work"],
        "dealbreakers": ["selfishness", "lack_of_empathy"],
        "wants_children": "yes",
        "marriage_timeline": "2_to_3_years",
        "shareable_intro": "Thích kết nối cộng đồng, đi tình nguyện và lan tỏa năng lượng tích cực."
    },
    # 11. Phúc - Nam 24 - Đà Nẵng
    {
        "id": "candidate_011",
        "display_name": "Phúc",
        "age": 24,
        "gender": "male",
        "interested_in": ["female"],
        "city": "Đà Nẵng",
        "occupation": "Nhiếp ảnh gia Freelance",
        "relationship_goal": "casual_to_serious",
        "relationship_pace": "slow",
        "communication_style": "gentle_direct",
        "social_level": 2,
        "lifestyle": ["painting", "photography", "indie_music", "surfing"],
        "core_values": ["beauty", "freedom", "peace", "authentic_emotions"],
        "affection_preferences": ["receiving_gifts", "quality_time"],
        "conflict_style": "need_space",
        "boundaries": ["needs_artistic_freedom"],
        "dealbreakers": ["rudeness", "lack_of_aesthetic_sense"],
        "wants_children": "undecided",
        "marriage_timeline": "someday",
        "shareable_intro": "Lướt sóng biển Đà Nẵng, nghe nhạc Indie và yêu những khoảnh khắc chân thật."
    },
    # 12. Hà - Nữ 25 - Đà Nẵng
    {
        "id": "candidate_012",
        "display_name": "Hà",
        "age": 25,
        "gender": "female",
        "interested_in": ["male"],
        "city": "Đà Nẵng",
        "occupation": "Quản lý Marketing",
        "relationship_goal": "long_term",
        "relationship_pace": "medium",
        "communication_style": "logical_direct",
        "social_level": 4,
        "lifestyle": ["gym", "tennis", "business_books", "travel"],
        "core_values": ["ambition", "efficiency", "excellence"],
        "affection_preferences": ["words_of_affirmation", "acts_of_service"],
        "conflict_style": "express_immediately",
        "boundaries": ["respect_career_goals"],
        "dealbreakers": ["lack_of_ambition", "no_plan_in_life"],
        "wants_children": "yes",
        "marriage_timeline": "2_to_3_years",
        "shareable_intro": "Năng động, chơi tennis, có định hướng sự nghiệp rõ ràng và tham vọng."
    },
    # 13. An - Nam 23 - Huế
    {
        "id": "candidate_013",
        "display_name": "An",
        "age": 23,
        "gender": "male",
        "interested_in": ["female"],
        "city": "Huế",
        "occupation": "Kế toán viên",
        "relationship_goal": "marriage",
        "relationship_pace": "slow",
        "communication_style": "gentle_direct",
        "social_level": 2,
        "lifestyle": ["cooking", "reading", "running", "aquarium"],
        "core_values": ["family", "loyalty", "stability", "hard_work"],
        "affection_preferences": ["acts_of_service", "quality_time"],
        "conflict_style": "calm_discussion",
        "boundaries": ["financial_transparency"],
        "dealbreakers": ["betrayal", "extravagance"],
        "wants_children": "yes",
        "marriage_timeline": "1_to_2_years",
        "shareable_intro": "Sống chậm ở Cố đô, thích chạy bộ bờ sông Hương và quan niệm gia đình là nhất."
    },
    # 14. Thy - Nữ 22 - Huế
    {
        "id": "candidate_014",
        "display_name": "Thy",
        "age": 22,
        "gender": "female",
        "interested_in": ["male"],
        "city": "Huế",
        "occupation": "Chuyên viên Sáng tạo Nội dung",
        "relationship_goal": "casual_to_serious",
        "relationship_pace": "medium",
        "communication_style": "humorous",
        "social_level": 4,
        "lifestyle": ["modern_dance", "travel", "street_food", "tiktok"],
        "core_values": ["joy", "freedom", "friendship"],
        "affection_preferences": ["physical_touch", "words_of_affirmation"],
        "conflict_style": "express_immediately",
        "boundaries": ["dislikes_controlling_behavior"],
        "dealbreakers": ["patriarchal_attitude", "boring"],
        "wants_children": "undecided",
        "marriage_timeline": "someday",
        "shareable_intro": "Vui vẻ, nhảy hiện đại, yêu ẩm thực đường phố và tận hưởng từng khoảnh khắc."
    },
    # 15. Hùng - Nam 27 - Cần Thơ
    {
        "id": "candidate_015",
        "display_name": "Hùng",
        "age": 27,
        "gender": "male",
        "interested_in": ["female"],
        "city": "Cần Thơ",
        "occupation": "Kỹ sư Nông nghiệp",
        "relationship_goal": "long_term",
        "relationship_pace": "medium",
        "communication_style": "direct",
        "social_level": 4,
        "lifestyle": ["football", "motorbikes", "fishing", "gardening"],
        "core_values": ["freedom", "courage", "honesty", "loyalty"],
        "affection_preferences": ["physical_touch", "acts_of_service"],
        "conflict_style": "calm_discussion",
        "boundaries": ["mutual_respect"],
        "dealbreakers": ["dishonesty", "talk_no_action"],
        "wants_children": "yes",
        "marriage_timeline": "2_to_3_years",
        "shareable_intro": "Thẳng thắn, thích đá bóng, thích đi phượt sông nước miền Tây."
    },
    # 16. Ngọc - Nữ 24 - Cần Thơ
    {
        "id": "candidate_016",
        "display_name": "Ngọc",
        "age": 24,
        "gender": "female",
        "interested_in": ["male"],
        "city": "Cần Thơ",
        "occupation": "Nhà thơ / Biên tập sách",
        "relationship_goal": "long_term",
        "relationship_pace": "slow",
        "communication_style": "gentle_direct",
        "social_level": 1,
        "lifestyle": ["journaling", "painting", "poetry", "nature_walks"],
        "core_values": ["soul_connection", "authenticity", "art"],
        "affection_preferences": ["quality_time", "words_of_affirmation"],
        "conflict_style": "need_space",
        "boundaries": ["needs_quiet_time"],
        "dealbreakers": ["rudeness", "extreme_materialism"],
        "wants_children": "undecided",
        "marriage_timeline": "3_to_5_years",
        "shareable_intro": "Lãng mạn, hướng nội, yêu thi văn, đi dạo bến Ninh Kiều và trân trọng sự chân thành."
    },
    # 17. Bình - Nam 29 - TP.HCM
    {
        "id": "candidate_017",
        "display_name": "Bình",
        "age": 29,
        "gender": "male",
        "interested_in": ["female"],
        "city": "TP.HCM",
        "occupation": "Huấn luyện viên Fitness",
        "relationship_goal": "casual_to_serious",
        "relationship_pace": "fast",
        "communication_style": "expressive",
        "social_level": 5,
        "lifestyle": ["gym", "dancing", "beach", "nightlife"],
        "core_values": ["joy", "present_moment", "excitement"],
        "affection_preferences": ["physical_touch", "quality_time"],
        "conflict_style": "express_immediately",
        "boundaries": ["respect_fitness_routine"],
        "dealbreakers": ["boredom", "extreme_introversion"],
        "wants_children": "no",
        "marriage_timeline": "someday",
        "shareable_intro": "Năng lượng dồi dào, tập gym hàng ngày, thích biển và tiệc tùng năng động."
    },
    # 18. Vy - Nữ 22 - TP.HCM
    {
        "id": "candidate_018",
        "display_name": "Vy",
        "age": 22,
        "gender": "female",
        "interested_in": ["male"],
        "city": "TP.HCM",
        "occupation": "Chuyên viên Phân tích Tài chính",
        "relationship_goal": "long_term",
        "relationship_pace": "slow",
        "communication_style": "logical_direct",
        "social_level": 3,
        "lifestyle": ["gym", "running", "financial_planning", "self_help"],
        "core_values": ["discipline", "career", "punctuality", "goals"],
        "affection_preferences": ["acts_of_service", "words_of_affirmation"],
        "conflict_style": "calm_discussion",
        "boundaries": ["respect_time_management"],
        "dealbreakers": ["laziness", "lack_of_ambition"],
        "wants_children": "yes",
        "marriage_timeline": "3_to_5_years",
        "shareable_intro": "Kỷ luật cao, dậy sớm chạy bộ, có kế hoạch tài chính rõ ràng cho tương lai."
    },
    # 19. Hoàng - Nam 26 - Hà Nội
    {
        "id": "candidate_019",
        "display_name": "Hoàng",
        "age": 26,
        "gender": "male",
        "interested_in": ["female"],
        "city": "Hà Nội",
        "occupation": "Nhạc sĩ / Producer",
        "relationship_goal": "long_term",
        "relationship_pace": "slow",
        "communication_style": "gentle_direct",
        "social_level": 2,
        "lifestyle": ["piano", "acoustic_guitar", "coffee", "night_owl"],
        "core_values": ["art", "authenticity", "empathy"],
        "affection_preferences": ["quality_time", "words_of_affirmation"],
        "conflict_style": "calm_discussion",
        "boundaries": ["needs_creative_space"],
        "dealbreakers": ["dishonesty", "materialism"],
        "wants_children": "undecided",
        "marriage_timeline": "3_to_5_years",
        "shareable_intro": "Sáng tác nhạc đêm, chơi piano và trân trọng sự hòa hợp tâm hồn."
    },
    # 20. Yến - Nữ 23 - TP.HCM
    {
        "id": "candidate_020",
        "display_name": "Yến",
        "age": 23,
        "gender": "female",
        "interested_in": ["male"],
        "city": "TP.HCM",
        "occupation": "Fashion Stylist",
        "relationship_goal": "long_term",
        "relationship_pace": "medium",
        "communication_style": "expressive",
        "social_level": 4,
        "lifestyle": ["fashion", "art_exhibitions", "coffee", "travel"],
        "core_values": ["aesthetic", "creativity", "open_mindedness"],
        "affection_preferences": ["receiving_gifts", "quality_time"],
        "conflict_style": "calm_discussion",
        "boundaries": ["respect_personal_style"],
        "dealbreakers": ["conservatism", "judging_others"],
        "wants_children": "no",
        "marriage_timeline": "someday",
        "shareable_intro": "Yêu thời trang, đi triển lãm nghệ thuật và tìm kiếm sự thấu hiểu thẩm mỹ."
    },
    # 21. Tuấn - Nam 25 - TP.HCM
    {
        "id": "candidate_021",
        "display_name": "Tuấn",
        "age": 25,
        "gender": "male",
        "interested_in": ["female"],
        "city": "TP.HCM",
        "occupation": "Bác sĩ Đa khoa",
        "relationship_goal": "marriage",
        "relationship_pace": "slow",
        "communication_style": "gentle_direct",
        "social_level": 3,
        "lifestyle": ["reading", "running", "badminton", "coffee"],
        "core_values": ["care", "responsibility", "family"],
        "affection_preferences": ["acts_of_service", "quality_time"],
        "conflict_style": "calm_discussion",
        "boundaries": ["respect_work_shifts"],
        "dealbreakers": ["irresponsibility", "dishonesty"],
        "wants_children": "yes",
        "marriage_timeline": "1_to_2_years",
        "shareable_intro": "Bác sĩ trẻ điềm tĩnh, có tinh thần trách nhiệm cao và mong muốn dựng xây gia đình."
    },
    # 22. Quỳnh - Nữ 26 - Hà Nội
    {
        "id": "candidate_022",
        "display_name": "Quỳnh",
        "age": 26,
        "gender": "female",
        "interested_in": ["male"],
        "city": "Hà Nội",
        "occupation": "Luật sư Doanh nghiệp",
        "relationship_goal": "long_term",
        "relationship_pace": "slow",
        "communication_style": "logical_direct",
        "social_level": 3,
        "lifestyle": ["reading", "tennis", "wine", "classical_music"],
        "core_values": ["justice", "integrity", "family"],
        "affection_preferences": ["quality_time", "words_of_affirmation"],
        "conflict_style": "calm_discussion",
        "boundaries": ["respect_confidentiality"],
        "dealbreakers": ["dishonesty", "disloyalty"],
        "wants_children": "yes",
        "marriage_timeline": "2_to_3_years",
        "shareable_intro": "Sống theo nguyên tắc, điềm tĩnh, thích nghe nhạc cổ điển và coi trọng sự trung thực."
    },
    # 23. Bảo - Nam 24 - Đà Nẵng
    {
        "id": "candidate_023",
        "display_name": "Bảo",
        "age": 24,
        "gender": "male",
        "interested_in": ["female"],
        "city": "Đà Nẵng",
        "occupation": "Huấn luyện viên Lướt sóng",
        "relationship_goal": "casual_to_serious",
        "relationship_pace": "medium",
        "communication_style": "humorous",
        "social_level": 4,
        "lifestyle": ["surfing", "skateboarding", "beach", "dogs"],
        "core_values": ["freedom", "positivity", "nature"],
        "affection_preferences": ["physical_touch", "quality_time"],
        "conflict_style": "calm_discussion",
        "boundaries": ["love_for_nature"],
        "dealbreakers": ["overly_materialistic", "pessimism"],
        "wants_children": "undecided",
        "marriage_timeline": "someday",
        "shareable_intro": "Phóng khoáng, gắn liền với sóng biển và thiên nhiên, thích phong cách tự do."
    },
    # 24. Chi - Nữ 23 - Hà Nội
    {
        "id": "candidate_024",
        "display_name": "Chi",
        "age": 23,
        "gender": "female",
        "interested_in": ["male"],
        "city": "Hà Nội",
        "occupation": "Nhà Quản lý Thư viện / Khảo cứu",
        "relationship_goal": "long_term",
        "relationship_pace": "slow",
        "communication_style": "gentle_direct",
        "social_level": 1,
        "lifestyle": ["reading", "tea", "history", "museums"],
        "core_values": ["knowledge", "peace", "depth"],
        "affection_preferences": ["quality_time"],
        "conflict_style": "need_space",
        "boundaries": ["needs_quiet_space"],
        "dealbreakers": ["loudness", "vulgarity"],
        "wants_children": "yes",
        "marriage_timeline": "3_to_5_years",
        "shareable_intro": "Thích không gian tĩnh mịch của thư viện, uống trà nóng và đọc sách lịch sử."
    },
    # 25. Vũ - Nam 27 - TP.HCM
    {
        "id": "candidate_025",
        "display_name": "Vũ",
        "age": 27,
        "gender": "male",
        "interested_in": ["female"],
        "city": "TP.HCM",
        "occupation": "Chuyên viên UI/UX",
        "relationship_goal": "long_term",
        "relationship_pace": "medium",
        "communication_style": "gentle_direct",
        "social_level": 3,
        "lifestyle": ["design", "coffee", "baking", "cats"],
        "core_values": ["empathy", "creativity", "harmony"],
        "affection_preferences": ["acts_of_service", "words_of_affirmation"],
        "conflict_style": "calm_discussion",
        "boundaries": ["dislikes_controlling_behavior"],
        "dealbreakers": ["dishonesty", "arrogance"],
        "wants_children": "yes",
        "marriage_timeline": "2_to_3_years",
        "shareable_intro": "Thiết kế sản phẩm tinh tế, yêu mèo và quan tâm đến cảm xúc của đối phương."
    }
]


def seed_database(db: Session = None):
    """Seed 25 ứng viên và 1 demo user vào cơ sở dữ liệu"""
    if db is None:
        init_db()
        db = SessionLocal()

    # 1. Seed Candidates
    existing_count = db.query(CandidateProfile).count()
    if existing_count < len(SAMPLE_CANDIDATES):
        for candidate_data in SAMPLE_CANDIDATES:
            existing = db.query(CandidateProfile).filter_by(id=candidate_data["id"]).first()
            if not existing:
                candidate = CandidateProfile(**candidate_data)
                db.add(candidate)
        db.commit()
        print(f"✅ [Seed] Đã cập nhật thành công {len(SAMPLE_CANDIDATES)} ứng viên mẫu!")

    # 2. Seed Default Demo User cho trải nghiệm ngay
    demo_user_id = "user_demo_01"
    existing_user = db.query(User).filter_by(id=demo_user_id).first()
    if not existing_user:
        hashed_pwd = hashlib.sha256("password123".encode()).hexdigest()
        demo_user = User(
            id=demo_user_id,
            email="demo@cupid.ai",
            password_hash=hashed_pwd,
            display_name="Người dùng Demo"
        )
        db.add(demo_user)
        db.commit()

        # Seed sẵn một số Approved Memories tiêu chuẩn cho demo user
        sample_memories = [
            {
                "owner_id": demo_user_id,
                "category": "social_preference",
                "key": "introvert",
                "value": "Hướng nội, thích cuối tuần yên tĩnh",
                "human_readable_value": "Hướng nội, thích dành thời gian quán cà phê hoặc đọc sách.",
                "confidence": 0.9,
                "stability": "stable",
                "sensitivity": "personal",
                "visibility": "MATCH_USE",
                "user_confirmed": True
            },
            {
                "owner_id": demo_user_id,
                "category": "relationship_goal",
                "key": "long_term",
                "value": "Mối quan hệ nghiêm túc lâu dài",
                "human_readable_value": "Muốn một mối quan hệ nghiêm túc.",
                "confidence": 0.95,
                "stability": "stable",
                "sensitivity": "normal",
                "visibility": "MATCH_USE",
                "user_confirmed": True
            },
            {
                "owner_id": demo_user_id,
                "category": "relationship_pace",
                "key": "slow",
                "value": "Tìm hiểu từ từ",
                "human_readable_value": "Thích tiến triển mối quan hệ từ từ.",
                "confidence": 0.88,
                "stability": "stable",
                "sensitivity": "normal",
                "visibility": "MATCH_USE",
                "user_confirmed": True
            },
            {
                "owner_id": demo_user_id,
                "category": "dealbreaker",
                "key": "dislikes_controlling_behavior",
                "value": "Không thích người quá kiểm soát",
                "human_readable_value": "Dị ứng với hành vi kiểm soát quá đà.",
                "confidence": 0.92,
                "stability": "stable",
                "sensitivity": "personal",
                "visibility": "MATCH_USE",
                "user_confirmed": True
            },
            {
                "owner_id": demo_user_id,
                "category": "lifestyle",
                "key": "coffee_reading",
                "value": "Cà phê & Đọc sách",
                "human_readable_value": "Thích đọc sách và cà phê yên tĩnh cuối tuần.",
                "confidence": 0.85,
                "stability": "stable",
                "sensitivity": "normal",
                "visibility": "SHAREABLE",
                "user_confirmed": True
            }
        ]

        for m_data in sample_memories:
            db.add(ApprovedMemory(**m_data))
        db.commit()
        print("✅ [Seed] Đã tạo thành công Demo User & Hồ sơ mẫu ban đầu!")


if __name__ == "__main__":
    seed_database()
