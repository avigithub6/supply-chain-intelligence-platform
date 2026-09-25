from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.agents.approval_agent import human_approval_checkpoint
from app.agents.data_agent import data_agent_node
from app.agents.execution_agent import execution_agent_node
from app.agents.graph_agent import graph_agent_node
from app.agents.rag_agent import rag_agent_node
from app.agents.recommendation_agent import (
    recommendation_agent_node,
)
from app.agents.state import AgentState
from app.agents.supervisor import supervisor_node
from app.agents.workflow_agent import workflow_action_node


def route_after_supervisor(state: AgentState) -> str:
    required_agents = state.get(
        "required_agents",
        [],
    )

    if not required_agents:
        return "recommendation_agent"

    return required_agents[0]


def route_after_data(state: AgentState) -> str:
    required_agents = state.get(
        "required_agents",
        [],
    )

    if "graph_agent" in required_agents:
        return "graph_agent"

    if "rag_agent" in required_agents:
        return "rag_agent"

    return "recommendation_agent"


def route_after_graph(state: AgentState) -> str:
    required_agents = state.get(
        "required_agents",
        [],
    )

    if "rag_agent" in required_agents:
        return "rag_agent"

    return "recommendation_agent"


def route_after_rag(
    state: AgentState,
) -> str:
    return "recommendation_agent"


def route_after_recommendation(
    state: AgentState,
) -> str:
    return "workflow_action"


def route_after_workflow_action(
    state: AgentState,
) -> str:
    pending_action = state.get(
        "pending_action",
    )

    if not pending_action:
        return "end"

    return "human_approval"


def route_after_approval(
    state: AgentState,
) -> str:
    approval_status = state.get(
        "approval_status",
        "pending",
    )

    if approval_status == "approved":
        return "execution_agent"

    if approval_status == "rejected":
        return "execution_agent"

    return "end"


def route_after_execution(
    state: AgentState,
) -> str:
    return "end"


def build_supply_chain_graph():
    builder = StateGraph(AgentState)

    # ---------------------------------------------------------
    # Existing investigation agents
    # ---------------------------------------------------------

    builder.add_node(
        "supervisor",
        supervisor_node,
    )

    builder.add_node(
        "data_agent",
        data_agent_node,
    )

    builder.add_node(
        "graph_agent",
        graph_agent_node,
    )

    builder.add_node(
        "rag_agent",
        rag_agent_node,
    )

    builder.add_node(
        "recommendation_agent",
        recommendation_agent_node,
    )

    # ---------------------------------------------------------
    # Milestone 5 workflow nodes
    # ---------------------------------------------------------

    builder.add_node(
        "workflow_action",
        workflow_action_node,
    )

    builder.add_node(
        "human_approval",
        human_approval_checkpoint,
    )

    # ---------------------------------------------------------
    # Milestone 5.6 execution node
    # ---------------------------------------------------------

    builder.add_node(
        "execution_agent",
        execution_agent_node,
    )

    # ---------------------------------------------------------
    # Start
    # ---------------------------------------------------------

    builder.add_edge(
        START,
        "supervisor",
    )

    # ---------------------------------------------------------
    # Supervisor routing
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Data Agent routing
    # ---------------------------------------------------------

    builder.add_conditional_edges(
        "data_agent",
        route_after_data,
        {
            "graph_agent": "graph_agent",
            "rag_agent": "rag_agent",
            "recommendation_agent": "recommendation_agent",
        },
    )

    # ---------------------------------------------------------
    # Graph Agent routing
    # ---------------------------------------------------------

    builder.add_conditional_edges(
        "graph_agent",
        route_after_graph,
        {
            "rag_agent": "rag_agent",
            "recommendation_agent": "recommendation_agent",
        },
    )

    # ---------------------------------------------------------
    # RAG Agent
    # ---------------------------------------------------------

    builder.add_conditional_edges(
        "rag_agent",
        route_after_rag,
        {
            "recommendation_agent": "recommendation_agent",
        },
    )

    # ---------------------------------------------------------
    # Recommendation → Workflow Action
    # ---------------------------------------------------------

    builder.add_conditional_edges(
        "recommendation_agent",
        route_after_recommendation,
        {
            "workflow_action": "workflow_action",
        },
    )

    # ---------------------------------------------------------
    # Workflow Action → Human Approval
    # ---------------------------------------------------------

    builder.add_conditional_edges(
        "workflow_action",
        route_after_workflow_action,
        {
            "human_approval": "human_approval",
            "end": END,
        },
    )

    # ---------------------------------------------------------
    # Human Approval → Execution
    # ---------------------------------------------------------

    builder.add_conditional_edges(
        "human_approval",
        route_after_approval,
        {
            "execution_agent": "execution_agent",
            "end": END,
        },
    )

    # ---------------------------------------------------------
    # Execution → END
    # ---------------------------------------------------------

    builder.add_conditional_edges(
        "execution_agent",
        route_after_execution,
        {
            "end": END,
        },
    )

    # ---------------------------------------------------------
    # Milestone 5.7.1
    # In-memory LangGraph checkpointer
    # ---------------------------------------------------------

    checkpointer = InMemorySaver()

    return builder.compile(
        checkpointer=checkpointer,
    )


supply_chain_graph = build_supply_chain_graph()