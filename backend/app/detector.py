import re
from typing import List, Dict, Any, Set, Tuple
from app.models import AnalysisCounts, ElementDetail
from app.glossary import glossary_engine

# Common SI & Scientific Units
UNITS_LIST = [
    # Compound units first (longer first)
    r"m/s\^2", r"m/s²", r"m/s", r"km/h", r"kg\\cdot m/s", r"kg\\cdot m/s\^2",
    r"g/cm\^3", r"g/cm³", r"kg/m\^3", r"kg/m³", r"N\\cdot m", r"J/s", r"W/m\^2",
    r"V/m", r"A/m", r"rad/s", r"rev/min", r"rpm",
    # Single units with prefixes
    r"kg", r"mg", r"μg", r"g",
    r"km", r"cm", r"mm", r"μm", r"nm", r"pm", r"m",
    r"ms", r"μs", r"ns", r"ps", r"s",
    r"kN", r"MN", r"N",
    r"kJ", r"MJ", r"GJ", r"J",
    r"kW", r"MW", r"GW", r"W",
    r"kPa", r"MPa", r"GPa", r"Pa", r"bar", r"atm",
    r"kV", r"mV", r"μV", r"V",
    r"mA", r"μA", r"kA", r"A",
    r"kΩ", r"MΩ", r"GΩ", r"Ω", r"ohm", r"ohms",
    r"μF", r"nF", r"pF", r"F",
    r"mH", r"μH", r"H",
    r"kHz", r"MHz", r"GHz", r"THz", r"Hz",
    r"°C", r"degC", r"°F", r"K",
    r"mol", r"mmol", r"μmol",
    r"cd", r"rad", r"sr", r"dB",
    r"eV", r"keV", r"MeV", r"GeV", r"TeV",
    r"cal", r"kcal", r"Tesla", r"T", r"Gauss", r"G"
]

# Sort units by descending length to match longest first
SORTED_UNITS = sorted(UNITS_LIST, key=len, reverse=True)
UNITS_REGEX_PART = "|".join(SORTED_UNITS)

# Known ASCII equations / physics formulas
ASCII_EQUATION_PATTERNS = [
    r"\bF\s*=\s*m\s*\*?\s*a\b",
    r"\bE\s*=\s*m\s*\*?\s*c(?:\^2|²)\b",
    r"\bv\s*=\s*u\s*\+\s*a\s*\*?\s*t\b",
    r"\bv(?:\^2|²)\s*=\s*u(?:\^2|²)\s*\+\s*2\s*\*?\s*a\s*\*?\s*s\b",
    r"\bs\s*=\s*u\s*\*?\s*t\s*\+\s*(?:1\/2|0\.5)\s*\*?\s*a\s*\*?\s*t(?:\^2|²)\b",
    r"\bP\s*=\s*V\s*\*?\s*I\b",
    r"\bV\s*=\s*I\s*\*?\s*R\b",
    r"\ba\^2\s*\+\s*b\^2\s*=\s*c\^2\b",
    r"\by\s*=\s*m\s*\*?\s*x\s*\+\s*c\b",
    r"\b[A-Za-z](?:_[a-zA-Z0-9]+)?\s*=\s*(?:[A-Za-z0-9_](?:\^[0-9]+|²|³)?\s*[\+\-\*\/\·]\s*)+[A-Za-z0-9_](?:\^[0-9]+|²|³)?\b"
]

class TechnicalDetector:
    def __init__(self):
        # Code patterns
        self.fenced_code_pattern = re.compile(r"```[a-zA-Z0-9_-]*\n[\s\S]*?\n```")
        self.inline_code_pattern = re.compile(r"`[^`\n]+`")

        # Equation patterns
        self.display_latex_pattern = re.compile(r"\$\$[\s\S]*?\$\$")
        self.latex_env_pattern = re.compile(r"\\begin\{(?:equation|align|gather|multline|matrix|bmatrix|pmatrix|split)\*?\}[\s\S]*?\\end\{(?:equation|align|gather|multline|matrix|bmatrix|pmatrix|split)\*?\}")
        self.inline_bracket_latex = re.compile(r"\\\[[\s\S]*?\\\]")
        self.inline_paren_latex = re.compile(r"\\\([\s\S]*?\\\)|\$(?!\$)[^\$\n]+?\$")
        
        # Citations
        self.citation_bracket_pattern = re.compile(r"\[\d+(?:[-–,]\s*\d+)*\]")
        self.citation_author_pattern = re.compile(r"\([A-Z][a-zA-Z]+(?:\s+et\s+al\.)?,\s*[12]\d{3}[a-z]?\)")
        self.citation_etal_pattern = re.compile(r"\bet\s+al\.\b")

        # Number with unit bound
        # e.g. 9.81 m/s^2, 5 kg, 3.0 x 10^8 m/s, -40 °C
        number_part = r"(?:[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|\d+(?:\.\d+)?\s*[x×]\s*10\s*[\^⁻-]?\d+)"
        self.number_unit_pattern = re.compile(
            rf"({number_part})\s*({UNITS_REGEX_PART})(?![a-zA-Z0-9])"
        )

        # Isolated numbers
        # avoid matching inside words or identifiers
        self.isolated_number_pattern = re.compile(
            r"(?<![A-Za-z0-9_])(?:[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|\d+(?:\.\d+)?\s*[x×]\s*10\s*[\^⁻-]?\d+)(?![A-Za-z0-9_])"
        )

        # Standalone units (e.g. after symbols or in expressions)
        self.isolated_unit_pattern = re.compile(
            rf"(?<=\s)({UNITS_REGEX_PART})(?=[\s\.,;\)\]]|$)"
        )

    def analyze(self, text: str, extra_glossary: Dict[str, str] = None) -> Tuple[AnalysisCounts, List[ElementDetail]]:
        """Extracts and counts all technical elements in the text."""
        elements: List[ElementDetail] = []
        
        # Word and character count
        words = len(text.split()) if text.strip() else 0
        characters = len(text)

        # 1. Code blocks
        code_matches = list(self.fenced_code_pattern.finditer(text)) + list(self.inline_code_pattern.finditer(text))
        for m in code_matches:
            elements.append(ElementDetail(type="code", value=m.group(0)))

        # Mask code blocks for subsequent detection so code content isn't double-counted
        masked_text = text
        for m in sorted(code_matches, key=lambda x: x.start(), reverse=True):
            masked_text = masked_text[:m.start()] + (" " * (m.end() - m.start())) + masked_text[m.end():]

        # 2. LaTeX & Equations
        eq_spans: List[Tuple[int, int, str]] = []
        for pat in [self.display_latex_pattern, self.latex_env_pattern, self.inline_bracket_latex, self.inline_paren_latex]:
            for m in pat.finditer(masked_text):
                eq_spans.append((m.start(), m.end(), m.group(0)))

        # ASCII equations
        for pat_str in ASCII_EQUATION_PATTERNS:
            for m in re.finditer(pat_str, masked_text):
                # Ensure it contains '=' and not overlapping an existing LaTeX match
                val = m.group(0).strip()
                if "=" in val and len(val) >= 3:
                    overlap = any(s <= m.start() < e or s < m.end() <= e for s, e, _ in eq_spans)
                    if not overlap:
                        eq_spans.append((m.start(), m.end(), val))

        for _, _, val in eq_spans:
            elements.append(ElementDetail(type="equation", value=val))

        # Mask equations
        for s, e, _ in sorted(eq_spans, key=lambda x: x[0], reverse=True):
            masked_text = masked_text[:s] + (" " * (e - s)) + masked_text[e:]

        # 3. Citations
        cit_matches = []
        for pat in [self.citation_bracket_pattern, self.citation_author_pattern, self.citation_etal_pattern]:
            for m in pat.finditer(masked_text):
                cit_matches.append((m.start(), m.end(), m.group(0)))
        
        for _, _, val in cit_matches:
            elements.append(ElementDetail(type="citation", value=val))

        for s, e, _ in sorted(cit_matches, key=lambda x: x[0], reverse=True):
            masked_text = masked_text[:s] + (" " * (e - s)) + masked_text[e:]

        # 4. Numbers with Units
        num_unit_spans = []
        for m in self.number_unit_pattern.finditer(masked_text):
            num_val = m.group(1).strip()
            unit_val = m.group(2).strip()
            num_unit_spans.append((m.start(), m.end(), num_val, unit_val))
            elements.append(ElementDetail(type="number", value=num_val))
            elements.append(ElementDetail(type="unit", value=unit_val))

        for s, e, _, _ in sorted(num_unit_spans, key=lambda x: x[0], reverse=True):
            masked_text = masked_text[:s] + (" " * (e - s)) + masked_text[e:]

        # 5. Isolated Numbers
        for m in self.isolated_number_pattern.finditer(masked_text):
            val = m.group(0).strip()
            if val:
                elements.append(ElementDetail(type="number", value=val))

        # 6. Technical Terms from Glossary
        all_terms = glossary_engine.get_terms_dict(extra_glossary)
        # Sort terms by length descending to match longest phrases first
        sorted_terms = sorted(all_terms.keys(), key=len, reverse=True)
        found_terms = 0
        text_lower = text.lower()
        for term in sorted_terms:
            pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
            matches = list(pattern.finditer(text_lower))
            if matches:
                found_terms += len(matches)
                for _ in matches:
                    elements.append(ElementDetail(type="term", value=term))

        counts = AnalysisCounts(
            words=words,
            characters=characters,
            equations=len([e for e in elements if e.type == "equation"]),
            numbers=len([e for e in elements if e.type == "number"]),
            units=len([e for e in elements if e.type == "unit"]),
            codeBlocks=len([e for e in elements if e.type == "code"]),
            citations=len([e for e in elements if e.type == "citation"]),
            technicalTerms=found_terms
        )

        return counts, elements

detector = TechnicalDetector()
