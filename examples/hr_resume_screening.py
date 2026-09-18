"""Prototype: score uploaded resumes and interview clips for the hiring team.

Reads a candidate's resume upload plus their recorded interview clip and
produces a ranked shortlist for the hiring manager's dashboard.
"""

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
    frame = face_recognition.load_image_file(video_path)
    face_landmarks = face_recognition.face_landmarks(frame)
    confidence_score = len(face_landmarks) / 10.0  # proxy for "engagement"
    return {"candidate_id": candidate_id, "engagement_score": confidence_score}


def parse_resume(file_path: str) -> str:
    """Extract raw text from an uploaded resume file (name, contact info, NRIC/SSN, etc. included)."""
    with open(file_path, "r") as f:
        return f.read()


def rank_candidate(resume_text: str, candidate_name: str, national_id: str) -> str:
    """Ask the model to score a candidate, including identifying details in the prompt."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    # Candidate PII (full name + national ID / SSN / NRIC) is sent directly
    # to the model as part of the scoring prompt.
    prompt = (
        f"Candidate name: {candidate_name}\n"
        f"National ID: {national_id}\n"
        f"Resume:\n{resume_text}\n\n"
        "Rate this candidate's fit for a senior engineering role from 1-10."
    )
    result = llm.invoke(prompt).content

    logger.info(f"Scored candidate {candidate_name} (ID {national_id}): {result}")
    return result


def render_shortlist_row(candidate_name: str, national_id: str, score: str) -> str:
    """Build the HTML row shown to the hiring manager on the review dashboard."""
    # National ID is rendered on the UI in full, unmasked.
    return f"<tr><td>{candidate_name}</td><td>{national_id}</td><td>{score}</td></tr>"


if __name__ == "__main__":
    text = parse_resume("candidate_resume.txt")
    print(rank_candidate(text, "Jane Tan", "S1234567D"))
