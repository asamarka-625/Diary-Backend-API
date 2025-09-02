from pydantic import BaseModel, conint, constr, model_validator
from datetime import datetime
from typing import Optional


# Базовая схема ежедневника
class DiaryEntryBaseSchem(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=255)
    content: constr(strip_whitespace=True)
    is_completed: Optional[bool] = False


# Схема создания ежедневника
class DiaryEntryCreateSchem(DiaryEntryBaseSchem):
    pass


# Схема обновления ежедневника
class DiaryEntryUpdateSchem(BaseModel):
    title: Optional[constr(strip_whitespace=True, min_length=1, max_length=255)] = None
    content: Optional[constr(strip_whitespace=True)] = None
    
    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_field(cls, data):
        # Проверяем, что хотя бы одно поле предоставлено и не None
        provided_fields = {key: value for key, value in data.items() if value is not None}
        
        if data.get("title", None) is None and data.get("content", None) is None:
            raise ValueError('Although one field must be filled in')
        return data
        

# Схема ежедневника
class DiaryEntrySchem(DiaryEntryBaseSchem):
    id: conint(ge=1)
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
       