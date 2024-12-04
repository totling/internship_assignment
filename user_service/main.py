import uvicorn
from fastapi import FastAPI

from kafka import start_producer, stop_producer
from router import router_auth, router_admin_manage, router_doc

app = FastAPI()


@app.on_event("startup")
async def startup():
    await start_producer()


@app.on_event("shutdown")
async def shutdown():
    await stop_producer()


app.include_router(router_auth, prefix="/public")
app.include_router(router_admin_manage, prefix="/protected")
app.include_router(router_doc, prefix="/admin")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
