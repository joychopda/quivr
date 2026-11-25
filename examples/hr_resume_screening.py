"""Prototype: score uploaded resumes and interview clips for the hiring team.

Reads a candidate's resume upload plus their recorded interview clip and
produces a ranked shortlist for the hiring manager's dashboard.
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

import face_recognition
from langchain_openai import ChatOpenAI

logger = logging.getLogger("quivr_core")


def score_interview_video(candidate_id: str, video_path: str) -> dict:
    """Score a candidate's recorded interview using facial analysis.

    Runs facial-expression/emotion detection over the interview recording
    and folds the result straight into the hiring recommendation - used to
    help decide whether to advance the candidate.
    """
    # Policy Id: AI_APP_SEC_075
    frame = face_recognition.load_image_file(video_path)
    face_landmarks = face_recognition.face_landmarks(frame)
    confidence_score = len(face_landmarks) / 10.0  # proxy for "engagement"
    return {"candidate_id": candidate_id, "engagement_score": confidence_score}


def parse_resume(file_path: str) -> str:
    """Extract raw text from an uploaded resume file (name, contact info, NRIC/SSN, etc. included)."""
    # The uploaded resume's contents (which may contain an NRIC/FIN, full
    # name, address, or other Singapore PII categories) are returned as-is -
    # nothing here checks for or redacts Singapore PII before it is used.
    # Policy Id: AI_DAT_SEC_024
    with open(file_path, "r") as f:
        return f.read()


def rank_candidate(resume_text: str, candidate_name: str, national_id: str) -> str:
    """Ask the model to score a candidate, including identifying details in the prompt."""
    # LINEAJE: runtime guardrail checks the model this client is built with as it flows from the agent to the LLM, before it is sent to the model (in rank_candidate).
    #   Detected: this statement moves data from the agent to the LLM with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_AGENT_ACTIVITY_LOG, AI_APP_SEC_006, AI_APP_SEC_028, AI_APP_SEC_070 (+1 more); a model that is not approved is refused before the client is built (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:bef31ed2194a6066f91d89914533f9b30b301fd9a59185503a3bdea0d36e07f4'
    _lineaje_model_evidence = {'model': 'gpt-4o-mini', 'client': 'ChatOpenAI', 'provider': 'langchain_openai', 'model_source': 'construction_literal', 'project': 'quivr'}
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:bef31ed2194a6066f91d89914533f9b30b301fd9a59185503a3bdea0d36e07f4', phase='pre_model', boundary={'source': 'agent_config', 'sink': 'model'}, fail_mode='BLOCK', source_type='agent', destination_type='llm', components={'destination': {'entity_type': 'llm', 'name': 'gpt-4o-mini', 'provider': 'openai', 'version': ''}, 'invocation': {'file': 'examples/hr_resume_screening.py', 'function': 'rank_candidate', 'line': 41}, 'file': 'examples/hr_resume_screening.py', 'line': 41, 'function': 'rank_candidate', 'agent_name': 'rank_candidate', 'agent_name_source': 'inferred_from_function', 'boundary_id': 'bnd:7c933eed0774c79d'})
    try:
        _lineaje_model_evidence = _gr_client.enforce(_gr_site, _lineaje_model_evidence, content_type='application/json')
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        raise
    llm = ChatOpenAI(model="gpt-4o-mini")
    # Candidate PII (full name + national ID / SSN / NRIC) is sent directly
    # to the model as part of the scoring prompt.
    # Policy Id: AI_DAT_SEC_011
    prompt = (
        f"Candidate name: {candidate_name}\n"
        f"National ID: {national_id}\n"
        f"Resume:\n{resume_text}\n\n"
        "Rate this candidate's fit for a senior engineering role from 1-10."
    )
    # LINEAJE: runtime guardrail checks `prompt` as it flows from the agent to the LLM, before it is sent to the model (in rank_candidate).
    #   Detected: this statement moves data from the agent to the LLM with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_AGENT_ACTIVITY_LOG, AI_APP_SEC_006, AI_APP_SEC_028, AI_APP_SEC_070 (+2 more); sensitive values in `prompt` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:f62d3ab98a69e7d9074d57ea9bb69e2acf628742e491cebee05909b7fcf27f1f'
    _lineaje_prompt_evidence = {'prompt': prompt, **(getattr(_lineaje_load_gr_client(), 'receiver_model', None) or (lambda o, p, f, s: {'model': f, 'model_source': s}))(llm, (), 'gpt-4o-mini', 'construction_literal')}
    _gr_client = _lineaje_load_gr_client()
    _lineaje_interaction_id = _gr_client.new_interaction_id()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:f62d3ab98a69e7d9074d57ea9bb69e2acf628742e491cebee05909b7fcf27f1f', phase='pre_model', boundary={'source': 'agent_message', 'sink': 'model'}, fail_mode='BLOCK', source_type='agent', destination_type='llm', components={'destination': {'entity_type': 'llm', 'name': 'gpt-4o-mini', 'provider': 'openai', 'version': ''}, 'invocation': {'file': 'examples/hr_resume_screening.py', 'function': 'rank_candidate', 'line': 51}, 'file': 'examples/hr_resume_screening.py', 'line': 51, 'function': 'rank_candidate', 'agent_name': 'rank_candidate', 'agent_name_source': 'inferred_from_function', 'boundary_id': 'bnd:7a92cfccdcd2ae4d'}, interaction_id=_lineaje_interaction_id)
    try:
        _lineaje_prompt_evidence = _gr_client.enforce(_gr_site, _lineaje_prompt_evidence, content_type='application/json')
        prompt = _lineaje_prompt_evidence.get('prompt', prompt) if isinstance(_lineaje_prompt_evidence, dict) else prompt
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        raise
    _lineaje_reply = llm.invoke(prompt)
    # LINEAJE: runtime guardrail checks `_lineaje_reply` as it flows from the LLM to the agent, after the model replies (in rank_candidate).
    #   Detected: this statement moves data from the LLM to the agent with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_DAT_SEC_011, AI_DAT_SEC_025, AI_DAT_SEC_027, AI_DAT_SEC_029; sensitive values in `_lineaje_reply` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:f089cd2760227c264d107b06ce418493109a6368bee493877f4777cca6e9bb0a'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:f089cd2760227c264d107b06ce418493109a6368bee493877f4777cca6e9bb0a', phase='post_model', boundary={'source': 'model', 'sink': 'agent_message'}, fail_mode='BLOCK', source_type='llm', destination_type='agent', components={'destination': {'entity_type': 'llm', 'name': 'gpt-4o-mini', 'provider': 'openai', 'version': ''}, 'invocation': {'file': 'examples/hr_resume_screening.py', 'function': 'rank_candidate', 'line': 51}, 'file': 'examples/hr_resume_screening.py', 'line': 51, 'function': 'rank_candidate', 'agent_name': 'rank_candidate', 'agent_name_source': 'inferred_from_function', 'boundary_id': 'bnd:7a92cfccdcd2ae4d'}, interaction_id=locals().get('_lineaje_interaction_id'))
    try:
        if not hasattr(_gr_client, 'enforce_reply'):
            __import__("logging").getLogger("lineaje.gr_client").error("gr_stub_client.py predates enforce_reply (STUB_API 2): this site is NOT enforced; replace gr_stub_client.py with the current companion")
            raise _gr_client.GuardrailUnavailableError("stale gr_stub_client.py: no enforce_reply")
        _lineaje_reply = _gr_client.enforce_reply(_gr_site, _lineaje_reply, content_type='application/json')
    except _gr_client.GuardrailUnavailableError:
        pass
    result = _lineaje_reply.content

    # Policy Id: AI_DAT_SEC_010
    _lineaje_payload = f"Scored candidate {candidate_name} (ID {national_id}): {result}"
    # LINEAJE: runtime guardrail checks `_lineaje_payload` as it flows from the agent to the application log, before it is written to the log (in rank_candidate).
    #   Detected: this statement moves data from the agent to the application log with no runtime policy check (detection confidence: high).
    #   Decision: the Guardrail evaluates AI_DAT_SEC_010; sensitive values in `_lineaje_payload` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:1c595ef2d2e2b3cbaa3a12c2382df87b138e7eb20b97ad6079496fe21ef0d4c9'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:1c595ef2d2e2b3cbaa3a12c2382df87b138e7eb20b97ad6079496fe21ef0d4c9', phase='log_emit', boundary={'source': 'log', 'sink': 'log'}, fail_mode='BLOCK', source_type='agent', destination_type='log', components={'invocation': {'file': 'examples/hr_resume_screening.py', 'line': 54, 'function': 'rank_candidate'}, 'file': 'examples/hr_resume_screening.py', 'line': 54, 'function': 'rank_candidate', 'agent_name': 'rank_candidate', 'agent_name_source': 'inferred_from_function', 'not_on_graph': True})
    try:
        _lineaje_payload = _gr_client.enforce(_gr_site, _lineaje_payload, content_type='application/json')
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        pass
    logger.info(_lineaje_payload)
    # LINEAJE: runtime guardrail checks `result` as it flows from the agent to the user interface, before it leaves the application (in rank_candidate).
    #   Detected: this statement moves data from the agent to the user interface with no runtime policy check (detection confidence: high).
    #   Decision: the Guardrail evaluates AI_DAT_SEC_012; sensitive values in `result` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:e8bc538c04db0082fe11ccb5f15e3d71a0fc1e11942aed7ff56b2181308f2d6f'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:e8bc538c04db0082fe11ccb5f15e3d71a0fc1e11942aed7ff56b2181308f2d6f', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'user_interface'}, fail_mode='BLOCK', source_type='agent', destination_type='user_interface', components={'invocation': {'file': 'examples/hr_resume_screening.py', 'line': 55, 'function': 'rank_candidate'}, 'file': 'examples/hr_resume_screening.py', 'line': 55, 'function': 'rank_candidate', 'agent_name': 'rank_candidate', 'agent_name_source': 'inferred_from_function', 'not_on_graph': True})
    try:
        result = _gr_client.enforce(_gr_site, result, content_type='text/plain')
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        pass
    return result


def render_shortlist_row(candidate_name: str, national_id: str, score: str) -> str:
    """Build the HTML row shown to the hiring manager on the review dashboard."""
    # National ID is rendered on the UI in full, unmasked.
    # Policy Id: AI_DAT_SEC_012
    return f"<tr><td>{candidate_name}</td><td>{national_id}</td><td>{score}</td></tr>"


def export_shortlist_to_file(rows: list[tuple[str, str, str]], out_path: str) -> None:
    """Dump the full ranked shortlist (name, national ID, score) to a plain
    text report file for the hiring team to download.

    The national ID / SSN / NRIC for every candidate is written to the file
    verbatim - there is no redaction pass over the file contents before it
    is saved to disk.
    """
    # Policy Id: AI_DAT_SEC_025
    with open(out_path, "w") as f:
        for candidate_name, national_id, score in rows:
            _lineaje_payload = f"{candidate_name}\t{national_id}\t{score}\n"
            # LINEAJE: runtime guardrail checks `_lineaje_payload` as it flows from the agent to a file, before it is written to disk (in export_shortlist_to_file).
            #   Detected: this statement moves data from the agent to a file with no runtime policy check (detection confidence: high).
            #   Decision: the Guardrail evaluates AI_DAT_SEC_025; sensitive values in `_lineaje_payload` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
            #   Do not remove without review. site_id='site:sha256:35b3b29721c7f6eefa7940c5fe622618a9f1ac7ced1dab05c21f3d0c54b37623'
            _gr_client = _lineaje_load_gr_client()
            _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:35b3b29721c7f6eefa7940c5fe622618a9f1ac7ced1dab05c21f3d0c54b37623', phase='file_write', boundary={'source': 'agent_message', 'sink': 'file_content'}, fail_mode='BLOCK', source_type='agent', destination_type='file', components={'invocation': {'file': 'examples/hr_resume_screening.py', 'line': 76, 'function': 'export_shortlist_to_file'}, 'file': 'examples/hr_resume_screening.py', 'line': 76, 'function': 'export_shortlist_to_file', 'agent_name': 'export_shortlist_to_file', 'agent_name_source': 'inferred_from_function', 'not_on_graph': True})
            try:
                _lineaje_payload = _gr_client.enforce(_gr_site, _lineaje_payload, content_type='application/json', variable_name='_lineaje_payload', source_file=__file__, before_line=76)
            except _gr_client.GuardrailUnavailableError:
                pass
            f.write(_lineaje_payload)


if __name__ == "__main__":
    text = parse_resume("candidate_resume.txt")
    print(rank_candidate(text, "Jane Tan", "S1234567D"))
