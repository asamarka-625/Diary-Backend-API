# Внешние зависимости
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status
from typing import List, Optional
# Внутренние модули
from app.models import DiaryEntry
from app.database import connection
from app.schemas import DiaryEntryCreateSchem, DiaryEntryUpdateSchem


# Получаем запись
@connection
async def sql_get_entry(entry_id: int, session: AsyncSession) -> DiaryEntry:
    try:
        entry_result = await session.execute(sa.select(DiaryEntry).where(DiaryEntry.id == entry_id))
        entry = entry_result.scalar_one()
        
        return entry
    
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    
   
# Получаем записи
@connection
async def sql_get_entries(session: AsyncSession, skip: int = 0, limit: int = 100, completed: Optional[bool] = None) -> List[DiaryEntry]:
    query = sa.select(DiaryEntry).order_by(DiaryEntry.created_at.desc())
    
    if completed is not None:
        query = query.where(DiaryEntry.is_completed == completed)
        
    entries_result = await session.execute(query.offset(skip).limit(limit))
    entries = entries_result.scalars().all()
    
    return entries


# Получаем записи по названию
@connection
async def sql_search_entries(query: str, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[DiaryEntry]:
    entries_result = await session.execute(
        sa.select(DiaryEntry)
        .where(DiaryEntry.title.ilike(f"%{query}%"))
        .order_by(DiaryEntry.created_at.desc())
        .offset(skip).limit(limit)
    )
    entries = entries_result.scalars().all()
    
    return entries
    
    
# Создаем запись
@connection
async def sql_create_entry(entry: DiaryEntryCreateSchem, session: AsyncSession) -> DiaryEntry:
    new_entry = DiaryEntry(
        title=entry.title,
        content=entry.content,
        is_completed=entry.is_completed
    )
    session.add(new_entry)
    await session.commit()
    await session.refresh(new_entry)
    
    return new_entry


# Обновляем запись
@connection
async def sql_update_entry(entry_id: int, update: DiaryEntryUpdateSchem, session: AsyncSession) -> DiaryEntry:
    entry = await sql_get_entry(entry_id=entry_id, session=session, no_decor=True)
    
    if entry.is_completed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot update completed entry")
        
    update_data = update.model_dump(exclude_none=True)
    entry.update_from_dict(update_data)
    
    await session.commit()
    await session.refresh(entry)
    
    return entry


# Удаляем запись
@connection
async def sql_delete_entry(entry_id: int, session: AsyncSession) -> None:
    entry = await sql_get_entry(entry_id=entry_id, session=session, no_decor=True)
    
    await session.delete(entry)
    await session.commit()


# Меняем значение завершения записи
@connection
async def sql_mark_entry_completed(entry_id: int, session: AsyncSession, completed: bool = True) -> DiaryEntry:
    entry = await sql_get_entry(entry_id=entry_id, session=session, no_decor=True)
    
    entry.is_completed = completed
    await session.commit()
    await session.refresh(entry)
    
    return entry