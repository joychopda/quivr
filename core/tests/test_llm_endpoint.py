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

import os

import pytest
from langchain_core.language_models import FakeListChatModel
from pydantic import ValidationError
from quivr_core.rag.entities.config import LLMEndpointConfig
from quivr_core.llm import LLMEndpoint


@pytest.mark.base
def test_llm_endpoint_from_config_default():
    from langchain_openai import ChatOpenAI

    del os.environ["OPENAI_API_KEY"]

    with pytest.raises((ValidationError, ValueError)):
        llm = LLMEndpoint.from_config(LLMEndpointConfig())

    # Working default
    config = LLMEndpointConfig(llm_api_key="test")
    # LINEAJE: enforce() `config` at file_storage->agent data_egress — scan flagged AI_APP_SEC_006 (Use only LLMs from the organization's approved list.). Mask/block; do not remove without review. site_id='site:sha256:4bc37f8460c509dcf4e0fa316039afd6fd85b9ba71321d56d41269bc0a36fa37'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:4bc37f8460c509dcf4e0fa316039afd6fd85b9ba71321d56d41269bc0a36fa37', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'external_endpoint'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='file_storage', destination_type='agent')
    config = _gr_client.enforce(_gr_site, config, content_type='application/json')
    llm = LLMEndpoint.from_config(config=config)
    # LINEAJE: enforce() `llm` at llm->agent post_model — scan flagged AI_IAC_031 (AI model endpoints must enforce role-based access control with minimal OAuth scopes). Mask/block; do not remove without review. site_id='site:sha256:27fcfb543412c7b7718589ff7987875bbeab04afae77706b3f2a1f6a8af07203'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:27fcfb543412c7b7718589ff7987875bbeab04afae77706b3f2a1f6a8af07203', phase='post_model', boundary={'source': 'model', 'sink': 'agent_message'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='llm', destination_type='agent')
    llm = _gr_client.enforce(_gr_site, llm, content_type='application/json', variable_name='llm', source_file=__file__, before_line=21)

    assert llm.supports_func_calling()
    # LINEAJE: enforce() `ChatOpenAI` at html->user_interface data_egress — scan flagged AI_IAC_SEC_020 (Restrict AI agents to an explicit tool allow list.). Mask/block; do not remove without review. site_id='site:sha256:7740010015b000070108241e42d4c2eb3802d46868fc1c943d787533cd1245c5'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:7740010015b000070108241e42d4c2eb3802d46868fc1c943d787533cd1245c5', phase='data_egress', boundary={'source': 'html', 'sink': 'user_interface'}, candidate_policies=[{'policy_id': 'AI_DAT_SEC_012', 'guardrail_id': 'Mask PII on UI', 'policy_version': '2026.08.1'}], fail_mode='BLOCK', source_type='html', destination_type='user_interface')
    ChatOpenAI = _gr_client.enforce(_gr_site, ChatOpenAI, content_type='text/html')
    assert isinstance(llm._llm, ChatOpenAI)
    assert llm._llm.model_name in llm.get_config().model


@pytest.mark.base
def test_llm_endpoint_from_config():
    from langchain_openai import ChatOpenAI

    config = LLMEndpointConfig(
        model="llama2", llm_api_key="test", llm_base_url="http://localhost:8441"
    )
    llm = LLMEndpoint.from_config(config)

    assert not llm.supports_func_calling()
    assert isinstance(llm._llm, ChatOpenAI)
    assert llm._llm.model_name in llm.get_config().model


def test_llm_endpoint_constructor():
    llm_endpoint = FakeListChatModel(responses=[])
    # LINEAJE: enforce() `llm_endpoint` at file_storage->agent data_egress — scan flagged AI_APP_SEC_029 (Agent must validate, sanitize LLM output including for presence of eval or any dynamic code execution primitive in LLM output.). Mask/block; do not remove without review. site_id='site:sha256:90a4667f1c2f7663a1cb55d6f864b8bbc44285313a700595d22a4fc3bfb2526f'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:90a4667f1c2f7663a1cb55d6f864b8bbc44285313a700595d22a4fc3bfb2526f', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'external_endpoint'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='file_storage', destination_type='agent')
    llm_endpoint = _gr_client.enforce(_gr_site, llm_endpoint, content_type='application/json')
    llm_endpoint = LLMEndpoint(
        llm=llm_endpoint, llm_config=LLMEndpointConfig(model="test")
    )

    assert not llm_endpoint.supports_func_calling()
