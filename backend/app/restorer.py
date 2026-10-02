import re
from typing import Dict, Any, Tuple, List

class RestorationEngine:
    def restore(self, translated_text: str, mapping: Dict[str, Dict[str, Any]]) -> Tuple[str, List[str], List[Dict[str, Any]]]:
        """Restores placeholders with original technical elements.
        
        Returns:
            restored_text: The final text with original equations, numbers, units, code, citations.
            missing_placeholders: List of placeholders that were lost or modified by translation.
            restoration_log: Detailed log of restored items.
        """
        restored = translated_text
        missing: List[str] = []
        restoration_log: List[Dict[str, Any]] = []

        # Sort placeholders so exact strings are replaced
        for ph, meta in mapping.items():
            if ph in restored:
                # Count occurrences
                count = restored.count(ph)
                restored = restored.replace(ph, meta["value"])
                restoration_log.append({
                    "placeholder": ph,
                    "type": meta["type"],
                    "value": meta["value"],
                    "status": "restored",
                    "occurrences": count
                })
            else:
                missing.append(ph)
                restoration_log.append({
                    "placeholder": ph,
                    "type": meta["type"],
                    "value": meta["value"],
                    "status": "missing"
                })

        # Check if there are any orphan or malformed placeholders remaining: e.g. {{TECH_...}}
        orphan_matches = re.findall(r"\{\{TECH_[A-Z]+_\d+\}\}", restored)
        if orphan_matches:
            for orphan in orphan_matches:
                missing.append(orphan)

        return restored, missing, restoration_log

restorer = RestorationEngine()
