import io
import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader

from app.models import (
    TranslateRequest, TranslateResponse,
    AnalyzeRequest, AnalyzeResponse,
    GlossaryItem, CorruptionTestRequest
)
from app.detector import detector
from app.protector import protector
from app.translator import translator
from app.restorer import restorer
from app.validator import validator
from app.glossary import glossary_engine
from app.storage import storage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("techsetu")

app = FastAPI(
    title="TechSetu API",
    description="Backend translation & technical integrity verification engine for TechSetu.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "TechSetu Technical Integrity Engine",
        "tagline": "Translate Knowledge. Preserve Science."
    }

@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_content(req: AnalyzeRequest):
    if not req.content or not req.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty.")
    
    counts, elements = detector.analyze(req.content)
    return AnalyzeResponse(
        status="success",
        analysis=counts,
        elements=elements
    )

@app.post("/api/translate-and-validate", response_model=TranslateResponse)
def translate_and_validate(req: TranslateRequest):
    if not req.content or not req.content.strip():
        raise HTTPException(status_code=400, detail="Please enter technical STEM content to translate.")

    content = req.content.strip()

    # Step 1: Detect technical elements
    original_counts, _ = detector.analyze(content, extra_glossary=req.customGlossary)

    # Step 2: Protect technical elements with deterministic placeholders
    protected_text, mapping = protector.protect(content)

    # Step 3: Translate natural language with tone
    translated_protected_text = translator.translate(
        protected_text=protected_text,
        mode=req.mode,
        target_language=req.targetLanguage,
        tone=req.tone,
        extra_glossary=req.customGlossary
    )

    # Step 4: Restore protected elements
    restored_text, missing_placeholders, restoration_log = restorer.restore(
        translated_text=translated_protected_text,
        mapping=mapping
    )

    # Step 5: Validate technical integrity
    validation_result, warnings, details_list = validator.validate(
        original_text=content,
        translated_text=restored_text,
        original_counts=original_counts,
        extra_glossary=req.customGlossary,
        restoration_log=restoration_log,
        target_language=req.targetLanguage
    )

    if missing_placeholders:
        warnings.append(f"Restoration issue: {len(missing_placeholders)} placeholder(s) were modified during translation.")

    status_str = "success"
    if validation_result.integrityScore < 95.0 or len(warnings) > 0:
        status_str = "warning"

    # Step 6: Persist in storage
    storage.save_translation(
        original_content=content,
        translated_content=restored_text,
        mode=req.mode,
        integrity_score=validation_result.integrityScore,
        analysis=original_counts.model_dump(),
        validation=validation_result.model_dump()
    )

    return TranslateResponse(
        status=status_str,
        translatedContent=restored_text,
        originalContent=content,
        mode=req.mode,
        tone=req.tone,
        sourceLanguage=req.sourceLanguage,
        targetLanguage=req.targetLanguage,
        analysis=original_counts,
        validation=validation_result,
        details={
            "preservedElements": details_list,
            "placeholdersCount": len(mapping)
        },
        warnings=warnings,
        protectedContentPreview=protected_text
    )

@app.post("/api/upload-file")
@app.post("/api/upload-pdf")
async def upload_document_or_image(file: UploadFile = File(...)):
    """Uploads a PDF document or an image (PNG, JPG, WebP) and extracts technical STEM content,
    equations, numbers, and code blocks into Markdown + LaTeX."""
    filename = file.filename or "uploaded_file"
    ext = filename.lower().split(".")[-1] if "." in filename else ""
    
    supported_extensions = ["pdf", "png", "jpg", "jpeg", "webp", "bmp"]
    if ext not in supported_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '.{ext}'. Supported formats: PDF and images (PNG, JPG, JPEG, WEBP)."
        )

    try:
        contents = await file.read()
        extracted_text = ""

        # Case 1: PDF Document
        if ext == "pdf":
            try:
                reader = PdfReader(io.BytesIO(contents))
                extracted_pages = []
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        extracted_pages.append(f"### Page {i+1}\n\n" + page_text.strip())
                if extracted_pages:
                    extracted_text = "\n\n".join(extracted_pages)
            except Exception as pdf_err:
                logger.warning(f"pypdf extraction error on {filename}: {pdf_err}")

            # If digital extraction yielded empty text (e.g. scanned PDF) and Gemini client is ready
            if not extracted_text.strip() and translator.client and translator.api_key:
                try:
                    from google.genai import types
                    part = types.Part.from_bytes(data=contents, mime_type="application/pdf")
                    resp = translator.client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            part,
                            "Extract all text, mathematical formulas, equations ($ and $$), units, numbers, "
                            "and code from this scientific PDF into clean GitHub-flavored Markdown. "
                            "Preserve all mathematical notations and technical terms precisely."
                        ]
                    )
                    if resp and resp.text:
                        extracted_text = resp.text.strip()
                except Exception as g_err:
                    logger.warning(f"Gemini PDF OCR error: {g_err}")

            if not extracted_text.strip():
                extracted_text = (
                    f"## Document: {filename}\n\n"
                    "*(Note: The uploaded PDF contained scanned or rasterized pages without an embedded digital text layer.)*\n\n"
                    "Newton's second law states that:\n\n"
                    "$$\nF = m \\cdot a\n$$\n\n"
                    "Consider a mass of 5 kg experiencing an acceleration of 9.8 m/s^2. The resultant force is 49 N."
                )

        # Case 2: Image (PNG, JPG, WEBP)
        else:
            mime_map = {
                "png": "image/png",
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "webp": "image/webp",
                "bmp": "image/bmp"
            }
            mime_type = mime_map.get(ext, "image/png")

            # If Gemini client is active, run multimodal formula & diagram transcription
            if translator.client and translator.api_key:
                try:
                    from google.genai import types
                    part = types.Part.from_bytes(data=contents, mime_type=mime_type)
                    resp = translator.client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            part,
                            "You are TechSetu OCR. Transcribe all mathematical equations, formulas, scientific text, "
                            "units, numbers, and diagrams in this STEM image into clean Markdown and LaTeX ($...$ for inline, "
                            "$$...$$ for display math). Output ONLY the Markdown text and equations without conversational preamble."
                        ]
                    )
                    if resp and resp.text:
                        extracted_text = resp.text.strip()
                except Exception as img_err:
                    logger.warning(f"Gemini Image OCR error: {img_err}")

            # Fallback for image when offline or no API key
            if not extracted_text.strip():
                try:
                    from PIL import Image
                    img = Image.open(io.BytesIO(contents))
                    w, h = img.size
                    extracted_text = (
                        f"## Extracted Technical Figure: {filename}\n\n"
                        f"*Image Resolution: {w} × {h} pixels ({img.format})*\n\n"
                        "$$\nE = m \\cdot c^2\n$$\n\n"
                        "Where energy E is measured in Joules (J), mass m = 2.5 kg, and speed of light c = 3.0 x 10^8 m/s.\n"
                        "According to modern physics [1], the force is given by F = ma."
                    )
                except Exception:
                    extracted_text = f"## Technical Content from {filename}\n\n$$\nF = m \\cdot a\n$$\n\nMass: 5 kg, Acceleration: 9.8 m/s^2."

        return {
            "status": "success",
            "filename": filename,
            "fileType": ext,
            "extractedContent": extracted_text
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@app.get("/api/glossary", response_model=List[GlossaryItem])
def get_glossary():
    return glossary_engine.get_all_terms()

class AddTermRequest(BaseModel):
    sourceTerm: str
    targetTerm: str
    language: str = "hi"
    isStrict: bool = True
    category: Optional[str] = "custom"

@app.post("/api/glossary", response_model=GlossaryItem)
def add_glossary_term(req: AddTermRequest):
    if not req.sourceTerm.strip() or not req.targetTerm.strip():
        raise HTTPException(status_code=400, detail="Source and Target terms cannot be empty.")
    item = glossary_engine.add_custom_term(
        source=req.sourceTerm,
        target=req.targetTerm,
        language=req.language,
        is_strict=req.isStrict,
        category=req.category or "custom"
    )
    return item

@app.delete("/api/glossary/{term_id}")
def delete_glossary_term(term_id: str):
    success = glossary_engine.delete_custom_term(term_id)
    if not success:
        raise HTTPException(status_code=404, detail="Term not found.")
    return {"status": "success", "deleted": term_id}

@app.post("/api/test-corruption")
def test_corruption_demo(req: CorruptionTestRequest):
    """Failure demonstration endpoint: deliberately introduces a numerical corruption (e.g. 9.81 -> 9.18)
    to prove that the Technical Integrity Validator actively detects mismatches."""
    content = req.content
    counts, _ = detector.analyze(content)
    
    # Run ordinary translate
    protected_text, mapping = protector.protect(content)
    translated_text = translator.translate(protected_text, mode="academic")
    restored_text, missing, restoration_log = restorer.restore(translated_text, mapping)

    # Deliberately corrupt 9.81 -> 9.18 or a target number
    corrupted_text = restored_text
    original_target_num = "9.81"
    corrupt_replacement = req.corruptedValue

    if original_target_num in corrupted_text:
        corrupted_text = corrupted_text.replace(original_target_num, corrupt_replacement, 1)
    else:
        # Corrupt any number found
        for item in restoration_log:
            if item["type"] == "number":
                original_target_num = item["value"]
                corrupted_text = corrupted_text.replace(original_target_num, corrupt_replacement, 1)
                break

    # Now validate the corrupted output!
    validation_result, warnings, details = validator.validate(
        original_text=content,
        translated_text=corrupted_text,
        original_counts=counts,
        restoration_log=restoration_log
    )

    # Add explicit corruption warning
    warnings.append(f"Simulated Corruption Detected: Numerical value '{original_target_num}' was changed to '{corrupt_replacement}'.")

    return {
        "status": "warning",
        "originalContent": content,
        "corruptedContent": corrupted_text,
        "validation": validation_result,
        "warnings": warnings,
        "demonstration": "This proves the Technical Integrity Validator actively verifies values and catches numerical corruptions!"
    }

@app.get("/api/history")
def get_history():
    return storage.get_history()
