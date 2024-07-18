from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic model for creating a new todo
class TodoCreate(BaseModel):
    title: str

# Pydantic model for a todo item, inherits from TodoCreate and adds id and completed fields
class Todo(TodoCreate):
    id: int
    completed: bool = False

# In-memory storage for todos (simulating a database)
todos = []

# Endpoint to create a new todo
@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    # Create a new todo item with an incremented id
    new_todo = Todo(id=len(todos) + 1, **todo.model_dump())
    todos.append(new_todo)  # Add the new todo to the list
    return new_todo  # Return the created todo as response

# Endpoint to fetch all todos
@app.get("/todos", response_model=list[Todo])
def get_todos():
    return todos  # Return the list of todos as response

# Endpoint to fetch a specific todo by its id
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo  # Return the todo if found
    # Raise HTTPException with 404 status code and message if todo is not found
    raise HTTPException(status_code=404, detail="Todo not found")

# Endpoint to update a todo by its id
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoCreate):
    for todo in todos:
        if todo.id == todo_id:
            todo.title = updated_todo.title  # Update the title of the todo
            return todo  # Return the updated todo
    # Raise HTTPException with 404 status code and message if todo is not found
    raise HTTPException(status_code=404, detail="Todo not found")

# Endpoint to delete a todo by its id
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            del todos[index]  # Delete the todo from the list
            return {"message": "Todo deleted successfully"}  # Return success message
    # Raise HTTPException with 404 status code and message if todo is not found
    raise HTTPException(status_code=404, detail="Todo not found")