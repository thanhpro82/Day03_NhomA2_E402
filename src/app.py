"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.
"""

import json
import os
import sys
import re
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import các thành phần từ file của Role 2, Role 3 & Multi-Provider Adapter
from tools import AVAILABLE_TOOLS
from prompts import (
    CHATBOT_BASELINE_PROMPT,
    REACT_SYSTEM_PROMPT,
    MAX_ITERATIONS,
    validate_input,
)
from providers import get_llm_provider, MockProvider

load_dotenv()

def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    
    if not os.path.exists(config_path):
        config_path = "test_cases.json"
        
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_baseline_chatbot(user_query: str, provider):
    """
    Dựng Chatbot gốc (Baseline) không có công cụ.
    """
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    
    # Check Guardrail trước khi gọi LLM
    guard_err = validate_input(user_query)
    if guard_err:
        print(guard_err)
        return
        
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot trả lời:\n{response}")


def parse_action(text: str):
    """
    Trích xuất tên tool và tham số từ chuỗi 'Action: tool_name[arg1, arg2]'
    """
    match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\[(.*?)\]", text, re.IGNORECASE)
    if match:
        tool_name = match.group(1).strip()
        raw_args = match.group(2).strip()
        args = [a.strip().strip("'\"") for a in raw_args.split(",") if a.strip()]
        return tool_name, args
    return None, []


def run_react_agent(user_query: str, provider):
    """
    Dựng vòng lặp ReAct Agent (Thought -> Action -> Observation) thực tế có Guardrails.
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    
    # 1. Input Guardrail check
    guard_err = validate_input(user_query)
    if guard_err:
        print(f"{guard_err}")
        return

    # Nếu chạy ở Offline MockProvider
    if isinstance(provider, MockProvider):
        print("ℹ️ [Mock Provider Mode]: Giả lập luồng ReAct cho Cupid Agent...")
        run_mock_react_demo(user_query)
        return

    current_prompt = f"Câu hỏi của người dùng: {user_query}"
    history = ""
    step = 0

    while step < MAX_ITERATIONS:
        step += 1
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")
        
        full_prompt = history + "\n" + current_prompt if history else current_prompt
        response = provider.generate(full_prompt, system_prompt=REACT_SYSTEM_PROMPT)
        print(f"🤖 Agent Response:\n{response}")

        if "Final Answer:" in response:
            print("\n✅ ReAct Agent đã hoàn thành nhiệm vụ.")
            return

        tool_name, args = parse_action(response)
        if tool_name:
            print(f"🛠️ Tool được gọi: {tool_name} với tham số: {args}")
            if tool_name in AVAILABLE_TOOLS:
                tool_func = AVAILABLE_TOOLS[tool_name]
                try:
                    obs = tool_func(*args)
                except Exception as e:
                    obs = f"LỖI khi thực thi tool '{tool_name}': {str(e)}"
            else:
                available_str = ", ".join(AVAILABLE_TOOLS.keys())
                obs = f"LỖI: Không tìm thấy công cụ '{tool_name}'. Các công cụ khả dụng: {available_str}"
            
            print(f"👁️ Observation:\n{obs}")
            history += f"\n{response}\nObservation: {obs}"
            current_prompt = "Hãy tiếp tục suy luận (Thought) hoặc đưa ra câu trả lời cuối cùng (Final Answer)."
        else:
            history += f"\n{response}"
            current_prompt = "LƯU Ý: Vui lòng đưa ra 'Action: tên_công_cụ[tham_số]' hoặc 'Final Answer: câu_trả_lời' theo đúng định dạng."

    if step >= MAX_ITERATIONS:
        print(f"\n🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước. Ngắt lặp an toàn!")


def run_mock_react_demo(user_query: str):
    """Demo luồng ReAct cho chế độ Offline Mock"""
    q_lower = user_query.lower()
    if "hồ sơ" in q_lower or "tương thích" in q_lower:
        print("\n--- 🔄 Vòng lặp ReAct (Step 1/5) ---")
        print("🧠 Thought: Người dùng muốn tra cứu hồ sơ và tính độ tương thích giữa Nam và Linh. Tôi cần dùng tool calculate_compatibility_score.")
        print("🛠️ Action: calculate_compatibility_score[Nam, Linh]")
        obs = AVAILABLE_TOOLS["calculate_compatibility_score"]("Nam", "Linh")
        print(f"👁️ Observation:\n{obs}")
        
        print("\n--- 🔄 Vòng lặp ReAct (Step 2/5) ---")
        print("🧠 Thought: Tôi đã có đầy đủ chỉ số tương thích. Giờ tôi tổng hợp câu trả lời cuối cùng.")
        print("🏁 Final Answer: Nam (ENFP) và Linh (INFJ) có chỉ số tương thích ấn tượng 87%! Cặp đôi hợp nhau về MBTI (95%), cùng ở Hà Nội và cùng thích mèo, cà phê.")
    else:
        print("\n--- 🔄 Vòng lặp ReAct (Step 1/5) ---")
        print("🧠 Thought: Đây là câu hỏi tư vấn chung, không cần tra cứu hồ sơ.")
        print("🏁 Final Answer: [Mock Mode] Trả lời trực tiếp câu hỏi của bạn.")


if __name__ == "__main__":
    print("==================================================")
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT (CUPID AGENT)")
    print("==================================================")
    
    # Khởi tạo Multi-Provider LLM Adapter
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")
    
    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json\n")
    
    # Chạy thử Test Case #3 & Test Case #4
    print("--- 📌 TEST CASE 3: CHẠY TRÊN CHATBOT BASELINE ---")
    run_baseline_chatbot(tests[2]["question"], provider)
    
    print("\n--------------------------------------------------")
    print("--- 📌 TEST CASE 3: CHẠY TRÊN REACT AGENT ---")
    run_react_agent(tests[2]["question"], provider)

    print("\n--------------------------------------------------")
    print("--- 📌 TEST CASE 6 (EDGE CASE / GUARDRAIL): CHẠY TRÊN REACT AGENT ---")
    run_react_agent(tests[5]["question"], provider)
