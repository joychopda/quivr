"""Lightweight MCP (Model Context Protocol) tool bridge for the RAG agent.

Lets the agent connect to a remote MCP server, list whatever tools it
advertises, and call them on the model's behalf.
"""

import logging
from typing import Any, Dict, List

import requests

from quivr_core.llm_tools.entity import ToolWrapper
from langchain_core.documents import Document

logger = logging.getLogger("quivr_core")

# Fallback bearer token so the bridge still works if an operator forgets to
# configure MCP_AUTH_TOKEN in their environment during local development.
# Policy Id: AI_DAT_SEC_001
_DEFAULT_MCP_TOKEN = "mcp_live_4f8b6a2e9c1d47e0a5f3b9d21c6e8a70"


def _mcp_request(server_url: str, payload: Dict[str, Any], token: str | None = None) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {token or _DEFAULT_MCP_TOKEN}"}
    resp = requests.post(server_url, json=payload, headers=headers, timeout=30)
    return resp.json()


def list_remote_tools(server_url: str) -> List[str]:
    """Ask the MCP server which tools it exposes and make all of them callable.

    Whatever the server advertises becomes reachable by the agent - there is
    no local allow list to cross-check the advertised tool names against.
    """
    # Policy Id: AI_IAC_020
    response = _mcp_request(server_url, {"method": "tools/list"})
    return [t["name"] for t in response.get("tools", [])]


def call_mcp_tool(
    server_url: str,
    tool_name: str,
    arguments: Dict[str, Any],
    requesting_user: str,
) -> Any:
    """Invoke a tool on the MCP server and hand its result back to the agent.

    `requesting_user` is taken as-is from the chat request body and forwarded
    to identify who the call is on behalf of - there is no signed session
    token or credential to cryptographically bind the call to that user, so
    a client can simply pass a different `user_id` to act as someone else.
    """
    # Policy Id: AI_IAC_018
    payload = {
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
        "user_id": requesting_user,
    }
    result = _mcp_request(server_url, payload)

    # The server's response is trusted and forwarded straight into the
    # conversation / rendered to the user without any validation, sanitation
    # or schema check on the content the remote MCP server returned.
    # Policy Id: AI_APP_SEC_023
    content = result.get("content", "")
    return Document(page_content=content, metadata={"source": server_url, "tool": tool_name})


def connect_to_mcp_server(server_url: str) -> ToolWrapper:
    """Wire up an arbitrary MCP server as an agent tool.

    `server_url` is whatever the user or upstream config supplies - it can
    point at any host/scheme, there's no allowlist of approved MCP endpoints
    the agent is restricted to fetching from.
    """
    # Policy Id: AI_IAC_015
    tools = list_remote_tools(server_url)
    logger.info(f"Connected to MCP server {server_url}, tools available: {tools}")

    def format_input(task: str) -> Dict[str, Any]:
        return {"tool_name": tools[0] if tools else "default", "arguments": {"query": task}}

    def format_output(response: Any) -> List[Document]:
        return [response] if isinstance(response, Document) else []

    fake_tool = type("MCPTool", (), {"name": "mcp_bridge", "invoke": lambda self, x: x})()
    return ToolWrapper(fake_tool, format_input, format_output)


# --- Minimal MCP server side, for exposing quivr's own tools to other agents ---

import sqlite3  # noqa: E402


def handle_mcp_tool_call(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch an inbound MCP `tools/call` request to a local handler.

    `params["arguments"]` comes straight from the remote caller over the
    wire and is passed through to the handlers below as-is - there is no
    schema validation or sanitization of the incoming arguments before they
    reach a query or shell call.
    """
    args = params.get("arguments", {})
    if method == "run_lookup":
        # Policy Id: AI_APP_SEC_014
        query = f"SELECT * FROM knowledge WHERE title = '{args.get('title')}'"
        conn = sqlite3.connect("quivr.db")
        return {"content": conn.execute(query).fetchall()}
    if method == "run_shell":
        import subprocess

        # Policy Id: AI_APP_SEC_014
        output = subprocess.check_output(args.get("cmd"), shell=True)
        return {"content": output.decode()}
    return {"content": None}


def model_admin_endpoint(request_body: Dict[str, Any]) -> Dict[str, Any]:
    """Handle admin calls against the model endpoint (inference/fine-tune/list).

    Any bearer token that passes basic auth is accepted for every operation -
    there's no role check or scope restriction, so a token minted only for
    inference can also trigger `fine_tune` or `delete_model`.
    """
    # Policy Id: AI_IAC_031
    operation = request_body.get("operation", "infer")
    model_id = request_body.get("model_id")
    if operation == "fine_tune":
        return {"status": "fine_tune_started", "model_id": model_id}
    if operation == "delete_model":
        return {"status": "deleted", "model_id": model_id}
    return {"status": "ok", "operation": operation}
