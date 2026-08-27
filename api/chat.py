from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from langchain.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from database.connection import get_db
from database.models import UserProfile, ChatHistory
from database.schemes import SimpleChatRequest, ChatResponse
from .profile import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

llm = ChatOllama(model="llama3.2")

@router.post("/", response_model=ChatResponse)
async def chat_simple(
    payload: SimpleChatRequest,
    current_user: UserProfile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.plan == "basic":
        stmt = select(ChatHistory).where(ChatHistory.user_id == current_user.id)
        result = await db.execute(stmt)
        user_requests_count = len(result.scalars().all())

        if user_requests_count >= 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="U have already used all of your limit"
            )

    try:
        messages = [
            SystemMessage(
                content=(
                    "Ты 10-летний Python backend и JavaScript frontend разработчик. "
                    "Отвечай на все вопросы от пользователя как подобает твоему уровню."
                )
            ),
            HumanMessage(content=payload.message)
        ]

        response = await llm.ainvoke(messages)
        response_text = str(response.content)

        new_history = ChatHistory(
            user_id=current_user.id,
            user_message=payload.message,
            bot_response=response_text
        )
        db.add(new_history)
        await db.commit()

        return ChatResponse(response=response_text)

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка Ollama: {str(e)}"
        )