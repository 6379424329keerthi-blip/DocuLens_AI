from typing import List, Dict, Optional, Any

try:
    from pydantic import BaseModel, Field, model_validator
    
    class DocumentChunk(BaseModel):
        content: str = ""
        page_number: int = 1
        chunk_type: str = "text"  # text, table, chart, image
        document_name: str = ""
        metadata: Dict[str, Any] = Field(default_factory=dict)

        @model_validator(mode="before")
        @classmethod
        def handle_aliases(cls, data: Any) -> Any:
            if isinstance(data, dict):
                if "text" in data and "content" not in data:
                    data["content"] = data["text"]
                if "page" in data and "page_number" not in data:
                    data["page_number"] = data["page"]
                if "document" in data and "document_name" not in data:
                    data["document_name"] = data["document"]
            return data

        @property
        def text(self) -> str:
            return self.content

        @property
        def page(self) -> int:
            return self.page_number

        @property
        def document(self) -> str:
            return self.document_name


    class Evidence(BaseModel):
        document: str = ""
        page: int = 1
        evidence_type: str = "text"  # text, table, chart, image
        content: str = ""
        relevance_score: float = 0.0
        description: Optional[str] = None

        @model_validator(mode="before")
        @classmethod
        def handle_aliases(cls, data: Any) -> Any:
            if isinstance(data, dict):
                if "document_name" in data and "document" not in data:
                    data["document"] = data["document_name"]
                if "page_number" in data and "page" not in data:
                    data["page"] = data["page_number"]
                if "content_snippet" in data and "content" not in data:
                    data["content"] = data["content_snippet"]
            return data

        @property
        def document_name(self) -> str:
            return self.document

        @property
        def page_number(self) -> int:
            return self.page

        @property
        def content_snippet(self) -> str:
            return self.content


    class AnswerResponse(BaseModel):
        answer: str = ""
        confidence: float = 0.0
        grounded: bool = False
        evidence: List[Evidence] = Field(default_factory=list)
        reasoning: Optional[str] = None
        cited_pages: List[int] = Field(default_factory=list)
        answer_type: Optional[str] = None

        @model_validator(mode="before")
        @classmethod
        def handle_aliases(cls, data: Any) -> Any:
            if isinstance(data, dict):
                if "answer_text" in data and "answer" not in data:
                    data["answer"] = data["answer_text"]
            return data

        @property
        def answer_text(self) -> str:
            return self.answer


    class ProcessedDocument(BaseModel):
        document_name: str
        total_pages: int = 0
        chunks: List[DocumentChunk] = Field(default_factory=list)
        page_images: Dict[int, str] = Field(default_factory=dict)
        tables: List[DocumentChunk] = Field(default_factory=list)
        processing_time: float = 0.0

except ImportError:
    # Standard library fallback when pydantic is not installed
    class DocumentChunk:
        def __init__(self, content: str = "", page_number: int = 1, chunk_type: str = "text",
                     document_name: str = "", metadata: Optional[Dict[str, Any]] = None, **kwargs):
            self.content = content or kwargs.get("text", "")
            self.page_number = page_number or kwargs.get("page", 1)
            self.chunk_type = chunk_type
            self.document_name = document_name or kwargs.get("document", "")
            self.metadata = metadata or {}
        
        @property
        def text(self) -> str:
            return self.content
        @property
        def page(self) -> int:
            return self.page_number
        @property
        def document(self) -> str:
            return self.document_name

    class Evidence:
        def __init__(self, document: str = "", page: int = 1, evidence_type: str = "text",
                     content: str = "", relevance_score: float = 0.0, description: Optional[str] = None, **kwargs):
            self.document = document or kwargs.get("document_name", "")
            self.page = page or kwargs.get("page_number", 1)
            self.evidence_type = evidence_type
            self.content = content or kwargs.get("content_snippet", "")
            self.relevance_score = float(relevance_score)
            self.description = description

        @property
        def document_name(self) -> str:
            return self.document
        @property
        def page_number(self) -> int:
            return self.page
        @property
        def content_snippet(self) -> str:
            return self.content

    class AnswerResponse:
        def __init__(self, answer: str = "", confidence: float = 0.0, grounded: bool = False,
                     evidence: Optional[List[Evidence]] = None, reasoning: Optional[str] = None,
                     cited_pages: Optional[List[int]] = None, answer_type: Optional[str] = None, **kwargs):
            self.answer = answer or kwargs.get("answer_text", "")
            self.confidence = float(confidence)
            self.grounded = bool(grounded)
            self.evidence = evidence or []
            self.reasoning = reasoning
            self.cited_pages = cited_pages or []
            self.answer_type = answer_type

        @property
        def answer_text(self) -> str:
            return self.answer

    class ProcessedDocument:
        def __init__(self, document_name: str, total_pages: int = 0,
                     chunks: Optional[List[DocumentChunk]] = None,
                     page_images: Optional[Dict[int, str]] = None,
                     tables: Optional[List[DocumentChunk]] = None,
                     processing_time: float = 0.0, **kwargs):
            self.document_name = document_name
            self.total_pages = total_pages
            self.chunks = chunks or []
            self.page_images = page_images or {}
            self.tables = tables or []
            self.processing_time = float(processing_time)
