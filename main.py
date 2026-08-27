from fastapi import FastAPI
import uvicorn
from api import auth, chat, profile, chat_message
from admin.setup import admin_setup

app = FastAPI(title='FastAPI LangChain')
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(chat.router)
app.include_router(chat_message.router)
admin_setup(app=app)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)