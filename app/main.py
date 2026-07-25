from fastapi import FastAPI
from app.api.routes import auth, reservations, chat


app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=['auth'])
app.include_router(reservations.router, prefix="/reservations", tags=['reservations'])
app.include_router(chat.router, prefix="/chat", tags=['chat'])

@app.get("/")
def default():
    return {
        'message': "Hello from the backend!!!"
    }


