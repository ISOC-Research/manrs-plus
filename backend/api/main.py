from fastapi import FastAPI
import routes
import uvicorn
from database import SessionLocal
from functions import *

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MANRS Ambassador 2023",
    description="",
    version="1.0.0",
)

# Configuration CORS
origins = [
    "http://localhost",
    "http://localhost:8000",  
    "*"
    # Ajoutez d'autres origines autorisées au besoin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Vous pouvez spécifier les méthodes HTTP autorisées (GET, POST, etc.)
    allow_headers=["*"],  # Vous pouvez spécifier les en-têtes autorisés
)

app.include_router(routes.router)

if __name__ == "__main__":
    
    db = SessionLocal()
    
    try:
        check_database_connection(db)
    except Exception as e:
        print(f"Error: Database connection failed - {e}")
        exit(1)  # Exit the application if the database connection fails
    finally:
        db.close()
        
    uvicorn.run(app, host="127.0.0.1", port=8000)