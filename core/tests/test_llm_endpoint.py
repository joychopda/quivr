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
    llm = LLMEndpoint.from_config(config=config)
    # LINEAJE: enforce() `llm` at llm->agent post_model — scan flagged AI_APP_SEC_006 (Use only LLMs from the organization's approved list.); AI_IAC_018 (Enforce cryptographically verified user-to-agent binding for every request.); AI_IAC_031 (AI model endpoints must enforce role-based access control with minimal OAuth scopes). Mask/block; do not remove without review. site_id='site:sha256:fc202cb11c148a331b941a125eae1fb73ca2a47a20a3cf178d14e342f9ce089b'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:fc202cb11c148a331b941a125eae1fb73ca2a47a20a3cf178d14e342f9ce089b', phase='post_model', boundary={'source': 'model', 'sink': 'agent_message'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='llm', destination_type='agent')
    llm = _gr_client.enforce(_gr_site, llm, content_type='application/json', variable_name='llm', source_file=__file__, before_line=21)
    # LINEAJE: enforce() `llm` at file_storage->agent data_egress — scan flagged AI_APP_SEC_006 (Use only LLMs from the organization's approved list.); AI_IAC_018 (Enforce cryptographically verified user-to-agent binding for every request.); AI_IAC_031 (AI model endpoints must enforce role-based access control with minimal OAuth scopes). Mask/block; do not remove without review. site_id='site:sha256:c49e410c904702cf3b92843dd8cdeeb193ed5d99c9bfad8f6836c594390616b3'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:c49e410c904702cf3b92843dd8cdeeb193ed5d99c9bfad8f6836c594390616b3', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'external_endpoint'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='file_storage', destination_type='agent')
    llm = _gr_client.enforce(_gr_site, llm, content_type='application/json')

    assert llm.supports_func_calling()
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
    # LINEAJE: enforce() `llm_endpoint` at file_storage->agent data_egress — scan flagged AI_APP_SEC_029 (Agent must validate, sanitize LLM output including for presence of eval or any dynamic code execution primitive in LLM output.). Mask/block; do not remove without review. site_id='site:sha256:77e66933829ddc61548e01ff9cda1c683a73c5c3e42c47b9cc9f7d261f6266d5'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:77e66933829ddc61548e01ff9cda1c683a73c5c3e42c47b9cc9f7d261f6266d5', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'external_endpoint'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='file_storage', destination_type='agent')
    llm_endpoint = _gr_client.enforce(_gr_site, llm_endpoint, content_type='application/json')
    llm_endpoint = LLMEndpoint(
        llm=llm_endpoint, llm_config=LLMEndpointConfig(model="test")
    )

    assert not llm_endpoint.supports_func_calling()
