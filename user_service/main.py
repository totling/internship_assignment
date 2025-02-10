import uvicorn
from fastapi import FastAPI

from user_service.kafka import start_producer, stop_producer, start_consumer, stop_consumer
from user_service.router import router_auth, router_admin_manage, router_doc

app = FastAPI()


@app.on_event("startup")
async def startup():
    await start_producer()
    await start_consumer()


@app.on_event("shutdown")
async def shutdown():
    await stop_producer()
    await stop_consumer()


app.include_router(router_auth, prefix="/public")
app.include_router(router_admin_manage, prefix="/protected")
app.include_router(router_doc, prefix="/admin")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
