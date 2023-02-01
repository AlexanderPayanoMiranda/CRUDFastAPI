from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException

from app.db.database import SessionLocal, engine
from app.db import schemas
from app.routers.functions import crud
from app.models import models

models.Base.metadata.create_all(bind=engine)

# Run app with uvicorn app.app:app --reload
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"msg": "Hello World"}


@app.get("/users", response_model=list[schemas.User])
def list_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, offset, limit)

    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")

    return db_user


@app.get("/user_by_email/{user_email}", response_model=schemas.User)
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")

    return db_user


@app.get("/users/{user_id}/todos", response_model=list[schemas.Todo])
def get_user_by_id(user_id: int, offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="Todo not found!")

    db_user_todos = crud.get_todos_for_user(user_id, db, offset, limit)

    return db_user_todos


@app.get("/todos", response_model=list[schemas.Todo])
def get_todos(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_todos = crud.get_todos(db, offset, limit)

    return db_todos


@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def get_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo_by_id(db, todo_id)

    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found!")

    return db_todo


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    check_email = crud.get_user_by_email(db, email=user.email)

    if check_email:
        raise HTTPException(status_code=400, detail="Email already registered!")

    db_user = crud.create_user(db, user)

    return db_user


@app.post("/users/{user_id}/todos", response_model=schemas.Todo)
def create_todo(user_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    todo = crud.create_todo(db, todo, user_id)

    return todo


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    status = crud.delete_user(db, user_id)

    return status


@app.put("/users/{user_id}")
def update_todo(user_id: int, new_user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.update_todo(db, user_id, new_user)

    return db_user


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, new_todo: schemas.TodoBase, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id, new_todo)

    return db_todo
