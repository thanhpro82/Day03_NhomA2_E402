"""
🗄️ SQLALCHEMY ORM DATA MODELS — CUPID AGENT 💘
"""

from datetime import datetime
import uuid
import json
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from src.database.connection import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    display_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="owner", cascade="all, delete-orphan")
    memory_candidates = relationship("MemoryCandidate", back_populates="owner", cascade="all, delete-orphan")
    approved_memories = relationship("ApprovedMemory", back_populates="owner", cascade="all, delete-orphan")
    match_requests = relationship("MatchRequest", back_populates="owner", cascade="all, delete-orphan")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, default="Trò chuyện mới")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False, index=True)
    sender_type = Column(String, nullable=False)  # 'user' hoặc 'agent'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


class MemoryCandidate(Base):
    __tablename__ = "memory_candidates"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=True)
    category = Column(String, nullable=False)
    key = Column(String, nullable=False)
    value = Column(Text, nullable=False)
    human_readable_value = Column(Text, nullable=False)
    confidence = Column(Float, default=0.8)
    stability = Column(String, default="stable")  # temporary, medium_term, stable, unknown
    sensitivity = Column(String, default="normal")  # normal, personal, sensitive, highly_sensitive
    recommended_usage = Column(String, default="match_profile")
    status = Column(String, default="PENDING")  # PENDING, APPROVED, REJECTED
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="memory_candidates")


class ApprovedMemory(Base):
    __tablename__ = "approved_memories"

    id = Column(String, primary_key=True, default=generate_uuid)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String, nullable=False)
    key = Column(String, nullable=False)
    value = Column(Text, nullable=False)
    human_readable_value = Column(Text, nullable=False)
    confidence = Column(Float, default=0.8)
    stability = Column(String, default="stable")
    sensitivity = Column(String, default="normal")
    visibility = Column(String, nullable=False)  # PRIVATE_ONLY, MATCH_USE, SHAREABLE, DO_NOT_SAVE
    source_conversation_id = Column(String, nullable=True)
    user_confirmed = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="approved_memories")


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(String, primary_key=True)  # e.g. candidate_001
    display_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)  # male, female, other
    interested_in = Column(JSON, nullable=False)  # ["female"]
    city = Column(String, nullable=False)
    occupation = Column(String, nullable=False)
    relationship_goal = Column(String, nullable=False)  # long_term, short_term, marriage, casual
    relationship_pace = Column(String, nullable=False)  # slow, medium, fast
    communication_style = Column(String, nullable=False)  # gentle_direct, deep_listener, humorous, calm
    social_level = Column(Integer, default=3)  # 1 (introvert) to 5 (extrovert)
    lifestyle = Column(JSON, nullable=False)  # ["reading", "coffee", "running"]
    core_values = Column(JSON, nullable=False)  # ["personal_growth", "honesty", "family"]
    affection_preferences = Column(JSON, nullable=False)  # ["quality_time", "acts_of_service"]
    conflict_style = Column(String, nullable=False)  # calm_discussion, need_space, express_immediately
    boundaries = Column(JSON, nullable=False)  # ["needs_personal_space"]
    dealbreakers = Column(JSON, nullable=False)  # ["dishonesty", "smoking"]
    wants_children = Column(String, default="undecided")
    marriage_timeline = Column(String, default="3_to_5_years")
    shareable_intro = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class MatchRequest(Base):
    __tablename__ = "match_requests"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String, default="COMPLETED")
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="match_requests")
    results = relationship("MatchResult", back_populates="match_request", cascade="all, delete-orphan")


class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(String, primary_key=True, default=generate_uuid)
    match_request_id = Column(String, ForeignKey("match_requests.id"), nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    candidate_id = Column(String, ForeignKey("candidate_profiles.id"), nullable=False)
    total_score = Column(Float, nullable=False)
    confidence = Column(Float, default=0.8)
    matched_dimensions = Column(JSON, nullable=False)
    differences = Column(JSON, nullable=False)
    missing_dimensions = Column(JSON, nullable=False)
    explanation_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    match_request = relationship("MatchRequest", back_populates="results")
    candidate = relationship("CandidateProfile")
    feedbacks = relationship("MatchFeedback", back_populates="match_result", cascade="all, delete-orphan")


class MatchFeedback(Base):
    __tablename__ = "match_feedback"

    id = Column(String, primary_key=True, default=generate_uuid)
    match_result_id = Column(String, ForeignKey("match_results.id"), nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    feedback_type = Column(String, nullable=False)  # INTERESTED, NOT_INTERESTED, EXPLAIN_MORE
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    match_result = relationship("MatchResult", back_populates="feedbacks")


class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)
    memory_id = Column(String, nullable=False)
    previous_visibility = Column(String, nullable=True)
    new_visibility = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    actor_id = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)
    resource_id = Column(String, nullable=True)
    decision = Column(String, nullable=False)  # ALLOW, DENIED, BLOCKED
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
