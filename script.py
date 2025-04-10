from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from dbcontroller import connect

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str
    date: datetime
    status: str = "pending"

@app.post("/tasks")
def create_task(task: Task):
    connection, cursor = connect()
    try:
        cursor.execute("""
            INSERT INTO tasks (title, description, date, status)
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (task.title, task.description, task.date, task.status))
        task_id = cursor.fetchone()[0]
        return {"message": "Task created", "id": task_id}
    finally:
        cursor.close()
        connection.close()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection, cursor = connect()
    try:
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        if task:
            return {"id": task[0], "title": task[1], "description": task[2], "date": task[3], "status": task[4]}
        raise HTTPException(status_code=404, detail="Task not found")
    finally:
        cursor.close()
        connection.close()

@app.get("/tasks")
def list_tasks(status=None, before_date=None):
    connection, cursor = connect()
    try:
        query = "SELECT * FROM tasks WHERE TRUE"
        params = []

        if status:
            query += " AND status = %s"
            params.append(status)
        if before_date:
            query += " AND date <= %s"
            params.append(before_date)

        cursor.execute(query, tuple(params))
        tasks = cursor.fetchall()
        return [{"id": task[0], "title": task[1], "description": task[2], "date": task[3], "status": task[4]} for task in tasks]
    finally:
        cursor.close()
        connection.close()

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    connection, cursor = connect()
    try:
        cursor.execute("""
            UPDATE tasks SET title = %s, description = %s, date = %s, status = %s
            WHERE id = %s
        """, (task.title, task.description, task.date, task.status, task_id))
        return {"message": "Task updated"}
    finally:
        cursor.close()
        connection.close()

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection, cursor = connect()
    try:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        return {"message": "Task deleted"}
    finally:
        cursor.close()
        connection.close()

