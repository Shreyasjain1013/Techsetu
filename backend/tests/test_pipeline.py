import pytest
from app.detector import detector
from app.protector import protector
from app.translator import translator
from app.restorer import restorer
from app.validator import validator
from app.glossary import glossary_engine

def test_t1_basic_translation():
    text = "Photosynthesis is the process by which green plants synthesize nutrients."
    counts, _ = detector.analyze(text)
    protected, mapping = protector.protect(text)
    trans = translator.translate(protected, mode="academic")
    restored, missing, log = restorer.restore(trans, mapping)
    val, warnings, _ = validator.validate(text, restored, counts, restoration_log=log)
    assert len(restored.strip()) > 0
    assert "प्रकाश संश्लेषण" in restored

def test_t2_equation_preservation():
    text = "Newton's second law is given by F = ma where force is calculated directly."
    counts, elements = detector.analyze(text)
    assert counts.equations >= 1
    protected, mapping = protector.protect(text)
    assert any("TECH_EQ" in k for k in mapping.keys())
    trans = translator.translate(protected, mode="academic")
    restored, missing, log = restorer.restore(trans, mapping)
    assert "F = ma" in restored
    val, _, _ = validator.validate(text, restored, counts, restoration_log=log)
    assert val.equations.preserved == val.equations.original

def test_t3_number_preservation():
    text = "The acceleration due to gravity on Earth is 9.81 and the constant is 3.14."
    counts, _ = detector.analyze(text)
    assert counts.numbers >= 2
    protected, mapping = protector.protect(text)
    trans = translator.translate(protected, mode="academic")
    restored, missing, log = restorer.restore(trans, mapping)
    assert "9.81" in restored
    assert "3.14" in restored

def test_t4_unit_preservation():
    text = "The mass is 5 kg and velocity is 12 m/s."
    counts, _ = detector.analyze(text)
    assert counts.units >= 2
    protected, mapping = protector.protect(text)
    trans = translator.translate(protected, mode="academic")
    restored, missing, log = restorer.restore(trans, mapping)
    assert "kg" in restored
    assert "m/s" in restored

def test_t5_code_preservation():
    text = "Calculate force using Python:\n```python\ndef calc_force(m, a):\n    return m * a\n```\nIt is simple."
    counts, _ = detector.analyze(text)
    assert counts.codeBlocks >= 1
    protected, mapping = protector.protect(text)
    trans = translator.translate(protected, mode="academic")
    restored, missing, log = restorer.restore(trans, mapping)
    assert "def calc_force(m, a):" in restored
    assert "```python" in restored

def test_t6_citation_preservation():
    text = "Recent experimental findings [12] demonstrate quantum coherence in photosynthesis."
    counts, _ = detector.analyze(text)
    assert counts.citations >= 1
    protected, mapping = protector.protect(text)
    trans = translator.translate(protected, mode="academic")
    restored, missing, log = restorer.restore(trans, mapping)
    assert "[12]" in restored

def test_t7_glossary_enforcement():
    text = "The machine learning algorithm optimizes the neural network."
    counts, _ = detector.analyze(text)
    protected, mapping = protector.protect(text)
    trans = translator.translate(protected, mode="academic")
    restored, missing, log = restorer.restore(trans, mapping)
    assert "मशीन लर्निंग" in restored
    assert "एल्गोरिदम" in restored
    assert "न्यूरल नेटवर्क" in restored

def test_t8_corruption_detection():
    # Demonstrates that if 9.81 is altered to 9.18, the validator detects it
    text = "The gravitational constant acceleration is 9.81 m/s^2."
    counts, _ = detector.analyze(text)
    protected, mapping = protector.protect(text)
    trans = translator.translate(protected, mode="academic")
    restored, missing, log = restorer.restore(trans, mapping)
    
    # Deliberately corrupt 9.81 to 9.18
    corrupted = restored.replace("9.81", "9.18")
    val, warnings, _ = validator.validate(text, corrupted, counts, restoration_log=log)
    
    # Validator must flag corruption
    assert any("9.81" in w for w in warnings)
    assert val.integrityScore < 100.0

def test_t9_empty_input():
    counts, _ = detector.analyze("")
    assert counts.words == 0
    assert counts.equations == 0

def test_t10_full_scientific_paper_slice():
    text = (
        "## Dynamics of Classical Systems\n\n"
        "Newton's second law states that:\n\n"
        "$$\nF = m \\cdot a\n$$\n\n"
        "Consider an experimental body with mass 5 kg and acceleration 9.8 m/s^2.\n"
        "According to recent findings [1], the resultant force is calculated as:\n\n"
        "```python\n"
        "force = 5.0 * 9.8\n"
        "print(f'Force: {force} N')\n"
        "```\n\n"
        "The calculated force is 49 N."
    )
    counts, elements = detector.analyze(text)
    assert counts.equations >= 1
    assert counts.codeBlocks >= 1
    assert counts.citations >= 1
    assert counts.units >= 2
    assert counts.numbers >= 3

    protected, mapping = protector.protect(text)
    trans = translator.translate(protected, mode="academic")
    restored, missing, log = restorer.restore(trans, mapping)
    val, warnings, details = validator.validate(text, restored, counts, restoration_log=log)

    assert "F = m \\cdot a" in restored or "F = m" in restored
    assert "49" in restored
    assert "N" in restored
    assert "[1]" in restored
    assert val.integrityScore >= 95.0

def test_t11_bhojpuri_translation():
    text = "Newton's second law states that F = ma with mass 5 kg."
    counts, _ = detector.analyze(text)
    protected, mapping = protector.protect(text)
    trans = translator.translate(protected, mode="academic", target_language="bho")
    restored, missing, log = restorer.restore(trans, mapping)
    val, warnings, _ = validator.validate(text, restored, counts, restoration_log=log, target_language="bho")

    assert "F = ma" in restored
    assert "5 kg" in restored or ("5" in restored and "kg" in restored)
    assert val.integrityScore >= 95.0
    assert val.equations.preserved == 1

def test_t12_document_and_image_upload():
    import io
    from PIL import Image
    from pypdf import PdfWriter
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    # Test PDF upload
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    buf_pdf = io.BytesIO()
    writer.write(buf_pdf)
    buf_pdf.seek(0)
    res_pdf = client.post('/api/upload-file', files={'file': ('test.pdf', buf_pdf.getvalue(), 'application/pdf')})
    assert res_pdf.status_code == 200
    assert len(res_pdf.json()['extractedContent']) > 0

    # Test Image upload (PNG)
    img = Image.new('RGB', (200, 100), color=(10, 20, 30))
    buf_img = io.BytesIO()
    img.save(buf_img, format='PNG')
    buf_img.seek(0)
    res_img = client.post('/api/upload-file', files={'file': ('diagram.png', buf_img.getvalue(), 'image/png')})
    assert res_img.status_code == 200
    assert len(res_img.json()['extractedContent']) > 0

if __name__ == "__main__":
    pytest.main(["-v", __file__])

