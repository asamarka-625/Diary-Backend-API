# Внешние зависимости
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Внутренние модули
from app.router import router
from app.database import setup_database


app = FastAPI(
    title="Diary Backend API",
    description="Backend для приложения-ежедневника",
    version="1.0.0"
)

app.include_router(router)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # Создание таблиц
    await setup_database()
    
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000, reload=False)
