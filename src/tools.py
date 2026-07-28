"""
🛠️ TOOL REGISTRY & SCHEMAS - CUPID AGENT (Dành cho Role 2: Tool Engineer)
Nơi khai báo các công cụ ghép đôi, phân tích tương thích và mô phỏng hẹn hò cho ReAct Agent.
"""

import json

# Database giả lập thông tin người dùng (Mock Database)
MOCK_USER_PROFILES = {
    "nam": {
        "name": "Nam",
        "age": 24,
        "mbti": "ENFP",
        "hobbies": ["du lịch", "nhiếp ảnh", "cà phê phượt", "mèo"],
        "lifestyle": "Thức khuya, hướng ngoại, thích phiêu lưu",
        "values": "Coi trọng tự do, sáng tạo, sống cảm xúc",
        "dealbreakers": ["hút thuốc", "kiểm soát quá đà"],
        "location": "Hà Nội"
    },
    "linh": {
        "name": "Linh",
        "age": 23,
        "mbti": "INFJ",
        "hobbies": ["đọc sách", "vẽ tranh", "mèo", "cà phê yên tĩnh"],
        "lifestyle": "Dậy sớm, hướng nội, thích không gian yên tĩnh",
        "values": "Sâu sắc, thấu hiểu, chân thành, gia đình",
        "dealbreakers": ["ồn ào bừa bãi", "dối tráo"],
        "location": "Hà Nội"
    },
    "minh": {
        "name": "Minh",
        "age": 26,
        "mbti": "ESTJ",
        "hobbies": ["chơi chứng khoán", "gym", "chạy bộ", "công nghệ"],
        "lifestyle": "Kỷ luật, thích lập kế hoạch, ngăn nắp",
        "values": "Sự nghiệp, thực tế, đúng giờ, tham vọng",
        "dealbreakers": ["thức khuya lười biếng", "hút thuốc"],
        "location": "TP.HCM"
    },
    "trang": {
        "name": "Trang",
        "age": 22,
        "mbti": "ENFP",
        "hobbies": ["đi đu concert", "du lịch", "ăn uống", "chó cảnh"],
        "lifestyle": "Sôi nổi, hướng ngoại, ngẫu hứng",
        "values": "Vui vẻ, trải nghiệm mới, bạn bè",
        "dealbreakers": ["gia trưởng", "quá nghiêm túc"],
        "location": "Hà Nội"
    }
}

# Ma trận độ hợp MBTI cơ bản
MBTI_COMPATIBILITY_MATRIX = {
    ("ENFP", "INFJ"): 95,
    ("ENFP", "ENFP"): 85,
    ("ENFP", "ESTJ"): 45,
    ("INFJ", "ESTJ"): 50,
    ("INFJ", "INFJ"): 88,
    ("ESTJ", "ESTJ"): 75
}

def get_user_profile(user_name: str) -> str:
    """
    Tra cứu hồ sơ thông tin chi tiết của người dùng trong hệ thống ghép đôi Cupid.
    
    Args:
        user_name (str): Tên hoặc ID của người dùng (VD: 'Nam', 'Linh', 'Minh', 'Trang').
        
    Returns:
        str: Chuỗi JSON chứa thông tin hồ sơ (tuổi, MBTI, sở thích, lối sống, giá trị sống, dealbreakers, vị trí)
             hoặc thông báo lỗi nếu không tìm thấy.
    """
    try:
        if not user_name or not isinstance(user_name, str):
            return "LỖI: Tên người dùng không hợp lệ. Vui lòng nhập tên dạng chuỗi."
            
        key = user_name.strip().lower()
        if key in MOCK_USER_PROFILES:
            return json.dumps(MOCK_USER_PROFILES[key], ensure_ascii=False, indent=2)
        
        available = ", ".join([p["name"] for p in MOCK_USER_PROFILES.values()])
        return f"LỖI: Không tìm thấy hồ sơ cho '{user_name}'. Các hồ sơ hiện có trong hệ thống: {available}."
    except Exception as e:
        return f"LỖI HỆ THỐNG khi tra cứu hồ sơ: {str(e)}"


def calculate_compatibility_score(user_a: str, user_b: str) -> str:
    """
    Tính toán chỉ số % tương thích tổng quan và chi tiết giữa 2 hồ sơ người dùng.
    
    Args:
        user_a (str): Tên người dùng A (VD: 'Nam')
        user_b (str): Tên người dùng B (VD: 'Linh')
        
    Returns:
        str: Báo cáo phân tích % độ tương thích theo MBTI, sở thích chung, và các yếu tố đời sống.
    """
    try:
        key_a = user_a.strip().lower()
        key_b = user_b.strip().lower()
        
        if key_a not in MOCK_USER_PROFILES or key_b not in MOCK_USER_PROFILES:
            return f"LỖI: Không thể tính độ tương thích. Vui lòng đảm bảo cả '{user_a}' và '{user_b}' đều tồn tại trong hệ thống."
            
        prof_a = MOCK_USER_PROFILES[key_a]
        prof_b = MOCK_USER_PROFILES[key_b]
        
        # 1. MBTI Compatibility Score
        mbti_pair = (prof_a["mbti"], prof_b["mbti"])
        rev_pair = (prof_b["mbti"], prof_a["mbti"])
        mbti_score = MBTI_COMPATIBILITY_MATRIX.get(mbti_pair, MBTI_COMPATIBILITY_MATRIX.get(rev_pair, 70))
        
        # 2. Shared Hobbies Score
        hobbies_a = set(prof_a["hobbies"])
        hobbies_b = set(prof_b["hobbies"])
        shared_hobbies = hobbies_a.intersection(hobbies_b)
        hobby_score = min(100, len(shared_hobbies) * 25 + 40)
        
        # 3. Location Match
        location_score = 100 if prof_a["location"] == prof_b["location"] else 50
        
        # Overall Weighted Score
        overall = int(mbti_score * 0.5 + hobby_score * 0.3 + location_score * 0.2)
        
        result = (
            f"=== BÁO CÁO ĐỘ TƯƠNG THÍCH: {prof_a['name']} ❤️ {prof_b['name']} ===\n"
            f"🎯 Chỉ số tương thích tổng quan: {overall}%\n"
            f"🧩 Độ hợp MBTI ({prof_a['mbti']} - {prof_b['mbti']}): {mbti_score}%\n"
            f"🎨 Sở thích chung ({len(shared_hobbies)} điểm chung): {', '.join(shared_hobbies) if shared_hobbies else 'Không có'}\n"
            f"📍 Khoảng cách địa lý: {'Cùng khu vực (' + prof_a['location'] + ')' if location_score == 100 else 'Khác thành phố'}\n"
        )
        return result
    except Exception as e:
        return f"LỖI HỆ THỐNG khi tính toán độ tương thích: {str(e)}"


def extract_red_green_flags(user_a: str, user_b: str) -> str:
    """
    Trích xuất danh sách Green Flags (Điểm cộng tuyệt vời) và Red Flags (Cảnh báo bất đồng/Dealbreakers) giữa 2 người.
    
    Args:
        user_a (str): Tên người dùng A (VD: 'Nam')
        user_b (str): Tên người dùng B (VD: 'Linh')
        
    Returns:
        str: Phân tích danh sách Green Flags và Red Flags chi tiết.
    """
    try:
        key_a = user_a.strip().lower()
        key_b = user_b.strip().lower()
        
        if key_a not in MOCK_USER_PROFILES or key_b not in MOCK_USER_PROFILES:
            return f"LỖI: Không thể phân tích Green/Red Flags vì không tìm thấy hồ sơ của '{user_a}' hoặc '{user_b}'."
            
        prof_a = MOCK_USER_PROFILES[key_a]
        prof_b = MOCK_USER_PROFILES[key_b]
        
        green_flags = []
        red_flags = []
        
        # Green Flags Check
        shared_hobbies = set(prof_a["hobbies"]).intersection(set(prof_b["hobbies"]))
        if shared_hobbies:
            green_flags.append(f"Cùng sở thích: {', '.join(shared_hobbies)}")
        if (prof_a["mbti"], prof_b["mbti"]) in [("ENFP", "INFJ"), ("INFJ", "ENFP")]:
            green_flags.append("Cặp đôi MBTI 'vàng trong làng ghép đôi' (ENFP x INFJ - Bù trừ hoàn hảo)")
        if prof_a["location"] == prof_b["location"]:
            green_flags.append(f"Cùng ở {prof_a['location']}, dễ dàng gặp mặt trực tiếp")
            
        # Red Flags / Conflict Check
        if "hướng ngoại" in prof_a["lifestyle"].lower() and "hướng nội" in prof_b["lifestyle"].lower():
            red_flags.append(f"Lối sống đối lập: {prof_a['name']} ({prof_a['lifestyle']}) vs {prof_b['name']} ({prof_b['lifestyle']})")
        if "thức khuya" in prof_a["lifestyle"].lower() and "dậy sớm" in prof_b["lifestyle"].lower():
            red_flags.append("Lệch nhịp sinh học: Một người thích thức khuya, một người dậy sớm")
            
        result = (
            f"🚩/🟢 PHÂN TÍCH GREEN & RED FLAGS ({prof_a['name']} & {prof_b['name']}):\n\n"
            f"🟢 GREEN FLAGS (Điểm cộng):\n" + ("\n".join([f"  • {gf}" for gf in green_flags]) if green_flags else "  • Chưa phát hiện điểm cộng nổi bật.") + "\n\n"
            f"🚩 RED FLAGS (Cảnh báo rủi ro):\n" + ("\n".join([f"  • {rf}" for rf in red_flags]) if red_flags else "  • Tuyệt vời! Không phát hiện xung đột nguy hiểm.")
        )
        return result
    except Exception as e:
        return f"LỖI HỆ THỐNG khi phân tích Red/Green Flags: {str(e)}"


def simulate_date_chat(user_a: str, user_b: str, topic: str = "lần đầu gặp mặt") -> str:
    """
    Mô phỏng kịch bản trò chuyện / gợi ý chủ đề mở lời (Icebreaker) cho buổi hẹn hò đầu tiên.
    
    Args:
        user_a (str): Tên người dùng A (VD: 'Nam')
        user_b (str): Tên người dùng B (VD: 'Linh')
        topic (str): Bối cảnh hoặc chủ đề trò chuyện (Mặc định: 'lần đầu gặp mặt')
        
    Returns:
        str: Kịch bản hội thoại mẫu và các chủ đề mở lời lý tưởng dựa trên sở thích chung.
    """
    try:
        key_a = user_a.strip().lower()
        key_b = user_b.strip().lower()
        
        if key_a not in MOCK_USER_PROFILES or key_b not in MOCK_USER_PROFILES:
            return f"LỖI: Không thể mô phỏng trò chuyện. Thiếu thông tin hồ sơ cho '{user_a}' hoặc '{user_b}'."
            
        prof_a = MOCK_USER_PROFILES[key_a]
        prof_b = MOCK_USER_PROFILES[key_b]
        
        shared = set(prof_a["hobbies"]).intersection(set(prof_b["hobbies"]))
        icebreaker_topic = list(shared)[0] if shared else "những quán cà phê đẹp"
        
        result = (
            f"🎭 MÔ PHỎNG KỊCH BẢN HẸN HÒ: {prof_a['name']} & {prof_b['name']} ({topic.upper()})\n"
            f"📍 Gợi ý địa điểm: Quán cà phê yên tĩnh tại {prof_a['location']}\n"
            f"💡 Chủ đề Icebreaker đề xuất: Thảo luận về sở thích '{icebreaker_topic}'\n\n"
            f"💬 Đoạn chat mẫu:\n"
            f"• {prof_a['name']}: 'Chào {prof_b['name']}, mình thấy bạn cũng rất thích {icebreaker_topic}. Bạn hay ghé quán nào ở {prof_a['location']} thế?'\n"
            f"• {prof_b['name']}: 'Chào {prof_a['name']}! Mình hay ghé mấy quán yên tĩnh cuối tuần. Thật cờ cờ khi bạn cũng thích {icebreaker_topic} đấy!'\n"
        )
        return result
    except Exception as e:
        return f"LỖI HỆ THỐNG khi mô phỏng trò chuyện: {str(e)}"


# Danh sách các tool được đăng ký để ReAct Agent sử dụng
AVAILABLE_TOOLS = {
    "get_user_profile": get_user_profile,
    "calculate_compatibility_score": calculate_compatibility_score,
    "extract_red_green_flags": extract_red_green_flags,
    "simulate_date_chat": simulate_date_chat,
}
