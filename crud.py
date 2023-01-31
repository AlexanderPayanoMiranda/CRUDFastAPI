from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is not None:
        user.Todos = get_todos_for_user(user_id, db)

    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    user.Todos = get_todos_for_user(user.id, db)

    return user


def get_users(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.User).offset(offset).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "---hash"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)

    db.add(db_user)
    db.commit()

    db.refresh(db_user)

    return db_user


def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), author_id=user_id)

    db.add(db_todo)
    db.commit()

    db.refresh(db_todo)

    return db_todo


def get_todo_by_id(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def get_todos(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(offset).limit(limit).all()


def get_todos_for_user(user_id: int, db: Session, offset: int = 0, limit: int = 100):
    user_todos = db.query(models.Todo).filter(models.Todo.author_id == user_id).offset(offset).limit(limit).all()

    return user_todos


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    db.delete(user)
    db.commit()

    return {"ok": True, "message": "User deleted"}


def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    db.delete(todo)
    db.commit()

    return {"ok": True, "message": "Todo deleted"}


def update_user(db: Session, user_id: int, user: schemas.User):
    user_query = db.query(models.User).filter(models.User.id == user_id)

    data_user = user_query.first()

    update_data = user.dict(exclude_unset=True)

    user_query.filter(models.User.id == user_id).update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(data_user)

    return {"status": "success", "user": data_user}


def update_todo(db: Session, todo_id: int, todo: schemas.Todo):
    todo_query = db.query(models.Todo).filter(models.Todo.id == todo_id)

    data_todo = todo_query.first()

    update_data = todo.dict(exclude_unset=True)

    todo_query.filter(models.Todo.id == todo_id).update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(data_todo)

    return {"status": "success", "todo": data_todo}
