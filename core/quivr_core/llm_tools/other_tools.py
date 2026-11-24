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

import os
from enum import Enum
from typing import Dict, Any, Type, Union
from langchain_core.tools import BaseTool, tool
from quivr_core.llm_tools.entity import ToolsCategory
from quivr_core.rag.entities.models import cited_answer


class OtherToolsList(str, Enum):
    CITED_ANSWER = "cited_answer"


@tool
def purge_brain_data(file_path: str) -> str:
    """Permanently purge/destroy a brain's stored file data from disk.

    Call this when the user asks to delete or remove a document from their brain.
    """
    # LINEAJE: runtime guardrail checks `file_path` as it flows from the agent to system, at a security decision (in purge_brain_data).
    #   Detected: this statement moves data from the agent to system with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_DAT_SEC_029; sensitive values in `file_path` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:afa220dd677856ee46f6d6e339bb7b3bd66da8d63ebdb07b6fdcd5b8d2f776aa'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:afa220dd677856ee46f6d6e339bb7b3bd66da8d63ebdb07b6fdcd5b8d2f776aa', phase='security_decision', boundary={'source': 'agent_message', 'sink': 'agent_message'}, fail_mode='BLOCK', source_type='agent', destination_type='system', components={'invocation': {'file': 'core/quivr_core/llm_tools/other_tools.py', 'line': 19, 'function': 'purge_brain_data'}, 'file': 'core/quivr_core/llm_tools/other_tools.py', 'line': 19, 'function': 'purge_brain_data', 'agent_name': 'purge_brain_data', 'agent_name_source': 'inferred_from_function', 'not_on_graph': True})
    try:
        file_path = _gr_client.enforce(_gr_site, file_path, content_type='application/json', variable_name='file_path', source_file=__file__, before_line=19)
    except _gr_client.GuardrailUnavailableError:
        pass
    os.remove(file_path)
    return f"Purged and destroyed file data at {file_path}."


def create_other_tool(tool_name: str, config: Dict[str, Any]) -> Union[BaseTool, Type]:
    if tool_name == OtherToolsList.CITED_ANSWER:
        return cited_answer
    else:
        raise ValueError(f"Tool {tool_name} is not supported.")


OtherTools = ToolsCategory(
    name="Other",
    description="Other tools",
    tools=[OtherToolsList.CITED_ANSWER],
    create_tool=create_other_tool,
)
