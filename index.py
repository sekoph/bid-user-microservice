from fastapi import FastAPI, applications,Depends
import strawberry
from strawberry.fastapi import GraphQLRouter
from graphqlfile.queries import Query
from sqlalchemy.orm import Session

from routes.user import usersRouter
from routes.user_type import usertypeRouter
from security.database import get_db

from fastapi.middleware.cors import CORSMiddleware

import py_eureka_client.eureka_client as eureka_client

import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

EUREKA_SERVER = os.getenv("EUREKA_SERVER")

# Initialize Eureka client
eureka_client.init(
    eureka_server=EUREKA_SERVER,
    app_name="user-service",
    instance_host="localhost",
    instance_port=8001
)

origins = [
    'http://localhost:8002',
    'http://localhost:8003',
    'http://localhost:3000',
    'http://localhost:5173',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

schema = strawberry.Schema(query=Query)

async def get_context(db:Session = Depends(get_db)):
    return {"db":db}

graphqlApp = GraphQLRouter(
    schema,
    context_getter=get_context
)


app.include_router(usersRouter)
app.include_router(usertypeRouter)
app.include_router(graphqlApp, prefix='/graphql')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)