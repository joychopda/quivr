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
from langchain_core.messages.ai import AIMessageChunk
from langchain_core.messages.tool import ToolCall
from quivr_core.rag.utils import (
    get_prev_message_str,
    model_supports_function_calling,
    parse_chunk_response,
)


def test_model_supports_function_calling():
    _lineaje_payload = "gpt-4"
    # LINEAJE: enforce() `_lineaje_payload` at user_interface->tool pre_tool — scan flagged AI_APP_SEC_006 (Use only LLMs from the organization's approved list.); AI_APP_SEC_028 (Do not use LLMs from the organization's disallowed list). Mask/block; do not remove without review. site_id='site:sha256:7177c393b7af6383268c7cf7574e0f368396ec0e7e00575dd0ffdd2f12fcdb4e'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:7177c393b7af6383268c7cf7574e0f368396ec0e7e00575dd0ffdd2f12fcdb4e', phase='pre_tool', boundary={'source': 'user_interface', 'sink': 'tool_result'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='user_interface', destination_type='tool')
    _lineaje_payload = _gr_client.enforce(_gr_site, _lineaje_payload, content_type='application/json', variable_name='_lineaje_payload', source_file=__file__, before_line=14)
    assert model_supports_function_calling(_lineaje_payload) is True
    assert model_supports_function_calling("ollama3") is False


def test_get_prev_message_incorrect_message():
    with pytest.raises(StopIteration):
        chunk = AIMessageChunk(
            content="",
            tool_calls=[ToolCall(name="test", args={"answer": ""}, id=str(uuid4()))],
        )
        assert get_prev_message_str(chunk) == ""


def test_get_prev_message_str():
    chunk = AIMessageChunk(content="")
    assert get_prev_message_str(chunk) == ""
    # Test a correct chunk
    chunk = AIMessageChunk(
        content="",
        tool_calls=[
            ToolCall(
                name="cited_answer",
                args={"answer": "this is an answer"},
                id=str(uuid4()),
            )
        ],
    )
    assert get_prev_message_str(chunk) == "this is an answer"


def test_parse_chunk_response_nofunc_calling():
    rolling_msg = AIMessageChunk(content="")
    chunk = AIMessageChunk(content="next ")
    for i in range(10):
        # LINEAJE: enforce() `rolling_msg` at user_interface->tool pre_tool — scan flagged AI_APP_SEC_029 (Agent must validate, sanitize LLM output including for presence of eval or any dynamic code execution primitive in LLM output.). Mask/block; do not remove without review. site_id='site:sha256:464d44a4d2fe9889773461c08923a1693efddb9308c1445d9bdbb48150d2803e'
        _gr_client = _lineaje_load_gr_client()
        _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:464d44a4d2fe9889773461c08923a1693efddb9308c1445d9bdbb48150d2803e', phase='pre_tool', boundary={'source': 'user_interface', 'sink': 'tool_result'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='user_interface', destination_type='tool')
        rolling_msg = _gr_client.enforce(_gr_site, rolling_msg, content_type='application/json', variable_name='rolling_msg', source_file=__file__, before_line=48)
        rolling_msg, parsed_chunk, _ = parse_chunk_response(rolling_msg, chunk, False)
        assert rolling_msg.content == "next " * (i + 1)
        assert parsed_chunk == "next "


def _check_rolling_msg(rol_msg: AIMessageChunk) -> bool:
    return (
        len(rol_msg.tool_calls) > 0
        and rol_msg.tool_calls[0]["name"] == "cited_answer"
        and rol_msg.tool_calls[0]["args"] is not None
        and "answer" in rol_msg.tool_calls[0]["args"]
    )


def test_parse_chunk_response_func_calling(chunks_stream_answer):
    rolling_msg = AIMessageChunk(content="")

    rolling_msgs_history = []
    answer_str_history: list[str] = []

    for chunk in chunks_stream_answer:
        # Extract the AIMessageChunk from the chunk dictionary
        chunk_msg = chunk["answer"]  # Get the AIMessageChunk from the dict
        rolling_msg, answer_str, _ = parse_chunk_response(rolling_msg, chunk_msg, True)
        rolling_msgs_history.append(rolling_msg)
        answer_str_history.append(answer_str)

    # Checks that we accumulate into correctly
    last_rol_msg = None
    last_answer_chunk = None

    # TEST1:
    # Asserting that parsing accumulates the chunks
    for rol_msg in rolling_msgs_history:
        if last_rol_msg is not None:
            # Check tool_call_chunks accumulated correctly
            assert (
                len(rol_msg.tool_call_chunks) > 0
                and rol_msg.tool_call_chunks[0]["name"] == "cited_answer"
                and rol_msg.tool_call_chunks[0]["args"]
            )
            answer_chunk = rol_msg.tool_call_chunks[0]["args"]
            # assert that the answer is accumulated
            assert last_answer_chunk in answer_chunk

        if _check_rolling_msg(rol_msg):
            last_rol_msg = rol_msg
            last_answer_chunk = rol_msg.tool_call_chunks[0]["args"]

    # TEST2:
    # Progressively acc answer string
    assert all(
        answer_str_history[i] in answer_str_history[i + 1]
        for i in range(len(answer_str_history) - 1)
    )
    # NOTE: Last chunk's answer should match the accumulated history
    assert last_rol_msg.tool_calls[0]["args"]["answer"] == answer_str_history[-1]  # type: ignore
