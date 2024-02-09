import uvicorn
from fastapi import FastAPI

from src.controller.authentication_controller import auth_router
from src.controller.grocery_list_controller import router, user_router

app = FastAPI()
app.include_router(router)
app.include_router(auth_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
