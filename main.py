from fastapi import FastAPI

# Documentation
from documents.description import api_description
from documents.tags import tags_metadata

#Routers
import routers.router_fragments
import routers.router_users
import routers.router_auth
import routers.router_stripe

app = FastAPI(
    title="Attendance Tracker",
    description=api_description,
    openapi_tags= tags_metadata
)

app.include_router(routers.router_fragments.router)
app.include_router(routers.router_users.router)
app.include_router(routers.router_auth.router)
app.include_router(routers.router_stripe.router)