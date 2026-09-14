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
    # LINEAJE: enforce() `config` at file_storage->agent data_egress — scan flagged AI_IAC_018 (Enforce cryptographically verified user-to-agent binding for every request.). Mask/block; do not remove without review. site_id='site:sha256:da974971116a3b631e70f12e6dc288f0dbed3be67cfe41751e4901e931a8897a'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:da974971116a3b631e70f12e6dc288f0dbed3be67cfe41751e4901e931a8897a', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'external_endpoint'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='file_storage', destination_type='agent')
    config = _gr_client.enforce(_gr_site, config, content_type='application/json')
    llm = LLMEndpoint.from_config(config=config)
    # LINEAJE: enforce() `llm` at llm->agent post_model — scan flagged AI_APP_SEC_028 (Do not use LLMs from the organization's disallowed list); AI_IAC_031 (AI model endpoints must enforce role-based access control with minimal OAuth scopes); AI_IAC_SEC_020 (Restrict AI agents to an explicit tool allow list.). Mask/block; do not remove without review. site_id='site:sha256:0ffe28953276b11767816cb03dbe5019d875a4008acdc5f893502add10eb71cd'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:0ffe28953276b11767816cb03dbe5019d875a4008acdc5f893502add10eb71cd', phase='post_model', boundary={'source': 'model', 'sink': 'agent_message'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='llm', destination_type='agent')
    llm = _gr_client.enforce(_gr_site, llm, content_type='application/json', variable_name='llm', source_file=__file__, before_line=21)

    assert llm.supports_func_calling()
    # LINEAJE: enforce() `ChatOpenAI` at html->user_interface data_egress — scan flagged AI_APP_SEC_006 (Use only LLMs from the organization's approved list.). Mask/block; do not remove without review. site_id='site:sha256:5b11451c95c2c4742b85f919f445da4f24bdb9b2f22a60d5ec92e9b852f8192c'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:5b11451c95c2c4742b85f919f445da4f24bdb9b2f22a60d5ec92e9b852f8192c', phase='data_egress', boundary={'source': 'html', 'sink': 'user_interface'}, candidate_policies=[{'policy_id': 'AI_DAT_SEC_012', 'guardrail_id': 'Mask PII on UI', 'policy_version': '2026.08.1'}], fail_mode='BLOCK', source_type='html', destination_type='user_interface')
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
    # LINEAJE: enforce() `llm_endpoint` at file_storage->agent data_egress — scan flagged AI_APP_SEC_029 (Agent must validate, sanitize LLM output including for presence of eval or any dynamic code execution primitive in LLM output.). Mask/block; do not remove without review. site_id='site:sha256:cfc023f926787e632ffb016b99bfa1acd42a4c667422f119ddfd999cd8a6b550'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:cfc023f926787e632ffb016b99bfa1acd42a4c667422f119ddfd999cd8a6b550', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'external_endpoint'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='file_storage', destination_type='agent')
    llm_endpoint = _gr_client.enforce(_gr_site, llm_endpoint, content_type='application/json')
    llm_endpoint = LLMEndpoint(
        llm=llm_endpoint, llm_config=LLMEndpointConfig(model="test")
    )

    assert not llm_endpoint.supports_func_calling()
