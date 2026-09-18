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
                # LINEAJE: enforce() `tool_name` at user_interface->agent post_agent_receive — scan flagged AI_APP_SEC_029 (Agent must validate, sanitize LLM output including for presence of eval or any dynamic code execution primitive in LLM output.). Mask/block; do not remove without review. site_id='site:sha256:1d1c403744af77726d466c6ea499a822d481ce0c38ab4cb98cfe75f4616ddf22'
                _gr_client = _lineaje_load_gr_client()
                _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:1d1c403744af77726d466c6ea499a822d481ce0c38ab4cb98cfe75f4616ddf22', phase='post_agent_receive', boundary={'source': 'user_interface', 'sink': 'agent_message'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='user_interface', destination_type='agent')
                tool_name = _gr_client.enforce(_gr_site, tool_name, content_type='application/json', variable_name='tool_name', source_file=__file__, before_line=30)
                return tools_class.create_tool(tool_name, config)
            elif tool_name.lower() == category and tools_class.default_tool:
                return tools_class.create_tool(tools_class.default_tool, config)
        raise ValueError(f"Tool {tool_name} is not supported.")
