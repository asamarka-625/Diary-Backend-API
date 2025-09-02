from dataclasses import dataclass, field
from dotenv import load_dotenv
import os
from functools import cached_property


load_dotenv()

    
@dataclass
class Config:
    _database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL"))
    
    
    def __post_init__(self):
        self.validate()
    
    # Валидация конфигурации
    def validate(self):
        if not self._database_url:
            raise ValueError("DATABASE_URL is required")
        
    @property
    def DATABASE_URL(self) -> str:
        return self._database_url
            
            
_instance = None

def get_config() -> Config:
    global _instance
    if _instance is None:
        _instance = Config()
        
    return _instance
