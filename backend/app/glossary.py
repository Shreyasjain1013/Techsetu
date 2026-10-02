import uuid
from typing import Dict, List, Optional
from app.models import GlossaryItem

BUILTIN_GLOSSARY: List[Dict[str, str]] = [
    # Physics & Mechanics
    {"source": "Newton's second law", "target": "न्यूटन का द्वितीय नियम", "cat": "physics"},
    {"source": "Newton's first law", "target": "न्यूटन का प्रथम नियम", "cat": "physics"},
    {"source": "Newton's third law", "target": "न्यूटन का तृतीय नियम", "cat": "physics"},
    {"source": "gravitational constant", "target": "गुरुत्वाकर्षण स्थिरांक", "cat": "physics"},
    {"source": "gravitational force", "target": "गुरुत्वाकर्षण बल", "cat": "physics"},
    {"source": "acceleration due to gravity", "target": "गुरुत्वीय त्वरण", "cat": "physics"},
    {"source": "velocity", "target": "वेग", "cat": "physics"},
    {"source": "acceleration", "target": "त्वरण", "cat": "physics"},
    {"source": "momentum", "target": "संवेग", "cat": "physics"},
    {"source": "force", "target": "बल", "cat": "physics"},
    {"source": "mass", "target": "द्रव्यमान", "cat": "physics"},
    {"source": "weight", "target": "भार", "cat": "physics"},
    {"source": "energy", "target": "ऊर्जा", "cat": "physics"},
    {"source": "kinetic energy", "target": "गतिज ऊर्जा", "cat": "physics"},
    {"source": "potential energy", "target": "स्थितिज ऊर्जा", "cat": "physics"},
    {"source": "conservation of energy", "target": "ऊर्जा संरक्षण", "cat": "physics"},
    {"source": "conservation of momentum", "target": "संवेग संरक्षण", "cat": "physics"},
    {"source": "work", "target": "कार्य", "cat": "physics"},
    {"source": "power", "target": "शक्ति", "cat": "physics"},
    {"source": "frequency", "target": "आवृत्ति", "cat": "physics"},
    {"source": "wavelength", "target": "तरंग दैर्घ्य", "cat": "physics"},
    {"source": "amplitude", "target": "आयाम", "cat": "physics"},
    {"source": "thermodynamics", "target": "ऊष्माप्रवैगिकी", "cat": "physics"},
    {"source": "temperature", "target": "तापमान", "cat": "physics"},
    {"source": "heat", "target": "ऊष्मा", "cat": "physics"},
    {"source": "pressure", "target": "दाब", "cat": "physics"},
    {"source": "volume", "target": "आयतन", "cat": "physics"},
    {"source": "density", "target": "घनत्व", "cat": "physics"},
    {"source": "friction", "target": "घर्षण", "cat": "physics"},
    {"source": "torque", "target": "आघूर्ण (टॉर्क)", "cat": "physics"},

    # Electromagnetism & Circuits
    {"source": "electric current", "target": "विद्युत धारा", "cat": "physics"},
    {"source": "current", "target": "धारा", "cat": "physics"},
    {"source": "voltage", "target": "वोल्टेज", "cat": "physics"},
    {"source": "potential difference", "target": "विभवान्तर", "cat": "physics"},
    {"source": "electric potential", "target": "विद्युत विभव", "cat": "physics"},
    {"source": "resistance", "target": "प्रतिरोध", "cat": "physics"},
    {"source": "resistivity", "target": "प्रतिरोधकता", "cat": "physics"},
    {"source": "capacitance", "target": "धारिता", "cat": "physics"},
    {"source": "capacitor", "target": "संधारित्र", "cat": "physics"},
    {"source": "inductance", "target": "प्रेरकत्व", "cat": "physics"},
    {"source": "inductor", "target": "प्रेरक", "cat": "physics"},
    {"source": "magnetic field", "target": "चुंबकीय क्षेत्र", "cat": "physics"},
    {"source": "electric field", "target": "विद्युत क्षेत्र", "cat": "physics"},
    {"source": "electromagnetic induction", "target": "विद्युत चुम्बकीय प्रेरण", "cat": "physics"},
    {"source": "electrochemical", "target": "विद्युत-रासायनिक", "cat": "chemistry"},
    {"source": "battery", "target": "बैटरी", "cat": "engineering"},
    {"source": "anode", "target": "एनोड", "cat": "chemistry"},
    {"source": "cathode", "target": "कैथोड", "cat": "chemistry"},
    {"source": "electrolyte", "target": "विद्युत अपघट्य", "cat": "chemistry"},

    # Mathematics
    {"source": "derivative", "target": "अवकलज", "cat": "math"},
    {"source": "integration", "target": "समाकलन", "cat": "math"},
    {"source": "integral", "target": "समाकल", "cat": "math"},
    {"source": "differential equation", "target": "अवकल समीकरण", "cat": "math"},
    {"source": "matrix", "target": "आव्यूह (मैट्रिक्स)", "cat": "math"},
    {"source": "vector", "target": "सदिश (वेक्टर)", "cat": "math"},
    {"source": "scalar", "target": "अदिश", "cat": "math"},
    {"source": "eigenvalue", "target": "आइगेनवैल्यू", "cat": "math"},
    {"source": "eigenvector", "target": "आइगेनवेक्टर", "cat": "math"},
    {"source": "probability", "target": "प्रायिकता", "cat": "math"},
    {"source": "random variable", "target": "यादृच्छिक चर", "cat": "math"},
    {"source": "distribution", "target": "वितरण", "cat": "math"},
    {"source": "mean", "target": "माध्य", "cat": "math"},
    {"source": "standard deviation", "target": "मानक विचलन", "cat": "math"},
    {"source": "variance", "target": "प्रसरण", "cat": "math"},

    # Computer Science & AI
    {"source": "algorithm", "target": "एल्गोरिदम", "cat": "cs"},
    {"source": "data structure", "target": "डेटा संरचना", "cat": "cs"},
    {"source": "neural network", "target": "न्यूरल नेटवर्क", "cat": "ai"},
    {"source": "artificial intelligence", "target": "कृत्रिम बुद्धिमत्ता", "cat": "ai"},
    {"source": "machine learning", "target": "मशीन लर्निंग", "cat": "ai"},
    {"source": "deep learning", "target": "डीप लर्निंग", "cat": "ai"},
    {"source": "gradient descent", "target": "ग्रेडिएंट डिसेंट", "cat": "ai"},
    {"source": "backpropagation", "target": "बैकप्रोपेगेशन", "cat": "ai"},
    {"source": "loss function", "target": "हानि फलन (लॉस फलन)", "cat": "ai"},
    {"source": "activation function", "target": "सक्रियण फलन", "cat": "ai"},
    {"source": "dataset", "target": "डेटासेट", "cat": "ai"},
    {"source": "training data", "target": "प्रशिक्षण डेटा", "cat": "ai"},
    {"source": "test data", "target": "परीक्षण डेटा", "cat": "ai"},
    {"source": "linear regression", "target": "रैखिक समाश्रयण", "cat": "ai"},
    {"source": "supervised learning", "target": "पर्यवेक्षित शिक्षण", "cat": "ai"},
    {"source": "unsupervised learning", "target": "अपर्यवेक्षित शिक्षण", "cat": "ai"},
    {"source": "reinforcement learning", "target": "सुदृढ़ीकरण शिक्षण", "cat": "ai"},
    {"source": "overfitting", "target": "अति-सन्निकटन (ओवरफिटिंग)", "cat": "ai"},
    {"source": "underfitting", "target": "अल्प-सन्निकटन (अंडरफिटिंग)", "cat": "ai"},
    {"source": "epoch", "target": "युग (इपोक)", "cat": "ai"},
    {"source": "batch size", "target": "बैच आकार", "cat": "ai"},
    {"source": "hyperparameter", "target": "हाइपरपैरामीटर", "cat": "ai"},
    {"source": "weights and biases", "target": "भार और पूर्वाग्रह (weights and biases)", "cat": "ai"},

    # Biology & Chemistry
    {"source": "photosynthesis", "target": "प्रकाश संश्लेषण", "cat": "biology"},
    {"source": "cellular respiration", "target": "कोशिकीय श्वसन", "cat": "biology"},
    {"source": "mitochondria", "target": "माइटोकॉन्ड्रिया", "cat": "biology"},
    {"source": "chloroplast", "target": "हरितलवक (क्लोरोप्लास्ट)", "cat": "biology"},
    {"source": "enzyme", "target": "एंजाइम", "cat": "biology"},
    {"source": "protein synthesis", "target": "प्रोटीन संश्लेषण", "cat": "biology"},
    {"source": "quantum mechanics", "target": "क्वांटम यांत्रिकी", "cat": "physics"},
    {"source": "special relativity", "target": "विशिष्ट सापेक्षता", "cat": "physics"},
    {"source": "general relativity", "target": "सामान्य सापेक्षता", "cat": "physics"}
]

class GlossaryEngine:
    def __init__(self):
        self.custom_terms: Dict[str, GlossaryItem] = {}

    def get_all_terms(self) -> List[GlossaryItem]:
        items = []
        for i, entry in enumerate(BUILTIN_GLOSSARY):
            items.append(GlossaryItem(
                id=f"builtin-{i}",
                sourceTerm=entry["source"],
                targetTerm=entry["target"],
                language="hi",
                isStrict=True,
                category=entry.get("cat", "general")
            ))
        items.extend(self.custom_terms.values())
        return items

    def add_custom_term(self, source: str, target: str, language: str = "hi", is_strict: bool = True, category: str = "custom") -> GlossaryItem:
        term_id = f"custom-{uuid.uuid4().hex[:8]}"
        item = GlossaryItem(
            id=term_id,
            sourceTerm=source.strip(),
            targetTerm=target.strip(),
            language=language,
            isStrict=is_strict,
            category=category
        )
        self.custom_terms[source.strip().lower()] = item
        return item

    def delete_custom_term(self, term_id: str) -> bool:
        to_del = None
        for k, v in self.custom_terms.items():
            if v.id == term_id:
                to_del = k
                break
        if to_del:
            del self.custom_terms[to_del]
            return True
        return False

    def get_terms_dict(self, extra_custom: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Returns sorted mapping from source term (lowercase) to target Hindi term."""
        mapping = {}
        for entry in BUILTIN_GLOSSARY:
            mapping[entry["source"].lower()] = entry["target"]
        for k, item in self.custom_terms.items():
            mapping[k.lower()] = item.targetTerm
        if extra_custom:
            for k, v in extra_custom.items():
                mapping[k.strip().lower()] = v.strip()
        return mapping

glossary_engine = GlossaryEngine()
