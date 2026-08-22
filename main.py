from fastapi import FastAPI
import uvicorn
from api import auth, profile
from admin.setup import admin_setup

app = FastAPI(title='FastAPI LangChain')
app.include_router(auth.router)
app.include_router(profile.router)
admin_setup(app=app)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)