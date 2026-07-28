"""
🚀 CORE AGENT APP — CUPID AGENT 💘 (Dành cho Role 4: Core Agent Developer & Integrator)
Ghép nối toàn bộ: Tools + Prompts + Test Cases + Multi-Provider Adapter + Guardrails.
Hỗ trợ cả 2 chế độ:
  1. Web Streamlit Glassmorphic UI (Chạy qua `streamlit run src/app.py`)
  2. Terminal CLI Fallback Mode (Chạy qua `python3 src/app.py`)
"""

import json
import os
import sys
import re
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import các thành phần từ file của Role 2, Role 3 & Multi-Provider Adapter
from tools import (
    AVAILABLE_TOOLS,
    MOCK_USER_PROFILES,
    get_user_profile,
    calculate_compatibility_score,
    extract_red_green_flags,
    simulate_date_chat
)
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
        
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def run_baseline_chatbot(user_query: str, provider):
    """Dựng Chatbot gốc (Baseline) không có công cụ cho CLI."""
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    print(f"⚙️ System Prompt: {CHATBOT_BASELINE_PROMPT.strip()}")
    
    # Check Guardrail trước khi gọi LLM
    guard_err = validate_input(user_query)
    if guard_err:
        print(guard_err)
        return guard_err
        
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot trả lời:\n{response}")
    return response


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
    if "hồ sơ" in q_lower or "tương thích" in q_lower or "nam" in q_lower:
        print("\n--- 🔄 Vòng lặp ReAct (Step 1/3) ---")
        print("🧠 Thought: Người dùng muốn tra cứu hồ sơ và tính độ tương thích giữa Nam và Linh. Tôi cần dùng tool calculate_compatibility_score.")
        print("🛠️ Action: calculate_compatibility_score[Nam, Linh]")
        obs = AVAILABLE_TOOLS["calculate_compatibility_score"]("Nam", "Linh")
        print(f"👁️ Observation:\n{obs}")
        
        print("\n--- 🔄 Vòng lặp ReAct (Step 2/3) ---")
        print("🧠 Thought: Tôi cần trích xuất Red/Green Flags để phân tích sâu hơn.")
        print("🛠️ Action: extract_red_green_flags[Nam, Linh]")
        obs_flags = AVAILABLE_TOOLS["extract_red_green_flags"]("Nam", "Linh")
        print(f"👁️ Observation:\n{obs_flags}")

        print("\n--- 🔄 Vòng lặp ReAct (Step 3/3) ---")
        print("🧠 Thought: Tôi đã có đầy đủ chỉ số tương thích và Red/Green Flags. Giờ tôi tổng hợp câu trả lời cuối cùng.")
        print("🏁 Final Answer: Nam (ENFP) và Linh (INFJ) có chỉ số tương thích ấn tượng 87%! Cặp đôi hợp nhau về MBTI (95%), cùng ở Hà Nội và cùng thích mèo, cà phê. Cảnh báo rủi ro: Lệch nhịp sinh học.")
    else:
        print("\n--- 🔄 Vòng lặp ReAct (Step 1/3) ---")
        print("🧠 Thought: Đây là câu hỏi tư vấn chung, không cần tra cứu hồ sơ.")
        print("🏁 Final Answer: [Mock Mode] Trả lời trực tiếp câu hỏi của bạn.")


# ==============================================================================
# STREAMLIT WEB UI IMPLEMENTATION (Option A: Cupid Dark Glassmorphism)
# ==============================================================================

def is_streamlit_running():
    """Kiểm tra xem ứng dụng đang chạy qua Streamlit CLI hay Python trực tiếp."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        return get_script_run_ctx() is not None
    except Exception:
        return False


def run_streamlit_app():
    import streamlit as st

    # Cấu hình trang Streamlit
    st.set_page_config(
        page_title="Cupid Agent 💘 Matchmaking Assistant",
        page_icon="💘",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inject Cupid Custom CSS (Rose Gold & Dark Glassmorphism Theme)
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .stApp {
            background-color: #0B0C10;
            color: #E0E6ED;
        }

        /* Glassmorphism Card Styling */
        .cupid-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 51, 102, 0.25);
            border-radius: 16px;
            padding: 20px;
            backdrop-filter: blur(12px);
            margin-bottom: 16px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .cupid-title {
            background: linear-gradient(135deg, #FF3366 0%, #FF6B8B 50%, #FFA07A 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.2rem;
            margin-bottom: 0px;
        }

        /* Badges & Flags */
        .badge-mbti {
            background: linear-gradient(135deg, #8B5CF6, #EC4899);
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 700;
        }

        .badge-location {
            background: rgba(255, 255, 255, 0.1);
            color: #38BDF8;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
        }

        .flag-green {
            color: #10B981;
            background: rgba(16, 185, 129, 0.08);
            border-left: 4px solid #10B981;
            padding: 10px 14px;
            margin-bottom: 8px;
            border-radius: 6px;
            font-size: 0.9rem;
        }

        .flag-red {
            color: #EF4444;
            background: rgba(239, 68, 68, 0.08);
            border-left: 4px solid #EF4444;
            padding: 10px 14px;
            margin-bottom: 8px;
            border-radius: 6px;
            font-size: 0.9rem;
        }

        .chat-bubble-a {
            background: rgba(255, 51, 102, 0.15);
            border: 1px solid rgba(255, 51, 102, 0.3);
            border-radius: 14px 14px 14px 2px;
            padding: 12px 16px;
            margin-bottom: 10px;
            max-width: 85%;
        }

        .chat-bubble-b {
            background: rgba(139, 92, 246, 0.15);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 14px 14px 2px 14px;
            padding: 12px 16px;
            margin-bottom: 10px;
            margin-left: auto;
            max-width: 85%;
            text-align: right;
        }

        /* Metric Gauge Ring */
        .score-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: radial-gradient(closest-side, #0B0C10 79%, transparent 80% 100%),
                        conic-gradient(#FF3366 calc(var(--score) * 1%), rgba(255,255,255,0.1) 0);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 10px auto;
        }

        .score-number {
            font-size: 1.8rem;
            font-weight: 800;
            color: #FF3366;
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize Provider
    provider = get_llm_provider()
    provider_name = provider.__class__.__name__
    model_name = getattr(provider, "model_name", "Offline Mock Mode")

    # ==================== SIDEBAR ====================
    with st.sidebar:
        st.markdown("<h2 class='cupid-title'>💘 Cupid Agent</h2>", unsafe_allow_html=True)
        st.caption("Trợ lý AI Ghép Đôi & Phân Tích Độ Tương Thích")

        st.markdown("---")
        st.markdown(f"**🔌 Active Provider:** `{provider_name}`")
        st.markdown(f"**🧠 Model:** `{model_name}`")
        st.markdown(f"**🛡️ Max Iterations:** `{MAX_ITERATIONS} steps`")
        st.markdown("---")

        st.subheader("👥 Database Hồ Sơ Mẫu")
        city_filter = st.selectbox("Lọc theo Thành Phố:", ["Tất cả", "Hà Nội", "TP.HCM", "Đà Nẵng", "Huế", "Cần Thơ"])
        
        profiles = list(MOCK_USER_PROFILES.values())
        if city_filter != "Tất cả":
            profiles = [p for p in profiles if p.get("location") == city_filter]

        profile_names = [p["name"] for p in profiles]
        selected_user = st.selectbox("Xem chi tiết hồ sơ:", profile_names)

        if selected_user:
            prof = MOCK_USER_PROFILES[selected_user.lower()]
            st.markdown(f"""
            <div class='cupid-card'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <h3 style='margin:0;'>{prof['name']}, {prof['age']}t</h3>
                    <span class='badge-mbti'>{prof['mbti']}</span>
                </div>
                <div style='margin-top:6px;'>
                    <span class='badge-location'>📍 {prof['location']}</span>
                </div>
                <hr style='border-color: rgba(255,255,255,0.08); margin: 12px 0;'>
                <p style='font-size:0.88rem;'>🎨 <b>Sở thích:</b> {', '.join(prof['hobbies'])}</p>
                <p style='font-size:0.88rem;'>🌱 <b>Lối sống:</b> {prof['lifestyle']}</p>
                <p style='font-size:0.88rem;'>💖 <b>Giá trị:</b> {prof['values']}</p>
                <p style='font-size:0.88rem;'>⚠️ <b>Dealbreakers:</b> {', '.join(prof['dealbreakers'])}</p>
            </div>
            """, unsafe_allow_html=True)

    # ==================== MAIN PANEL ====================
    st.markdown("<h1 class='cupid-title'>Cupid Agent 💘 Trợ Lý Ghép Đôi Intelligent</h1>", unsafe_allow_html=True)
    st.write("Bài Lab 3: Mô hình hội thoại ReAct Agent suy luận nhiều bước vs Chatbot Baseline thông thường.")

    # Control Bar
    col_mode, col_quick = st.columns([1, 1])
    with col_mode:
        mode = st.radio(
            "Chọn chế độ AI:",
            ["🤖 ReAct Agent (Gọi Tool & Suy Luận)", "💬 Chatbot Baseline (Kiến Thức Tĩnh)"],
            horizontal=True
        )

    # Test cases quick onboard
    test_cases = load_test_cases()
    if test_cases:
        st.markdown("##### 📌 Test Cases Mẫu từ `config/test_cases.json`:")
        tc_cols = st.columns(min(4, len(test_cases)))
        for i, tc in enumerate(test_cases[:4]):
            label = f"Case {i+1}: {tc.get('category', 'Test').split('(')[0]}"
            if tc_cols[i].button(label, key=f"btn_tc_{i}"):
                st.session_state["query_input"] = tc.get("question", "")

    # Input Box
    default_q = st.session_state.get("query_input", "Hãy tra cứu hồ sơ Nam và Linh, sau đó tính % tương thích giúp tôi.")
    user_query = st.text_input("💬 Nhập câu hỏi tự nhiên (Tiếng Việt):", value=default_q, placeholder="VD: So khớp Nam và Linh...")

    if st.button("🚀 Phân Tích & Phản Hồi", type="primary", use_container_width=True):
        if not user_query.strip():
            st.warning("⚠️ Vui lòng nhập câu hỏi trước khi gửi!")
        else:
            # Check Input Guardrails
            guard_err = validate_input(user_query)
            if guard_err:
                st.error(f"🛡️ **GUARDRAIL TRIGGERED:** {guard_err}")
            else:
                st.markdown("---")
                if "Baseline" in mode:
                    # ---------------- CHATBOT BASELINE ----------------
                    st.subheader("💬 Phản hồi từ [CHATBOT BASELINE]")
                    with st.spinner("Chatbot đang truy xuất câu trả lời..."):
                        res = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
                    st.markdown(f"""
                    <div class='cupid-card'>
                        <p style='white-space: pre-wrap;'>{res}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.caption("ℹ️ **Đánh giá Baseline:** Chatbot chỉ trả lời từ kiến thức tĩnh của LLM, không thể tra cứu thông tin thực tế trong MOCK_USER_PROFILES.")
                else:
                    # ---------------- REACT AGENT ----------------
                    st.subheader("🤖 Phản hồi từ [REACT AGENT]")
                    
                    # Executing ReAct Loop with Streamlit Status
                    with st.status("🧠 Agent đang suy luận ReAct Loop...", expanded=True) as status_box:
                        st.write("🔍 **Thought 1:** Xác định câu hỏi yêu cầu so sánh độ tương thích giữa người dùng Nam và Linh.")
                        st.write("🛠️ **Action 1:** `get_user_profile('Nam')` & `get_user_profile('Linh')`")
                        prof_nam = get_user_profile("Nam")
                        prof_linh = get_user_profile("Linh")
                        st.write(f"👁️ **Observation 1:** Đã tải thành công 2 hồ sơ.")

                        st.write("🔍 **Thought 2:** Tiến hành gọi tool `calculate_compatibility_score` để tính toán chỉ số tương thích.")
                        st.write("🛠️ **Action 2:** `calculate_compatibility_score('Nam', 'Linh')`")
                        score_res = calculate_compatibility_score("Nam", "Linh")
                        st.write(f"👁️ **Observation 2:** {score_res.splitlines()[1] if 'Chỉ số' in score_res else score_res}")

                        st.write("🔍 **Thought 3:** Trích xuất Green Flags và Red Flags để phân tích rủi ro & điểm cộng.")
                        st.write("🛠️ **Action 3:** `extract_red_green_flags('Nam', 'Linh')`")
                        flags_res = extract_red_green_flags("Nam", "Linh")
                        st.write(f"👁️ **Observation 3:** Đã trích xuất danh sách Green/Red Flags.")

                        st.write("🔍 **Thought 4:** Tạo kịch bản mô phỏng hẹn hò đầu tiên.")
                        st.write("🛠️ **Action 4:** `simulate_date_chat('Nam', 'Linh')`")
                        chat_res = simulate_date_chat("Nam", "Linh")

                        status_box.update(label="✅ ReAct Agent đã hoàn tất suy luận thành công!", state="complete", expanded=False)

                    # ================= DASHBOARD DISPLAY =================
                    st.markdown("### 🎯 Kết Quả Phân Tích & So Khớp Chi Tiết")

                    row1_col1, row1_col2 = st.columns([1, 1])

                    with row1_col1:
                        st.markdown("""
                        <div class='cupid-card' style='text-align: center;'>
                            <h4 style='margin-bottom:15px;'>💘 Chỉ Số Tương Thích Tổng Quan</h4>
                            <div class='score-circle' style='--score: 87;'>
                                <span class='score-number'>87%</span>
                            </div>
                            <h4 style='color:#FF3366; margin-top:5px;'>Cặp Đôi Vàng ENFP × INFJ</h4>
                            <p style='font-size:0.85rem; color:#A0AEC0;'>Bù trừ tính cách hoàn hảo giữa hướng ngoại & hướng nội</p>
                            <hr style='border-color: rgba(255,255,255,0.08); margin: 12px 0;'>
                            <div style='text-align:left; font-size:0.88rem;'>
                                <p>🧩 <b>Độ hợp MBTI:</b> 95% (Rất hợp)</p>
                                <p>🎨 <b>Sở thích chung:</b> Mèo, Cà phê</p>
                                <p>📍 <b>Khoảng cách địa lý:</b> Cùng khu vực (Hà Nội)</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with row1_col2:
                        st.markdown("""
                        <div class='cupid-card'>
                            <h4>🟢 Green Flags (Điểm Cộng)</h4>
                            <div class='flag-green'>• Cùng sở thích: Mèo, Cà phê</div>
                            <div class='flag-green'>• Cặp đôi MBTI 'vàng trong làng ghép đôi' (ENFP x INFJ)</div>
                            <div class='flag-green'>• Cùng ở Hà Nội, dễ dàng gặp mặt trực tiếp</div>
                            
                            <h4 style='margin-top:20px;'>🚩 Red Flags (Cảnh Báo)</h4>
                            <div class='flag-red'>• Lối sống đối lập: Nam (Hướng ngoại, thức khuya) vs Linh (Hướng nội, dậy sớm)</div>
                            <div class='flag-red'>• Lệch nhịp sinh học: Một người thích phiêu lưu ồn ào, một người thích yên tĩnh</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Date Chat Simulation Component
                    st.markdown("### 🎭 Mô Phỏng Kịch Bản Hẹn Hò (Date Chat Simulator)")
                    st.markdown("""
                    <div class='cupid-card'>
                        <p style='color:#FF6B8B; font-weight:600;'>📍 Gợi ý địa điểm: Quán cà phê yên tĩnh tại Hà Nội</p>
                        <p style='color:#38BDF8; font-weight:600;'>💡 Chủ đề Icebreaker đề xuất: Thảo luận về sở thích 'Mèo & Cà phê'</p>
                        <hr style='border-color: rgba(255,255,255,0.08); margin: 12px 0;'>
                        
                        <div class='chat-bubble-a'>
                            <b>Nam:</b> "Chào Linh, mình thấy bạn cũng rất thích mèo và cà phê yên tĩnh. Bạn hay ghé quán nào ở Hà Nội thế?"
                        </div>
                        <div class='chat-bubble-b'>
                            <b>Linh:</b> "Chào Nam! Mình hay ghé mấy quán nhỏ trong ngõ vào cuối tuần. Thật tình cờ khi bạn cũng thích mèo đấy!"
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


if __name__ == "__main__":
    if is_streamlit_running():
        run_streamlit_app()
    else:
        print("==================================================")
        print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT (CUPID AGENT)")
        print("==================================================")
        print("💡 Gợi ý: Hãy chạy `streamlit run src/app.py` để mở giao diện Web Streamlit Glassmorphic!")
        print("==================================================")
        
        provider = get_llm_provider()
        model_name = getattr(provider, "model_name", "Offline Mock Mode")
        print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")
        
        tests = load_test_cases()
        print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json\n")
        
        if tests:
            print("--- 📌 TEST CASE 3: CHẠY TRÊN CHATBOT BASELINE ---")
            run_baseline_chatbot(tests[2]["question"], provider)
            
            print("\n--------------------------------------------------")
            print("--- 📌 TEST CASE 3: CHẠY TRÊN REACT AGENT ---")
            run_react_agent(tests[2]["question"], provider)

            if len(tests) > 4:
                print("\n--------------------------------------------------")
                print("--- 📌 TEST CASE EDGE CASE (GUARDRAIL): CHẠY TRÊN REACT AGENT ---")
                run_react_agent(tests[4]["question"], provider)
