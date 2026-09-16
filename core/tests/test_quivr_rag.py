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

from uuid import uuid4

import pytest
from quivr_core.rag.entities.chat import ChatHistory
from quivr_core.rag.entities.config import LLMEndpointConfig, RetrievalConfig
from quivr_core.llm import LLMEndpoint
from quivr_core.rag.entities.models import ParsedRAGChunkResponse, RAGResponseMetadata
from quivr_core.rag.quivr_rag_langgraph import QuivrQARAGLangGraph


@pytest.fixture(scope="function")
def mock_chain_qa_stream(monkeypatch, chunks_stream_answer):
    class MockQAChain:
        async def astream_events(self, *args, **kwargs):
            default_metadata = {
                "langgraph_node": "generate",
                "is_final_node": False,
                "citations": None,
                "followup_questions": None,
                "sources": None,
                "metadata_model": None,
            }

            # Send all chunks except the last one
            for chunk in chunks_stream_answer[:-1]:
                yield {
                    "event": "on_chat_model_stream",
                    "metadata": default_metadata,
                    "data": {"chunk": chunk["answer"]},
                }

            # Send the last chunk
            yield {
                "event": "end",
                "metadata": {
                    "langgraph_node": "generate",
                    "is_final_node": True,
                    "citations": [],
                    "followup_questions": None,
                    "sources": [],
                    "metadata_model": None,
                },
                "data": {"chunk": chunks_stream_answer[-1]["answer"]},
            }

    def mock_qa_chain(*args, **kwargs):
        self = args[0]
        self.final_nodes = ["generate"]
        return MockQAChain()

    monkeypatch.setattr(QuivrQARAGLangGraph, "build_chain", mock_qa_chain)


@pytest.mark.base
@pytest.mark.asyncio
async def test_quivrqaraglanggraph(
    mem_vector_store, full_response, mock_chain_qa_stream, openai_api_key
):
    # Making sure the model
    llm_config = LLMEndpointConfig(model="gpt-4o")
    # LINEAJE: enforce() `llm_config` at file_storage->agent data_egress — scan flagged AI_APP_SEC_006 (Use only LLMs from the organization's approved list.); AI_APP_SEC_028 (Do not use LLMs from the organization's disallowed list); AI_IAC_SEC_020 (Restrict AI agents to an explicit tool allow list.). Mask/block; do not remove without review. site_id='site:sha256:8be21e904a02214c1ab3496da6d6f889267f4b34aa4e714de3a1fa55fb42ca0a'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:8be21e904a02214c1ab3496da6d6f889267f4b34aa4e714de3a1fa55fb42ca0a', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'external_endpoint'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='file_storage', destination_type='agent')
    llm_config = _gr_client.enforce(_gr_site, llm_config, content_type='application/json')
    # LINEAJE: enforce() `llm_config` at html->user_interface data_egress — scan flagged AI_IAC_018 (Enforce cryptographically verified user-to-agent binding for every request.). Mask/block; do not remove without review. site_id='site:sha256:da0afe78431d5a7a7b8146415a2de212c7689fc41c35dcfa30c2136ae2ce7d67'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:da0afe78431d5a7a7b8146415a2de212c7689fc41c35dcfa30c2136ae2ce7d67', phase='data_egress', boundary={'source': 'html', 'sink': 'user_interface'}, candidate_policies=[{'policy_id': 'AI_DAT_SEC_012', 'guardrail_id': 'Mask PII on UI', 'policy_version': '2026.08.1'}], fail_mode='BLOCK', source_type='html', destination_type='user_interface')
    llm_config = _gr_client.enforce(_gr_site, llm_config, content_type='text/html')
    llm = LLMEndpoint.from_config(llm_config)
    retrieval_config = RetrievalConfig(llm_config=llm_config)
    chat_history = ChatHistory(uuid4(), uuid4())
    rag_pipeline = QuivrQARAGLangGraph(
        retrieval_config=retrieval_config, llm=llm, vector_store=mem_vector_store
    )

    stream_responses: list[ParsedRAGChunkResponse] = []

    # Making sure that we are calling the func_calling code path
    assert rag_pipeline.llm_endpoint.supports_func_calling()
    # LINEAJE: enforce() `chat_history` at agent->tool post_tool — scan flagged AI_APP_SEC_014 (MCP server must validate and sanitize all input); AI_APP_SEC_029 (Agent must validate, sanitize LLM output including for presence of eval or any dynamic code execution primitive in LLM output.); AI_APP_SEC_038 (The AI Model must validate and sanitize any input before processing.). Mask/block; do not remove without review. site_id='site:sha256:ec1de840f29034ca9d09b698098a15dd827d812786112c6a2903d9c38b7487a4'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:ec1de840f29034ca9d09b698098a15dd827d812786112c6a2903d9c38b7487a4', phase='post_tool', boundary={'source': 'tool_result', 'sink': 'agent_message'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='agent', destination_type='tool')
    chat_history = _gr_client.enforce(_gr_site, chat_history, content_type='application/json', variable_name='chat_history', source_file=__file__, before_line=72)
    async for resp in rag_pipeline.answer_astream(
        "answer in bullet points. tell me something", chat_history, []
    ):
        stream_responses.append(resp)

    # This assertion passed
    assert all(
        not r.last_chunk for r in stream_responses[:-1]
    ), "Some chunks before last have last_chunk=True"
    assert stream_responses[-1].last_chunk

    # Let's check this assertion
    for idx, response in enumerate(stream_responses[1:-1]):
        assert (
            len(response.answer) > 0
        ), f"Sent an empty answer {response} at index {idx+1}"

    # Verify metadata
    default_metadata = RAGResponseMetadata().model_dump()
    assert all(
        r.metadata.model_dump() == default_metadata for r in stream_responses[:-1]
    )
    last_response = stream_responses[-1]
    # TODO(@aminediro) : test responses with sources
    assert last_response.metadata.sources == []
    assert last_response.metadata.citations == []

    # Assert whole response makes sense
    assert "".join([r.answer for r in stream_responses]) == full_response
