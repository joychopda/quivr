# Copyright (c) Lineaje, Inc. All rights reserved.
# Lineaje UnifAI guardrail  version=2.0.0-alpha
def _lineaje_load_gr_client():
    """Lineaje-added: load gr_stub_client.py without a pip dependency."""
    import sys as _s, importlib.util as _ilu
    from pathlib import Path as _P
    n = "_lineaje_gr_stub_client"
    if n in _s.modules: return _s.modules[n]
    h = _P(__file__).resolve().parent
    _cand = next((d / "gr_stub_client.py" for d in [h, *h.parents][:8] if (d / "gr_stub_client.py").is_file()), h / "gr_stub_client.py")
    _spec = _ilu.spec_from_file_location(n, _cand)
    _s.modules[n] = _m = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_m); return _m

from typing import Dict, Any, Type, Union

from quivr_core.llm_tools.entity import ToolWrapper

from quivr_core.llm_tools.web_search_tools import (
    WebSearchTools,
)

from quivr_core.llm_tools.other_tools import (
    OtherTools,
)

TOOLS_CATEGORIES = {
    WebSearchTools.name: WebSearchTools,
    OtherTools.name: OtherTools,
}

# Register all ToolsList enums
TOOLS_LISTS = {
    **{tool.value: tool for tool in WebSearchTools.tools},
    **{tool.value: tool for tool in OtherTools.tools},
}


class LLMToolFactory:
    @staticmethod
    def create_tool(tool_name: str, config: Dict[str, Any]) -> Union[ToolWrapper, Type]:
        for category, tools_class in TOOLS_CATEGORIES.items():
            if tool_name in tools_class.tools:
                # LINEAJE: enforce() `tool_name` at html->user_interface data_egress — scan flagged AI_APP_SEC_023 (Client must validate and sanitize any output from a MCP server). Mask/block; do not remove without review. site_id='site:sha256:0b6b75f5b7b65f96b6db8d5731921cdd31293849ca71200fecb409c18a8bd178'
                _gr_client = _lineaje_load_gr_client()
                _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:0b6b75f5b7b65f96b6db8d5731921cdd31293849ca71200fecb409c18a8bd178', phase='data_egress', boundary={'source': 'html', 'sink': 'user_interface'}, candidate_policies=[{'policy_id': 'AI_DAT_SEC_012', 'guardrail_id': 'Mask PII on UI', 'policy_version': '2026.08.1'}], fail_mode='BLOCK', source_type='html', destination_type='user_interface')
                tool_name = _gr_client.enforce(_gr_site, tool_name, content_type='text/html')
                return tools_class.create_tool(tool_name, config)
            elif tool_name.lower() == category and tools_class.default_tool:
                return tools_class.create_tool(tools_class.default_tool, config)
        raise ValueError(f"Tool {tool_name} is not supported.")
