"""Prototype clinical assistant: answers patient questions and drafts
treatment suggestions from a patient's chart for the reviewing clinician.
"""

import requests
from langchain_openai import ChatOpenAI


def chat_with_patient(message: str) -> str:
    """Respond to a patient's message in the portal chat widget."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    # The reply goes straight back to the patient with no disclosure that
    # they are talking to an AI system rather than clinic staff.
    return llm.invoke(f"You are a friendly clinic assistant. Patient asks: {message}").content


def suggest_diagnosis(symptoms: str, imaging_notes: str) -> str:
    """Draft a diagnostic suggestion from reported symptoms and imaging notes."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    # Produces a diagnostic suggestion straight to the patient-facing summary
    # with no prior disclosure step that AI was used to generate it.
    return llm.invoke(
        f"Symptoms: {symptoms}\nImaging notes: {imaging_notes}\nSuggest a likely diagnosis."
    ).content


def draft_treatment_plan(diagnosis: str, patient_history: str) -> str:
    """Draft a treatment plan recommendation for the clinician to review."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    plan = llm.invoke(
        f"Diagnosis: {diagnosis}\nHistory: {patient_history}\nDraft a treatment plan."
    ).content
    # Returned as-is - no disclaimer noting the plan is AI-generated and that
    # a human clinician retains final decision authority over it.
    return plan


def sync_patient_record_to_analytics(patient_id: str, record: dict) -> None:
    """Forward the patient record to the analytics service for population health tracking."""
    # Patient record (which includes PII such as name/DOB/diagnosis) is
    # posted to the downstream service over plain HTTP with no
    # field-level or transport encryption of the PII payload.
    requests.post(f"http://analytics.internal/patients/{patient_id}", json=record)
