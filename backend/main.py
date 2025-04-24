from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route for the root URL ("/")
@app.get("/")
async def read_root():
    return {"message": "Hello from the Interest Calculator Backend!"}

# Define another example route
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    # This route takes a path parameter 'item_id' and an optional query parameter 'q'
    return {"item_id": item_id, "q": q}