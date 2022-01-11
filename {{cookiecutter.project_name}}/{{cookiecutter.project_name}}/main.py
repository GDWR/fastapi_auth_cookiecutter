from fastapi import FastAPI

from database import create_db_and_tables, create_admin
from routes import all_routers
from settings import HOST, PORT

api = FastAPI()

for router in all_routers:
    api.include_router(router)


@api.on_event("startup")
def startup_event():
    create_db_and_tables()
    create_admin()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(api, host=HOST, port=PORT)
