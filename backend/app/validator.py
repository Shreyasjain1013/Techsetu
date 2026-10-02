import re
from typing import Dict, Any, List, Tuple
from app.models import ValidationResult, ValidationCategory, AnalysisCounts
from app.detector import detector
from app.glossary import glossary_engine

class TechnicalValidator:
    def validate(
        self,
        original_text: str,
        translated_text: str,
        original_counts: AnalysisCounts,
        extra_glossary: Dict[str, str] = None,
        restoration_log: List[Dict[str, Any]] = None,
        target_language: str = "hi"
    ) -> Tuple[ValidationResult, List[str], List[Dict[str, Any]]]:
        """Validates technical integrity between original STEM content and translated text.
        
        Returns:
            validation_result: Standardized validation object with counts and integrity score.
            warnings: List of specific technical mismatch warnings.
            preserved_details: Breakdown of verified elements.
        """
        warnings: List[str] = []
        preserved_details: List[Dict[str, Any]] = []

        # Analyze translated text
        trans_counts, trans_elements = detector.analyze(translated_text, extra_glossary)

        # 1. Equations check
        # 1. Equations check
        eq_orig = original_counts.equations
        eq_pres = 0
        if restoration_log:
            for x in restoration_log:
                if x["type"] == "equation" and x["status"] == "restored":
                    if x["value"] in translated_text:
                        eq_pres += 1
                    else:
                        warnings.append(f"Equation modified or missing: '{x['value']}'")
        else:
            eq_pres = min(eq_orig, trans_counts.equations)

        if eq_orig > 0 and eq_pres < eq_orig:
            warnings.append(f"Equation mismatch: {eq_orig} original equations detected, but only {eq_pres} preserved.")

        # 2. Code blocks check
        code_orig = original_counts.codeBlocks
        code_pres = 0
        if restoration_log:
            for x in restoration_log:
                if x["type"] == "code" and x["status"] == "restored":
                    if x["value"] in translated_text:
                        code_pres += 1
                    else:
                        warnings.append("Code block modified or missing.")
        else:
            code_pres = min(code_orig, trans_counts.codeBlocks)

        if code_orig > 0 and code_pres < code_orig:
            warnings.append(f"Code block mismatch: {code_orig} code block(s) detected, but only {code_pres} preserved.")

        # 3. Numbers check & value-level verification
        num_orig = original_counts.numbers
        num_pres = 0
        if restoration_log:
            for item in restoration_log:
                if item["type"] == "number" and item["status"] == "restored":
                    val = item["value"]
                    if val in translated_text:
                        num_pres += 1
                    else:
                        warnings.append(f"Numerical corruption: Number '{val}' was not found in translated output.")
        else:
            num_pres = min(num_orig, trans_counts.numbers)

        if num_orig > 0 and num_pres < num_orig:
            warnings.append(f"Number count mismatch: {num_orig} numbers in original, {num_pres} preserved.")

        # 4. Units check
        unit_orig = original_counts.units
        unit_pres = 0
        if restoration_log:
            for item in restoration_log:
                if item["type"] == "unit" and item["status"] == "restored":
                    val = item["value"]
                    if val in translated_text:
                        unit_pres += 1
                    else:
                        warnings.append(f"Unit mismatch: Scientific unit '{val}' was not found in translated output.")
        else:
            unit_pres = min(unit_orig, trans_counts.units)

        if unit_orig > 0 and unit_pres < unit_orig:
            warnings.append(f"Unit mismatch: {unit_orig} scientific units detected, {unit_pres} preserved.")

        # 5. Citations check
        cit_orig = original_counts.citations
        cit_pres = 0
        if restoration_log:
            for item in restoration_log:
                if item["type"] == "citation" and item["status"] == "restored":
                    val = item["value"]
                    if val in translated_text:
                        cit_pres += 1
                    else:
                        warnings.append(f"Citation missing: Citation '{val}' was not found in translated output.")
        else:
            cit_pres = min(cit_orig, trans_counts.citations)

        if cit_orig > 0 and cit_pres < cit_orig:
            warnings.append(f"Citation mismatch: {cit_orig} citations expected, {cit_pres} preserved.")

        # 6. Glossary terms check
        term_orig = original_counts.technicalTerms
        term_pres = 0
        terms_map = glossary_engine.get_terms_dict(extra_glossary)
        orig_lower = original_text.lower()
        trans_text_str = translated_text

        for en_term, hi_term in terms_map.items():
            if re.search(rf"\b{re.escape(en_term)}\b", orig_lower):
                # Check if the target term appears in translated text
                is_compliant = hi_term in trans_text_str
                if not is_compliant and target_language == "bho":
                    bho_alts = {
                        "न्यूटन का द्वितीय नियम": ["न्यूटन के दूसरका नियम", "न्यूटन के द्वितीय नियम"],
                        "द्रव्यमान": ["द्रब्यमान", "द्रव्यमान"],
                        "प्रकाश संश्लेषण": ["प्रकाश संस्लेसन", "प्रकाश संश्लेषण"]
                    }
                    if any(alt in trans_text_str for alt in bho_alts.get(hi_term, [])):
                        is_compliant = True

                if is_compliant:
                    term_pres += 1
                    preserved_details.append({
                        "type": "term",
                        "source": en_term,
                        "target": hi_term,
                        "status": "compliant"
                    })
                else:
                    warnings.append(f"Glossary term deviation: '{en_term}' -> expected '{hi_term}'.")
                    preserved_details.append({
                        "type": "term",
                        "source": en_term,
                        "target": hi_term,
                        "status": "deviated"
                    })

        # Calculate deterministic integrity score
        category_weights = {
            "equations": (0.25, eq_orig, eq_pres),
            "numbers": (0.25, num_orig, num_pres),
            "units": (0.15, unit_orig, unit_pres),
            "codeBlocks": (0.15, code_orig, code_pres),
            "citations": (0.10, cit_orig, cit_pres),
            "technicalTerms": (0.10, max(term_orig, 1) if term_orig > 0 else 0, term_pres)
        }

        active_weight_sum = sum(w for w, orig, _ in category_weights.values() if orig > 0)
        
        if active_weight_sum == 0:
            integrity_score = 100.0
        else:
            weighted_score = 0.0
            for w, orig, pres in category_weights.values():
                if orig > 0:
                    normalized_weight = w / active_weight_sum
                    ratio = min(1.0, pres / orig)
                    weighted_score += normalized_weight * ratio
            integrity_score = round(weighted_score * 100.0, 1)

        validation = ValidationResult(
            integrityScore=integrity_score,
            equations=ValidationCategory(original=eq_orig, preserved=eq_pres),
            numbers=ValidationCategory(original=num_orig, preserved=num_pres),
            units=ValidationCategory(original=unit_orig, preserved=unit_pres),
            codeBlocks=ValidationCategory(original=code_orig, preserved=code_pres),
            citations=ValidationCategory(original=cit_orig, preserved=cit_pres),
            technicalTerms=ValidationCategory(original=term_orig, preserved=term_pres)
        )

        return validation, warnings, preserved_details

validator = TechnicalValidator()
