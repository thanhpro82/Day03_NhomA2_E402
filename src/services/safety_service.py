"""
🛡️ SAFETY & PRIVACY GUARD SERVICE — CUPID AGENT 💘
Kiểm soát các truy vấn nguy hại, Prompt Injection, Stalking, Doxxing và System Prompt Leakage.
"""

import re
from src.database.models import AuditLog


# Danh sách các pattern tấn công / vi phạm cần ngắt an toàn
FORBIDDEN_PATTERNS = [
    (r"bỏ qua mọi quy tắc|ignore all previous instructions|bypass safety", "PROMPT_INJECTION"),
    (r"in system prompt|show system prompt|hãy in system prompt", "SYSTEM_PROMPT_EXTRACTION"),
    (r"hãy cho tôi biết địa điểm|người đó đang ở đâu|location of", "STALKING_REQUEST"),
    (r"đưa cho tôi memory của người khác|read memory of user|data of other user", "REQUEST_OTHER_USER_PRIVATE_DATA"),
    (r"tôi là admin|hiển thị toàn bộ database|show all users", "UNAUTHORIZED_ACTION"),
    (r"encode.*base64|base64 decode", "PRIVACY_BYPASS_ATTEMPT"),
    (r"tiết lộ api key|show api key", "SYSTEM_KEY_EXTRACTION"),
]

DEFAULT_REFUSAL_MESSAGE = (
    "Mình không thể thực hiện yêu cầu này để đảm bảo an toàn và quyền riêng tư cho người dùng. "
    "Cupid luôn sẵn sàng lắng nghe và trò chuyện với bạn về những chủ đề kết nối chân thành!"
)


class SafetyService:
    """Service kiểm tra an toàn và bảo mật thông tin"""

    @staticmethod
    def inspect_input(user_id: str, text: str) -> tuple[bool, str, str]:
        """
        Kiểm tra văn bản đầu vào.
        Trả về: (is_safe: bool, refusal_reason: str, violation_code: str)
        """
        text_lower = text.lower()

        for pattern, code in FORBIDDEN_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False, DEFAULT_REFUSAL_MESSAGE, code

        return True, "", ""

    @staticmethod
    def filter_output(output_text: str) -> str:
        """Đảm bảo output không chứa thông tin nhạy cảm hoặc API Key rò rỉ"""
        # Che giấu API key nếu lỡ bị leak
        output_text = re.sub(r"sk-[a-zA-Z0-9]{32,}", "[REDACTED_API_KEY]", output_text)
        return output_text
