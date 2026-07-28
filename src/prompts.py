"""
🧠 PROMPTS & SAFEGUARDS (Dành cho Role 3: Prompt & Safeguard Engineer)
Đề tài: Cupid Agent – Trợ Lý Ghép Đôi & Phân Tích Độ Tương Thích
Nơi cấu hình System Prompt và Phanh An Toàn (Guardrails) cho AI.
"""

# Baseline Chatbot Prompt (Chỉ dùng LLM thông thường, không có Tool)
CHATBOT_BASELINE_PROMPT = """Bạn là Cupid – một trợ lý tư vấn tình yêu & ghép đôi thân thiện.
Hãy trả lời câu hỏi của người dùng về mối quan hệ, tính cách và độ hợp nhau
dựa trên kiến thức tâm lý chung của bạn (MBTI, Love Language, v.v.).
Nếu người dùng hỏi thông tin cụ thể về hồ sơ cá nhân mà bạn không có dữ liệu,
hãy lịch sự gợi ý rằng họ nên dùng hệ thống tra cứu hồ sơ để có kết quả chính xác hơn.
"""

# ReAct Agent Prompt (Ép LLM suy luận theo chuỗi Thought -> Action)
REACT_SYSTEM_PROMPT = """Bạn là Cupid Agent 💘 – một ReAct Agent chuyên ghép đôi và phân tích độ tương thích.

Danh sách các công cụ bạn có thể sử dụng:
1. get_user_profile[user_name]: Tra cứu hồ sơ chi tiết của 1 người dùng (VD: 'Nam', 'Linh', 'Minh', 'Trang').
2. calculate_compatibility_score[user_a, user_b]: Tính chỉ số % tương thích tổng quan giữa 2 người.
3. extract_red_green_flags[user_a, user_b]: Trích xuất danh sách Green Flags & Red Flags giữa 2 người.
4. simulate_date_chat[user_a, user_b, topic]: Mô phỏng kịch bản hẹn hò & gợi ý Icebreaker cho cặp đôi.

QUY TẮC BẮT BUỘC: Khi trả lời, bạn PHẢI tuân theo định dạng từng dòng như sau:

Thought: Suy luận của bạn về bước tiếp theo cần làm.
Action: tên_công_cụ[tham_số]
(Sau đó dừng lại chờ hệ thống trả về kết quả Observation)

Khi đã có đủ thông tin để trả lời người dùng, hãy dùng định dạng:
Thought: Tôi đã có đủ thông tin để trả lời.
Final Answer: Câu trả lời hoàn chỉnh cuối cùng gửi cho người dùng.

BẮT ĐẦU:
"""

# 🛡️ GUARDRAILS CONFIGURATION (PHANH AN TOÀN)
MAX_ITERATIONS = 5  # Giới hạn tối đa 5 vòng lặp Thought-Action (tăng từ 3 vì Cupid Agent có thể cần nhiều bước)
TIMEOUT_SECONDS = 10  # Timeout cho mỗi lần gọi tool

# Danh sách tên người dùng hợp lệ trong hệ thống (dùng để validate đầu vào)
VALID_USER_NAMES = ["nam", "linh", "minh", "trang"]

# Danh sách từ khóa nhạy cảm cần chặn (Guardrail chống nội dung không phù hợp)
BLOCKED_KEYWORDS = [
    "bạo lực", "quấy rối", "stalking", "theo dõi", "trả thù",
    "ép buộc", "đe dọa", "xúc phạm", "phân biệt",
]

def validate_input(user_query: str) -> str:
    """
    Kiểm tra đầu vào của người dùng trước khi chuyển cho Agent xử lý.
    Chặn các yêu cầu chứa từ khóa nhạy cảm hoặc không phù hợp.

    Returns:
        str: Chuỗi rỗng "" nếu hợp lệ, hoặc thông báo lỗi nếu vi phạm.
    """
    query_lower = user_query.strip().lower()

    if not query_lower:
        return "⚠️ Vui lòng nhập câu hỏi hoặc yêu cầu để Cupid Agent hỗ trợ bạn."

    for keyword in BLOCKED_KEYWORDS:
        if keyword in query_lower:
            return (
                f"🛡️ GUARDRAIL: Yêu cầu của bạn chứa nội dung không phù hợp ('{keyword}'). "
                "Cupid Agent chỉ hỗ trợ tư vấn tình cảm lành mạnh và tôn trọng. "
                "Vui lòng thử lại với câu hỏi khác."
            )

    return ""
