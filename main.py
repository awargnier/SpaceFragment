from fastapi import FastAPI

# Documentation
from documents.description import api_description
from documents.tags import tags_metadata

#Routers
import routers.router_fragments

app = FastAPI(
    title="Attendance Tracker",
    description=api_description,
    openapi_tags= tags_metadata
)

app.include_router(routers.router_fragments.router)