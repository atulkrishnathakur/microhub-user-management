from fastapi import FastAPI

app = FastAPI()


@app.get("/a1")
def a1():
    return {"message": "user management a1"}

@app.get("/a2")
def a2():
    return {"message": "user management a2"}

@app.get("/a3")
def a3():
    return {"message": "user management a3"}

@app.get("/a4")
def a4():
    return {"message": "user management a4"}