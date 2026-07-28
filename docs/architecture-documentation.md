# 🏗️ Architecture Documentation — Cupid Agent 💘

## 1. Tổng quan Kiến trúc
Cupid Agent MVP được xây dựng theo mô hình **Modular Monolith** với nguyên tắc cốt lõi:
- **Privacy First**: Dữ liệu riêng tư cá nhân (`PRIVATE_ONLY`) không đi vào Matching Engine.
- **Consent First**: Mọi memory candidate trích xuất từ chat bắt buộc trải qua bước người dùng gắn nhãn quyền sử dụng.
- **Explainability**: Matching Engine chạy hoàn toàn theo công thức mã Python (Weighted Scoring), không để LLM tự tạo điểm số. LLM chỉ được dùng để diễn giải `reason_code` thành câu văn tự nhiên.
- **Hard Security Barrier**: LLM không có quyền truy vấn DB trực tiếp. Backend API đóng vai trò kiểm soát phân quyền tuyệt đối (`WHERE owner_id = authenticated_user_id`).

## 2. Các Service thành phần

```text
User
  ↓
Frontend (Streamlit / Dark Glassmorphic UI)
  ↓
Auth & Session Middleware
  ↓
Safety & Moderation Service
  ↓
Conversation Service & Context Builder
  ↓
LLM Provider Abstraction (OpenAI / Gemini / MockProvider Fallback)
  ↓
Memory Extraction Service & Consent Manager
  ↓
Relationship Profile Service
  ↓
Rule-based Weighted Matching Engine (No Raw Chat Reading)
  ↓
Match Explanation Service (LLM Reason Code Formatter)
  ↓
Security Audit Logging Service
```

## 3. Quy trình bảo vệ Quyền riêng tư (Privacy Guard)
1. **Input Moderation**: Kiểm tra Prompt Injection, System Prompt Extraction, Stalking, Unauthorized Action.
2. **Context Window Builder**: Chỉ nạp `ApprovedMemories` thuộc về chính `authenticated_user_id` có `visibility` được phép.
3. **Matching Engine Isolation**: Chỉ sử dụng các thuộc tính có `visibility IN ('MATCH_USE', 'SHAREABLE')`. Raw conversation messages tuyệt đối không đi vào Matching Engine.
4. **Audit Logging**: Mọi hành vi được lưu trong bảng `audit_logs` mà không lưu nội dung trò chuyện nhạy cảm.
