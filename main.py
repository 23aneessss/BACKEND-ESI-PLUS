from fastapi import FastAPI
from routers import auth, todo , blog , chat
from database import engine
from models import user, todo as todo_model, post , comment , convai
from models.convai import Base as convai_base


from sqlalchemy.orm import declarative_base

app = FastAPI()

todo_model.Base.metadata.create_all(bind=engine)  
convai_base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(blog.router)
app.include_router(chat.router) 
