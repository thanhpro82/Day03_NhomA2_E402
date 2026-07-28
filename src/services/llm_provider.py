"""
🤖 MULTI-PROVIDER LLM ADAPTER — CUPID AGENT 💘
Hỗ trợ OpenAI, Gemini và Smart Mock Provider Fallback.
"""

import json
import os
import re
from abc import ABC, abstractmethod
from src.config import (
    OPENAI_API_KEY,
    GEMINI_API_KEY,
    DEFAULT_PROVIDER,
    CUPID_SYSTEM_PROMPT,
    MEMORY_EXTRACTION_SYSTEM_PROMPT,
    MATCH_EXPLANATION_SYSTEM_PROMPT
)


class BaseLLMProvider(ABC):
    """Lớp cơ sở trừu tượng cho các nhà cung cấp LLM"""

    @abstractmethod
    def chat(self, messages: list, system_prompt: str = CUPID_SYSTEM_PROMPT) -> str:
        pass

    @abstractmethod
    def extract_memories(self, conversation_text: str) -> list:
        pass

    @abstractmethod
    def explain_match(self, match_data: dict, candidate_info: dict) -> str:
        pass


class MockLLMProvider(BaseLLMProvider):
    """Mock Provider thông minh chạy offline 100% khi chưa có API Key"""

    def chat(self, messages: list, system_prompt: str = CUPID_SYSTEM_PROMPT) -> str:
        last_user_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user" or m.get("sender_type") == "user":
                last_user_msg = m.get("content", "")
                break

        msg_lower = last_user_msg.lower()

        # Phản hồi ấm áp theo đúng System Prompt
        if "hướng nội" in msg_lower or "cà phê" in msg_lower or "đọc sách" in msg_lower:
            return (
                "Cảm ơn bạn đã chia sẻ nhé. Một không gian quán cà phê yên tĩnh với cuốn sách yêu thích thật sự là một "
                "cách nạp lại năng lượng tuyệt vời sau chuỗi ngày bận rộn.\n\n"
                "Bạn thường thích dành những khoảnh khắc bình yên đó một mình hay muốn có một người đồng điệu cùng ngồi bên cạnh?"
            )
        elif "nghiêm túc" in msg_lower or "từ từ" in msg_lower or "kiểm soát" in msg_lower:
            return (
                "Mình rất trân trọng góc nhìn của bạn. Việc muốn tìm hiểu một người từ từ và giữ khoảng trời cá nhân "
                "chính là nền tảng cho sự tôn trọng và bền vững trong tình cảm.\n\n"
                "Khi bắt đầu một mối quan hệ mới, điều gì là ranh giới quan trọng nhất mà bạn mong đối phương thấu hiểu?"
            )
        elif "cuối tuần" in msg_lower:
            return (
                "Nghe thật êm đềm! Những ngày cuối tuần trôi qua chậm rãi giúp chúng ta kết nối lại với chính mình.\n\n"
                "Nếu có một người bạn đồng hành cùng gu, bạn mong ước một ngày cuối tuần lý tưởng của hai người sẽ diễn ra như thế nào?"
            )
        else:
            return (
                f"Lắng nghe bạn chia sẻ làm Cupid hiểu hơn về thế giới nội tâm của bạn. "
                f"Mỗi thói quen và cảm xúc nhỏ đều góp phần định hình phong cách sống riêng.\n\n"
                f"Điều gì trong cuộc sống hiện tại khiến bạn cảm thấy bình yên và là chính mình nhất?"
            )

    def extract_memories(self, conversation_text: str) -> list:
        txt_lower = conversation_text.lower()
        candidates = []

        if "hướng nội" in txt_lower:
            candidates.append({
                "category": "social_preference",
                "key": "introvert_nature",
                "value": "Tính cách hướng nội",
                "human_readable_value": "Là người thiên về hướng nội, chuộng sự yên tĩnh.",
                "confidence": 0.89,
                "stability": "stable",
                "sensitivity": "personal",
                "recommended_usage": "match_profile"
            })
        if "cà phê" in txt_lower or "đọc sách" in txt_lower:
            candidates.append({
                "category": "lifestyle",
                "key": "coffee_reading_hobby",
                "value": "Thích đọc sách và cà phê cuối tuần",
                "human_readable_value": "Thích dành thời gian ở quán cà phê yên tĩnh hoặc đọc sách.",
                "confidence": 0.92,
                "stability": "stable",
                "sensitivity": "normal",
                "recommended_usage": "match_profile"
            })
        if "nghiêm túc" in txt_lower:
            candidates.append({
                "category": "relationship_goal",
                "key": "long_term_intent",
                "value": "Tìm kiếm mối quan hệ nghiêm túc",
                "human_readable_value": "Hướng tới mối quan hệ nghiêm túc, lâu dài.",
                "confidence": 0.95,
                "stability": "stable",
                "sensitivity": "normal",
                "recommended_usage": "match_profile"
            })
        if "từ từ" in txt_lower:
            candidates.append({
                "category": "relationship_pace",
                "key": "slow_pace",
                "value": "Muốn tìm hiểu từ từ",
                "human_readable_value": "Thích tiến triển tình cảm chậm rãi, chắc chắn.",
                "confidence": 0.88,
                "stability": "stable",
                "sensitivity": "normal",
                "recommended_usage": "match_profile"
            })
        if "kiểm soát" in txt_lower:
            candidates.append({
                "category": "dealbreaker",
                "key": "anti_controlling_behavior",
                "value": "Không chấp nhận hành vi kiểm soát quá đà",
                "human_readable_value": "Không phù hợp với người có tính cách quá kiểm soát.",
                "confidence": 0.94,
                "stability": "stable",
                "sensitivity": "personal",
                "recommended_usage": "match_profile"
            })

        # Nếu không bắt được từ khóa đặc thù, giả định 1 memory tổng quát
        if not candidates:
            candidates.append({
                "category": "communication_style",
                "key": "open_minded_talker",
                "value": "Giao tiếp chân thành, gợi mở",
                "human_readable_value": "Thích chia sẻ chân thành về bản thân.",
                "confidence": 0.80,
                "stability": "stable",
                "sensitivity": "normal",
                "recommended_usage": "match_profile"
            })

        return candidates

    def explain_match(self, match_data: dict, candidate_info: dict) -> str:
        name = candidate_info.get("display_name", "Đối phương")
        city = candidate_info.get("city", "Hà Nội")
        occupation = candidate_info.get("occupation", "Kỹ sư")

        matched = match_data.get("matched_dimensions", [])
        diffs = match_data.get("differences", [])
        missing = match_data.get("missing_dimensions", [])

        positives = []
        for m in matched:
            if m.get("dimension") == "relationship_goal":
                positives.append("Cả hai đều cùng hướng tới một mối quan hệ nghiêm túc lâu dài.")
            elif m.get("dimension") == "relationship_pace":
                positives.append("Đều ưu tiên nhịp độ tìm hiểu từ từ, chắc chắn.")
            elif m.get("dimension") == "communication_style":
                positives.append("Coi trọng phong cách giao tiếp nhẹ nhàng, lắng nghe sâu sắc.")
            elif m.get("dimension") == "boundaries":
                positives.append("Đều cần không gian cá nhân và dị ứng với hành vi kiểm soát.")
            elif m.get("dimension") == "lifestyle":
                positives.append("Có cùng sở thích tận hưởng không gian quán cà phê hoặc đọc sách.")

        if not positives:
            positives.append("Có sự hòa hợp tốt về mục tiêu quan hệ và lối sống.")

        differences_text = []
        for d in diffs:
            if d.get("dimension") == "social_level":
                differences_text.append(f"{name} có mức độ hướng ngoại/nội hơi khác một chút, tạo sự bù trừ thú vị.")

        if not differences_text:
            differences_text.append("Không có xung đột lớn về ranh giới cá nhân hay dealbreaker.")

        missing_text = "Chưa đủ dữ liệu để đánh giá quan điểm tài chính & hôn nhân chi tiết." if missing else "Đã có đủ dữ liệu cơ bản để đánh giá."

        return (
            f"💘 **{name} ({candidate_info.get('age')} tuổi, {occupation} - {city})** có thể rất phù hợp với bạn.\n\n"
            f"✨ **Điểm tương đồng nổi bật:**\n" + "\n".join(f"- {p}" for p in positives) + "\n\n"
            f"⚖️ **Điểm khác biệt / Cần lưu ý:**\n" + "\n".join(f"- {d}" for d in differences_text) + "\n\n"
            f"🔍 **Thông tin cần tìm hiểu thêm:**\n- {missing_text}\n\n"
            f"💬 **Câu hỏi gợi ý để trò chuyện:**\n"
            f"“Nếu có một cuối tuần rảnh, bạn thường muốn dành phần lớn thời gian cùng người yêu hay vẫn giữ một khoảng thời gian riêng?”"
        )


class OpenAIProvider(BaseLLMProvider):
    """Provider thực tế dùng OpenAI API Key"""

    def __init__(self, api_key: str):
        import openai
        self.client = openai.OpenAI(api_key=api_key)

    def chat(self, messages: list, system_prompt: str = CUPID_SYSTEM_PROMPT) -> str:
        try:
            formatted = [{"role": "system", "content": system_prompt}]
            for m in messages:
                role = "assistant" if m.get("sender_type") == "agent" or m.get("role") == "assistant" else "user"
                formatted.append({"role": role, "content": m.get("content", "")})

            res = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=formatted,
                temperature=0.7
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f"⚠️ OpenAI Chat error ({e}), fallback sang MockLLMProvider.")
            return MockLLMProvider().chat(messages, system_prompt)

    def extract_memories(self, conversation_text: str) -> list:
        try:
            prompt = f"{MEMORY_EXTRACTION_SYSTEM_PROMPT}\n\nĐoạn trò chuyện:\n{conversation_text}"
            res = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            data = json.loads(res.choices[0].message.content)
            candidates = data.get("candidates", data.get("memories", []))
            if candidates:
                return candidates
        except Exception as e:
            print(f"⚠️ OpenAI Memory Extraction error ({e}), fallback sang MockLLMProvider.")
        return MockLLMProvider().extract_memories(conversation_text)

    def explain_match(self, match_data: dict, candidate_info: dict) -> str:
        try:
            prompt = f"{MATCH_EXPLANATION_SYSTEM_PROMPT}\n\nKết quả so sánh:\nCandidate: {json.dumps(candidate_info, ensure_ascii=False)}\nMatch Analysis: {json.dumps(match_data, ensure_ascii=False)}"
            res = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f"⚠️ OpenAI Explain Match error ({e}), fallback sang MockLLMProvider.")
            return MockLLMProvider().explain_match(match_data, candidate_info)


class GeminiLLMProvider(BaseLLMProvider):
    """Provider dùng Google Gemini API"""

    def __init__(self, api_key: str):
        from google import genai
        self.client = genai.Client(api_key=api_key)

    def chat(self, messages: list, system_prompt: str = CUPID_SYSTEM_PROMPT) -> str:
        try:
            full_text = system_prompt + "\n\nLịch sử chat:\n"
            for m in messages:
                sender = "Cupid" if m.get("sender_type") == "agent" or m.get("role") == "assistant" else "User"
                full_text += f"{sender}: {m.get('content', '')}\n"

            res = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_text
            )
            return res.text
        except Exception as e:
            print(f"⚠️ Gemini Chat error ({e}), fallback sang MockLLMProvider.")
            return MockLLMProvider().chat(messages, system_prompt)

    def extract_memories(self, conversation_text: str) -> list:
        try:
            prompt = f"{MEMORY_EXTRACTION_SYSTEM_PROMPT}\n\nTrả về JSON danh sách 'candidates': [...] \n\nĐoạn trò chuyện:\n{conversation_text}"
            res = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            match = re.search(r"\{.*\}", res.text, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                cands = data.get("candidates", [])
                if cands:
                    return cands
        except Exception as e:
            print(f"⚠️ Gemini Extract Memories error ({e}), fallback sang MockLLMProvider.")
        return MockLLMProvider().extract_memories(conversation_text)

    def explain_match(self, match_data: dict, candidate_info: dict) -> str:
        try:
            prompt = f"{MATCH_EXPLANATION_SYSTEM_PROMPT}\n\nCandidate: {json.dumps(candidate_info, ensure_ascii=False)}\nMatch Data: {json.dumps(match_data, ensure_ascii=False)}"
            res = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return res.text
        except Exception as e:
            print(f"⚠️ Gemini Explain Match error ({e}), fallback sang MockLLMProvider.")
            return MockLLMProvider().explain_match(match_data, candidate_info)


def get_llm_provider() -> BaseLLMProvider:
    """Tự động lựa chọn provider phù hợp theo environment"""
    provider_type = DEFAULT_PROVIDER.lower()

    if provider_type == "openai" and OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your_"):
        try:
            return OpenAIProvider(OPENAI_API_KEY)
        except Exception as e:
            print(f"⚠️ Không thể khởi tạo OpenAI Provider ({e}), fallback sang Mock Provider.")

    if provider_type == "gemini" and GEMINI_API_KEY and not GEMINI_API_KEY.startswith("your_"):
        try:
            return GeminiLLMProvider(GEMINI_API_KEY)
        except Exception as e:
            print(f"⚠️ Không thể khởi tạo Gemini Provider ({e}), fallback sang Mock Provider.")

    return MockLLMProvider()
