# 💘 CUPID AGENT — TRỢ LÝ TRÒ CHUYỆN, HIỂU NGƯỜI DÙNG & GỢI Ý ĐỐI TƯỢNG PHÙ HỢP

> **MVP Kiểm chứng giả thuyết**: *Người dùng có sẵn sàng trò chuyện tự nhiên với một AI Companion để AI thấu hiểu dần dần và đưa ra những gợi ý hẹn hò có thể giải thích hay không?*

---

## 🌟 Điểm nổi bật của Sản phẩm

1. **Cupid Agent Companion Chat**: Trò chuyện ấm áp, lắng nghe tự nhiên, không phán xét, gợi mở 1 câu hỏi/lượt.
2. **Structured Memory Extraction**: Trích xuất các thuộc tính cá nhân (sở thích, ranh giới, giá trị sống, dealbreaker,...) chuẩn JSON Schema.
3. **Human-in-the-Loop Consent Control**: Người dùng toàn quyền kiểm soát từng memory với 4 cấp độ:
   - `PRIVATE_ONLY`: Chỉ dùng khi Cupid chat với chính bạn.
   - `MATCH_USE`: Dùng tính điểm tương thích, không hiện nguyên văn.
   - `SHAREABLE`: Dùng tính điểm tương thích & xuất hiện ở phần giới thiệu.
   - `DO_NOT_SAVE`: Loại bỏ hoàn toàn, không lưu.
4. **Transparent Relationship Profile**: Trang *"Cupid hiểu gì về bạn"* minh bạch 10 nhóm thuộc tính, hỗ trợ sửa, xóa, báo Cupid hiểu sai.
5. **Rule-based Weighted Matching Engine**: Tính điểm tương thích chuẩn với 25 ứng viên mẫu giả lập (**tuyệt đối không đọc raw chat**).
6. **Explainable Recommendations**: LLM diễn giải lý do phù hợp, điểm tương đồng, điểm khác biệt và câu hỏi gợi mở trò chuyện.
7. **Privacy & Security First**: Tách biệt dữ liệu người dùng tuyệt đối (`WHERE owner_id = authenticated_user_id`), phòng chống Prompt Injection & System Prompt Extraction, lưu nhật ký Audit bảo mật.
8. **100% Offline Smart Mock Mode**: Chạy demo full-flow mượt mà không cần API Key.

---

## 🛠️ Hướng dẫn Cài đặt & Khởi chạy

### Cách 1: Chạy trực tiếp bằng Python Virtualenv

```bash
# 1. Khởi tạo môi trường ảo Python & Cài đặt thư viện
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Khởi tạo Database & Seed 25 Candidate Mẫu
PYTHONPATH=. python3 src/database/seed.py

# 3. Khởi chạy Web UI (Streamlit Dark Glassmorphism Theme)
PYTHONPATH=. streamlit run src/app.py
```

Ứng dụng sẽ tự động mở tại trình duyệt: `http://localhost:8501`

---

### Cách 2: Chạy bằng Docker Compose

```bash
docker compose up --build
```

---

### Cách 3: Sử dụng Makefile

```bash
make dev      # Chạy ứng dụng Streamlit dev server
make test     # Chạy bộ unit, integration & security tests
make seed     # Khởi tạo 25 ứng viên mẫu
make reset    # Reset và tạo lại database mẫu sạch
```

---

## ⚙️ Cấu hình API Key (Tùy chọn)

Sao chép file `.env.example` thành `.env`:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env`:
- `LLM_PROVIDER=auto` (hoặc `openai` / `gemini` / `mock`)
- `OPENAI_API_KEY=sk-...` (nếu dùng OpenAI)
- `GEMINI_API_KEY=...` (nếu dùng Gemini)

*Ghi chú: Nếu chưa có API Key, hệ thống tự động bật **Smart Offline MockLLMProvider** giúp bạn demo trọn vẹn toàn bộ tính năng mà không có bất kỳ lỗi nào.*

---

## 🎬 Hướng dẫn Test Luồng Demo 10 Bước (Demo Flow)

1. Mở ứng dụng tại `http://localhost:8501`. Mặc định hệ thống tự đăng nhập tài khoản **Người dùng Demo** (`demo@cupid.ai`).
2. Vào tab **💬 Cupid Chat**, gửi đoạn văn tâm sự:
   > *"Mình khá hướng nội và thích dành cuối tuần ở quán cà phê hoặc đọc sách. Mình muốn một mối quan hệ nghiêm túc nhưng thích tìm hiểu từ từ. Mình không thích người quá kiểm soát."*
3. Cupid sẽ phản hồi tự nhiên, ấm áp và hỏi thêm 1 câu mở.
4. Bấm nút **🧠 Trích xuất Memory từ cuộc trò chuyện**.
5. Chuyển sang tab **🧠 Duyệt Memory**: Bạn sẽ thấy danh sách các memory candidate được trích xuất (hướng nội, đọc sách & cà phê, mối quan hệ nghiêm túc, tìm hiểu từ từ, dị ứng kiểm soát). Gán quyền `MATCH_USE` hoặc `SHAREABLE` cho từng thuộc tính.
6. Chuyển sang tab **📋 Cupid hiểu gì về bạn**: Kiểm tra profile của bạn đã được cập nhật đầy đủ các nhóm thuộc tính.
7. Chuyển sang tab **💘 Tìm người phù hợp**: Nhấn **🚀 Tìm người phù hợp ngay**.
8. Matching Engine so sánh và trả về Top 3 ứng viên mẫu phù hợp nhất (VD: Minh, Linh,...).
9. Mở phần **💡 Xem giải thích chi tiết**: Đọc giải thích tự nhiên từ LLM (lý do hợp, điểm giống, điểm khác, câu hỏi gợi mở).
10. Bấm nút **❤️ Quan tâm** hoặc **❌ Không phù hợp** để gửi feedback.

---

## 🧪 Hướng dẫn Chạy Kiểm thử (Testing Suite)

Hệ thống bao gồm bộ kiểm thử toàn diện cho Unit, Integration và Security:

```bash
# Chạy bộ test đầy đủ
PYTHONPATH=. .venv/bin/pytest src/tests/ -v
```

Các bài test bao gồm:
- `src/tests/unit/test_matching_engine.py`: Test weighted scoring, hard constraints, dealbreaker penalty, privacy visibility isolation.
- `src/tests/integration/test_user_flow.py`: Test toàn bộ luồng người dùng khép kín từ Đăng ký -> Chat -> Memory -> Consent -> Profile -> Match -> Feedback.
- `src/tests/security/test_privacy_guard.py`: Test chống Prompt Injection, System Prompt Extraction, Stalking, Doxxing, và cách ly dữ liệu giữa User A & User B.

---

## 📁 Cấu trúc Thư mục Dự án

```text
Day03_NhomA2_E402/
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── README.md
├── requirements.txt
├── config/
│   └── test_cases.json
├── docs/
│   ├── architecture-documentation.md
│   └── implementation-plan.md
├── src/
│   ├── app.py                     # Streamlit Frontend Web App
│   ├── config.py                  # Environment & App Settings & Prompts
│   ├── database/
│   │   ├── connection.py          # SQLAlchemy Connection & Session
│   │   ├── models.py              # 11 ORM Data Models
│   │   └── seed.py                # Script khởi tạo 25 Candidates hư cấu & Demo User
│   ├── services/
│   │   ├── llm_provider.py        # LLM Adapter (OpenAI/Gemini/MockProvider)
│   │   ├── conversation_service.py # Quản lý hội thoại & context
│   │   ├── memory_service.py      # Trích xuất memory & Consent
│   │   ├── profile_service.py     # Quản lý Relationship Profile CRUD
│   │   ├── matching_engine.py     # Rule-based Weighted Scoring Engine
│   │   ├── explanation_service.py # Match Explanation Service
│   │   ├── safety_service.py      # Moderation & Privacy Filter
│   │   ├── audit_service.py       # Security Audit Logging
│   │   └── auth_service.py        # Authentication & Isolation
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── security/
```
