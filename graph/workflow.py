from langgraph.graph import (
    StateGraph,
    END
)

from graph.state import (
    GraphState
)

from graph.nodes.router_node import (
    router_node
)

from graph.nodes.rag_node import (
    rag_node
)

from graph.nodes.tool_node import (
    tool_node
)

from graph.nodes.memory_node import (
    memory_node
)

from graph.nodes.response_node import (
    response_node
)

# =========================================================
# GRAPH
# =========================================================

workflow = StateGraph(
    GraphState
)

# =========================================================
# NODES
# =========================================================

workflow.add_node(
    "router",
    router_node
)

workflow.add_node(
    "rag",
    rag_node
)

workflow.add_node(
    "tool",
    tool_node
)

workflow.add_node(
    "memory",
    memory_node
)

workflow.add_node(
    "response",
    response_node
)

# =========================================================
# ENTRY
# =========================================================

workflow.set_entry_point(
    "router"
)

# =========================================================
# CONDITIONAL ROUTING
# =========================================================

workflow.add_conditional_edges(

    "router",

    lambda state: state["route"],

    {

        "rag": "rag",

        "tool": "tool"
    }
)

# =========================================================
# RAG FLOW
# =========================================================

workflow.add_edge(
    "rag",
    "memory"
)

# =========================================================
# TOOL FLOW
# =========================================================

workflow.add_edge(
    "tool",
    "memory"
)

# =========================================================
# MEMORY FLOW
# =========================================================

workflow.add_edge(
    "memory",
    "response"
)

# =========================================================
# END
# =========================================================

workflow.add_edge(
    "response",
    END
)

# =========================================================
# COMPILE
# =========================================================

app_graph = workflow.compile()