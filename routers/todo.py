# routers/todos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from database import SessionLocal
from models.todo import Todo
from schemas.todo import TodoCreate, TodoOut

router = APIRouter( 
    prefix="/todos",
    tags=["todos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(todo: TodoCreate, db: db_dependency):
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.get("/all", response_model=list[TodoOut])
async def get_all_todos(db: db_dependency):
    todos = db.query(Todo).all()
    if not todos:
        raise HTTPException(status_code=404, detail="No tasks found")
    return todos


@router.get("/done", response_model=list[TodoOut])
async def get_completed_todos(db: db_dependency):
    todos = db.query(Todo).filter_by(is_done=True).all()
    if not todos:
        raise HTTPException(status_code=404, detail="No completed tasks found")
    return todos


@router.get("/pending", response_model=list[TodoOut])
async def get_pending_todos(db: db_dependency):
    todos = db.query(Todo).filter_by(is_done=False).all()
    if not todos:
        raise HTTPException(status_code=404, detail="No pending tasks found")
    return todos


@router.put("/", status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    newTitle: Optional[str] = None,
    newStat: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(Todo.id == task_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")

    if newTitle and newTitle.strip():
        todo.title = newTitle
    if newStat is not None:
        todo.is_done = newStat

    db.commit()
    db.refresh(todo)
    return {"message": "Task updated successfully", "task": todo}


@router.delete("/", status_code=status.HTTP_200_OK)
def delete_task(todo_id: int, db: db_dependency):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(todo)
    db.commit()
    return {"message": "Task deleted successfully"}
