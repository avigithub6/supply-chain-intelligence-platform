from langgraph.graph import END, START, StateGraph

from app.agents.data_agent import data_agent_node
from app.agents.graph_agent import graph_agent_node
from app.agents.rag_agent import rag_agent_node
from app.agents.recommendation_agent import recommendation_agent_node
from app.agents.state import AgentState
from app.agents.supervisor import supervisor_node


def route_after_supervisor(state: AgentState) -> str:
    """
    Decide which agent should run first after the supervisor.
    """

    required_agents = state.get("required_agents", [])

    if not required_agents:
        return "recommendation_agent"

    return required_agents[0]


def route_after_data(state: AgentState) -> str:
    """
    Decide which agent should run after the data agent.
    """

    required_agents = state.get("required_agents", [])

    if "graph_agent" in required_agents:
        return "graph_agent"

    if "rag_agent" in required_agents:
        return "rag_agent"

    return "recommendation_agent"


def route_after_graph(state: AgentState) -> str:
    """
    Decide which agent should run after the graph agent.
    """

    required_agents = state.get("required_agents", [])

    if "rag_agent" in required_agents:
        return "rag_agent"

    return "recommendation_agent"


def route_after_rag(state: AgentState) -> str:
    """
    The recommendation agent runs after RAG.
    """

    return "recommendation_agent"


def build_supply_chain_graph():
    """
    Build and compile the Supply Chain LangGraph workflow.
    """

    builder = StateGraph(AgentState)

    # Register nodes
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("data_agent", data_agent_node)
    builder.add_node("graph_agent", graph_agent_node)
    builder.add_node("rag_agent", rag_agent_node)
    builder.add_node(
        "recommendation_agent",
        recommendation_agent_node,
    )

    # Entry point
    builder.add_edge(START, "supervisor")

    # Supervisor routing
    builder.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "data_agent": "data_agent",
            "graph_agent": "graph_agent",
            "rag_agent": "rag_agent",
            "recommendation_agent": "recommendation_agent",
        },
    )

    # Data agent routing
    builder.add_conditional_edges(
        "data_agent",
        route_after_data,
        {
            "graph_agent": "graph_agent",
            "rag_agent": "rag_agent",
            "recommendation_agent": "recommendation_agent",
        },
    )

    # Graph agent routing
    builder.add_conditional_edges(
        "graph_agent",
        route_after_graph,
        {
            "rag_agent": "rag_agent",
            "recommendation_agent": "recommendation_agent",
        },
    )

    # RAG always goes to recommendation
    builder.add_conditional_edges(
        "rag_agent",
        route_after_rag,
        {
            "recommendation_agent": "recommendation_agent",
        },
    )

    # Recommendation is the final node
    builder.add_edge(
        "recommendation_agent",
        END,
    )

    return builder.compile()


# Default compiled graph for application use
supply_chain_graph = build_supply_chain_graph()