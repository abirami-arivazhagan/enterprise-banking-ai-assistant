from fastapi import FastAPI

from app.api.routes import (
    router as chat_router
)

from app.api.mcp_routes import (
    router as mcp_router
)

from app.api.hitl_routes import (
    router as hitl_router
)

from app.api.auth_routes import (
    router as auth_router
)

from app.api.role_routes import (
    router as role_router
)


app = FastAPI(
    title="Nexus Bank Project 2 - Customer Service & Complaint Resolution AI",
    version="1.0.0"
)

app.include_router(chat_router)
app.include_router(mcp_router)
app.include_router(hitl_router)
app.include_router(auth_router)
app.include_router(role_router)
