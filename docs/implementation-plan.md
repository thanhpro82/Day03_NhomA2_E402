# Implementation Plan - MVP Cupid Agent 💘

Xây dựng MVP **Cupid Agent — Trợ lý trò chuyện, hiểu người dùng và gợi ý đối tượng phù hợp**.

## 1. Tóm tắt cách hiểu bài toán
- **Mục tiêu**: Kiểm chứng giả thuyết: *Người dùng có sẵn sàng trò chuyện với một AI Companion (Cupid) để AI thấu hiểu dần dần và đưa ra gợi ý hẹn hò kèm giải thích minh bạch hay không?*
- **Core Loop**:
  1. Người dùng trò chuyện tự nhiên với Cupid Agent.
  2. Cupid phản hồi tự nhiên, lắng nghe, gợi mở (tối đa 1 câu hỏi/lượt), trích xuất memory candidates.
  3. Người dùng duyệt & phân quyền memory (`PRIVATE_ONLY`, `MATCH_USE`, `SHAREABLE`, `DO_NOT_SAVE`).
  4. Profile "Cupid hiểu gì về bạn" tự động cập nhật.
  5. Matching Engine (Weighted scoring, rule-based, KHÔNG đọc raw chat) tính toán độ tương thích với 20-30 candidate giả lập.
  6. LLM sinh giải thích tự nhiên (Explainable Recommendation) dựa trên `reason_code`.
  7. Người dùng phản hồi "Quan tâm" / "Không phù hợp".

## 2. Kiến trúc đề xuất
- **Architecture**: Modular Monolith (FastAPI Core Backend + Streamlit Glassmorphic Frontend Web UI).
- **Security Barrier**:
  - LLM KHÔNG truy cập DB trực tiếp.
  - Matching Engine KHÔNG đọc raw chat.
  - Data isolation: Mọi query DB bắt buộc có `WHERE owner_id = authenticated_user_id`.
- **LLM Abstraction**: `LLMProvider` hỗ trợ OpenAI, Gemini và `MockProvider` fallback (cho phép demo full-flow offline khi không có API Key).

## 3. Cấu trúc thư mục
```text
Day03_NhomA2_E402/
├── .env.example
├── README.md
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── config/
│   ├── system_prompts.py
│   └── test_cases.json
├── docs/
│   └── implementation-plan.md
├── src/
│   ├── app.py                     # Streamlit Frontend Web App
│   ├── config.py                  # Settings & Prompts
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py              # SQLAlchemy ORM Data Models
│   │   └── seed.py                # 25 Fake Candidates Seed Script
│   ├── services/
│   │   ├── llm_provider.py        # Abstract Provider (OpenAI/Gemini/Mock)
│   │   ├── conversation_service.py
│   │   ├── memory_service.py      # Extraction & Approval
│   │   ├── profile_service.py
│   │   ├── matching_engine.py     # Rule-based Weighted Scoring
│   │   ├── explanation_service.py # LLM Explainability
   │   ├── safety_service.py      # Moderation & Privacy Filter
   │   └── audit_service.py       # Audit logging
   └── tests/
       ├── unit/
       ├── integration/
       └── security/
```

## 4. Data Model Schema
- `users`: `id`, `email`, `password_hash`, `created_at`
- `conversations`: `id`, `user_id`, `title`, `created_at`, `updated_at`
- `messages`: `id`, `conversation_id`, `sender_type`, `content`, `created_at`
- `memory_candidates`: `id`, `user_id`, `conversation_id`, `category`, `key`, `value`, `human_readable_value`, `confidence`, `stability`, `sensitivity`, `recommended_usage`, `status`, `created_at`
- `approved_memories`: `id`, `owner_id`, `category`, `key`, `value`, `human_readable_value`, `confidence`, `stability`, `sensitivity`, `visibility`, `user_confirmed`, `created_at`, `updated_at`
- `candidate_profiles`: 25 candidate profiles với 20 trường thông tin tiêu chuẩn.
- `match_requests`, `match_results`, `match_feedback`, `consent_records`, `audit_logs`.

## 5. Danh sách API Endpoints
- Auth: `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`
- Conversation: `POST /conversations`, `GET /conversations`, `GET /conversations/{id}`, `POST /conversations/{id}/messages`
- Memory: `POST /conversations/{id}/extract-memories`, `GET /memory-candidates`, `PATCH /memory-candidates/{id}/decision`
- Profile: `GET /profile`, `PATCH /profile/memories/{id}`, `DELETE /profile/memories/{id}`
- Matching: `GET /candidates`, `POST /matches/recommend`, `GET /matches/results/{id}`, `POST /matches/{id}/feedback`

## 6. Luồng Chat & Memory Lifecycle
1. User gửi tin nhắn -> Guardrails (`SafetyService`) kiểm tra Prompt Injection / Stalking / System Prompt Leakage.
2. `ConversationService` truyền `approved_memories` đã duyệt vào context (không bao giờ truyền dữ liệu user khác).
3. Cupid Agent phản hồi ấm áp, tự nhiên, đặt 1 câu hỏi mở.
4. `MemoryExtractionService` dùng JSON Schema trích xuất Memory Candidates.
5. User duyệt phân quyền (`PRIVATE_ONLY`, `MATCH_USE`, `SHAREABLE`, `DO_NOT_SAVE`).
6. Memory được approved được đưa vào `approved_memories` & hiển thị ở Profile "Cupid hiểu gì về bạn".

## 7. Công thức Matching Engine
- **Hard Constraints**: Giới tính quan tâm, độ tuổi, thành phố, absolute dealbreakers (Xung đột -> Score = 0).
- **Weighted Dimensions** (100%):
  - Relationship Goal: 20%
  - Core Values: 20%
  - Communication Style: 15%
  - Relationship Pace: 10%
  - Lifestyle & Energy: 10%
  - Conflict Style: 10%
  - Boundaries: 10%
  - Shared Interests: 5%
- **Penalties**: Dealbreaker soft conflict (-30%), Missing critical data (-5%/trường).

## 8. Các Milestones Triển Khai
- Milestone 1: Mock Provider & Core Architecture & Streamlit UI (Cho phép dùng thử Chat Agent & Full Flow ngay với Demo User Session).
- Milestone 2: ORM Data Models, SQLite Storage & Seed 25 Candidates.
- Milestone 3: Structured Memory Extraction & Consent Approval UI.
- Milestone 4: Relationship Profile UI & CRUD.
- Milestone 5: Rule-based Weighted Matching Engine & Explanation Generator.
- Milestone 6: Candidate Cards & Feedback.
- Milestone 7: Auth, Security Guardrails & Test Suite (Unit, Integration, Security).
- Milestone 8: Docker, Makefile, README & Final Verification.

## 9. Giả định
- Cho phép trải nghiệm luồng Chat Agent & Matching ngay bằng Default Active User Session (có nút chuyển đổi tài khoản).
- 25 ứng viên mẫu hoàn toàn giả lập.
- Chạy 100% offline được qua `MockProvider` nếu chưa thiết lập API key.

## 10. Technical Risks & Mitigations
- Prompt Injection: Dùng strict input sanitizer + policy barrier.
- Memory extraction errors: Có bước Human-in-the-loop (Consent UI) cho phép người dùng sửa/xóa/đánh dấu sai.
- Privacy Leaks: Matching Engine chỉ được đọc dữ liệu có `visibility IN ('MATCH_USE', 'SHAREABLE')`.
