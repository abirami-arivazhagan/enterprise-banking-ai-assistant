from fastapi import APIRouter
from pydantic import BaseModel
from mcp.registry import (
    MCPRegistry
)
from mcp.tool_adapter import (
    MCPToolAdapter
)

router = APIRouter()
registry = MCPRegistry()
adapter = MCPToolAdapter()

class MCPInvokeRequest(BaseModel):
    server_name: str
    tool_name: str
    params: dict

@router.get("/mcp/tools")
def list_tools():
    return registry.list_tools()

@router.post("/mcp/invoke")
def invoke_tool(
    payload: MCPInvokeRequest
):
    return adapter.execute(
        payload.server_name,
        payload.tool_name,
        payload.params
    )