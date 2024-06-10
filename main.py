from fastapi import FastAPI

app=FastAPI(
    title="FastApi CRUD",
    description='An example of how to use FastApi',
    version="0.0.1",
)

@app.get("/", tags=['Start Root'])
def readRoot():
    return {"Fast":"Api"}
