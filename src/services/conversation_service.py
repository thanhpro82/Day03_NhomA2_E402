"""
💬 CONVERSATION SERVICE — CUPID AGENT 💘
Quản lý luồng tin nhắn, context window và cách tương tác của Cupid Agent.
"""

from sqlalchemy.orm import Session
from src.database.models import Conversation, Message, ApprovedMemory
from src.services.llm_provider import get_llm_provider
from src.services.safety_service import SafetyService
from src.services.audit_service import AuditService
from src.config import CUPID_SYSTEM_PROMPT


class ConversationService:
    """Service xử lý nghiệp vụ hội thoại"""

    @staticmethod
    def get_or_create_conversation(db: Session, user_id: str, conversation_id: str = None) -> Conversation:
        """Lấy phiên trò chuyện hiện tại hoặc tạo phiên mới cho user"""
        if conversation_id:
            conv = db.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            ).first()
            if conv:
                return conv

        # Tạo conversation mới
        new_conv = Conversation(user_id=user_id, title="Cuộc trò chuyện với Cupid")
        db.add(new_conv)
        db.commit()
        db.refresh(new_conv)

        # Log audit
        AuditService.log_event(db, actor_id=user_id, action="CREATE_CONVERSATION", resource_id=new_conv.id)

        # Gửi tin nhắn chào mừng mặc định của Cupid
        welcome_msg = Message(
            conversation_id=new_conv.id,
            sender_type="agent",
            content="Chào bạn, mình là Cupid 💘! Rất vui được đồng hành cùng bạn. Hôm nay của bạn thế nào?"
        )
        db.add(welcome_msg)
        db.commit()

        return new_conv

    @staticmethod
    def list_user_conversations(db: Session, user_id: str) -> list:
        """Lấy danh sách các cuộc trò chuyện của user (Bảo mật: WHERE user_id = authenticated_user_id)"""
        return db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc()).all()

    @staticmethod
    def get_messages(db: Session, user_id: str, conversation_id: str) -> list:
        """Lấy lịch sử tin nhắn của một cuộc trò chuyện"""
        conv = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()

        if not conv:
            return []

        return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()

    @staticmethod
    def send_message(db: Session, user_id: str, conversation_id: str, user_content: str) -> Message:
        """
        Gửi tin nhắn của người dùng, kiểm tra an toàn và nhận câu trả lời từ Cupid Agent.
        """
        conv = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()

        if not conv:
            raise ValueError("Không tìm thấy phiên trò chuyện hoặc không có quyền truy cập.")

        # 1. Kiểm tra an toàn (Safety Inspection)
        is_safe, refusal_msg, violation_code = SafetyService.inspect_input(user_id, user_content)
        if not is_safe:
            AuditService.log_event(db, actor_id=user_id, action="SAFETY_BLOCKED", resource_id=conversation_id, decision="BLOCKED", details=violation_code)
            # Lưu tin nhắn người dùng và câu từ chối an toàn
            user_msg = Message(conversation_id=conversation_id, sender_type="user", content=user_content)
            agent_msg = Message(conversation_id=conversation_id, sender_type="agent", content=refusal_msg)
            db.add(user_msg)
            db.add(agent_msg)
            db.commit()
            return agent_msg

        # 2. Lưu tin nhắn người dùng
        user_msg = Message(conversation_id=conversation_id, sender_type="user", content=user_content)
        db.add(user_msg)
        db.commit()

        # 3. Lấy bối cảnh (Context Building: Chỉ lấy ApprovedMemories của chính user_id)
        approved_memories = db.query(ApprovedMemory).filter(
            ApprovedMemory.owner_id == user_id,
            ApprovedMemory.visibility.in_(["PRIVATE_ONLY", "MATCH_USE", "SHAREABLE"])
        ).all()

        memory_context = ""
        if approved_memories:
            memory_lines = [f"- {m.human_readable_value}" for m in approved_memories]
            memory_context = "\nThông tin bạn đã biết về người dùng (dùng để ứng xử phù hợp, không lặp lại nguyên văn):\n" + "\n".join(memory_lines)

        full_system_prompt = f"{CUPID_SYSTEM_PROMPT}\n{memory_context}"

        # 4. Lấy lịch sử 10 tin nhắn gần nhất
        history_msgs = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()[-10:]
        msg_history_payload = [{"sender_type": m.sender_type, "content": m.content} for m in history_msgs]

        # 5. Gọi LLM Provider
        provider = get_llm_provider()
        raw_response = provider.chat(msg_history_payload, system_prompt=full_system_prompt)
        safe_response = SafetyService.filter_output(raw_response)

        # 6. Lưu phản hồi của Agent
        agent_msg = Message(conversation_id=conversation_id, sender_type="agent", content=safe_response)
        db.add(agent_msg)
        db.commit()

        AuditService.log_event(db, actor_id=user_id, action="SEND_MESSAGE", resource_id=conversation_id, decision="ALLOW")
        return agent_msg
