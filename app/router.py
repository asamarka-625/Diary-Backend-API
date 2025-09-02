# Внешние зависимости
from fastapi import APIRouter, status
from pydantic import constr, conint
from typing import List, Optional
# Внутренние модули
from app.schemas import DiaryEntrySchem, DiaryEntryCreateSchem, DiaryEntryUpdateSchem
from app.crud import (sql_get_entry, sql_get_entries, sql_search_entries, sql_create_entry, sql_update_entry,
                      sql_delete_entry, sql_mark_entry_completed)


router = APIRouter()


# Получаем записи
@router.get("/api/v1/entries/", response_model=List[DiaryEntrySchem])
async def read_entries(
    skip: conint(ge=0) = 0,
    limit: conint(ge=1) = 100,
    completed: Optional[bool] = None
):
    entries = await sql_get_entries(skip=skip, limit=limit, completed=completed)
    
    return entries


# Получаем запись
@router.get("/api/v1/entries/{entry_id}", response_model=DiaryEntrySchem)
async def read_entry(entry_id: conint(ge=1)):
    entry = await sql_get_entry(entry_id=entry_id)
    
    return entry


# Получаем записи по названию
@router.get("/api/v1/entries/search/{entry_id}", response_model=List[DiaryEntrySchem])
async def search_entries(
    query: constr(strip_whitespace=True, min_length=1, max_length=255),
    skip: conint(ge=0) = 0,
    limit: conint(ge=1) = 100
):
    entries = await sql_search_entries(query=query, skip=skip, limit=limit)
    
    return entries
    
   
# Создаем запись   
@router.post("/api/v1/entries/", response_model=DiaryEntrySchem, status_code=status.HTTP_201_CREATED)
async def create_entry(entry: DiaryEntryCreateSchem):
    entry = await sql_create_entry(entry=entry)
    
    return entry
    

# Обновляем запись
@router.put("/api/v1/entries/{entry_id}", response_model=DiaryEntrySchem)
async def update_entry(entry_id: conint(ge=1), update: DiaryEntryUpdateSchem):
    entry = await sql_update_entry(entry_id=entry_id, update=update)
    
    return entry


# Удаляем запись
@router.delete("/api/v1/entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(entry_id: conint(ge=1)):
    await sql_delete_entry(entry_id=entry_id)


# Обновляем значение завершения записи
@router.patch("/api/v1/entries/{entry_id}/complete", response_model=DiaryEntrySchem)
async def mark_entry_completed(entry_id: conint(ge=1), completed: bool = True):
    entry = await sql_mark_entry_completed(entry_id=entry_id, completed=completed)
    
    return entry


@router.get("/health")
def health_check():
    return {"status": "healthy"}