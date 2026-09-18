"""Prototype clinical assistant: answers patient questions and drafts
treatment suggestions from a patient's chart for the reviewing clinician.
"""
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


import requests
from langchain_openai import ChatOpenAI


def chat_with_patient(message: str) -> str:
    """Respond to a patient's message in the portal chat widget."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    # The reply goes straight back to the patient with no disclosure that
    # they are talking to an AI system rather than clinic staff.
    # Policy Id: AI_IAC_023
    _lineaje_payload = f"You are a friendly clinic assistant. Patient asks: {message}"
    # LINEAJE: enforce() `_lineaje_payload` at agent->llm pre_model — scan flagged AI_APP_SEC_014 (MCP server must validate and sanitize all input); AI_APP_SEC_038 (The AI Model must validate and sanitize any input before processing.); AI_APP_SEC_039 (Sanitize and validate all input to the AI Model.). Mask/block; do not remove without review. site_id='site:sha256:42613912a86adcd2c3eca0a717a1d4883d44f6305341fcd1cd38eefceb475be6'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:42613912a86adcd2c3eca0a717a1d4883d44f6305341fcd1cd38eefceb475be6', phase='pre_model', boundary={'source': 'agent_message', 'sink': 'model'}, candidate_policies=[{'policy_id': 'AI_APP_SEC_006', 'guardrail_id': 'Enforce Approved LLM.', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_APP_SEC_028', 'guardrail_id': 'Enforce Approved LLM', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_DAT_SEC_029', 'guardrail_id': 'Emit immutable, forensic-ready audit records for all AI decisions.', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_APP_SEC_014', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_APP_SEC_038', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_APP_SEC_039', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_APP_SEC_059', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_APP_SEC_067', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_023', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_025', 'guardrail_id': None, 'policy_version': None}], fail_mode='BLOCK', source_type='agent', destination_type='llm')
    _lineaje_payload = _gr_client.enforce(_gr_site, _lineaje_payload, content_type='application/json', variable_name='_lineaje_payload', source_file=__file__, before_line=15)
    return llm.invoke(_lineaje_payload).content


def suggest_diagnosis(symptoms: str, imaging_notes: str) -> str:
    """Draft a diagnostic suggestion from reported symptoms and imaging notes."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    # Produces a diagnostic suggestion straight to the patient-facing summary
    # with no prior disclosure step that AI was used to generate it.
    # Policy Id: AI_IAC_025
    _lineaje_payload = f"Symptoms: {symptoms}\nImaging notes: {imaging_notes}\nSuggest a likely diagnosis."
    # LINEAJE: enforce() `_lineaje_payload` at agent->llm pre_model — scan flagged AI_APP_SEC_006 (Use only LLMs from the organization's approved list.); AI_APP_SEC_038 (The AI Model must validate and sanitize any input before processing.); AI_APP_SEC_039 (Sanitize and validate all input to the AI Model.). Mask/block; do not remove without review. site_id='site:sha256:6f3e356647de42f4421b55d027ca3b8d2989405124990a3c2e2aeac4fbe70b35'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:6f3e356647de42f4421b55d027ca3b8d2989405124990a3c2e2aeac4fbe70b35', phase='pre_model', boundary={'source': 'agent_message', 'sink': 'model'}, candidate_policies=[{'policy_id': 'AI_APP_SEC_006', 'guardrail_id': 'Enforce Approved LLM.', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_APP_SEC_028', 'guardrail_id': 'Enforce Approved LLM', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_DAT_SEC_029', 'guardrail_id': 'Emit immutable, forensic-ready audit records for all AI decisions.', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_APP_SEC_038', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_APP_SEC_039', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_APP_SEC_059', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_APP_SEC_067', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_DAT_SEC_009', 'guardrail_id': 'Encrypt PII in Transit', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_DAT_SEC_011', 'guardrail_id': 'Redact PII', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_IAC_015', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_018', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_023', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_025', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_DAT_SEC_027', 'guardrail_id': 'Minimise and redact all outbound AI outputs.', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_IAC_026', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_031', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_SEC_020', 'guardrail_id': None, 'policy_version': None}], fail_mode='BLOCK', source_type='agent', destination_type='llm')
    _lineaje_payload = _gr_client.enforce(_gr_site, _lineaje_payload, content_type='application/json', variable_name='_lineaje_payload', source_file=__file__, before_line=24)
    return llm.invoke(
        _lineaje_payload
    ).content


def draft_treatment_plan(diagnosis: str, patient_history: str) -> str:
    """Draft a treatment plan recommendation for the clinician to review."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    _lineaje_payload = f"Diagnosis: {diagnosis}\nHistory: {patient_history}\nDraft a treatment plan."
    # LINEAJE: enforce() `_lineaje_payload` at agent->llm pre_model — scan flagged AI_APP_SEC_006 (Use only LLMs from the organization's approved list.); AI_APP_SEC_038 (The AI Model must validate and sanitize any input before processing.); AI_APP_SEC_039 (Sanitize and validate all input to the AI Model.). Mask/block; do not remove without review. site_id='site:sha256:edaab65ede4fd55ec1ed93fa4ea1e452f722bde4c62911784938c459b607b116'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:edaab65ede4fd55ec1ed93fa4ea1e452f722bde4c62911784938c459b607b116', phase='pre_model', boundary={'source': 'agent_message', 'sink': 'model'}, candidate_policies=[{'policy_id': 'AI_APP_SEC_006', 'guardrail_id': 'Enforce Approved LLM.', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_APP_SEC_028', 'guardrail_id': 'Enforce Approved LLM', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_DAT_SEC_029', 'guardrail_id': 'Emit immutable, forensic-ready audit records for all AI decisions.', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_APP_SEC_038', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_APP_SEC_039', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_APP_SEC_059', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_APP_SEC_067', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_DAT_SEC_009', 'guardrail_id': 'Encrypt PII in Transit', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_DAT_SEC_011', 'guardrail_id': 'Redact PII', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_IAC_015', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_018', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_023', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_025', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_DAT_SEC_027', 'guardrail_id': 'Minimise and redact all outbound AI outputs.', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_IAC_026', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_031', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_IAC_SEC_020', 'guardrail_id': None, 'policy_version': None}], fail_mode='BLOCK', source_type='agent', destination_type='llm')
    _lineaje_payload = _gr_client.enforce(_gr_site, _lineaje_payload, content_type='application/json', variable_name='_lineaje_payload', source_file=__file__, before_line=32)
    plan = llm.invoke(
        _lineaje_payload
    ).content
    # Returned as-is - no disclaimer noting the plan is AI-generated and that
    # a human clinician retains final decision authority over it.
    # Policy Id: AI_IAC_026
    # LINEAJE: enforce() `plan` at agent->user_interface data_egress — scan flagged AI_IAC_026 (AI clinical recommendations must disclose that human clinicians retain final decision authority). Mask/block; do not remove without review. site_id='site:sha256:1a6cd559e67a5c6f86cfae72647ded2673c9a6ed1da47ae8b8943a410ab6cb9c'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:1a6cd559e67a5c6f86cfae72647ded2673c9a6ed1da47ae8b8943a410ab6cb9c', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'user_interface'}, candidate_policies=[{'policy_id': 'AI_DAT_SEC_012', 'guardrail_id': 'Mask PII on UI', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_IAC_026', 'guardrail_id': None, 'policy_version': None}], fail_mode='BLOCK', source_type='agent', destination_type='user_interface')
    plan = _gr_client.enforce(_gr_site, plan, content_type='text/plain')
    return plan


def sync_patient_record_to_analytics(patient_id: str, record: dict) -> None:
    """Forward the patient record to the analytics service for population health tracking."""
    # Patient record (which includes PII such as name/DOB/diagnosis) is
    # posted to the downstream service over plain HTTP with no
    # field-level or transport encryption of the PII payload.
    # Policy Id: AI_DAT_SEC_009
    requests.post(f"http://analytics.internal/patients/{patient_id}", json=record)
