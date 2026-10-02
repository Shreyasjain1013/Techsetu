import re
from typing import Dict, List, Tuple, Any
from app.detector import detector, UNITS_REGEX_PART, ASCII_EQUATION_PATTERNS

class ProtectionRecord:
    def __init__(self, placeholder: str, elem_type: str, original_value: str, span: Tuple[int, int]):
        self.placeholder = placeholder
        self.elem_type = elem_type
        self.original_value = original_value
        self.span = span

class ProtectionEngine:
    def __init__(self):
        self.counters = {
            "code": 1,
            "eq": 1,
            "cit": 1,
            "num": 1,
            "unit": 1
        }

    def _next_placeholder(self, elem_type: str) -> str:
        tag_map = {
            "code": "TECH_CODE",
            "equation": "TECH_EQ",
            "citation": "TECH_CIT",
            "number": "TECH_NUM",
            "unit": "TECH_UNIT"
        }
        prefix = tag_map.get(elem_type, "TECH_ELEM")
        key = "eq" if elem_type == "equation" else ("cit" if elem_type == "citation" else ("num" if elem_type == "number" else elem_type))
        idx = self.counters.get(key, 1)
        self.counters[key] = idx + 1
        return f"{{{{{prefix}_{idx:03d}}}}}"

    def protect(self, text: str) -> Tuple[str, Dict[str, Dict[str, Any]]]:
        """Protects technical elements in text with deterministic placeholders.
        Returns:
            protected_text: Text with placeholders in place of raw scientific components.
            mapping: Dictionary mapping placeholder -> {'type': str, 'value': str}
        """
        # Reset counters
        self.counters = {"code": 1, "eq": 1, "cit": 1, "num": 1, "unit": 1}
        mapping: Dict[str, Dict[str, Any]] = {}
        
        # We will collect spans of elements to replace: (start, end, placeholder, elem_type, value)
        spans_to_replace: List[Tuple[int, int, str, str, str]] = []

        # 1. Code blocks (Highest priority)
        for m in detector.fenced_code_pattern.finditer(text):
            ph = self._next_placeholder("code")
            val = m.group(0)
            spans_to_replace.append((m.start(), m.end(), ph, "code", val))
            mapping[ph] = {"type": "code", "value": val}

        for m in detector.inline_code_pattern.finditer(text):
            # Check overlap with fenced code
            if not any(s <= m.start() < e for s, e, _, _, _ in spans_to_replace):
                ph = self._next_placeholder("code")
                val = m.group(0)
                spans_to_replace.append((m.start(), m.end(), ph, "code", val))
                mapping[ph] = {"type": "code", "value": val}

        # Mask text for subsequent phases
        masked = text
        for s, e, _, _, _ in sorted(spans_to_replace, key=lambda x: x[0], reverse=True):
            masked = masked[:s] + ("\x00" * (e - s)) + masked[e:]

        # 2. LaTeX and Equations
        eq_spans = []
        for pat in [detector.display_latex_pattern, detector.latex_env_pattern, detector.inline_bracket_latex, detector.inline_paren_latex]:
            for m in pat.finditer(masked):
                if "\x00" not in m.group(0):
                    eq_spans.append((m.start(), m.end(), m.group(0)))

        # ASCII equations
        for pat_str in ASCII_EQUATION_PATTERNS:
            for m in re.finditer(pat_str, masked):
                val = m.group(0).strip()
                if "\x00" not in val and "=" in val and len(val) >= 3:
                    overlap = any(s <= m.start() < e or s < m.end() <= e for s, e, _ in eq_spans)
                    if not overlap:
                        eq_spans.append((m.start(), m.end(), val))

        for s, e, val in sorted(eq_spans, key=lambda x: x[0]):
            ph = self._next_placeholder("equation")
            spans_to_replace.append((s, e, ph, "equation", val))
            mapping[ph] = {"type": "equation", "value": val}

        for s, e, _ in sorted(eq_spans, key=lambda x: x[0], reverse=True):
            masked = masked[:s] + ("\x00" * (e - s)) + masked[e:]

        # 3. Citations
        cit_spans = []
        for pat in [detector.citation_bracket_pattern, detector.citation_author_pattern, detector.citation_etal_pattern]:
            for m in pat.finditer(masked):
                if "\x00" not in m.group(0):
                    cit_spans.append((m.start(), m.end(), m.group(0)))

        for s, e, val in sorted(cit_spans, key=lambda x: x[0]):
            ph = self._next_placeholder("citation")
            spans_to_replace.append((s, e, ph, "citation", val))
            mapping[ph] = {"type": "citation", "value": val}

        for s, e, _ in sorted(cit_spans, key=lambda x: x[0], reverse=True):
            masked = masked[:s] + ("\x00" * (e - s)) + masked[e:]

        # 4. Numbers with Units (e.g. "9.81 m/s^2" -> "{{TECH_NUM_001}} {{TECH_UNIT_001}}")
        num_unit_spans = []
        for m in detector.number_unit_pattern.finditer(masked):
            if "\x00" not in m.group(0):
                num_val = m.group(1).strip()
                unit_val = m.group(2).strip()
                num_ph = self._next_placeholder("number")
                unit_ph = self._next_placeholder("unit")
                mapping[num_ph] = {"type": "number", "value": num_val}
                mapping[unit_ph] = {"type": "unit", "value": unit_val}
                replacement = f"{num_ph} {unit_ph}"
                num_unit_spans.append((m.start(), m.end(), replacement, "num_unit", m.group(0)))

        for s, e, rep, typ, val in sorted(num_unit_spans, key=lambda x: x[0]):
            spans_to_replace.append((s, e, rep, typ, val))

        for s, e, _, _, _ in sorted(num_unit_spans, key=lambda x: x[0], reverse=True):
            masked = masked[:s] + ("\x00" * (e - s)) + masked[e:]

        # 5. Isolated Numbers
        for m in detector.isolated_number_pattern.finditer(masked):
            if "\x00" not in m.group(0):
                val = m.group(0).strip()
                ph = self._next_placeholder("number")
                mapping[ph] = {"type": "number", "value": val}
                spans_to_replace.append((m.start(), m.end(), ph, "number", val))

        # Now replace all collected spans from right to left (descending by start index)
        # to preserve indices
        spans_to_replace.sort(key=lambda x: x[0], reverse=True)
        protected_text = text
        for s, e, rep, typ, val in spans_to_replace:
            protected_text = protected_text[:s] + rep + protected_text[e:]

        return protected_text, mapping

protector = ProtectionEngine()
