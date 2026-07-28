"""
💾 MOCK DATABASE - CUPID AGENT (Dành cho Role 1: Data & Test Case Designer)
Dữ liệu giả lập hồ sơ người dùng và ma trận tương thích MBTI cho hệ thống ghép đôi.
"""

# ============================================================
# 📋 DATABASE HỒ SƠ NGƯỜI DÙNG (20 profiles)
# Mỗi profile gồm: name, gender, age, mbti, zodiac,
# love_language, hobbies, lifestyle, values, dealbreakers, location
# ============================================================

MOCK_USER_PROFILES = {
    # ── HÀ NỘI ──────────────────────────────────────────────
    "nam": {
        "name": "Nam",
        "gender": "Nam",
        "age": 24,
        "mbti": "ENFP",
        "zodiac": "Song Tử",
        "love_language": "Cử chỉ yêu thương",
        "hobbies": ["du lịch", "nhiếp ảnh", "cà phê phượt", "mèo", "nấu ăn"],
        "lifestyle": "Thức khuya, hướng ngoại, thích phiêu lưu",
        "values": "Coi trọng tự do, sáng tạo, sống cảm xúc",
        "dealbreakers": ["hút thuốc", "kiểm soát quá đà"],
        "location": "Hà Nội"
    },
    "linh": {
        "name": "Linh",
        "gender": "Nữ",
        "age": 23,
        "mbti": "INFJ",
        "zodiac": "Bọ Cạp",
        "love_language": "Thời gian bên nhau",
        "hobbies": ["đọc sách", "vẽ tranh", "mèo", "cà phê yên tĩnh", "thiền"],
        "lifestyle": "Dậy sớm, hướng nội, thích không gian yên tĩnh",
        "values": "Sâu sắc, thấu hiểu, chân thành, gia đình",
        "dealbreakers": ["ồn ào bừa bãi", "dối trá"],
        "location": "Hà Nội"
    },
    "trang": {
        "name": "Trang",
        "gender": "Nữ",
        "age": 22,
        "mbti": "ENFP",
        "zodiac": "Nhân Mã",
        "love_language": "Lời khen ngợi",
        "hobbies": ["đi đu concert", "du lịch", "ăn uống", "chó cảnh"],
        "lifestyle": "Sôi nổi, hướng ngoại, ngẫu hứng",
        "values": "Vui vẻ, trải nghiệm mới, bạn bè",
        "dealbreakers": ["gia trưởng", "quá nghiêm túc"],
        "location": "Hà Nội"
    },
    "hoa": {
        "name": "Hoa",
        "gender": "Nữ",
        "age": 25,
        "mbti": "ESFJ",
        "zodiac": "Cự Giải",
        "love_language": "Hành động phục vụ",
        "hobbies": ["nấu ăn", "làm bánh", "yoga", "chăm sóc cây cảnh", "mèo"],
        "lifestyle": "Dậy sớm, chu đáo, thích chăm sóc mọi người",
        "values": "Gia đình, sự ổn định, quan tâm chăm sóc, trung thành",
        "dealbreakers": ["vô tâm", "không biết quan tâm"],
        "location": "Hà Nội"
    },
    "long": {
        "name": "Long",
        "gender": "Nam",
        "age": 28,
        "mbti": "ENTP",
        "zodiac": "Bảo Bình",
        "love_language": "Lời khen ngợi",
        "hobbies": ["tranh luận", "podcast", "cờ vua", "startup", "du lịch"],
        "lifestyle": "Thức khuya, hướng ngoại, thích thách thức",
        "values": "Đổi mới, trí tuệ, hài hước, dám khác biệt",
        "dealbreakers": ["bảo thủ", "thiếu logic"],
        "location": "Hà Nội"
    },
    "ngan": {
        "name": "Ngân",
        "gender": "Nữ",
        "age": 24,
        "mbti": "ISFJ",
        "zodiac": "Kim Ngưu",
        "love_language": "Hành động phục vụ",
        "hobbies": ["nấu ăn", "đan len", "đọc sách", "chăm sóc cây cảnh", "xem phim"],
        "lifestyle": "Dậy sớm, hướng nội, thích cuộc sống bình yên",
        "values": "Gia đình, lòng trung thành, sự hy sinh, ổn định",
        "dealbreakers": ["phản bội", "vô trách nhiệm"],
        "location": "Hà Nội"
    },
    "tuan": {
        "name": "Tuấn",
        "gender": "Nam",
        "age": 26,
        "mbti": "INFP",
        "zodiac": "Song Ngư",
        "love_language": "Thời gian bên nhau",
        "hobbies": ["viết truyện", "guitar", "đọc sách", "xem phim", "đi dạo"],
        "lifestyle": "Thức khuya, hướng nội, mơ mộng và lãng mạn",
        "values": "Sự chân thành, nghệ thuật, cảm xúc, tâm hồn",
        "dealbreakers": ["thực dụng quá mức", "thiếu lãng mạn"],
        "location": "Hà Nội"
    },

    # ── TP.HCM ───────────────────────────────────────────────
    "minh": {
        "name": "Minh",
        "gender": "Nam",
        "age": 26,
        "mbti": "ESTJ",
        "zodiac": "Ma Kết",
        "love_language": "Hành động phục vụ",
        "hobbies": ["chơi chứng khoán", "gym", "chạy bộ", "công nghệ"],
        "lifestyle": "Kỷ luật, thích lập kế hoạch, ngăn nắp",
        "values": "Sự nghiệp, thực tế, đúng giờ, tham vọng",
        "dealbreakers": ["thức khuya lười biếng", "hút thuốc"],
        "location": "TP.HCM"
    },
    "khang": {
        "name": "Khang",
        "gender": "Nam",
        "age": 25,
        "mbti": "ISTP",
        "zodiac": "Xử Nữ",
        "love_language": "Cử chỉ yêu thương",
        "hobbies": ["sửa xe", "đi phượt", "game", "câu cá", "nấu ăn"],
        "lifestyle": "Linh hoạt, ít nói, thích tự do và hành động",
        "values": "Thực tế, tự lập, kiên nhẫn, giản dị",
        "dealbreakers": ["drama queen", "đòi hỏi quá nhiều"],
        "location": "TP.HCM"
    },
    "thao": {
        "name": "Thảo",
        "gender": "Nữ",
        "age": 23,
        "mbti": "INTP",
        "zodiac": "Bảo Bình",
        "love_language": "Thời gian bên nhau",
        "hobbies": ["lập trình", "đọc manga", "game", "nghiên cứu khoa học", "cà phê"],
        "lifestyle": "Thức khuya, hướng nội, thích phân tích và khám phá",
        "values": "Tri thức, sự thật, tự do tư duy, logic",
        "dealbreakers": ["thiếu logic", "quá cảm tính"],
        "location": "TP.HCM"
    },
    "binh": {
        "name": "Bình",
        "gender": "Nam",
        "age": 29,
        "mbti": "ESFP",
        "zodiac": "Sư Tử",
        "love_language": "Cử chỉ yêu thương",
        "hobbies": ["nhảy múa", "karaoke", "ăn uống", "đi bar", "du lịch biển"],
        "lifestyle": "Hướng ngoại, vui vẻ, thích làm trung tâm chú ý",
        "values": "Niềm vui, khoảnh khắc hiện tại, sự phấn khích, bạn bè",
        "dealbreakers": ["nhàm chán", "quá khép kín"],
        "location": "TP.HCM"
    },
    "vy": {
        "name": "Vy",
        "gender": "Nữ",
        "age": 22,
        "mbti": "ESTJ",
        "zodiac": "Ma Kết",
        "love_language": "Hành động phục vụ",
        "hobbies": ["gym", "chạy bộ", "quản lý tài chính", "đọc sách self-help"],
        "lifestyle": "Kỷ luật, dậy sớm, thích mọi thứ có kế hoạch",
        "values": "Sự nghiệp, kỷ luật, đúng giờ, mục tiêu rõ ràng",
        "dealbreakers": ["lười biếng", "không có chí tiến thủ"],
        "location": "TP.HCM"
    },

    # ── ĐÀ NẴNG ──────────────────────────────────────────────
    "duc": {
        "name": "Đức",
        "gender": "Nam",
        "age": 27,
        "mbti": "INTJ",
        "zodiac": "Bảo Bình",
        "love_language": "Thời gian bên nhau",
        "hobbies": ["cờ vua", "đọc sách", "lập trình", "thiên văn học", "cà phê yên tĩnh"],
        "lifestyle": "Hướng nội, thức khuya, thích nghiên cứu một mình",
        "values": "Tri thức, logic, chiều sâu, độc lập",
        "dealbreakers": ["hời hợt", "không có mục tiêu sống"],
        "location": "Đà Nẵng"
    },
    "mai": {
        "name": "Mai",
        "gender": "Nữ",
        "age": 24,
        "mbti": "ENFJ",
        "zodiac": "Sư Tử",
        "love_language": "Lời khen ngợi",
        "hobbies": ["tình nguyện", "nhảy hiện đại", "du lịch", "nấu ăn", "viết blog"],
        "lifestyle": "Hướng ngoại, năng động, thích truyền cảm hứng",
        "values": "Sự kết nối, đồng cảm, phát triển bản thân, cộng đồng",
        "dealbreakers": ["ích kỷ", "thiếu đồng cảm"],
        "location": "Đà Nẵng"
    },
    "phuc": {
        "name": "Phúc",
        "gender": "Nam",
        "age": 24,
        "mbti": "ISFP",
        "zodiac": "Thiên Bình",
        "love_language": "Quà tặng",
        "hobbies": ["vẽ tranh", "chụp ảnh", "nghe nhạc indie", "lướt sóng", "cà phê"],
        "lifestyle": "Hướng nội, sống chậm, thích thẩm mỹ và nghệ thuật",
        "values": "Cái đẹp, sự tự do, bình yên, cảm xúc chân thật",
        "dealbreakers": ["ồn ào thô lỗ", "thiếu thẩm mỹ"],
        "location": "Đà Nẵng"
    },
    "ha": {
        "name": "Hà",
        "gender": "Nữ",
        "age": 25,
        "mbti": "ENTJ",
        "zodiac": "Bạch Dương",
        "love_language": "Lời khen ngợi",
        "hobbies": ["startup", "gym", "du lịch", "đọc sách kinh doanh", "tennis"],
        "lifestyle": "Hướng ngoại, quyết đoán, thích dẫn dắt",
        "values": "Tham vọng, hiệu quả, sự xuất sắc, tầm nhìn xa",
        "dealbreakers": ["thiếu tham vọng", "không có kế hoạch"],
        "location": "Đà Nẵng"
    },

    # ── HUẾ ───────────────────────────────────────────────────
    "an": {
        "name": "An",
        "gender": "Nam",
        "age": 23,
        "mbti": "ISFJ",
        "zodiac": "Cự Giải",
        "love_language": "Hành động phục vụ",
        "hobbies": ["nấu ăn", "đọc sách", "chạy bộ", "chăm cá cảnh", "xem phim"],
        "lifestyle": "Dậy sớm, hướng nội, hiền lành, thích cuộc sống giản dị",
        "values": "Gia đình, trung thành, sự ổn định, chăm chỉ",
        "dealbreakers": ["phản bội", "tiêu xài hoang phí"],
        "location": "Huế"
    },
    "thy": {
        "name": "Thy",
        "gender": "Nữ",
        "age": 22,
        "mbti": "ESFP",
        "zodiac": "Nhân Mã",
        "love_language": "Cử chỉ yêu thương",
        "hobbies": ["nhảy hiện đại", "du lịch", "ăn vặt", "karaoke", "tiktok"],
        "lifestyle": "Hướng ngoại, vui vẻ, thích ngẫu hứng",
        "values": "Niềm vui, tự do, bạn bè, khoảnh khắc sống",
        "dealbreakers": ["gia trưởng", "nhàm chán"],
        "location": "Huế"
    },

    # ── CẦN THƠ ──────────────────────────────────────────────
    "hung": {
        "name": "Hùng",
        "gender": "Nam",
        "age": 27,
        "mbti": "ESTP",
        "zodiac": "Bạch Dương",
        "love_language": "Cử chỉ yêu thương",
        "hobbies": ["đá bóng", "đi phượt", "câu cá", "nhậu bạn bè", "sửa xe"],
        "lifestyle": "Hướng ngoại, mạo hiểm, thích hành động hơn nói",
        "values": "Tự do, dũng cảm, thẳng thắn, nghĩa khí",
        "dealbreakers": ["ẻo lả", "nói nhiều không làm"],
        "location": "Cần Thơ"
    },
    "ngoc": {
        "name": "Ngọc",
        "gender": "Nữ",
        "age": 24,
        "mbti": "INFP",
        "zodiac": "Song Ngư",
        "love_language": "Thời gian bên nhau",
        "hobbies": ["viết nhật ký", "vẽ tranh", "đọc thơ", "xem phim", "đi dạo sông"],
        "lifestyle": "Hướng nội, lãng mạn, mơ mộng, thích thiên nhiên",
        "values": "Tâm hồn, sự chân thành, nghệ thuật, ý nghĩa cuộc sống",
        "dealbreakers": ["thô lỗ", "thực dụng quá mức"],
        "location": "Cần Thơ"
    }
}


# ============================================================
# 🧩 MA TRẬN ĐỘ HỢP MBTI (% tương thích theo cặp)
# Dựa trên lý thuyết tương thích nhận thức MBTI
# Điểm cao = bổ trợ tốt, điểm thấp = dễ xung đột
# ============================================================

MBTI_COMPATIBILITY_MATRIX = {
    # ── Cặp đôi "vàng" (Golden Pairs) - Bổ trợ hoàn hảo ──
    ("ENFP", "INFJ"): 95,
    ("ENFJ", "INFP"): 95,
    ("ENTP", "INTJ"): 93,
    ("ENTJ", "INTP"): 93,
    ("ENFJ", "INTJ"): 90,
    ("ENFP", "INTJ"): 90,
    ("ENTP", "INFJ"): 88,
    ("ENTJ", "INFJ"): 85,

    # ── Cặp đôi tốt - Hợp nhau về nhiều mặt ──
    ("ENFP", "ENFJ"): 88,
    ("INFJ", "ENFJ"): 88,
    ("ENFP", "ENFP"): 85,
    ("INFJ", "INFJ"): 85,
    ("INFP", "INFJ"): 90,
    ("INFP", "ENFP"): 85,
    ("INFP", "INFP"): 82,
    ("ESFJ", "ISTP"): 82,
    ("ESFJ", "ISFP"): 80,
    ("ESFJ", "INFJ"): 78,
    ("ESFJ", "ENFP"): 80,
    ("ESFJ", "ENFJ"): 85,
    ("ESFJ", "ESFJ"): 80,
    ("ESFJ", "ISFJ"): 85,
    ("ISFJ", "ISFJ"): 82,
    ("ISFJ", "ESFP"): 78,
    ("ISFJ", "ESTP"): 75,
    ("ISFJ", "INFP"): 80,
    ("ISFJ", "ENFJ"): 82,
    ("ISTP", "ISTP"): 72,
    ("ISTP", "INTJ"): 75,
    ("ISTP", "ENFP"): 65,
    ("ISTP", "ESTP"): 78,
    ("ISFP", "ENFJ"): 85,
    ("ISFP", "ESFP"): 78,
    ("ISFP", "INFP"): 82,
    ("ISFP", "ISFP"): 75,
    ("ISFP", "INTJ"): 68,
    ("ENFJ", "ENFJ"): 82,
    ("ENFJ", "ISTP"): 70,
    ("ENFJ", "ENTJ"): 85,
    ("ENTP", "ENTP"): 80,
    ("ENTP", "ENFP"): 85,
    ("ENTP", "INFP"): 82,
    ("ENTP", "INTP"): 85,
    ("INTP", "INTJ"): 88,
    ("INTP", "INTP"): 78,
    ("INTP", "INFP"): 75,
    ("INTP", "ISTP"): 72,
    ("ENTJ", "ENTJ"): 78,
    ("ENTJ", "INTJ"): 85,
    ("ENTJ", "ENFP"): 80,
    ("ENTJ", "ESTJ"): 78,
    ("ESFP", "ESFP"): 78,
    ("ESFP", "ENFP"): 82,
    ("ESFP", "ESTP"): 80,
    ("ESFP", "ISTP"): 75,
    ("ESTP", "ESTP"): 75,
    ("ESTP", "ISTP"): 78,
    ("ESTP", "ENTJ"): 72,
    ("ESTP", "ENTP"): 75,

    # ── Cặp khó - Cần nỗ lực nhiều ──
    ("ENFP", "ESTJ"): 45,
    ("INFJ", "ESTJ"): 50,
    ("INFP", "ESTJ"): 42,
    ("INFP", "ESTP"): 48,
    ("INFJ", "ESTP"): 52,
    ("INTJ", "ESFP"): 45,
    ("INTJ", "ESFJ"): 55,
    ("INTP", "ESFJ"): 48,
    ("INTP", "ESFP"): 45,
    ("ESTJ", "ESTJ"): 75,
    ("ESTJ", "ISTP"): 68,
    ("ESTJ", "ESFJ"): 78,
    ("ESTJ", "INTJ"): 60,
    ("ESTJ", "ENFJ"): 55,
    ("ESTJ", "ISFJ"): 80,
    ("ESTJ", "ESFP"): 65,
    ("ESTJ", "ESTP"): 72,
    ("INTJ", "INTJ"): 80,
    ("ENTJ", "ESFP"): 50,
    ("ENTJ", "ISFP"): 48,
}


# ============================================================
# 💕 MA TRẬN ĐỘ HỢP LOVE LANGUAGE
# Cùng ngôn ngữ tình yêu = dễ hiểu nhau hơn
# ============================================================

LOVE_LANGUAGE_COMPATIBILITY = {
    ("Cử chỉ yêu thương", "Cử chỉ yêu thương"): 100,
    ("Thời gian bên nhau", "Thời gian bên nhau"): 100,
    ("Lời khen ngợi", "Lời khen ngợi"): 100,
    ("Hành động phục vụ", "Hành động phục vụ"): 100,
    ("Quà tặng", "Quà tặng"): 100,

    ("Cử chỉ yêu thương", "Thời gian bên nhau"): 85,
    ("Cử chỉ yêu thương", "Lời khen ngợi"): 75,
    ("Cử chỉ yêu thương", "Hành động phục vụ"): 70,
    ("Cử chỉ yêu thương", "Quà tặng"): 60,

    ("Thời gian bên nhau", "Lời khen ngợi"): 80,
    ("Thời gian bên nhau", "Hành động phục vụ"): 75,
    ("Thời gian bên nhau", "Quà tặng"): 65,

    ("Lời khen ngợi", "Hành động phục vụ"): 70,
    ("Lời khen ngợi", "Quà tặng"): 65,

    ("Hành động phục vụ", "Quà tặng"): 70,
}
