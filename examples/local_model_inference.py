"""Prototype: run a locally-hosted HF model for quick classification/generation
requests from an internal API handler, without routing through the main
quivr_core LLM abstraction.
"""

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
    output_ids = model.generate(input_ids, max_new_tokens=64)
    completion = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return jsonify({"completion": completion})


if __name__ == "__main__":
    app.run(port=5005)
