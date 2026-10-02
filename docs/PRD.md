TECHSETU
Multilingual Technical Translator for Complex Science
Hackathon Problem Statement
PS 2.4 — Multi-Lingual Technical Translator for Complex Science
Domain
Smart Education
Primary Demo
English → Hindi
Tagline
Translate Knowledge. Preserve Science.
 
1. PRODUCT SUMMARY
TechSetu is a web-based AI technical translation platform that translates complex STEM material into an Indian language while preserving the technical information inside it.
Unlike a normal translator, TechSetu is designed to protect:
•	Equations
•	Numbers
•	Units
•	Code
•	Citations
•	Technical terminology
•	Markdown/LaTeX structure
before translation and verify them after translation.
Core principle
The language can change. The science must not.
 
2. OFFICIAL PS REQUIREMENTS
The official PS asks for a translation engine for advanced STEM material that preserves equations, code, units, citations and terminology.
The MVP specifically requires:
1.	Translate a LaTeX/Markdown science-paper section.
2.	Translate it into one Indian language such as Hindi.
3.	Protect equations, code and units using placeholders.
4.	Enforce a terminology glossary.
5.	Automatically check that equations and numbers remain unchanged.
These requirements are P0 and cannot be removed.
 
3. PROBLEM
Students may understand scientific concepts but struggle with English-heavy technical material.
Normal translation systems can create problems when dealing with technical content.
Example:
Original
Newton's second law states:

F = ma

If m = 5 kg and a = 9.8 m/s²,
the force is 49 N.
The natural-language portion can be translated, but:
F = ma
5 kg
9.8 m/s²
49 N
must remain technically correct.
TechSetu therefore separates:
language translation
from
technical information preservation.
 
4. PRODUCT GOAL
Build a reliable MVP that can:
Technical Content
       ↓
Detect technical elements
       ↓
Protect them
       ↓
Translate natural language
       ↓
Restore technical elements
       ↓
Verify technical integrity
       ↓
Show translated result
The product should demonstrate this complete flow during the hackathon.
 
5. TARGET USER
Primary
STEM students.
Subjects include:
•	Physics
•	Chemistry
•	Mathematics
•	Computer Science
•	Engineering
•	Biology
Secondary
•	Teachers
•	Educational content creators
•	Researchers
For the hackathon, optimize the UX primarily for students.
 
6. PRODUCT SCOPE
P0 — MUST WORK
Input
•	Paste technical text
•	Markdown
•	LaTeX
Translation
•	English → Hindi
•	Academic translation mode
Technical protection
•	Equations
•	Numbers
•	Units
•	Code
•	Citations
Terminology
•	Built-in glossary
•	Glossary enforcement
Validation
•	Equation preservation
•	Number preservation
•	Unit preservation
•	Code preservation
•	Citation preservation
•	Glossary compliance
Output
•	Hindi translation
•	Side-by-side comparison
•	Integrity report
 
7. P1 — IMPLEMENT IF P0 IS STABLE
•	PDF upload
•	PDF text extraction
•	Custom glossary
•	Student-friendly translation mode
•	Download translated text/Markdown
•	Translation statistics
•	Translation history
 
8. P2 — ONLY IF TIME REMAINS
•	Additional Indian languages
•	Bilingual explanation mode
•	Advanced terminology consistency
•	PDF export
•	Long-document optimization
•	Saved user glossary
 
9. DO NOT BUILD DURING MVP
Do not spend hackathon time on:
•	Training a new LLM
•	Mobile application
•	Blockchain
•	Complex authentication
•	Large admin dashboard
•	10+ languages
•	Complicated microservices
•	Unnecessary AI agents
•	Features unrelated to technical translation
 
10. CORE DIFFERENTIATOR
TechSetu is not simply:
English → Hindi
It is:
Technical Document
       ↓
Technical Element Detection
       ↓
Protection
       ↓
AI Translation
       ↓
Restoration
       ↓
Integrity Validation
       ↓
Verified Translation
The Technical Integrity Layer is the main innovation.
 
11. USER FLOW
Main flow
Landing Page
     ↓
Translator Workspace
     ↓
Paste / Upload Content
     ↓
Select Hindi
     ↓
Select Translation Mode
     ↓
Analyze
     ↓
Detect Technical Elements
     ↓
Protect
     ↓
Translate
     ↓
Restore
     ↓
Validate
     ↓
Show Translation
     ↓
Show Integrity Report
The entire product should be designed around making this flow reliable.
 
12. FRONTEND REQUIREMENTS
12.1 Landing Page
Show:
Heading
Translate Knowledge. Preserve Science.
Description
Translate complex STEM content into Indian languages while preserving equations, code, units, numbers and technical terminology.
Buttons
Start Translating
How It Works
 
13. TRANSLATOR WORKSPACE
Main application screen.
Input section
User can:
•	Paste content
•	Enter Markdown/LaTeX
•	Upload PDF if P1 is implemented
Display:
•	Word count
•	Character count
•	Clear button
 
14. LANGUAGE CONTROLS
Source
English
Target
Hindi
Architecture should allow future languages.
Possible future:
Marathi
Bengali
Tamil
Telugu
Gujarati
Punjabi
Kannada
Malayalam
Do not implement all of them unless P0 is already complete.
 
15. TRANSLATION MODE
Academic — P0
Formal technical translation.
Student-Friendly — P1
Simpler language while preserving technical accuracy.
Bilingual — P2
Original English + translated Hindi.
Academic mode is the default.
 
16. ANALYSIS SCREEN
Before translation, show detected content.
Example:
DOCUMENT ANALYSIS

Words              1,842
Equations             14
Numbers               23
Units                 12
Code blocks             4
Citations               7
Technical terms        87
These values must come from actual analysis.
Never use fake statistics.
 
17. TECHNICAL ELEMENT DETECTION
The backend should detect:
Equations
F = ma
E = mc²
v = u + at
and LaTeX such as:
\frac{d}{dx}
Numbers
9.81
5
3.14
0.001
Units
kg
m/s
m/s²
J
W
Pa
°C
K
Hz
Code
x = 10
print(x)
Citations
[1]
[12]
(Author, 2024)
Technical terms
Examples:
Neural Network
Machine Learning
Gradient Descent
Photosynthesis
Electromagnetic Induction
 
18. PROTECTION ENGINE
Before sending content to the translation model, technical elements should be replaced with placeholders.
Example:
Original
The force is F = ma and the mass is 5 kg.
Protected
The force is {{TECH_EQ_001}}
and the mass is {{TECH_NUM_001}} {{TECH_UNIT_001}}.
Mapping:
{{TECH_EQ_001}} → F = ma
{{TECH_NUM_001}} → 5
{{TECH_UNIT_001}} → kg
The translation model receives the protected version.
 
19. PLACEHOLDER RULES
Placeholders must:
•	Be unique.
•	Not be translated.
•	Not be modified.
•	Not be deleted.
•	Be restored exactly.
•	Be checked after translation.
Recommended format:
{{TECH_EQ_001}}
{{TECH_NUM_001}}
{{TECH_UNIT_001}}
{{TECH_CODE_001}}
{{TECH_CIT_001}}
The backend owns placeholder creation and restoration.
The frontend must never create or manipulate these placeholders.
 
20. TRANSLATION ENGINE
The AI receives protected text.
Example:
Newton's second law states that {{TECH_EQ_001}}.
The mass is {{TECH_NUM_001}} {{TECH_UNIT_001}}.
AI instructions:
1.	Translate natural language.
2.	Never modify placeholders.
3.	Do not translate code.
4.	Do not modify equations.
5.	Do not modify numbers.
6.	Do not modify units.
7.	Preserve Markdown/LaTeX structure.
8.	Preserve citations.
9.	Follow glossary terminology.
10.	Do not invent information.
The exact AI provider should be configurable through environment variables.
The official PS lists LLM API, IndicTrans2, spaCy and regex/LaTeX parsing among suggested tools.
 
21. GLOSSARY SYSTEM
The glossary is a core P0 requirement.
Example:
English	Hindi
Machine Learning	मशीन लर्निंग
Neural Network	न्यूरल नेटवर्क
Dataset	डेटासेट
Gradient Descent	ग्रेडिएंट डिसेंट
Algorithm	एल्गोरिदम
Built-in glossary
The system should contain common STEM terms.
Custom glossary
P1.
User can add:
Neural Network
→ न्यूरल नेटवर्क
Strict mode
If strict mode is enabled, the configured term should be used consistently.
 
22. RESTORATION
After translation, protected elements are restored.
Example:
{{TECH_EQ_001}}
becomes:
F = ma
The AI should not recreate equations.
Restoration must be deterministic.
 
23. VALIDATION ENGINE
After restoration:
Original
   ↓
Extract technical elements

Translated
   ↓
Extract technical elements

   ↓
Compare
The validator checks whether important technical information was preserved.
 
24. VALIDATION CHECKS
Equations
Check:
•	Number of equations
•	Equation content
•	LaTeX content where applicable
Numbers
Check that numerical values remain unchanged.
Example:
9.81 → 9.81 ✓
not:
9.81 → 9.18 ✗
Units
Check:
kg
m/s²
°C
etc.
Code
Code blocks must remain unchanged.
Citations
Citation identifiers should remain present.
Glossary
Check configured terminology.
 
25. INTEGRITY REPORT
After validation:
TECHNICAL INTEGRITY

Equations        8 / 8     ✓
Numbers         23 / 23    ✓
Units           12 / 12    ✓
Code             4 / 4     ✓
Citations        7 / 7     ✓
Glossary        19 / 20    ⚠

Integrity Score
98.7%
The score must be calculated from real validation results.
The score represents technical preservation, not perfect translation quality.
 
26. RESULT SCREEN
Use a side-by-side interface.
┌──────────────────────┬──────────────────────┐
│ ORIGINAL             │ HINDI                │
├──────────────────────┼──────────────────────┤
│ Newton's second law  │ न्यूटन का द्वितीय... │
│                      │                      │
│ F = ma               │ F = ma               │
│                      │                      │
│ 5 kg                 │ 5 kg                 │
│                      │                      │
│ 9.8 m/s²             │ 9.8 m/s²             │
└──────────────────────┴──────────────────────┘
Allow:
•	Copy translation
•	Download if implemented
•	View validation report
 
27. TECHNICAL ELEMENT HIGHLIGHTING
Optional P1 visual feature.
Highlight:
[EQUATION]
[UNIT]
[CODE]
[CITATION]
[TERM]
This helps judges understand what the system actually protects.
 
28. BACKEND ARCHITECTURE
The backend should be modular:
Backend API
    │
    ├── Input Validator
    │
    ├── Document Parser
    │
    ├── Technical Element Detector
    │
    ├── Protection Engine
    │
    ├── Glossary Engine
    │
    ├── Translation Engine
    │
    ├── Restoration Engine
    │
    └── Integrity Validator
 
29. END-TO-END BACKEND FLOW
Request
   ↓
Validate Input
   ↓
Parse Content
   ↓
Detect Technical Elements
   ↓
Protect Elements
   ↓
Load Glossary
   ↓
Translate
   ↓
Check Placeholders
   ↓
Restore Elements
   ↓
Validate Technical Integrity
   ↓
Generate Report
   ↓
Return Response
 
30. API CONTRACT
Frontend and backend must use a shared API contract.
Main MVP endpoint
POST /api/translate-and-validate
This should perform the complete pipeline.
 
Request
{
  "content": "technical content",
  "format": "markdown",
  "sourceLanguage": "en",
  "targetLanguage": "hi",
  "mode": "academic"
}
 
Response
{
  "status": "completed",
  "translatedContent": "...",
  "analysis": {
    "words": 1842,
    "equations": 14,
    "numbers": 23,
    "units": 12,
    "codeBlocks": 4,
    "citations": 7,
    "technicalTerms": 87
  },
  "validation": {
    "integrityScore": 98.7,
    "equations": {
      "total": 14,
      "preserved": 14
    },
    "numbers": {
      "total": 23,
      "preserved": 23
    },
    "units": {
      "total": 12,
      "preserved": 12
    }
  }
}
The exact schema can be expanded, but frontend and backend must agree before integration.
 
31. OPTIONAL API ENDPOINTS
If required:
POST   /api/analyze
POST   /api/translate
POST   /api/validate

GET    /api/glossary
POST   /api/glossary
DELETE /api/glossary/:id

GET    /api/history
GET    /api/translation/:id
The combined endpoint is preferred for the MVP because it reduces integration complexity.
 
32. DATABASE
Supabase can store persistent application data.
For MVP, database complexity should remain low.
Recommended tables:
documents
id
user_id
filename
source_language
target_language
format
original_content
created_at
translations
id
document_id
mode
translated_content
integrity_score
status
created_at
glossary_terms
id
user_id
source_term
target_term
language
is_strict
created_at
validation_results
id
translation_id
equations_total
equations_preserved
numbers_total
numbers_preserved
units_total
units_preserved
code_total
code_preserved
citations_total
citations_preserved
glossary_total
glossary_compliant
integrity_score
created_at
 
33. SUPABASE RULE
Do not use Supabase for temporary placeholder mappings unless necessary.
Temporary processing:
{{TECH_EQ_001}} → F = ma
should remain backend processing state.
Supabase should primarily store persistent product information.
Authentication/history are optional if time is limited.
 
34. FRONTEND ↔ BACKEND INTEGRATION RULE
This is critical.
Frontend owns
UI
State
User interaction
Displaying API responses
Backend owns
Parsing
Detection
Protection
AI
Restoration
Validation
Database operations
Frontend must NOT
•	Detect equations independently.
•	Create placeholders.
•	Calculate integrity scores.
•	Call the LLM directly.
•	Store API secrets.
Backend must NOT
•	Return undocumented response structures.
•	Assume frontend behavior.
•	Put UI-specific logic into APIs.
 
35. SHARED DATA CONTRACT
Both sides must use the same names.
Example:
equations
numbers
units
codeBlocks
citations
technicalTerms
integrityScore
Do not use:
equationCount
equationsCount
totalEquation
eq_count
interchangeably.
Choose one schema and keep it consistent.
 
36. ERROR HANDLING
Frontend must handle:
Empty input
Please enter technical content.
Unsupported file
This file type is not supported.
Translation failure
Translation could not be completed.
Please try again.
Validation failure
Technical inconsistencies were detected.
Please review the highlighted elements.
API failure
Translation service is temporarily unavailable.
Backend should return predictable HTTP status codes and structured error responses.
 
37. SECURITY
Mandatory:
•	No API keys in frontend.
•	Secrets only in .env.
•	.env must be gitignored.
•	Validate uploaded files.
•	Limit file size.
•	Sanitize rendered content.
•	Never execute uploaded code.
•	Validate API input.
•	Never expose server secrets.
 
38. ENVIRONMENT
.env
SUPABASE_URL=
SUPABASE_PUBLISHABLE_KEY=
LLM_API_KEY=
.env.example contains placeholders only.
Never commit real credentials.
 
39. FRONTEND DESIGN
Style:
•	Clean
•	Modern
•	Educational
•	Professional
•	Easy to understand
•	Indian-language friendly
Avoid:
•	Excessive animation
•	Overloaded dashboards
•	Decorative AI elements
•	Complicated navigation
The primary demo should be immediately understandable.
 
40. REQUIRED UI STATES
Every major operation needs:
Idle
User can start.
Loading
Show real processing state.
Success
Show result.
Error
Explain what failed.
Empty
Explain what the user needs to provide.
Do not create fake progress indicators.
 
41. DEMO DOCUMENT
Use one carefully prepared STEM document containing:
•	Normal paragraphs
•	Equations
•	Numbers
•	Units
•	Technical terms
•	Citation
•	Code block
Example:
Newton's second law states:

F = ma

If m = 5 kg and a = 9.8 m/s²,
then F = 49 N.

The calculation can be implemented in Python:

F = m * a
This gives the system enough technical elements to demonstrate.
 
42. DEMO SCENARIO
Step 1
Show the problem.
Step 2
Paste/upload technical content.
Step 3
Select:
English → Hindi
Academic
Step 4
Click:
Translate & Verify
Step 5
Show:
14 equations detected
23 numbers detected
12 units detected
4 code blocks detected
Step 6
Show Hindi translation.
Step 7
Show:
Equations ✓
Numbers ✓
Units ✓
Code ✓
Citations ✓
Glossary ✓
Step 8
Show integrity score.
This should be the main 5-minute demonstration.
 
43. FAILURE DEMO
If possible, demonstrate the validator detecting an incorrect value.
Original:
9.81 m/s²
Incorrect test:
9.18 m/s²
System:
⚠ Numerical mismatch

Original: 9.81
Result:   9.18
This proves the validation system is functional.
 
44. TEST CASES
Minimum tests:
T1 — Basic translation
Normal paragraph translates correctly.
T2 — Equation
F = ma
remains unchanged.
T3 — Number
9.81
remains unchanged.
T4 — Unit
5 kg
remains unchanged.
T5 — Code
Code block remains unchanged.
T6 — Citation
[12]
remains present.
T7 — Glossary
Configured term is used.
T8 — Corruption
Modified number is detected.
T9 — Empty input
Correct error shown.
T10 — Translation API failure
Correct error shown.
 
45. AGENT RESPONSIBILITIES
Manager Agent
Owns:
•	Architecture
•	Task assignment
•	Integration
•	Priority
•	Final verification
 
Product Agent
Owns:
•	PRD
•	Requirements
•	User flow
•	Feature priority
 
Frontend Agent
Owns:
•	UI
•	UX
•	Components
•	API integration
•	Loading/error/success states
 
Backend Agent
Owns:
•	APIs
•	Parser
•	Detection
•	Protection
•	Translation
•	Restoration
•	Validation
•	Supabase
 
QA Agent
Owns:
•	Testing
•	Bug detection
•	Regression testing
•	Demo readiness
 
46. DOCUMENTATION SOURCE OF TRUTH
docs/
├── PRD.md
├── ARCHITECTURE.md
├── DATABASE.md
├── API_CONTRACT.md
├── USER_FLOW.md
├── AI_SPEC.md
└── STATUS.md
PRD
What are we building?
ARCHITECTURE
How is it structured?
DATABASE
What data exists?
API_CONTRACT
How do frontend and backend communicate?
USER_FLOW
How does the user interact with it?
AI_SPEC
How does translation and validation work?
STATUS
What is currently happening?
 
47. STATUS.MD RULE
Every agent must read:
docs/STATUS.md
before starting a major task.
After a major task, update:
docs/STATUS.md
with:
Current Goal
Active Tasks
Decisions
Files Modified
Blockers
Handoff
Next Action
Use:
[x] Complete
[~] In progress
[ ] Not started
[!] Blocked
 
48. 10-HOUR DEVELOPMENT PRIORITY
Hour 0–1
Planning + architecture.
Hour 1–3
Frontend + backend foundation in parallel.
Hour 3–5
Core translation pipeline.
Hour 5–6
Integrity validation.
Hour 6–7
Frontend/backend integration.
Hour 7–8
Testing.
Hour 8–9
UI polish + demo data.
Hour 9–10
Final testing + presentation.
 
49. TIME PRIORITY
If time becomes limited:
Keep
Translation
Protection
Restoration
Validation
Frontend
API integration
Remove first
Extra languages
History
Advanced PDF export
Advanced analytics
Bilingual explanation
Custom themes
Never sacrifice the core technical integrity pipeline for cosmetic features.
 
50. FINAL MVP ARCHITECTURE
                    USER
                      │
                      ▼
              ┌──────────────┐
              │   FRONTEND   │
              │              │
              │ Input        │
              │ Language     │
              │ Translation  │
              │ Result       │
              │ Validation   │
              └──────┬───────┘
                     │
                     ▼
                REST API
                     │
                     ▼
              ┌──────────────┐
              │   BACKEND    │
              │              │
              │ Parser       │
              │ Detector     │
              │ Protection   │
              │ Glossary     │
              │ Translator   │
              │ Restoration  │
              │ Validator    │
              └──────┬───────┘
                     │
              ┌──────┴──────┐
              ▼             ▼
         LLM / Indic     Supabase
         Translation      Database
 
51. FINAL PRODUCT DEFINITION
TechSetu
A technical translation and integrity verification platform for STEM education.
Input
Technical English content.
Processing
Detect
→ Protect
→ Translate
→ Restore
→ Verify
Output
Hindi technical content + integrity report.
Core technology
LLM Translation
+
Technical Element Detection
+
Placeholder Protection
+
Glossary
+
Deterministic Restoration
+
Integrity Validation
Primary value
Students can access technical STEM knowledge in an Indian language without losing important scientific information.
 
52. SCOPE LOCK
The team should consider the following the complete hackathon MVP:
✓ English → Hindi

✓ Technical text input

✓ Markdown/LaTeX

✓ Equation detection

✓ Number detection

✓ Unit detection

✓ Code detection

✓ Citation detection

✓ Technical terminology

✓ Placeholder protection

✓ AI translation

✓ Glossary enforcement

✓ Restoration

✓ Integrity validation

✓ Side-by-side translation

✓ Integrity report

✓ Error handling

✓ Frontend/backend API integration
Everything else is optional.
 
53. ONE-LINE PRODUCT STATEMENT
TechSetu translates complex STEM content into Indian languages while protecting and automatically verifying the equations, numbers, units, code, citations and terminology that carry the scientific meaning.
 
54. END CONDITION
The project is considered ready for judging when this works reliably:
USER
 ↓
Paste technical STEM content
 ↓
Select English → Hindi
 ↓
Translate & Verify
 ↓
Backend detects technical elements
 ↓
Backend protects them
 ↓
AI translates natural language
 ↓
Backend restores protected elements
 ↓
Validator checks integrity
 ↓
Frontend displays translation
 ↓
Frontend displays actual validation report
This end-to-end path is more important than every optional feature in the PRD.

