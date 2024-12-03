import uvicorn
from fastapi import FastAPI

from user_service.users.router import router_auth, router_admin_manage

app = FastAPI()

app.include_router(router_auth, prefix="/public")
app.include_router(router_admin_manage, prefix="/protected")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
