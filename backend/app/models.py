from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class AnalysisCounts(BaseModel):
    words: int = 0
    characters: int = 0
    equations: int = 0
    numbers: int = 0
    units: int = 0
    codeBlocks: int = 0
    citations: int = 0
    technicalTerms: int = 0

class ElementDetail(BaseModel):
    type: str # 'equation', 'number', 'unit', 'code', 'citation', 'term'
    value: str
    placeholder: Optional[str] = None
    preserved: Optional[bool] = None

class ValidationCategory(BaseModel):
    original: int = 0
    preserved: int = 0

class ValidationResult(BaseModel):
    integrityScore: float = 100.0
    equations: ValidationCategory = Field(default_factory=ValidationCategory)
    numbers: ValidationCategory = Field(default_factory=ValidationCategory)
    units: ValidationCategory = Field(default_factory=ValidationCategory)
    codeBlocks: ValidationCategory = Field(default_factory=ValidationCategory)
    citations: ValidationCategory = Field(default_factory=ValidationCategory)
    technicalTerms: ValidationCategory = Field(default_factory=ValidationCategory)

class TranslateRequest(BaseModel):
    content: str
    format: str = "markdown" # 'markdown', 'latex', 'plain'
    sourceLanguage: str = "en"
    targetLanguage: str = "hi"
    mode: str = "academic" # 'academic', 'student_friendly', 'bilingual'
    tone: str = "academic" # 'academic', 'gen_z', 'corporate', 'empathetic'
    customGlossary: Optional[Dict[str, str]] = None

class TranslateResponse(BaseModel):
    status: str = "success" # 'success', 'warning', 'error'
    translatedContent: str
    originalContent: str
    mode: str
    tone: str = "academic"
    sourceLanguage: str
    targetLanguage: str
    analysis: AnalysisCounts
    validation: ValidationResult
    details: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    protectedContentPreview: Optional[str] = None

class AnalyzeRequest(BaseModel):
    content: str
    format: str = "markdown"

class AnalyzeResponse(BaseModel):
    status: str = "success"
    analysis: AnalysisCounts
    elements: List[ElementDetail] = Field(default_factory=list)

class GlossaryItem(BaseModel):
    id: Optional[str] = None
    sourceTerm: str
    targetTerm: str
    language: str = "hi"
    isStrict: bool = True
    category: Optional[str] = "general"

class CorruptionTestRequest(BaseModel):
    content: str = "Newton's second law states that F = ma with acceleration 9.81 m/s^2."
    corruptedValue: str = "9.18"
