from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.dependencies import get_current_student
from app.db.models.user import StudentProfile
from app.db.models.ai import AIConversation, AIMessage
from app.schemas.ai import AIChatRequest, AIChatResponse, AIConversationOut, AIMessageOut
from app.services.ai_tutor_service import ai_service

router = APIRouter(prefix="/ai", tags=["AI Tutor"])

@router.post("/chat", response_model=AIChatResponse)
async def chat_with_tutor(
    request: AIChatRequest,
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Interact with the SPECTRA Intelligent AI Tutor.
    Context-aware regarding the student's subject, weak areas, and active quiz state.
    """
    response = await ai_service.chat(
        db=db,
        student_id=student.id,
        prompt=request.message,
        conversation_id=request.conversation_id,
        subject_id=request.subject_id,
        topic_id=request.topic_id,
        is_during_quiz=request.is_during_quiz
    )
    return response

@router.get("/conversations", response_model=List[AIConversationOut])
def list_conversations(
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Retrieve chat history sessions for the student."""
    convs = (
        db.query(AIConversation)
        .filter(AIConversation.student_id == student.id)
        .order_by(AIConversation.created_at.desc())
        .all()
    )
    results = []
    for c in convs:
        msgs = (
            db.query(AIMessage)
            .filter(AIMessage.conversation_id == c.id)
            .order_by(AIMessage.created_at.asc())
            .all()
        )
        results.append(
            AIConversationOut(
                id=c.id,
                title=c.title,
                created_at=c.created_at,
                messages=[AIMessageOut.model_validate(m) for m in msgs]
            )
        )
    return results

@router.get("/conversations/{id}", response_model=AIConversationOut)
def get_conversation_detail(
    id: int,
    student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Retrieve all messages in a specific conversation session."""
    c = db.query(AIConversation).filter(
        AIConversation.id == id,
        AIConversation.student_id == student.id
    ).first()
    if not c:
        raise HTTPException(status_code=404, detail="Conversation not found")

    msgs = (
        db.query(AIMessage)
        .filter(AIMessage.conversation_id == c.id)
        .order_by(AIMessage.created_at.asc())
        .all()
    )
    return AIConversationOut(
        id=c.id,
        title=c.title,
        created_at=c.created_at,
        messages=[AIMessageOut.model_validate(m) for m in msgs]
    )
