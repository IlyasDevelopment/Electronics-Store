import os
import uvicorn

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from routers import router

app = FastAPI()
app.include_router(router)

load_dotenv('.env')
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DB_URL"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
