from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.models import Chat, UserProfile
from database.schemes import ChatCreateScheme, ChatResponseScheme, ChatUpdateScheme
from .profile import get_current_user

router = APIRouter(prefix='/chat', tags=['Chat'])


@router.get('/', response_model=List[ChatResponseScheme], tags=['Chat'])
async def get_list(
    current_user: UserProfile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = await db.execute(select(Chat).where(Chat.user_id == current_user.id))
    return stmt.scalars().all()


@router.post('/', response_model=ChatResponseScheme, status_code=status.HTTP_201_CREATED, tags=['Chat'])
async def post(
    scheme: ChatCreateScheme,
    current_user: UserProfile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    chat = Chat(
        **scheme.model_dump(),
        user_id=current_user.id
    )

    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


@router.put('/{id_}/', response_model=ChatResponseScheme, tags=['Chat'])
async def put(
    id_: int,
    scheme: ChatUpdateScheme,
    current_user: UserProfile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)  
):
    stmt = await db.execute(select(Chat).where(Chat.id == id_, 
                                               Chat.user_id == current_user.id))
    scalar = stmt.scalar_one_or_none()

    if not scalar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Chat not found or access denied"
        )
    
    update_data = scheme.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(scalar, key, value)

    await db.commit()
    await db.refresh(scalar)
    return scalar


@router.delete('/{id_}/', status_code=status.HTTP_204_NO_CONTENT, tags=['Chat'])
async def delete(
    id_: int,
    current_user: UserProfile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = await db.execute(select(Chat).where(Chat.id == id_, 
                                               Chat.user_id == current_user.id))
    scalar = stmt.scalar_one_or_none()

    if not scalar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Chat not found or access denied"
        )

    await db.delete(scalar)
    await db.commit()
    return None