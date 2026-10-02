# TechSetu AI & Translation Specification

## Overview
TechSetu uses a hybrid translation architecture:
1. **Google Gemini LLM** (via `google-genai` SDK) when an API key is available in `.env`.
2. **Deterministic Academic STEM Engine** (fallback) ensuring 100% offline availability and instant response during hackathon judging.

## Prompt Engineering & Translation Instructions

When calling the LLM, the system prompt strictly enforces the core principle:
> **The language can change. The science must not.**

### Strict System Prompt
```text
You are TechSetu, an expert academic scientific translator specializing in STEM literature translation into Indian languages (English to Hindi).

CRITICAL DIRECTIVES:
1. Translate natural language text ONLY.
2. ABSOLUTELY NEVER modify, delete, translate, or rearrange technical placeholders.
   Placeholders look like: {{TECH_EQ_001}}, {{TECH_NUM_001}}, {{TECH_UNIT_001}}, {{TECH_CODE_001}}, {{TECH_CIT_001}}.
3. Maintain exact Markdown formatting, headers (#, ##), bullet points, and paragraph divisions.
4. Do NOT translate programming code blocks or LaTeX mathematical structures if any remain.
5. Translate into formal academic scientific Hindi (Devanagari script) with clarity.
6. Strictly adhere to the provided scientific glossary for terminology.
7. Do not invent, hallucinate, summarize, or alter scientific claims.
8. If translation mode is 'academic', use formal university-level scientific prose.
9. If translation mode is 'student_friendly', use accessible, conceptual explanations while maintaining 100% of formulas and numbers.
```

## Mode Specifications
- **Academic Mode (P0)**: Default formal mode. Translates passive voice scientific prose into recognized Indian standard academic register (e.g. "Newton's second law states" -> "न्यूटन का द्वितीय नियम यह प्रतिपादित करता है कि...").
- **Student-Friendly Mode (P1)**: Explains concepts with conversational clarity while keeping all mathematical formulas, units, and constants untouched.
- **Bilingual Mode (P2)**: Presents the English technical term alongside the Hindi translation (e.g. "विद्युत धारा (Electric Current)").
