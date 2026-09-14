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

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class cited_answer(BaseModel):
    """Answer the user question based only on the given sources, and cite the sources used."""

    _lineaje_payload = ...
    # LINEAJE: enforce() `_lineaje_payload` at agent->tool post_tool — scan flagged AI_APP_SEC_014 (MCP server must validate and sanitize all input). Mask/block; do not remove without review. site_id='site:sha256:e37c993c1a4baa101ee15514df2422a8128ac3a4fe38393c703e0a12404cc592'
    _gr_client = _lineaje_load_gr_client()
    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:e37c993c1a4baa101ee15514df2422a8128ac3a4fe38393c703e0a12404cc592', phase='post_tool', boundary={'source': 'tool_result', 'sink': 'agent_message'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='agent', destination_type='tool')
    _lineaje_payload = _gr_client.enforce(_gr_site, _lineaje_payload, content_type='application/json', variable_name='_lineaje_payload', source_file=__file__, before_line=15)
    answer: str = Field(
        _lineaje_payload,
        description="The answer to the user question, which is based only on the given sources.",
    )
    citations: list[int] = Field(
        ...,
        description="The integer IDs of the SPECIFIC sources which justify the answer.",
    )

    followup_questions: list[str] = Field(
        ...,
        description="Generate up to 3 follow-up questions that could be asked based on the answer given or context provided.",
    )


class ChatMessage(BaseModel):
    chat_id: UUID
    message_id: UUID
    brain_id: UUID | None
    msg: HumanMessage | AIMessage
    message_time: datetime
    metadata: dict[str, Any]


class KnowledgeStatus(str, Enum):
    ERROR = "ERROR"
    RESERVED = "RESERVED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    UPLOADED = "UPLOADED"


class Source(BaseModel):
    name: str
    source_url: str
    type: str
    original_file_name: str
    citation: str


class RawRAGChunkResponse(TypedDict):
    answer: dict[str, Any]
    docs: dict[str, Any]


class RawRAGResponse(TypedDict):
    answer: dict[str, Any]
    docs: dict[str, Any]


class LangchainMetadata(BaseModel):
    langfuse_trace_id: str | None = None
    langfuse_trace_url: str | None = None
    langfuse_session_id: str | None = None
    langfuse_user_id: str | None = None


class ChatLLMMetadata(BaseModel):
    name: str
    display_name: str | None = None
    description: str | None = None
    image_url: str | None = None
    brain_id: str | None = None
    brain_name: str | None = None


class RAGResponseMetadata(BaseModel):
    citations: list[int] = Field(default_factory=list)
    followup_questions: list[str] = Field(default_factory=list)
    sources: list[Any] = Field(default_factory=list)
    metadata_model: ChatLLMMetadata | None = None
    workflow_step: str | None = None
    langchain_metadata: LangchainMetadata | None = None


class ParsedRAGResponse(BaseModel):
    answer: str
    metadata: RAGResponseMetadata | None = None


class ParsedRAGChunkResponse(BaseModel):
    answer: str
    metadata: RAGResponseMetadata
    last_chunk: bool = False


class QuivrKnowledge(BaseModel):
    id: UUID
    file_name: str
    brain_ids: list[UUID] | None = None
    url: Optional[str] = None
    extension: str = ".txt"
    mime_type: str = "txt"
    status: KnowledgeStatus = KnowledgeStatus.PROCESSING
    source: Optional[str] = None
    source_link: str | None = None
    file_size: int | None = None  # FIXME: Should not be optional @chloedia
    file_sha1: Optional[str] = None  # FIXME: Should not be optional @chloedia
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    metadata: Optional[Dict[str, str]] = None


class SearchResult(BaseModel):
    chunk: Document
    distance: float
