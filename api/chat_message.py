from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from langchain.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from database.connection import get_db
from database.models import UserProfile, Chat, ChatMessage
from database.schemes import ChatMessageResponseScheme, ChatMessageCreateScheme
from .profile import get_current_user
from typing import List

router = APIRouter(prefix="/chat_message", tags=["Chat Message"])

@router.get('/', response_model=List[ChatMessageResponseScheme], tags=['Chat Message'])
async def get_list(
    current_user: UserProfile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = await db.execute(
        select(ChatMessage)
        .join(Chat, ChatMessage.chat_id == Chat.id)
        .where(Chat.user_id == current_user.id)
    )
    return stmt.scalars().all()

llm = ChatOllama(model="llama3.2")

@router.post("/", response_model=ChatMessageResponseScheme)
async def chat(
    scheme: ChatMessageCreateScheme,
    current_user: UserProfile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = await db.execute(select(Chat).where(Chat.id == scheme.chat_id, 
                                               Chat.user_id == current_user.id))
    scalar = stmt.scalar_one_or_none()

    if not scalar:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You are not owner of this chat')
    
    if current_user.plan == "Basic":
        count_stmt = select(func.count(ChatMessage.id)).join(Chat).where(Chat.user_id == current_user.id)
        user_requests_count = (await db.execute(count_stmt)).scalar() or 0

        if user_requests_count >= 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have already used all of your limit"
            )
    try:
        messages = [
            SystemMessage(
                content=(
                    "Ты 10-летний Python backend и JavaScript frontend разработчик. "
                    "Отвечай на все вопросы от пользователя как подобает твоему уровню."
                )
            ),
            HumanMessage(content=scheme.message)
        ]

        response = await llm.ainvoke(messages)
        response_text = str(response.content)

        new_history = ChatMessage(response=response_text, **scheme.model_dump())

        db.add(new_history)
        await db.commit()
        await db.refresh(new_history)

        return new_history

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка Ollama: {str(e)}"
        )