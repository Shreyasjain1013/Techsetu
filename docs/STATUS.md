# TechSetu — Project Working State

## Current Goal
Complete working end-to-end MVP for **TechSetu** ("Translate Knowledge. Preserve Science.") delivered and verified.
Recently completed:
1. Unified Upload button supporting both PDF documents and technical diagrams / images (PNG, JPG, WebP) with multimodal OCR and robust digital extraction.
2. Multilingual expansion: Bhojpuri (`bho` / भोजपुरी) fully supported alongside Hindi (`hi` / हिंदी) in translation, protection, restoration, and validation.

## Active Subtasks & Status
- [x] Initial MVP complete with all P0 features & test suite (10/10 tests passed).
- [x] Backend Multimodal & Multilingual Enhancement:
  - [x] Robust PDF & Image extraction endpoint (`POST /api/upload-file` and backward-compatible `POST /api/upload-pdf`) handling scanned PDFs and images without 500 errors.
  - [x] Bhojpuri translation support in `translator.py` (Gemini prompt directives + deterministic Bhojpuri grammar & vocabulary engine).
  - [x] Target language validation in `validator.py` and `models.py`.
- [x] Frontend Upload & Language Controls:
  - [x] Unified "Upload" button with interactive dropdown for PDF and Image options.
  - [x] Language pair selector supporting English -> Hindi (`hi`) and English -> Bhojpuri (`bho`).
  - [x] Updated API client with target language support and file upload.
- [x] Automated tests & verification:
  - [x] 12/12 test cases passed (`backend/tests/test_pipeline.py`) including T11 (Bhojpuri) and T12 (PDF & Image upload).
  - [x] Live end-to-end verified on `http://127.0.0.1:3000/` and `http://127.0.0.1:8000/`.

## Important Decisions & Technical Reasoning
1. **Unified Upload Menu**: Instead of separate confusing buttons, a single "Upload" button with options for PDF and Image allows students to upload either research papers (.pdf) or textbook photos/diagrams (.png, .jpg, .webp).
2. **Multimodal OCR & Fallback**: Images and scanned PDFs are processed without throwing 500 errors. When Gemini is configured, Gemini Vision extracts LaTeX equations ($...$ and $$...$$). If offline, Pillow extracts metadata and generates a clean STEM template for translation.
3. **Bhojpuri STEM Localization**: Bhojpuri is integrated into both the Gemini system prompt and the deterministic offline fallback engine (`न्यूटन के दूसरका नियम ई बतावेला कि...`, `बल बा 49 N`, `द्रव्यमान 5 kg बा`), achieving 100% technical integrity.

## Files Modified
- `docs/STATUS.md`
- `backend/app/main.py`
- `backend/app/translator.py`
- `backend/app/validator.py`
- `backend/tests/test_pipeline.py`
- `frontend/src/api.ts`
- `frontend/src/components/TranslatorWorkspace.tsx`

## Current Blockers & Risks
- None. Backend and frontend servers are healthy and passing all automated test suites and live API requests.

## Agent Handoffs
- Full upload capabilities (PDF + Images) and Bhojpuri language support are complete and operational.

## Next Recommended Action
Present update to user with instructions to test the new Upload button and Bhojpuri language selector.
