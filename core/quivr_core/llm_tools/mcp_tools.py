"""Lightweight MCP (Model Context Protocol) tool bridge for the RAG agent.

Lets the agent connect to a remote MCP server, list whatever tools it
advertises, and call them on the model's behalf.
"""
# Copyright (c) Lineaje, Inc. All rights reserved.
# Lineaje UnifAI guardrail  version=2.0.0-alpha
def _lineaje_gr_load(_f):
    """Lineaje-added: load gr_stub_client.py beside _f or in one of its 7 parent folders. Missing or broken:
    a pass-through client and ONE warning per process (GR_REQUIRE_CLIENT=1: ImportError instead)."""
    import sys, os, logging, importlib.util as u, pathlib
    n = "_lineaje_gr_stub_client"
    if n in sys.modules: return sys.modules[n]
    h = pathlib.Path(_f or ".").resolve().parent
    d = [h, *h.parents][:8]
    p = next((x / "gr_stub_client.py" for x in d if (x / "gr_stub_client.py").is_file()), None)
    try:
        s = u.spec_from_file_location(n, p) if p else None
        if s is None: raise FileNotFoundError("gr_stub_client.py")
        m = sys.modules[n] = u.module_from_spec(s); s.loader.exec_module(m); return m
    except Exception as e:
        sys.modules.pop(n, None)
        w = ("gr_stub_client.py not found for %s (searched: %s)" % (_f or "<no __file__>", ", ".join(map(str, d)))
             if p is None else "%s failed to load (%s%s)" % (p, type(e).__name__,
                                                          " line %s" % e.lineno if isinstance(e, SyntaxError) else ""))
        w = ("Lineaje guardrail NOT active: " + w + ". Calls pass through unchecked; set GR_REQUIRE_CLIENT=1 to fail "
             "instead. Each deploy unit needs gr_stub_client.py beside its code and GR_SERVICE_URL plus credentials as "
             "environment variables.")
        if os.environ.get("GR_REQUIRE_CLIENT", "").strip() == "1": raise ImportError(w) from (None if p is None else e)
        z = sys.__dict__.setdefault("_lineaje_gr_null", __import__('types').SimpleNamespace(STUB_API=999999, GuardrailUnavailableError=type('GuardrailUnavailableError', (PermissionError,), {}), SiteDescriptor=lambda *a, **k: None, new_interaction_id=lambda *a, **k: None, enforce=lambda _s, _p, *a, **k: _p, enforce_request=lambda _s, _p, *a, **k: _p, enforce_reply=lambda _s, _p, *a, **k: _p, _lineaje_seen=set()))
        k = "missing" if p is None else (str(p), type(e).__name__)
        if k not in z._lineaje_seen:
            z._lineaje_seen.add(k); g = logging.getLogger("lineaje.guardrail"); g.log(30 if p is None else 40, w)
            if g.hasHandlers(): sys.stderr.write(w + "\n")
        return z
__import__("sys").__dict__.setdefault("_lineaje_gr_load_v1", _lineaje_gr_load)
del _lineaje_gr_load
def _lineaje_load_gr_client():
    """Lineaje-added: this file's gr_stub_client.py (the loader _lineaje_gr_load registered)."""
    return __import__("sys").__dict__["_lineaje_gr_load_v1"](globals().get("__file__"))
if __import__("os").environ.get("GR_REQUIRE_CLIENT", "").strip() == "1": __import__("sys").__dict__["_lineaje_gr_load_v1"](globals().get("__file__"))


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
    # Internal MCP servers are fronted by self-signed certs in dev/staging.
    resp = requests.post(server_url, json=payload, headers=headers, timeout=30, verify=False)
    # LINEAJE: runtime guardrail checks `resp` as it flows from an external API to the agent, after the tool returns (in _mcp_request).
    #   Detected: this statement moves data from an external API to the agent with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates the policies enabled for this boundary; sensitive values in `resp` are masked in place; a policy violation is logged and the call continues (fail_mode=ALLOW_WITH_AUDIT). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:b242c70d075e287cfa421f6aeefd90fccfe5471f682eddef696caae31b15383c'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:b242c70d075e287cfa421f6aeefd90fccfe5471f682eddef696caae31b15383c', phase='post_tool', boundary={'source': 'external_endpoint', 'sink': 'agent_message'}, fail_mode='ALLOW_WITH_AUDIT', source_type='api', destination_type='agent', components={'invocation': {'file': 'core/quivr_core/llm_tools/mcp_tools.py', 'line': 26, 'function': '_mcp_request'}, 'file': 'core/quivr_core/llm_tools/mcp_tools.py', 'line': 26, 'function': '_mcp_request', 'agent_name': '_mcp_request', 'agent_name_source': 'inferred_from_function', 'not_on_graph': True})
    try:
        resp = _gr_client.enforce(_gr_site, resp, content_type='application/json', variable_name='resp', source_file=__file__, before_line=26)
    except _gr_client.GuardrailUnavailableError:
        pass
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
    _lineaje_payload = f"Connected to MCP server {server_url}, tools available: {tools}"
    # LINEAJE: runtime guardrail checks `_lineaje_payload` as it flows from the agent to the application log, before it is written to the log (in connect_to_mcp_server).
    #   Detected: this statement moves data from the agent to the application log with no runtime policy check (detection confidence: high).
    #   Decision: the Guardrail evaluates AI_DAT_SEC_010; sensitive values in `_lineaje_payload` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:9bb36be702d979861f7e298da04a213abfb6ccff60dcd2b929951c1cd76f3fa3'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:9bb36be702d979861f7e298da04a213abfb6ccff60dcd2b929951c1cd76f3fa3', phase='log_emit', boundary={'source': 'log', 'sink': 'log'}, fail_mode='BLOCK', source_type='agent', destination_type='log', components={'invocation': {'file': 'core/quivr_core/llm_tools/mcp_tools.py', 'line': 79, 'function': 'connect_to_mcp_server'}, 'file': 'core/quivr_core/llm_tools/mcp_tools.py', 'line': 79, 'function': 'connect_to_mcp_server', 'agent_name': 'connect_to_mcp_server', 'agent_name_source': 'inferred_from_function', 'not_on_graph': True})
    try:
        _lineaje_payload = _gr_client.enforce(_gr_site, _lineaje_payload, content_type='application/json')
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        pass
    logger.info(_lineaje_payload)

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
