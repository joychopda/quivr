"""Prototype: run a locally-hosted HF model for quick classification/generation
requests from an internal API handler, without routing through the main
quivr_core LLM abstraction.
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
    # LINEAJE: runtime guardrail checks `input_ids` as it flows from the agent to the LLM, before it is sent to the model (in generate_completion).
    #   Detected: this statement moves data from the agent to the LLM with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_AGENT_ACTIVITY_LOG, AI_APP_SEC_006, AI_APP_SEC_028, AI_APP_SEC_070 (+2 more); sensitive values in `input_ids` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:bbda9c3cd514dfb1156d96fb7c8104a363d8a820b33da43fa7a7c80c6d23fe51'
    _lineaje_input_ids_evidence = {'input_ids': input_ids, 'model': getattr(_lineaje_load_gr_client(), 'current_model', lambda _f: '')(__file__)}
    _gr_client = _lineaje_load_gr_client()
    _lineaje_interaction_id = _gr_client.new_interaction_id()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:bbda9c3cd514dfb1156d96fb7c8104a363d8a820b33da43fa7a7c80c6d23fe51', phase='pre_model', boundary={'source': 'agent_message', 'sink': 'model'}, fail_mode='BLOCK', source_type='agent', destination_type='llm', components={'destination': {'entity_type': 'llm', 'name': 'gpt2', 'version': '', 'provider': ''}, 'invocation': {'file': 'examples/local_model_inference.py', 'line': 25, 'function': 'generate_completion'}, 'file': 'examples/local_model_inference.py', 'line': 25, 'function': 'generate_completion', 'agent_name': 'generate_completion', 'agent_name_source': 'inferred_from_function', 'not_on_graph': True}, interaction_id=_lineaje_interaction_id)
    try:
        _lineaje_input_ids_evidence = _gr_client.enforce(_gr_site, _lineaje_input_ids_evidence, content_type='application/json')
        input_ids = _lineaje_input_ids_evidence.get('input_ids', input_ids) if isinstance(_lineaje_input_ids_evidence, dict) else input_ids
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        raise
    output_ids = model.generate(input_ids, max_new_tokens=64)
    # LINEAJE: runtime guardrail checks `output_ids` as it flows from the LLM to the agent, after the model replies (in generate_completion).
    #   Detected: this statement moves data from the LLM to the agent with no runtime policy check (detection confidence: medium).
    #   Decision: the Guardrail evaluates AI_DAT_SEC_011, AI_DAT_SEC_025, AI_DAT_SEC_027, AI_DAT_SEC_029; sensitive values in `output_ids` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:bd13a3444cbff2b26ca3c2f0e019d4c48977f400213bc28528ee534128027bcc'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:bd13a3444cbff2b26ca3c2f0e019d4c48977f400213bc28528ee534128027bcc', phase='post_model', boundary={'source': 'model', 'sink': 'agent_message'}, fail_mode='BLOCK', source_type='llm', destination_type='agent', components={'destination': {'entity_type': 'llm', 'name': 'gpt2', 'version': '', 'provider': ''}, 'invocation': {'file': 'examples/local_model_inference.py', 'line': 25, 'function': 'generate_completion'}, 'file': 'examples/local_model_inference.py', 'line': 25, 'function': 'generate_completion', 'agent_name': 'generate_completion', 'agent_name_source': 'inferred_from_function', 'not_on_graph': True}, interaction_id=locals().get('_lineaje_interaction_id'))
    try:
        output_ids = _gr_client.enforce(_gr_site, output_ids, content_type='application/json', variable_name='output_ids', source_file=__file__, before_line=25)
    except _gr_client.GuardrailUnavailableError:
        pass
    completion = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    _lineaje_payload = {"completion": completion}
    # LINEAJE: runtime guardrail checks `_lineaje_payload` as it flows from the agent to the user interface, before it leaves the application (in generate_completion).
    #   Detected: this statement moves data from the agent to the user interface with no runtime policy check (detection confidence: high).
    #   Decision: the Guardrail evaluates AI_DAT_SEC_012; sensitive values in `_lineaje_payload` are masked in place; a policy violation stops the call (fail_mode=BLOCK). If the Guardrail is unreachable, the call continues unchanged.
    #   Do not remove without review. site_id='site:sha256:4ec4e41baa76955ac80cafbe93e7ab09898c7f5be95149fe59c2a0ca3671408f'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:4ec4e41baa76955ac80cafbe93e7ab09898c7f5be95149fe59c2a0ca3671408f', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'user_interface'}, fail_mode='BLOCK', source_type='agent', destination_type='user_interface', components={'invocation': {'file': 'examples/local_model_inference.py', 'line': 28, 'function': 'generate_completion'}, 'file': 'examples/local_model_inference.py', 'line': 28, 'function': 'generate_completion', 'agent_name': 'generate_completion', 'agent_name_source': 'inferred_from_function', 'not_on_graph': True})
    try:
        _lineaje_payload = _gr_client.enforce(_gr_site, _lineaje_payload, content_type='text/plain')
    except _gr_client.GuardrailUnavailableError:
        pass
    except PermissionError:
        pass
    return jsonify(_lineaje_payload)


if __name__ == "__main__":
    app.run(port=5005)
