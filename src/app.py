"""
🚀 CUPID AGENT — WEB APPLICATION 💘
Giao diện Cao cấp với hỗ trợ Giao diện Sáng (Warm Light Theme) và Giao diện Tối (Dark Theme).
"""

import os
import sys
import json
import streamlit as st

# Ensure src modules are in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.connection import SessionLocal, init_db
from src.database.seed import seed_database
from src.database.models import User, Conversation, Message, MemoryCandidate, ApprovedMemory, MatchResult, AuditLog
from src.services.auth_service import AuthService
from src.services.conversation_service import ConversationService
from src.services.memory_service import MemoryService
from src.services.profile_service import ProfileService
from src.services.matching_engine import MatchingEngine
from src.services.explanation_service import ExplanationService
from src.config import SUGGESTED_CHAT_PROMPTS, CATEGORY_LABELS_VI, VISIBILITY_OPTIONS


# ------------------------------------------------------------------------------
# 1. INITIALIZATION & SESSION STATE MANAGEMENT
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Cupid Agent 💘 Trợ lý ghép đôi & Thấu hiểu",
    page_icon="💘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database & Seed Candidates
init_db()

@st.cache_resource
def run_once_seed():
    seed_database()

run_once_seed()

# Initialize Session State
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_demo_01"  # Default Active Session cho phép test ngay
if "user_email" not in st.session_state:
    st.session_state.user_email = "demo@cupid.ai"
if "display_name" not in st.session_state:
    st.session_state.display_name = "Người dùng Demo"
if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None
if "selected_nav" not in st.session_state:
    st.session_state.selected_nav = "💬 Cupid Chat"
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # Mặc định là Warm Light Theme


# ------------------------------------------------------------------------------
# 2. CUSTOM CSS STYLING (Light & Dark Theme Engine)
# ------------------------------------------------------------------------------
is_dark = (st.session_state.theme == "dark")

if is_dark:
    bg_app = "#0B0C10"
    text_color = "#E0E6ED"
    bg_card = "rgba(255, 255, 255, 0.04)"
    border_card = "rgba(255, 51, 102, 0.3)"
    agent_bubble = "rgba(255, 51, 102, 0.15)"
    user_bubble = "rgba(139, 92, 246, 0.18)"
    agent_text = "#FCE7F3"
    user_text = "#F3E8FF"
    badge_bg = "rgba(255, 255, 255, 0.1)"
    sidebar_bg = "#12141C"
else:
    bg_app = "#FFF9FA"
    text_color = "#1E293B"
    bg_card = "#FFFFFF"
    border_card = "rgba(255, 51, 102, 0.25)"
    agent_bubble = "#FFF0F4"
    user_bubble = "#F3E8FF"
    agent_text = "#1E293B"
    user_text = "#1E293B"
    badge_bg = "rgba(255, 51, 102, 0.08)"
    sidebar_bg = "#FAF0F3"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp {{
        background-color: {bg_app};
        color: {text_color};
    }}

    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
    }}

    /* Card Styling */
    .cupid-card {{
        background: {bg_card};
        border: 1px solid {border_card};
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 4px 20px 0 rgba(255, 51, 102, 0.08);
    }}

    .cupid-title {{
        background: linear-gradient(135deg, #FF3366 0%, #FF6B8B 50%, #E11D48 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 4px;
    }}

    /* Badges */
    .badge-visibility {{
        background: linear-gradient(135deg, #8B5CF6, #EC4899);
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
    }}

    .badge-confidence {{
        background: rgba(16, 185, 129, 0.15);
        color: #059669;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 3px 8px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 600;
    }}

    .badge-category {{
        background: {badge_bg};
        color: #0284C7;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }}

    /* Chat Messages */
    .chat-bubble-agent {{
        background: {agent_bubble};
        border: 1px solid rgba(255, 51, 102, 0.3);
        border-radius: 16px 16px 16px 4px;
        padding: 16px 20px;
        margin-bottom: 14px;
        color: {agent_text};
        line-height: 1.6;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }}

    .chat-bubble-user {{
        background: {user_bubble};
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px 16px 4px 16px;
        padding: 16px 20px;
        margin-bottom: 14px;
        color: {user_text};
        line-height: 1.6;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }}

    /* Score Circle */
    .score-badge {{
        font-size: 1.8rem;
        font-weight: 800;
        color: #FF3366;
    }}

    /* Buttons readability */
    .stButton button {{
        border-radius: 10px;
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION & AUTH CONTEXT
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="cupid-title">💘 Cupid Agent</div>', unsafe_allow_html=True)
    st.caption("Trợ lý trò chuyện, hiểu người dùng & gợi ý đối tượng phù hợp")
    st.divider()

    # User Account Status Indicator
    st.write(f"👤 **Tài khoản:** {st.session_state.display_name}")
    st.caption(f"📧 {st.session_state.user_email}")

    if st.button("🚪 Đăng xuất", use_container_width=True):
        st.session_state.user_id = "user_demo_01"
        st.session_state.user_email = "demo@cupid.ai"
        st.session_state.display_name = "Người dùng Demo"
        st.session_state.current_conversation_id = None
        st.rerun()

    st.divider()

    # Theme Switcher (Chuyển đổi Sáng / Tối)
    theme_choice = st.selectbox(
        "🎨 Giao diện (Theme):",
        ["🌸 Soft Light (Giao diện Sáng)", "🌙 Dark Glass (Giao diện Tối)"],
        index=0 if st.session_state.theme == "light" else 1
    )
    new_theme_val = "light" if "Light" in theme_choice else "dark"
    if new_theme_val != st.session_state.theme:
        st.session_state.theme = new_theme_val
        st.rerun()

    st.divider()

    # Main Navigation Radio
    nav_options = [
        "💬 Cupid Chat",
        "🧠 Duyệt Memory",
        "📋 Cupid hiểu gì về bạn",
        "💘 Tìm người phù hợp",
        "🛡️ Quyền riêng tư & Audit",
        "🔐 Đăng nhập / Đăng ký"
    ]

    selected_page = st.radio("Chuyển trang navigation:", nav_options, index=nav_options.index(st.session_state.selected_nav))
    st.session_state.selected_nav = selected_page

    st.divider()
    st.caption("🔒 Privacy & Consent First Architecture")
    st.caption("⚡ Powered by Rule-based Matching Engine")


# Database Helper
db = SessionLocal()


# ------------------------------------------------------------------------------
# PAGE 1: 💬 CUPID CHAT
# ------------------------------------------------------------------------------
if st.session_state.selected_nav == "💬 Cupid Chat":
    st.markdown("## 💬 Trò chuyện cùng Cupid Agent")
    st.caption("Hãy thoải mái chia sẻ về phong cách sống, cảm xúc và điều bạn kỳ vọng trong tình cảm. Cupid luôn lắng nghe mà không phán xét.")

    col_side, col_main = st.columns([1, 3])

    with col_side:
        st.subheader("📜 Phiên gần đây")
        if st.button("➕ Cuộc trò chuyện mới", type="primary", use_container_width=True):
            new_conv = ConversationService.get_or_create_conversation(db, st.session_state.user_id)
            st.session_state.current_conversation_id = new_conv.id
            st.rerun()

        conversations = ConversationService.list_user_conversations(db, st.session_state.user_id)
        if not conversations:
            new_conv = ConversationService.get_or_create_conversation(db, st.session_state.user_id)
            st.session_state.current_conversation_id = new_conv.id
            conversations = [new_conv]

        if not st.session_state.current_conversation_id and conversations:
            st.session_state.current_conversation_id = conversations[0].id

        for conv in conversations:
            is_active = (conv.id == st.session_state.current_conversation_id)
            btn_label = f"{'🟢' if is_active else '💬'} {conv.title[:20]}"
            if st.button(btn_label, key=f"conv_{conv.id}", use_container_width=True):
                st.session_state.current_conversation_id = conv.id
                st.rerun()

    with col_main:
        active_conv_id = st.session_state.current_conversation_id
        if active_conv_id:
            messages = ConversationService.get_messages(db, st.session_state.user_id, active_conv_id)

            # Container hiển thị tin nhắn
            chat_container = st.container()
            with chat_container:
                for m in messages:
                    if m.sender_type == "agent":
                        st.markdown(f'<div class="chat-bubble-agent"><b>💘 Cupid:</b><br>{m.content}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-bubble-user"><b>👤 Bạn:</b><br>{m.content}</div>', unsafe_allow_html=True)

            st.divider()

            # Gợi ý câu hỏi khi người dùng chưa biết nói gì
            st.caption("💡 **Gợi ý câu hỏi để khởi đầu tâm sự:**")
            p_cols = st.columns(len(SUGGESTED_CHAT_PROMPTS))
            for idx, prompt_text in enumerate(SUGGESTED_CHAT_PROMPTS):
                with p_cols[idx]:
                    if st.button(prompt_text, key=f"sug_{idx}", use_container_width=True):
                        with st.spinner("Cupid đang lắng nghe và suy ngẫm..."):
                            ConversationService.send_message(db, st.session_state.user_id, active_conv_id, prompt_text)
                        st.rerun()

            # Ô nhập nội dung tin nhắn
            user_input = st.chat_input("Nhập tâm sự hoặc câu hỏi của bạn với Cupid...")
            if user_input:
                with st.spinner("Cupid đang soạn phản hồi..."):
                    ConversationService.send_message(db, st.session_state.user_id, active_conv_id, user_input)
                st.rerun()

            st.divider()
            col_actions, _ = st.columns([2, 2])
            with col_actions:
                if st.button("🧠 Trích xuất Memory từ cuộc trò chuyện", use_container_width=True):
                    with st.spinner("Hệ thống đang phân tích các memory candidate..."):
                        extracted = MemoryService.extract_memories_from_conversation(db, st.session_state.user_id, active_conv_id)
                        if extracted:
                            st.success(f"Đã trích xuất {len(extracted)} memory candidates! Vui lòng sang tab 'Duyệt Memory' để phân quyền.")
                        else:
                            st.info("Chưa tìm thấy thuộc tính mới cần lưu.")


# ------------------------------------------------------------------------------
# PAGE 2: 🧠 DUYỆT MEMORY & CONSENT
# ------------------------------------------------------------------------------
elif st.session_state.selected_nav == "🧠 Duyệt Memory":
    st.markdown("## 🧠 Duyệt Memory Candidates & Phân quyền Consent")
    st.caption("Sau mỗi cuộc trò chuyện, Cupid đề xuất những thuộc tính có thể ghi nhớ. **Bạn là người hoàn toàn quyết định** thông tin nào được lưu và sử dụng vào mục đích gì.")

    pending_list = MemoryService.get_pending_candidates(db, st.session_state.user_id)

    if not pending_list:
        st.info("🎉 Bạn không có memory candidate nào đang chờ duyệt. Hãy trò chuyện thêm với Cupid và nhấn 'Trích xuất Memory' nhé!")
    else:
        st.write(f"📋 **Có {len(pending_list)} đề xuất ghi nhớ cần bạn duyệt:**")

        for idx, candidate in enumerate(pending_list):
            with st.container():
                st.markdown(f"""
                <div class="cupid-card">
                    <h4>{CATEGORY_LABELS_VI.get(candidate.category, candidate.category)}</h4>
                    <p><b>Nội dung trích xuất:</b> <i>"{candidate.human_readable_value}"</i></p>
                    <p><span class="badge-confidence">Độ tin cậy: {int(candidate.confidence * 100)}%</span> | <span class="badge-category">Stability: {candidate.stability}</span></p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    if st.button("🔒 Chat riêng tư (PRIVATE_ONLY)", key=f"priv_{candidate.id}", use_container_width=True):
                        MemoryService.process_consent_decision(db, st.session_state.user_id, candidate.id, "PRIVATE_ONLY")
                        st.toast("Đã lưu memory vào chế độ Chat riêng tư!")
                        st.rerun()
                    st.caption("Chỉ Cupid dùng khi trò chuyện với bạn.")

                with col2:
                    if st.button("💘 Tính tương thích (MATCH_USE)", key=f"match_{candidate.id}", use_container_width=True):
                        MemoryService.process_consent_decision(db, st.session_state.user_id, candidate.id, "MATCH_USE")
                        st.toast("Đã duyệt memory cho Matching Engine!")
                        st.rerun()
                    st.caption("Dùng tính hợp, không hiện nguyên văn.")

                with col3:
                    if st.button("🌐 Hiển thị bài giới thiệu (SHAREABLE)", key=f"share_{candidate.id}", use_container_width=True):
                        MemoryService.process_consent_decision(db, st.session_state.user_id, candidate.id, "SHAREABLE")
                        st.toast("Đã duyệt memory ở chế độ Công khai ghép đôi!")
                        st.rerun()
                    st.caption("Dùng tính hợp & có thể xuất hiện bài giới thiệu.")

                with col4:
                    if st.button("❌ Không lưu (DO_NOT_SAVE)", key=f"nosave_{candidate.id}", use_container_width=True):
                        MemoryService.process_consent_decision(db, st.session_state.user_id, candidate.id, "DO_NOT_SAVE")
                        st.toast("Đã loại bỏ memory!")
                        st.rerun()
                    st.caption("Bỏ qua hoàn toàn, không lưu vào DB.")

                st.divider()


# ------------------------------------------------------------------------------
# PAGE 3: 📋 CUPID HIỂU GÌ VỀ BẠN (RELATIONSHIP PROFILE)
# ------------------------------------------------------------------------------
elif st.session_state.selected_nav == "📋 Cupid hiểu gì về bạn":
    st.markdown("## 📋 Trang 'Cupid hiểu gì về bạn'")
    st.caption("Tổng hợp minh bạch toàn bộ dữ liệu mà Cupid đã thấu hiểu từ bạn. Bạn có thể kiểm tra, đổi quyền sử dụng hoặc đánh dấu Cupid hiểu sai.")

    profile_data = ProfileService.get_user_profile_grouped(db, st.session_state.user_id)
    grouped = profile_data["grouped_memories"]

    st.write(f"📊 **Tổng số thuộc tính đã lưu:** {profile_data['total_count']}")

    # Form thêm thuộc tính tự chọn
    with st.expander("➕ Tự thêm thuộc tính mới vào hồ sơ"):
        with st.form("add_custom_memory_form"):
            new_cat = st.selectbox("Danh mục:", list(CATEGORY_LABELS_VI.keys()), format_func=lambda x: CATEGORY_LABELS_VI[x])
            new_val = st.text_input("Nội dung diễn giải (VD: Thích nấu ăn cuối tuần và không thích hút thuốc):")
            new_vis = st.selectbox("Quyền sử dụng:", ["MATCH_USE", "SHAREABLE", "PRIVATE_ONLY"])
            submit_add = st.form_submit_button("Thêm vào hồ sơ")
            if submit_add and new_val:
                ProfileService.add_custom_memory(db, st.session_state.user_id, new_cat, new_val, new_vis)
                st.success("Đã thêm thuộc tính mới thành công!")
                st.rerun()

    st.divider()

    # Hiển thị 10 hạng mục tiêu chuẩn
    categories_to_display = [
        ("relationship_goal", "🎯 Mục tiêu mối quan hệ"),
        ("core_value", "💎 Giá trị sống"),
        ("communication_style", "🗣️ Phong cách giao tiếp"),
        ("lifestyle", "🌿 Phong cách sống"),
        ("social_preference", "🤝 Mức độ hướng ngoại/hướng nội"),
        ("relationship_pace", "⏱️ Tốc độ phát triển mối quan hệ"),
        ("personal_boundary", "🛡️ Ranh giới cá nhân"),
        ("dealbreaker", "🚫 Điều không thể chấp nhận (Dealbreaker)"),
    ]

    for cat_key, cat_label in categories_to_display:
        st.subheader(cat_label)
        memories_in_cat = grouped.get(cat_key, [])

        if not memories_in_cat:
            st.caption("📌 Chưa có dữ liệu cho hạng mục này.")
        else:
            for mem in memories_in_cat:
                c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
                with c1:
                    st.write(f"• **{mem.human_readable_value}**")
                    st.caption(f"Confidence: {int(mem.confidence*100)}% | Stability: {mem.stability}")
                with c2:
                    current_vis = mem.visibility
                    new_vis = st.selectbox("Quyền:", ["MATCH_USE", "SHAREABLE", "PRIVATE_ONLY"], index=["MATCH_USE", "SHAREABLE", "PRIVATE_ONLY"].index(current_vis) if current_vis in ["MATCH_USE", "SHAREABLE", "PRIVATE_ONLY"] else 0, key=f"vis_sel_{mem.id}")
                    if new_vis != current_vis:
                        ProfileService.update_memory_visibility(db, st.session_state.user_id, mem.id, new_vis)
                        st.toast(f"Đã cập nhật quyền sang {new_vis}")
                        st.rerun()
                with c3:
                    if st.button("⚠️ Cupid hiểu sai", key=f"wrong_{mem.id}", use_container_width=True):
                        ProfileService.flag_misunderstanding(db, st.session_state.user_id, mem.id)
                        st.toast("Đã xóa thuộc tính do Cupid hiểu sai!")
                        st.rerun()
                with c4:
                    if st.button("🗑️ Xóa", key=f"del_{mem.id}", use_container_width=True):
                        ProfileService.delete_memory(db, st.session_state.user_id, mem.id)
                        st.toast("Đã xóa thuộc tính!")
                        st.rerun()
        st.divider()

    # 9. Những dữ liệu còn thiếu
    st.subheader("🔍 Những dữ liệu còn thiếu (Missing Dimensions)")
    if profile_data["missing_categories"]:
        st.warning(f"Hồ sơ của bạn còn thiếu: {', '.join(profile_data['missing_labels'])}. Trò chuyện thêm với Cupid để ghép đôi chính xác hơn nhé!")
    else:
        st.success("🎉 Hồ sơ của bạn đã đầy đủ các thuộc tính cốt lõi để ghép đôi!")


# ------------------------------------------------------------------------------
# PAGE 4: 💘 TÌM NGƯỜI PHÙ HỢP (EXPLAINABLE RECOMMENDATIONS)
# ------------------------------------------------------------------------------
elif st.session_state.selected_nav == "💘 Tìm người phù hợp":
    st.markdown("## 💘 Gợi ý đối tượng phù hợp (Top 3 Candidates)")
    st.caption("Matching Engine so sánh hồ sơ của bạn với 25 ứng viên mẫu giả lập bằng công thức Weighted Scoring minh bạch (**không đọc raw chat**).")

    # Filter điều chỉnh tiêu chí
    with st.expander("⚙️ Điều chỉnh tiêu chí tìm kiếm (Filter Preferences)"):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            pref_gender = st.selectbox("Bạn quan tâm giới tính:", ["female", "male", "all"])
        with col_f2:
            pref_city = st.selectbox("Thành phố ưu tiên:", ["Tất cả", "Hà Nội", "TP.HCM", "Đà Nẵng", "Huế", "Cần Thơ"])
        with col_f3:
            pref_goal = st.selectbox("Mục tiêu ưu tiên:", ["Bất kỳ", "long_term", "marriage", "casual_to_serious"])

    if st.button("🚀 Tìm người phù hợp ngay", type="primary", use_container_width=True):
        filters = {}
        if pref_gender != "all":
            filters["interested_in"] = [pref_gender]
        if pref_city != "Tất cả":
            filters["city"] = pref_city

        with st.spinner("Matching Engine đang tính toán điểm tương thích..."):
            match_req, top_matches = MatchingEngine.run_match(db, st.session_state.user_id, filters)
            st.session_state.latest_matches = top_matches

    if "latest_matches" in st.session_state and st.session_state.latest_matches:
        top_matches = st.session_state.latest_matches
        st.success(f"🎉 Hệ thống đã tìm thấy {len(top_matches)} đối tượng phù hợp nhất với bạn!")

        for match_res, candidate, score_info in top_matches:
            st.markdown(f"""
            <div class="cupid-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2>{candidate.display_name}, {candidate.age} tuổi</h2>
                    <div class="score-badge">{score_info['total_score']}% Hợp</div>
                </div>
                <p>📍 <b>{candidate.city}</b> | 💼 {candidate.occupation} | 🎯 Mục tiêu: {candidate.relationship_goal}</p>
                <p><b>Lời giới thiệu:</b> <i>"{candidate.shareable_intro}"</i></p>
                <p><span class="badge-confidence">Confidence Score: {int(score_info['confidence']*100)}%</span></p>
            </div>
            """, unsafe_allow_html=True)

            # Phần giải thích tự nhiên từ LLM
            with st.expander(f"💡 Xem giải thích chi tiết vì sao {candidate.display_name} phù hợp với bạn", expanded=True):
                if match_res.explanation_text:
                    st.markdown(match_res.explanation_text)
                else:
                    with st.spinner("LLM đang tổng hợp câu giải thích tự nhiên..."):
                        exp_text = ExplanationService.generate_explanation(db, st.session_state.user_id, match_res.id)
                        st.markdown(exp_text)

            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                if st.button(f"❤️ Quan tâm {candidate.display_name}", key=f"like_{candidate.id}", use_container_width=True):
                    st.toast(f"Đã ghi nhận phản hồi 'Quan tâm' với {candidate.display_name}!")
            with col_b2:
                if st.button(f"❌ Không phù hợp", key=f"dislike_{candidate.id}", use_container_width=True):
                    st.toast(f"Đã ghi nhận phản hồi 'Không phù hợp' với {candidate.display_name}.")
            with col_b3:
                if st.button(f"💬 Hỏi Cupid thêm về {candidate.display_name}", key=f"ask_{candidate.id}", use_container_width=True):
                    st.session_state.selected_nav = "💬 Cupid Chat"
                    st.rerun()

            st.divider()


# ------------------------------------------------------------------------------
# PAGE 5: 🛡️ QUYỀN RIÊNG TƯ & SECURITY AUDIT
# ------------------------------------------------------------------------------
elif st.session_state.selected_nav == "🛡️ Quyền riêng tư & Audit":
    st.markdown("## 🛡️ Quyền riêng tư & Security Audit Logs")
    st.caption("Cupid cam kết bảo vệ dữ liệu cá nhân tuyệt đối. **LLM không bao giờ có quyền truy cập trực tiếp vào DB** và mọi hành vi đều được ghi lại nhật ký audit.")

    st.subheader("📜 Nhật ký truy vết bảo mật (Audit Logs)")
    logs = db.query(AuditLog).filter(AuditLog.actor_id == st.session_state.user_id).order_by(AuditLog.timestamp.desc()).limit(20).all()

    if not logs:
        st.info("Chưa có nhật ký truy vết nào.")
    else:
        for log in logs:
            st.write(f"• `[{log.timestamp.strftime('%H:%M:%S %d/%m/%Y')}]` **Action:** `{log.action}` | **Decision:** `{log.decision}` | Details: {log.details or 'N/A'}")

    st.divider()
    st.subheader("🧹 Quản lý dữ liệu cá nhân")
    if st.button("🗑️ Xóa toàn bộ dữ liệu & Reset hồ sơ của tôi", type="secondary"):
        db.query(ApprovedMemory).filter(ApprovedMemory.owner_id == st.session_state.user_id).delete()
        db.query(MemoryCandidate).filter(MemoryCandidate.user_id == st.session_state.user_id).delete()
        db.commit()
        st.success("Đã xóa toàn bộ dữ liệu hồ sơ cá nhân thành công!")
        st.rerun()


# ------------------------------------------------------------------------------
# PAGE 6: 🔐 ĐĂNG NHẬP / ĐĂNG KÝ (AUTH PANEL)
# ------------------------------------------------------------------------------
elif st.session_state.selected_nav == "🔐 Đăng nhập / Đăng ký":
    st.markdown("## 🔐 Đăng nhập & Đăng ký Tài khoản")
    st.caption("Mỗi người dùng có một không gian dữ liệu tách biệt tuyệt đối.")

    tab_login, tab_register = st.tabs(["Đăng nhập", "Đăng ký tài khoản mới"])

    with tab_login:
        with st.form("login_form"):
            l_email = st.text_input("Email:")
            l_pwd = st.text_input("Mật khẩu:", type="password")
            submit_login = st.form_submit_button("Đăng nhập")

            if submit_login:
                ok, res = AuthService.authenticate_user(db, l_email, l_pwd)
                if ok:
                    st.session_state.user_id = res.id
                    st.session_state.user_email = res.email
                    st.session_state.display_name = res.display_name
                    st.success(f"Đăng nhập thành công! Chào mừng {res.display_name}")
                    st.session_state.selected_nav = "💬 Cupid Chat"
                    st.rerun()
                else:
                    st.error(res)

    with tab_register:
        with st.form("register_form"):
            r_name = st.text_input("Tên hiển thị:")
            r_email = st.text_input("Email đăng ký:")
            r_pwd = st.text_input("Mật khẩu:", type="password")
            submit_reg = st.form_submit_button("Tạo tài khoản")

            if submit_reg:
                ok, res = AuthService.register_user(db, r_email, r_pwd, r_name)
                if ok:
                    st.session_state.user_id = res.id
                    st.session_state.user_email = res.email
                    st.session_state.display_name = res.display_name
                    st.success(f"Tạo tài khoản thành công! Bạn đã sẵn sàng trải nghiệm.")
                    st.session_state.selected_nav = "💬 Cupid Chat"
                    st.rerun()
                else:
                    st.error(res)


db.close()
