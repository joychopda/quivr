"""Prototype clinical assistant: answers patient questions and drafts
treatment suggestions from a patient's chart for the reviewing clinician.
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


import requests
from langchain_openai import ChatOpenAI


def chat_with_patient(message: str) -> str:
    """Respond to a patient's message in the portal chat widget."""
    # LINEAJE: runtime guardrail checks the model this client is built with as it flows from the agent to the LLM, before it is sent to the model (in chat_with_patient).
    #   Detected: this statement moves data from the agent to the LLM with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_AGENT_ACTIVITY_LOG, AI_APP_SEC_006, AI_APP_SEC_028, AI_APP_SEC_070 (+1 more); a model that is not approved is refused before the client is built (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:b6c5b3acef26087a42d48c70ffa079c8864cb633106508368556fcdf2bf3e2a8'
    _lineaje_model_evidence = {'model': 'gpt-4o-mini', 'client': 'ChatOpenAI', 'provider': 'langchain_openai', 'model_source': 'construction_literal', 'project': 'quivr'}
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:b6c5b3acef26087a42d48c70ffa079c8864cb633106508368556fcdf2bf3e2a8', phase='pre_model', boundary={'source': 'agent_config', 'sink': 'model'}, fail_mode='BLOCK', source_type='agent', destination_type='llm', components={'destination': {'entity_type': 'llm', 'name': 'gpt-4o-mini', 'provider': 'openai', 'version': ''}, 'invocation': {'file': 'examples/healthcare_assistant.py', 'function': 'chat_with_patient', 'line': 11}, 'file': 'examples/healthcare_assistant.py', 'line': 11, 'function': 'chat_with_patient', 'agent_name': 'chat_with_patient', 'agent_name_source': 'inferred_from_function', 'boundary_id': 'bnd:c9298653a60c67b9'})
    try:
        _lineaje_model_evidence = _gr_client.enforce(_gr_site, _lineaje_model_evidence, content_type='application/json')
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        raise
    llm = ChatOpenAI(model="gpt-4o-mini")
    # The reply goes straight back to the patient with no disclosure that
    # they are talking to an AI system rather than clinic staff.
    # Policy Id: AI_IAC_023
    _lineaje_arg = f"You are a friendly clinic assistant. Patient asks: {message}"
    # LINEAJE: runtime guardrail checks `_lineaje_arg` as it flows from the agent to the LLM, before it is sent to the model (in chat_with_patient).
    #   Detected: this statement moves data from the agent to the LLM with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_AGENT_ACTIVITY_LOG, AI_APP_SEC_006, AI_APP_SEC_028, AI_APP_SEC_070 (+2 more); sensitive values in `_lineaje_arg` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:ce39cd8fb7265a1bd0abdddf6f640b213fc2e81bd223edcb56b2450554c502ba'
    _lineaje__lineaje_arg_evidence = {'_lineaje_arg': _lineaje_arg, **(getattr(_lineaje_load_gr_client(), 'receiver_model', None) or (lambda o, p, f, s: {'model': f, 'model_source': s}))(llm, (), 'gpt-4o-mini', 'construction_literal')}
    _gr_client = _lineaje_load_gr_client()
    _lineaje_interaction_id = _gr_client.new_interaction_id()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:ce39cd8fb7265a1bd0abdddf6f640b213fc2e81bd223edcb56b2450554c502ba', phase='pre_model', boundary={'source': 'agent_message', 'sink': 'model'}, fail_mode='BLOCK', source_type='agent', destination_type='llm', components={'destination': {'entity_type': 'llm', 'name': 'gpt-4o-mini', 'provider': 'openai', 'version': ''}, 'invocation': {'file': 'examples/healthcare_assistant.py', 'function': 'chat_with_patient', 'line': 15}, 'file': 'examples/healthcare_assistant.py', 'line': 15, 'function': 'chat_with_patient', 'agent_name': 'chat_with_patient', 'agent_name_source': 'inferred_from_function', 'boundary_id': 'bnd:f6041ce8bdcaffbf'}, interaction_id=_lineaje_interaction_id)
    try:
        _lineaje__lineaje_arg_evidence = _gr_client.enforce(_gr_site, _lineaje__lineaje_arg_evidence, content_type='application/json')
        _lineaje_arg = _lineaje__lineaje_arg_evidence.get('_lineaje_arg', _lineaje_arg) if isinstance(_lineaje__lineaje_arg_evidence, dict) else _lineaje_arg
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        raise
    return llm.invoke(_lineaje_arg).content


def suggest_diagnosis(symptoms: str, imaging_notes: str) -> str:
    """Draft a diagnostic suggestion from reported symptoms and imaging notes."""
    # LINEAJE: runtime guardrail checks the model this client is built with as it flows from the agent to the LLM, before it is sent to the model (in suggest_diagnosis).
    #   Detected: this statement moves data from the agent to the LLM with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_AGENT_ACTIVITY_LOG, AI_APP_SEC_006, AI_APP_SEC_028, AI_APP_SEC_070 (+1 more); a model that is not approved is refused before the client is built (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:2035bb16e8d2fe45509bd87ef0a9cdcf3503b04640fd130a89b22c59685f127a'
    _lineaje_model_evidence = {'model': 'gpt-4o-mini', 'client': 'ChatOpenAI', 'provider': 'langchain_openai', 'model_source': 'construction_literal', 'project': 'quivr'}
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:2035bb16e8d2fe45509bd87ef0a9cdcf3503b04640fd130a89b22c59685f127a', phase='pre_model', boundary={'source': 'agent_config', 'sink': 'model'}, fail_mode='BLOCK', source_type='agent', destination_type='llm', components={'destination': {'entity_type': 'llm', 'name': 'gpt-4o-mini', 'provider': 'openai', 'version': ''}, 'invocation': {'file': 'examples/healthcare_assistant.py', 'function': 'suggest_diagnosis', 'line': 20}, 'file': 'examples/healthcare_assistant.py', 'line': 20, 'function': 'suggest_diagnosis', 'agent_name': 'suggest_diagnosis', 'agent_name_source': 'inferred_from_function', 'boundary_id': 'bnd:f35e574de35a4678'})
    try:
        _lineaje_model_evidence = _gr_client.enforce(_gr_site, _lineaje_model_evidence, content_type='application/json')
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        raise
    llm = ChatOpenAI(model="gpt-4o-mini")
    # Produces a diagnostic suggestion straight to the patient-facing summary
    # with no prior disclosure step that AI was used to generate it.
    # Policy Id: AI_IAC_025
    _lineaje_arg = f"Symptoms: {symptoms}\nImaging notes: {imaging_notes}\nSuggest a likely diagnosis."
    # LINEAJE: runtime guardrail checks `_lineaje_arg` as it flows from the agent to the LLM, before it is sent to the model (in suggest_diagnosis).
    #   Detected: this statement moves data from the agent to the LLM with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_AGENT_ACTIVITY_LOG, AI_APP_SEC_006, AI_APP_SEC_028, AI_APP_SEC_070 (+2 more); sensitive values in `_lineaje_arg` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:ae0fab00e87b21c8b260fdc4de65efe406143f17a015809fb63d53c394d4cc86'
    _lineaje__lineaje_arg_evidence = {'_lineaje_arg': _lineaje_arg, **(getattr(_lineaje_load_gr_client(), 'receiver_model', None) or (lambda o, p, f, s: {'model': f, 'model_source': s}))(llm, (), 'gpt-4o-mini', 'construction_literal')}
    _gr_client = _lineaje_load_gr_client()
    _lineaje_interaction_id = _gr_client.new_interaction_id()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:ae0fab00e87b21c8b260fdc4de65efe406143f17a015809fb63d53c394d4cc86', phase='pre_model', boundary={'source': 'agent_message', 'sink': 'model'}, fail_mode='BLOCK', source_type='agent', destination_type='llm', components={'destination': {'entity_type': 'llm', 'name': 'gpt-4o-mini', 'provider': 'openai', 'version': ''}, 'invocation': {'file': 'examples/healthcare_assistant.py', 'function': 'suggest_diagnosis', 'line': 24}, 'file': 'examples/healthcare_assistant.py', 'line': 24, 'function': 'suggest_diagnosis', 'agent_name': 'suggest_diagnosis', 'agent_name_source': 'inferred_from_function', 'boundary_id': 'bnd:cd7740526abe934c'}, interaction_id=_lineaje_interaction_id)
    try:
        _lineaje__lineaje_arg_evidence = _gr_client.enforce(_gr_site, _lineaje__lineaje_arg_evidence, content_type='application/json')
        _lineaje_arg = _lineaje__lineaje_arg_evidence.get('_lineaje_arg', _lineaje_arg) if isinstance(_lineaje__lineaje_arg_evidence, dict) else _lineaje_arg
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        raise
    return llm.invoke(
        _lineaje_arg
    ).content


def draft_treatment_plan(diagnosis: str, patient_history: str) -> str:
    """Draft a treatment plan recommendation for the clinician to review."""
    # LINEAJE: runtime guardrail checks the model this client is built with as it flows from the agent to the LLM, before it is sent to the model (in draft_treatment_plan).
    #   Detected: this statement moves data from the agent to the LLM with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_AGENT_ACTIVITY_LOG, AI_APP_SEC_006, AI_APP_SEC_028, AI_APP_SEC_070 (+1 more); a model that is not approved is refused before the client is built (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:bc01f1cb6653bdae51e044310b02ac47b63e5f1353fc133f05221d12f68907ce'
    _lineaje_model_evidence = {'model': 'gpt-4o-mini', 'client': 'ChatOpenAI', 'provider': 'langchain_openai', 'model_source': 'construction_literal', 'project': 'quivr'}
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:bc01f1cb6653bdae51e044310b02ac47b63e5f1353fc133f05221d12f68907ce', phase='pre_model', boundary={'source': 'agent_config', 'sink': 'model'}, fail_mode='BLOCK', source_type='agent', destination_type='llm', components={'destination': {'entity_type': 'llm', 'name': 'gpt-4o-mini', 'provider': 'openai', 'version': ''}, 'invocation': {'file': 'examples/healthcare_assistant.py', 'function': 'draft_treatment_plan', 'line': 31}, 'file': 'examples/healthcare_assistant.py', 'line': 31, 'function': 'draft_treatment_plan', 'agent_name': 'draft_treatment_plan', 'agent_name_source': 'inferred_from_function', 'boundary_id': 'bnd:16913be6cbdfdd4b'})
    try:
        _lineaje_model_evidence = _gr_client.enforce(_gr_site, _lineaje_model_evidence, content_type='application/json')
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        raise
    llm = ChatOpenAI(model="gpt-4o-mini")
    _lineaje_arg = f"Diagnosis: {diagnosis}\nHistory: {patient_history}\nDraft a treatment plan."
    # LINEAJE: runtime guardrail checks `_lineaje_arg` as it flows from the agent to the LLM, before it is sent to the model (in draft_treatment_plan).
    #   Detected: this statement moves data from the agent to the LLM with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_AGENT_ACTIVITY_LOG, AI_APP_SEC_006, AI_APP_SEC_028, AI_APP_SEC_070 (+2 more); sensitive values in `_lineaje_arg` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:41a3c0beabe30dd2963d7855bdcf82568a5358e5be3b38fd024ee0d003428b43'
    _lineaje__lineaje_arg_evidence = {'_lineaje_arg': _lineaje_arg, **(getattr(_lineaje_load_gr_client(), 'receiver_model', None) or (lambda o, p, f, s: {'model': f, 'model_source': s}))(llm, (), 'gpt-4o-mini', 'construction_literal')}
    _gr_client = _lineaje_load_gr_client()
    _lineaje_interaction_id = _gr_client.new_interaction_id()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:41a3c0beabe30dd2963d7855bdcf82568a5358e5be3b38fd024ee0d003428b43', phase='pre_model', boundary={'source': 'agent_message', 'sink': 'model'}, fail_mode='BLOCK', source_type='agent', destination_type='llm', components={'destination': {'entity_type': 'llm', 'name': 'gpt-4o-mini', 'provider': 'openai', 'version': ''}, 'invocation': {'file': 'examples/healthcare_assistant.py', 'function': 'draft_treatment_plan', 'line': 32}, 'file': 'examples/healthcare_assistant.py', 'line': 32, 'function': 'draft_treatment_plan', 'agent_name': 'draft_treatment_plan', 'agent_name_source': 'inferred_from_function', 'boundary_id': 'bnd:01f6ed9b443630b6'}, interaction_id=_lineaje_interaction_id)
    try:
        _lineaje__lineaje_arg_evidence = _gr_client.enforce(_gr_site, _lineaje__lineaje_arg_evidence, content_type='application/json')
        _lineaje_arg = _lineaje__lineaje_arg_evidence.get('_lineaje_arg', _lineaje_arg) if isinstance(_lineaje__lineaje_arg_evidence, dict) else _lineaje_arg
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        raise
    plan = llm.invoke(
        _lineaje_arg
    ).content
    # Returned as-is - no disclaimer noting the plan is AI-generated and that
    # a human clinician retains final decision authority over it.
    # Policy Id: AI_IAC_026
    # LINEAJE: runtime guardrail checks `plan` as it flows from the agent to the user interface, before it leaves the application (in draft_treatment_plan).
    #   Detected: this statement moves data from the agent to the user interface with no runtime policy check (detection confidence: high).
    #   Decision: the Guardrail evaluates AI_DAT_SEC_012; sensitive values in `plan` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:1a6cd559e67a5c6f86cfae72647ded2673c9a6ed1da47ae8b8943a410ab6cb9c'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:1a6cd559e67a5c6f86cfae72647ded2673c9a6ed1da47ae8b8943a410ab6cb9c', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'user_interface'}, fail_mode='BLOCK', source_type='agent', destination_type='user_interface', components={'invocation': {'file': 'examples/healthcare_assistant.py', 'line': 38, 'function': 'draft_treatment_plan'}, 'file': 'examples/healthcare_assistant.py', 'line': 38, 'function': 'draft_treatment_plan', 'agent_name': 'draft_treatment_plan', 'agent_name_source': 'inferred_from_function', 'not_on_graph': True})
    try:
        plan = _gr_client.enforce(_gr_site, plan, content_type='text/plain')
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        pass
    return plan


def sync_patient_record_to_analytics(patient_id: str, record: dict) -> None:
    """Forward the patient record to the analytics service for population health tracking."""
    # Patient record (which includes PII such as name/DOB/diagnosis) is
    # posted to the downstream service over plain HTTP with no
    # field-level or transport encryption of the PII payload.
    # Policy Id: AI_DAT_SEC_009
    requests.post(f"http://analytics.internal/patients/{patient_id}", json=record)
