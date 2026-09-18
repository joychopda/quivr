"""Prototype: run a locally-hosted HF model for quick classification/generation
requests from an internal API handler, without routing through the main
quivr_core LLM abstraction.
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


from flask import Flask, jsonify, request
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")


@app.route("/local-generate", methods=["POST"])
def generate_completion():
    """Take a raw request body field and generate a completion from it."""
    user_text = request.json.get("prompt", "")

    # The request body's `prompt` field is fed straight into the tokenizer
    # and the model's generate() call with no validation or sanitization of
    # its contents beforehand.
    # Policy Id: AI_APP_SEC_038
    input_ids = tokenizer(user_text, return_tensors="pt").input_ids
    # LINEAJE: enforce() `input_ids` at agent->llm pre_model — scan flagged AI_APP_SEC_039 (Sanitize and validate all input to the AI Model.). Mask/block; do not remove without review. site_id='site:sha256:bbda9c3cd514dfb1156d96fb7c8104a363d8a820b33da43fa7a7c80c6d23fe51'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:bbda9c3cd514dfb1156d96fb7c8104a363d8a820b33da43fa7a7c80c6d23fe51', phase='pre_model', boundary={'source': 'agent_message', 'sink': 'model'}, candidate_policies=[{'policy_id': 'AI_APP_SEC_006', 'guardrail_id': 'Enforce Approved LLM.', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_APP_SEC_028', 'guardrail_id': 'Enforce Approved LLM', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_DAT_SEC_029', 'guardrail_id': 'Emit immutable, forensic-ready audit records for all AI decisions.', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_APP_SEC_039', 'guardrail_id': None, 'policy_version': None}], fail_mode='BLOCK', source_type='agent', destination_type='llm')
    input_ids = _gr_client.enforce(_gr_site, input_ids, content_type='application/json', variable_name='input_ids', source_file=__file__, before_line=25)
    output_ids = model.generate(input_ids, max_new_tokens=64)
    completion = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    _lineaje_payload = {"completion": completion}
    # LINEAJE: enforce() `_lineaje_payload` at agent->user_interface data_egress — scan flagged AI_DAT_SEC_012 (Mask PII on user interfaces); AI_IAC_023 (Chatbot and AI interfaces must disclose AI identity to the user); AI_DAT_SEC_027 (Enforce output data minimization for model, tool, and API responses.). Mask/block; do not remove without review. site_id='site:sha256:4ec4e41baa76955ac80cafbe93e7ab09898c7f5be95149fe59c2a0ca3671408f'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:4ec4e41baa76955ac80cafbe93e7ab09898c7f5be95149fe59c2a0ca3671408f', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'user_interface'}, candidate_policies=[{'policy_id': 'AI_DAT_SEC_012', 'guardrail_id': 'Mask PII on UI', 'policy_version': '2026.08.1'}, {'policy_id': 'AI_IAC_023', 'guardrail_id': None, 'policy_version': None}, {'policy_id': 'AI_DAT_SEC_027', 'guardrail_id': 'Minimise and redact all outbound AI outputs.', 'policy_version': '2026.08.1'}], fail_mode='BLOCK', source_type='agent', destination_type='user_interface')
    _lineaje_payload = _gr_client.enforce(_gr_site, _lineaje_payload, content_type='text/plain')
    return jsonify(_lineaje_payload)


if __name__ == "__main__":
    app.run(port=5005)
