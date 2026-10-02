# TechSetu API Contract Specification

## Base URL
`/api`

## Core Principles
1. Stable, typed JSON contracts across Frontend and Backend.
2. Standardized field naming: `equations`, `numbers`, `units`, `codeBlocks`, `citations`, `technicalTerms`, `integrityScore`.
3. Deterministic errors with informative codes and human-friendly messages.

---

## 1. Translate & Validate (Primary MVP Endpoint)
Performs the full pipeline: Parse → Detect → Protect → Translate → Restore → Validate → Score.

- **Method**: `POST`
- **Path**: `/api/translate-and-validate`
- **Content-Type**: `application/json`

### Request Body
```json
{
  "content": "Newton's second law states that F = ma. If m = 5 kg and a = 9.8 m/s^2, the force is 49 N.",
  "format": "markdown",
  "sourceLanguage": "en",
  "targetLanguage": "hi",
  "mode": "academic"
}
```
*Parameters*:
- `content` *(string, required)*: Source technical STEM document.
- `format` *(string, default "markdown")*: "markdown" | "latex" | "plain".
- `sourceLanguage` *(string, default "en")*: "en".
- `targetLanguage` *(string, default "hi")*: "hi".
- `mode` *(string, default "academic")*: "academic" | "student_friendly" | "bilingual".

### Response Body (`200 OK`)
```json
{
  "status": "success",
  "translatedContent": "न्यूटन का द्वितीय नियम बताता है कि F = ma। यदि m = 5 kg और a = 9.8 m/s^2, तो बल 49 N है।",
  "analysis": {
    "words": 19,
    "equations": 1,
    "numbers": 3,
    "units": 3,
    "codeBlocks": 0,
    "citations": 0,
    "technicalTerms": 4
  },
  "validation": {
    "integrityScore": 100.0,
    "equations": {
      "original": 1,
      "preserved": 1
    },
    "numbers": {
      "original": 3,
      "preserved": 3
    },
    "units": {
      "original": 3,
      "preserved": 3
    },
    "codeBlocks": {
      "original": 0,
      "preserved": 0
    },
    "citations": {
      "original": 0,
      "preserved": 0
    },
    "technicalTerms": {
      "original": 4,
      "preserved": 4
    }
  },
  "details": {
    "preservedElements": [
      { "type": "equation", "value": "F = ma", "status": "preserved" },
      { "type": "number", "value": "5", "status": "preserved" },
      { "type": "unit", "value": "kg", "status": "preserved" },
      { "type": "number", "value": "9.8", "status": "preserved" },
      { "type": "unit", "value": "m/s^2", "status": "preserved" },
      { "type": "number", "value": "49", "status": "preserved" },
      { "type": "unit", "value": "N", "status": "preserved" }
    ],
    "warnings": []
  }
}
```

---

## 2. Pre-Translation Document Analysis
Enables the frontend to display detected element badges before translation.

- **Method**: `POST`
- **Path**: `/api/analyze`
- **Content-Type**: `application/json`

### Request Body
```json
{
  "content": "The energy is E = mc^2 where c = 3.0 x 10^8 m/s.",
  "format": "markdown"
}
```

### Response Body (`200 OK`)
```json
{
  "status": "success",
  "analysis": {
    "words": 10,
    "characters": 49,
    "equations": 1,
    "numbers": 2,
    "units": 1,
    "codeBlocks": 0,
    "citations": 0,
    "technicalTerms": 2
  },
  "elements": [
    { "type": "equation", "value": "E = mc^2" },
    { "type": "number", "value": "3.0" },
    { "type": "number", "value": "10^8" },
    { "type": "unit", "value": "m/s" }
  ]
}
```

---

## 3. PDF Document Ingestion (P1)
Extracts technical text and equations from uploaded PDF files.

- **Method**: `POST`
- **Path**: `/api/upload-pdf`
- **Content-Type**: `multipart/form-data`

### Request
Form field: `file` (binary PDF)

### Response Body (`200 OK`)
```json
{
  "status": "success",
  "filename": "sample_paper.pdf",
  "extractedContent": "..."
}
```

---

## 4. Glossary Endpoints
- **`GET /api/glossary`**: Returns list of built-in and user-custom terms.
- **`POST /api/glossary`**: Adds a custom user term `{ "sourceTerm": "...", "targetTerm": "...", "language": "hi", "isStrict": true }`.
- **`DELETE /api/glossary/{id}`**: Deletes a custom term.

---

## 5. Corruption Test Endpoint (Failure Demo)
Simulates numerical/technical corruption to demonstrate that the validator catches discrepancies (e.g. `9.81` corrupted to `9.18`).

- **Method**: `POST`
- **Path**: `/api/test-corruption`
- **Content-Type**: `application/json`

### Request Body
```json
{
  "content": "Acceleration due to gravity is 9.81 m/s^2.",
  "corruptedValue": "9.18"
}
```

### Response Body (`200 OK`)
```json
{
  "status": "warning",
  "integrityScore": 66.7,
  "warnings": [
    "Numerical mismatch: Expected 9.81, found 9.18"
  ],
  "validation": { ... }
}
```
