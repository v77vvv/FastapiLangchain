from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from database.schemes import SimpleChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Langchain"])

llm = ChatOllama(model="llama3.2")

@router.post("/", response_model=ChatResponse)
async def chat_simple(payload: SimpleChatRequest):
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
        return ChatResponse(response=str(response.content))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка Ollama: {str(e)}"
        )