import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controller.authentication_controller import auth_router
from src.controller.grocery_list_controller import router, user_router

app = FastAPI(title="List Management", description="list management used to save list ", version="1.0.0")
app.include_router(router)
app.include_router(auth_router)
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
