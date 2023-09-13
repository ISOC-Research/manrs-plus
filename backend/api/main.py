from fastapi import FastAPI
import routes
import uvicorn
from database import SessionLocal
from functions import *

app = FastAPI(
    title="MANRS Ambassador 2023",
    description="",
    version="1.0.0",
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