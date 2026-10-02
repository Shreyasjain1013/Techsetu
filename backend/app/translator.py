import os
import re
import logging
from typing import Dict, Optional, List
from app.config import GEMINI_API_KEY
from app.glossary import glossary_engine

logger = logging.getLogger(__name__)

# STEM academic phrases dictionary for deterministic offline translation fallback (Hindi)
STEM_ACADEMIC_PHRASES = {
    "states that": "यह प्रतिपादित करता है कि",
    "states": "बताता है",
    "is given by": "इसके द्वारा दिया जाता है",
    "can be written as": "इस प्रकार लिखा जा सकता है",
    "is defined as": "के रूप में परिभाषित किया गया है",
    "where": "जहाँ",
    "if": "यदि",
    "then": "तो",
    "and": "और",
    "with": "के साथ",
    "the force is": "बल है",
    "the mass is": "द्रव्यमान है",
    "the velocity is": "वेग है",
    "the acceleration is": "त्वरण है",
    "the energy is": "ऊर्जा है",
    "the temperature is": "तापमान है",
    "the pressure is": "दाब है",
    "the current is": "विद्युत धारा है",
    "the voltage is": "वोल्टेज है",
    "the resistance is": "प्रतिरोध है",
    "the calculation can be implemented in python": "यह गणना पायथन (Python) में इस प्रकार कार्यान्वित की जा सकती है",
    "consider a system where": "एक ऐसी प्रणाली पर विचार करें जहाँ",
    "according to": "के अनुसार",
    "shows that": "प्रदर्शित करता है कि",
    "results in": "का परिणाम होता है",
    "proportional to": "के समानुपाती",
    "inversely proportional to": "के व्युत्क्रमानुपाती",
    "let us assume": "मान लीजिए कि",
    "therefore": "अतः",
    "hence": "इस प्रकार",
    "we obtain": "हमें प्राप्त होता है",
    "substituting the values": "मानों को प्रतिस्थापित करने पर",
    "we get": "हमें मिलता है",
    "the following equation": "निम्नलिखित समीकरण",
    "in this experiment": "इस प्रयोग में",
    "experimental results show": "प्रायोगिक परिणाम दर्शाते हैं",
    "overall": "समग्र रूप से",
    "in conclusion": "निष्कर्षतः"
}

# Student-friendly adaptations (Hindi)
STEM_STUDENT_PHRASES = {
    "states that": "सरल शब्दों में कहता है कि",
    "is given by": "को ऐसे निकाला जा सकता है",
    "where": "यहाँ",
    "if": "अगर",
    "then": "तब",
    "the calculation can be implemented in python": "आप इसे पायथन कोड लिखकर आसानी से चला सकते हैं",
    "consider a system where": "मान लीजिए एक स्थिति है जहाँ"
}

# Gen Z Slang Phrases (Hindi / Hinglish slang)
STEM_GEN_Z_PHRASES_HI = {
    "states that": "सीधे फैक्ट्स बोलता है (no cap) कि",
    "states": "बोलता है",
    "is given by": "का असली सीन ये है कि",
    "can be written as": "को ऐसे लिख सकते हैं (it's giving)",
    "is defined as": "का सिंपल मतलब ये है",
    "where": "जहाँ सीन ये है कि",
    "let us assume": "सोचो एक हाइपोथेटिकल सीन जहाँ",
    "therefore": "सो बेसिकली",
    "hence": "तो ब्रो",
    "we get": "अपन को मिलता है (we cooked)",
    "we obtain": "अपने हाथ लगता है",
    "the force is": "फोर्स का सीन है",
    "the mass is": "मास है",
    "the acceleration is": "एक्सेलेरेशन है",
    "shows that": "सीधा फ्लेक्स करता है कि",
    "results in": "का एंड रिजल्ट है",
    "the calculation can be implemented in python": "पायथन में ये कोड सीधा रन करेगा (clean code fr)",
    "overall": "ओवरऑल वाइब ये है कि",
    "in conclusion": "फाइनल वाइब चेक ये है:"
}

# Corporate Professional Phrases (Hindi)
STEM_CORPORATE_PHRASES_HI = {
    "states that": "स्पष्ट रूप से संरेखित (align) करता है कि",
    "states": "इंगित करता है",
    "is given by": "इस मुख्य मीट्रिक द्वारा निर्धारित है",
    "can be written as": "मानकीकृत रूप में प्रस्तुत किया जा सकता है",
    "is defined as": "के परिचालन मानदंड के रूप में परिभाषित है",
    "where": "जिसमें प्रमुख वेरिएबल्स हैं",
    "let us assume": "रणनीतिक परिदृश्य की कल्पना करें जहाँ",
    "therefore": "व्यावसायिक व तकनीकी दृष्टिकोण से अतः",
    "hence": "तदनुसार",
    "we get": "हमारा मुख्य आउटकम/डिलिवरेबल है",
    "we obtain": "प्राप्त परिणाम है",
    "shows that": "डेटा-ड्रिवन अंतर्दृष्टि इंगित करती है कि",
    "results in": "का रणनीतिक परिणाम है",
    "the calculation can be implemented in python": "इस पाइपलाइन को पायथन में क्रियान्वित किया जा सकता है",
    "overall": "व्यापक मूल्यांकन के अनुसार",
    "in conclusion": "कार्यकारी सारांश (Executive Summary):"
}

# Empathetic Mentor Phrases (Hindi)
STEM_EMPATHETIC_PHRASES_HI = {
    "states that": "प्यार से समझाता है (घबराइए मत, बहुत आसान है) कि",
    "states": "समझाता है",
    "is given by": "को आप बहुत आसानी से ऐसे समझ सकते हैं",
    "can be written as": "को सरलता से ऐसे लिखा जा सकता है",
    "is defined as": "को समझने के लिए ऐसे परिभाषित किया गया है",
    "where": "जहाँ आइए मिलकर देखें कि",
    "let us assume": "आइए आराम से एक स्थिति पर विचार करें जहाँ",
    "therefore": "इसलिए आप समझ सकते हैं कि",
    "hence": "इस प्यारे तरीके से",
    "we get": "देखिए, हमें बहुत आसानी से यह परिणाम मिलता है",
    "we obtain": "हमें सरलता से मिलता है",
    "shows that": "सुंदरता से दर्शाता है कि",
    "results in": "का सुंदर परिणाम मिलता है",
    "the calculation can be implemented in python": "आप इसे छोटे से पायथन कोड से खुद चलाकर देख सकते हैं",
    "overall": "पूरे मन से समझने पर",
    "in conclusion": "आसानी से याद रखने योग्य मुख्य सीख:"
}

# Bhojpuri STEM Academic Phrases (भोजपुरी)
BHOJPURI_ACADEMIC_PHRASES = {
    "states that": "ई बतावेला कि",
    "states": "बतावेला",
    "is given by": "एहसे निकालल जा सकेला",
    "can be written as": "एह तरे लिखल जा सकेला",
    "is defined as": "के रूप में परिभाषित कइल गइल बा",
    "where": "जहाँ",
    "if": "अगर",
    "then": "त",
    "and": "आउर",
    "with": "के साथ",
    "the force is": "बल बा",
    "the mass is": "द्रव्यमान बा",
    "the velocity is": "वेग बा",
    "the acceleration is": "त्वरण बा",
    "the energy is": "ऊर्जा बा",
    "the temperature is": "तापमान बा",
    "the pressure is": "दाब बा",
    "the current is": "विद्युत धारा बा",
    "the voltage is": "वोल्टेज बा",
    "the resistance is": "प्रतिरोध बा",
    "the calculation can be implemented in python": "ई गणना पायथन (Python) में एह तरे कइल जा सकेला",
    "consider a system where": "मान लीं एगो प्रणाली जहाँ",
    "according to": "के अनुसार",
    "shows that": "देखावेला कि",
    "results in": "का परिणाम आवेला",
    "proportional to": "के समानुपाती बा",
    "inversely proportional to": "के व्युत्क्रमानुपाती बा",
    "let us assume": "मान लीं कि",
    "therefore": "एहसे",
    "hence": "एह प्रकार",
    "we obtain": "हमन के मिलेला",
    "substituting the values": "मान रखला पर",
    "we get": "हमन के मिलेला",
    "the following equation": "नीचे दिहल समीकरण",
    "in this experiment": "एह प्रयोग में",
    "experimental results show": "प्रायोगिक परिणाम देखावेला",
    "overall": "समग्र रूप से",
    "in conclusion": "निष्कर्ष में"
}

# Bhojpuri Gen Z Phrases
STEM_GEN_Z_PHRASES_BHO = {
    "states that": "सीधे सच बतावेला (no cap) कि",
    "states": "बतावेला",
    "is given by": "के असली सीन ई बा कि",
    "can be written as": "एह तरे लिखल जा सकेला (it's giving)",
    "is defined as": "के सिंपल मतलब ई बा",
    "where": "जहाँ सीन ई बा कि",
    "let us assume": "सोचीं एगो हाइपोथेटिकल सीन जहाँ",
    "therefore": "त बेसिकली",
    "hence": "त भाई",
    "we get": "हमन के मिलेला (we cooked)",
    "the force is": "फोर्स के सीन बा",
    "the mass is": "मास बा",
    "the acceleration is": "एक्सेलेरेशन बा",
    "shows that": "सीधा फ्लेक्स करेला कि",
    "the calculation can be implemented in python": "पायथन में ई कोड सीधा दौड़ी (clean code fr)",
    "in conclusion": "फाइनल वाइब चेक ई बा:"
}

# Bhojpuri Corporate Phrases
STEM_CORPORATE_PHRASES_BHO = {
    "states that": "स्पष्ट रूप से संरेखित करेला कि",
    "is given by": "एह मुख्य मीट्रिक द्वारा निर्धारित बा",
    "can be written as": "मानकीकृत रूप में प्रस्तुत कइल जा सकेला",
    "is defined as": "के परिचालन मानदंड के रूप में परिभाषित बा",
    "where": "जहवाँ प्रमुख वेरिएबल्स बा",
    "we get": "हमन के मुख्य आउटकम बा",
    "shows that": "डेटा-ड्रिवन अंतर्दृष्टि इंगित करेला कि",
    "the calculation can be implemented in python": "एह पाइपलाइन के पायथन में क्रियान्वित कइल जा सकेला",
    "in conclusion": "कार्यकारी सारांश:"
}

# Bhojpuri Empathetic Phrases
STEM_EMPATHETIC_PHRASES_BHO = {
    "states that": "प्यार से समझावेला (घबराईं मत, बहुत सहज बा) कि",
    "is given by": "के रउआ बहुत सहजता से एह तरे समझ सकीं",
    "can be written as": "के सरलता से एह तरे लिखल जा सकेला",
    "is defined as": "के समझे खातिर एह रूप में परिभाषित कइल गइल बा",
    "where": "जहाँ आईं मिल के देखीं कि",
    "let us assume": "आईं आराम से एगो स्थिति पर विचार करीं जहाँ",
    "we get": "देखीं, हमन के ई सहज परिणाम मिलेला",
    "shows that": "सुंदरता से देखावेला कि",
    "the calculation can be implemented in python": "रउआ एहके छोटहन पायथन कोड से खुद चला के देख सकीं",
    "in conclusion": "सहजता से याद रखे लायक सीख:"
}

# Connectives for Hindi
HINDI_CONNECTIVES = {
    "states:": "बताता है:",
    "is:": "है:",
    "are:": "हैं:",
    "the": "",
    "is": "है",
    "are": "हैं",
    "of": "का",
    "in": "में",
    "on": "पर",
    "to": "को",
    "for": "के लिए",
    "with": "के साथ",
    "by": "द्वारा",
    "from": "से",
    "between": "के बीच",
    "where": "जहाँ",
    "which": "जो",
    "that": "कि",
    "this": "यह",
    "these": "ये",
    "can be": "हो सकता है",
    "calculated": "परिकलित",
    "determined": "निर्धारित",
    "measured": "मापा गया",
    "observed": "देखा गया"
}

# Connectives for Bhojpuri
BHOJPURI_CONNECTIVES = {
    "states:": "बतावेला:",
    "is:": "बा:",
    "are:": "बाड़ीं:",
    "the": "",
    "is": "बा",
    "are": "बाड़ीं",
    "of": "के",
    "in": "में",
    "on": "पर",
    "to": "के",
    "for": "खातिर",
    "with": "के साथ",
    "by": "द्वारा",
    "from": "से",
    "between": "के बीच में",
    "where": "जहाँ",
    "which": "जे",
    "that": "कि",
    "this": "ई",
    "these": "ई सभ",
    "can be": "हो सकेला",
    "calculated": "परिकलित",
    "determined": "निर्धारित",
    "measured": "नापल गइल",
    "observed": "देखल गइल"
}

class TranslationEngine:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Gemini GenAI client successfully initialized.")
            except Exception as e:
                logger.warning(f"Could not initialize Google GenAI Client: {e}")

    def translate(
        self,
        protected_text: str,
        mode: str = "academic",
        target_language: str = "hi",
        tone: str = "academic",
        extra_glossary: Optional[Dict[str, str]] = None
    ) -> str:
        """Translates protected text from English to Hindi or Bhojpuri while keeping placeholders intact."""
        # Try Gemini API if available
        if self.client and self.api_key:
            try:
                result = self._translate_with_gemini(protected_text, mode, target_language, tone, extra_glossary)
                if result and len(result.strip()) > 0:
                    return result
            except Exception as e:
                logger.error(f"Gemini API translation error: {e}. Falling back to Academic Offline Engine.")

        # Fallback to intelligent deterministic engine with tone support
        return self._translate_deterministic(protected_text, mode, target_language, tone, extra_glossary)

    def _translate_with_gemini(
        self,
        protected_text: str,
        mode: str,
        target_language: str,
        tone: str,
        extra_glossary: Optional[Dict[str, str]]
    ) -> str:
        glossary_items = glossary_engine.get_terms_dict(extra_glossary)
        relevant_terms = [
            f"{k} -> {v}" for k, v in glossary_items.items()
            if k.lower() in protected_text.lower()
        ]
        glossary_prompt_part = ""
        if relevant_terms:
            glossary_prompt_part = "\nSTRICT GLOSSARY TERMS (MUST USE THESE EQUIVALENTS):\n" + "\n".join(relevant_terms)

        lang_name = "Bhojpuri (भोजपुरी)" if target_language == "bho" else "Hindi (हिंदी)"
        
        # Tone specific instruction
        if tone == "gen_z":
            tone_instruction = (
                "STYLE & TONE: Gen Z Slang / Casual Explainer (no cap, fr fr, high energy). "
                "Explain the natural language using relatable, modern youth idioms, colloquial phrasing, "
                "and energetic Hinglish/Hindi/Bhojpuri expressions (e.g. 'no cap', 'we cooked', 'its giving', 'scene ye hai', 'chill hoke samjho'). "
                "Make it super engaging and accessible for students while keeping technical explanations 100% accurate."
            )
        elif tone == "corporate":
            tone_instruction = (
                "STYLE & TONE: Corporate Professional / Executive Briefing. "
                "Frame the explanation in polished, structured corporate consulting style "
                "(focusing on operational metrics, strategic alignment, executive clarity, deliverables, and actionable insights)."
            )
        elif tone == "empathetic":
            tone_instruction = (
                "STYLE & TONE: Empathetic Mentor / Encouraging Tutor. "
                "Explain with great warmth, patience, encouragement, and pedagogical care. "
                "Reassure the learner, break down intimidation, use supportive phrases ('Let's see together', 'You've got this', 'Notice how simple this step is')."
            )
        else: # academic
            tone_instruction = (
                "STYLE & TONE: Academic Rigor. "
                "Use formal, rigorous Indian university academic scientific terminology (Devanagari script) with authoritative clarity."
            )

        mode_instruction = ""
        if target_language == "bho":
            mode_instruction = (
                "Translate into authentic, fluent Bhojpuri (भोजपुरी) in Devanagari script for STEM learners. "
                "Use natural Bhojpuri grammar and expressions (e.g. 'न्यूटन के दूसरका नियम ई बतावेला कि...', "
                "'बल बा 49 N', 'जहाँ द्रव्यमान 5 kg बा', 'त ई गणना पायथन में कइल जा सकेला')."
            )
        else:
            mode_instruction = (
                "Use formal, rigorous Indian university academic scientific Hindi (Devanagari script)."
                if mode == "academic"
                else "Use clear, accessible, conceptual Hindi for students while maintaining 100% technical rigor."
            )

        system_instruction = (
            f"You are TechSetu, an expert academic scientific translator specializing in STEM literature translation "
            f"from English into {lang_name}.\n\n"
            "CRITICAL RULES:\n"
            "1. TRANSLATE NATURAL LANGUAGE ONLY.\n"
            "2. ABSOLUTELY NEVER MODIFY, DELETE, OR TRANSLATE ANY PLACEHOLDER!\n"
            "   Placeholders look exactly like: {{TECH_EQ_001}}, {{TECH_NUM_001}}, {{TECH_UNIT_001}}, {{TECH_CODE_001}}, {{TECH_CIT_001}}.\n"
            "   They must appear verbatim in your output.\n"
            "3. Preserve all Markdown structure, headers (#, ##), and bullet points.\n"
            "4. Do NOT translate programming syntax or LaTeX formulas.\n"
            f"5. {tone_instruction}\n"
            f"6. {mode_instruction}\n"
            f"{glossary_prompt_part}\n"
            "Output ONLY the translated text without conversational intro or preamble."
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=protected_text,
            config={
                "system_instruction": system_instruction,
                "temperature": 0.2 if tone == "gen_z" else 0.1
            }
        )
        return response.text

    def _translate_deterministic(
        self,
        protected_text: str,
        mode: str,
        target_language: str,
        tone: str,
        extra_glossary: Optional[Dict[str, str]]
    ) -> str:
        """Deterministic translation fallback that preserves all placeholders and converts STEM prose with tone."""
        glossary = glossary_engine.get_terms_dict(extra_glossary)
        
        if target_language == "bho":
            connectives = BHOJPURI_CONNECTIVES
            if tone == "gen_z":
                phrases = {**BHOJPURI_ACADEMIC_PHRASES, **STEM_GEN_Z_PHRASES_BHO}
            elif tone == "corporate":
                phrases = {**BHOJPURI_ACADEMIC_PHRASES, **STEM_CORPORATE_PHRASES_BHO}
            elif tone == "empathetic":
                phrases = {**BHOJPURI_ACADEMIC_PHRASES, **STEM_EMPATHETIC_PHRASES_BHO}
            else:
                phrases = BHOJPURI_ACADEMIC_PHRASES
        else:
            connectives = HINDI_CONNECTIVES
            if tone == "gen_z":
                phrases = {**STEM_ACADEMIC_PHRASES, **STEM_GEN_Z_PHRASES_HI}
            elif tone == "corporate":
                phrases = {**STEM_ACADEMIC_PHRASES, **STEM_CORPORATE_PHRASES_HI}
            elif tone == "empathetic":
                phrases = {**STEM_ACADEMIC_PHRASES, **STEM_EMPATHETIC_PHRASES_HI}
            elif mode == "student_friendly":
                phrases = STEM_STUDENT_PHRASES
            else:
                phrases = STEM_ACADEMIC_PHRASES
        
        lines = protected_text.split("\n")
        translated_lines = []

        for line in lines:
            if not line.strip():
                translated_lines.append("")
                continue

            # If the line is purely a placeholder or header, preserve structure
            if re.match(r"^\{\{TECH_[A-Z]+_\d+\}\}$", line.strip()):
                translated_lines.append(line)
                continue

            curr_line = line

            # 1. Apply Glossary terms
            sorted_terms = sorted(glossary.keys(), key=len, reverse=True)
            for en_term in sorted_terms:
                target_term = glossary[en_term]
                # If Bhojpuri, customize specific common terms if appropriate
                if target_language == "bho" and en_term.lower() == "newton's second law":
                    target_term = "न्यूटन के दूसरका नियम"
                curr_line = re.sub(
                    rf"\b{re.escape(en_term)}\b",
                    target_term,
                    curr_line,
                    flags=re.IGNORECASE
                )

            # 2. Apply academic phrases
            sorted_phrases = sorted(phrases.keys(), key=len, reverse=True)
            for en_p in sorted_phrases:
                target_p = phrases[en_p]
                curr_line = re.sub(
                    rf"\b{re.escape(en_p)}\b",
                    target_p,
                    curr_line,
                    flags=re.IGNORECASE
                )

            # 3. Apply connectives
            for en_w, target_w in connectives.items():
                pattern = r"(?<!\{\{)\b" + re.escape(en_w) + r"\b(?!\}\})"
                curr_line = re.sub(
                    pattern,
                    target_w,
                    curr_line,
                    flags=re.IGNORECASE
                )

            # Clean double spaces
            curr_line = re.sub(r"[ ]{2,}", " ", curr_line).strip()
            translated_lines.append(curr_line)

        return "\n".join(translated_lines)

translator = TranslationEngine()
