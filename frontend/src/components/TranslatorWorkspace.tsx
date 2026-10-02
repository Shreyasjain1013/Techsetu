import React, { useState, useEffect, useRef } from 'react';
import {
  Sparkles, RotateCcw, Copy, Check, Download, Upload,
  Cpu, FileText, ArrowRight, ShieldCheck, AlertCircle, RefreshCw, BookOpen,
  Image as ImageIcon, ChevronDown, CheckCircle2
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { AnalysisCounts, ElementDetail, TranslateResponse, ValidationResult } from '../types';
import { translateAndValidate, analyzeContent, uploadDocumentOrImage, testCorruption } from '../api';
import { LaTeXRenderer } from './LaTeXRenderer';
import { IntegrityPanel } from './IntegrityPanel';

const STEM_SAMPLES = {
  mechanics: `## Dynamics of Classical Systems

Newton's second law states that:

$$
F = m \\cdot a
$$

Consider an experimental body with mass 5 kg and acceleration 9.8 m/s^2.
According to classical gravitation [1], the resultant force is 49 N.

The calculation can be implemented in Python:

\`\`\`python
def calculate_force(mass_kg, accel_mps2):
    return mass_kg * accel_mps2

force_newtons = calculate_force(5.0, 9.8)
print(f"Resultant Force: {force_newtons} N")
\`\`\`

Under constant gravitational force, velocity is given by v = u + at.`,

  thermodynamics: `## Thermodynamics and Kinetic Theory

The ideal gas law expresses the state of a gas as:

$$
P \\cdot V = n \\cdot R \\cdot T
$$

Where the pressure is 101.3 kPa, volume is 0.0224 m^3, and temperature is 273.15 K.
The molar gas constant is R = 8.314 J/mol.

According to recent chemical kinetics studies [2], the root-mean-square velocity of particles is:

$$
v_{\\text{rms}} = \\sqrt{\\frac{3 \\cdot R \\cdot T}{M}}
$$

At a frequency of 50 Hz and temperature of 100 °C, the electrochemical potential difference remains stable at 1.5 V.`,

  ai: `## Neural Network Optimization with Gradient Descent

A deep learning neural network optimizes its loss function using gradient descent.
The weight update equation is defined as:

$$
w_{t+1} = w_t - \\eta \\cdot \\nabla L(w_t)
$$

Where the learning rate is 0.001 and batch size is 32.
The activation function for hidden layers is ReLU:

\`\`\`python
import numpy as np

def relu_activation(x):
    return np.maximum(0, x)

weights = np.array([0.25, -0.45, 0.85])
\`\`\`

As demonstrated in recent benchmark literature [3], training on a dataset of 50000 samples for 100 epochs yields an accuracy of 98.6%.`,
};

export const TranslatorWorkspace: React.FC = () => {
  const [content, setContent] = useState<string>(STEM_SAMPLES.mechanics);
  const [mode, setMode] = useState<'academic' | 'student_friendly'>('academic');
  const [targetLang, setTargetLang] = useState<'hi' | 'bho'>('hi');
  const [showUploadMenu, setShowUploadMenu] = useState<boolean>(false);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [uploadStatusText, setUploadStatusText] = useState<string>('');
  const [analysis, setAnalysis] = useState<AnalysisCounts>({
    words: 0,
    characters: 0,
    equations: 0,
    numbers: 0,
    units: 0,
    codeBlocks: 0,
    citations: 0,
    technicalTerms: 0,
  });
  const [translationResult, setTranslationResult] = useState<TranslateResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [copied, setCopied] = useState<boolean>(false);
  const [isTestingCorruption, setIsTestingCorruption] = useState<boolean>(false);

  const pdfInputRef = useRef<HTMLInputElement>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);
  const anyFileInputRef = useRef<HTMLInputElement>(null);
  const uploadMenuRef = useRef<HTMLDivElement>(null);

  // Close upload menu on outside click
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (uploadMenuRef.current && !uploadMenuRef.current.contains(event.target as Node)) {
        setShowUploadMenu(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Run live pre-analysis on content changes
  useEffect(() => {
    if (!content.trim()) {
      setAnalysis({
        words: 0,
        characters: 0,
        equations: 0,
        numbers: 0,
        units: 0,
        codeBlocks: 0,
        citations: 0,
        technicalTerms: 0,
      });
      return;
    }

    const timer = setTimeout(async () => {
      try {
        const res = await analyzeContent(content);
        setAnalysis(res.analysis);
      } catch {
        setAnalysis((prev) => ({
          ...prev,
          words: content.trim().split(/\s+/).length,
          characters: content.length,
        }));
      }
    }, 250);

    return () => clearTimeout(timer);
  }, [content]);

  const handleTranslate = async () => {
    if (!content.trim()) {
      setErrorMessage('Please enter technical STEM content to translate.');
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      const res = await translateAndValidate(content, mode, targetLang);
      setTranslationResult(res);

      // Trigger celebratory confetti if high integrity score
      if (res.validation.integrityScore >= 95.0) {
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.7 },
          colors: ['#06b6d4', '#10b981', '#38bdf8'],
        });
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'Translation service temporarily unavailable. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setContent('');
    setTranslationResult(null);
    setErrorMessage(null);
  };

  const handleLoadSample = (sampleKey: keyof typeof STEM_SAMPLES) => {
    setContent(STEM_SAMPLES[sampleKey]);
    setTranslationResult(null);
    setErrorMessage(null);
  };

  const handleCopy = () => {
    if (!translationResult) return;
    navigator.clipboard.writeText(translationResult.translatedContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    if (!translationResult) return;
    const langLabel = targetLang === 'bho' ? 'Bhojpuri' : 'Hindi';
    const blob = new Blob([translationResult.translatedContent], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `TechSetu_${langLabel}_${Date.now()}.md`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleFileUpload = async (file: File) => {
    setIsUploading(true);
    setShowUploadMenu(false);
    setErrorMessage(null);
    setUploadStatusText(`Extracting scientific content from ${file.name}...`);

    try {
      const res = await uploadDocumentOrImage(file);
      setContent(res.extractedContent);
      setTranslationResult(null);
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to process document or image');
    } finally {
      setIsUploading(false);
      setUploadStatusText('');
      if (pdfInputRef.current) pdfInputRef.current.value = '';
      if (imageInputRef.current) imageInputRef.current.value = '';
      if (anyFileInputRef.current) anyFileInputRef.current.value = '';
    }
  };

  const handleTriggerCorruptionDemo = async () => {
    setIsTestingCorruption(true);
    try {
      const res = await testCorruption(content, '9.18');
      if (translationResult) {
        setTranslationResult({
          ...translationResult,
          status: 'warning',
          translatedContent: res.corruptedContent,
          validation: res.validation,
          warnings: res.warnings,
        });
      }
    } catch (err: any) {
      alert('Corruption demo failed: ' + err.message);
    } finally {
      setIsTestingCorruption(false);
    }
  };

  const targetLangLabel = targetLang === 'bho' ? 'Bhojpuri (भोजपुरी)' : 'Hindi (हिंदी)';

  return (
    <div className="workspace-wrapper">
      {/* Workspace Toolbar */}
      <div className="workspace-toolbar">
        <div className="toolbar-controls-group">
          {/* Language Pair Selector (English -> Hindi or Bhojpuri) */}
          <div className="lang-selector-box" style={{ gap: '0.5rem' }}>
            <span>English (en)</span>
            <ArrowRight size={14} color="#06b6d4" />
            <select
              value={targetLang}
              onChange={(e) => {
                setTargetLang(e.target.value as 'hi' | 'bho');
                setTranslationResult(null);
              }}
              style={{
                background: 'transparent',
                border: 'none',
                color: '#38bdf8',
                fontWeight: 700,
                fontSize: '0.88rem',
                cursor: 'pointer',
                outline: 'none',
                fontFamily: 'inherit',
              }}
            >
              <option value="hi" style={{ background: '#0f172a', color: '#fff' }}>Hindi (हिंदी)</option>
              <option value="bho" style={{ background: '#0f172a', color: '#38bdf8' }}>Bhojpuri (भोजपुरी)</option>
            </select>
          </div>

          {/* Mode Selector */}
          <div className="mode-selector-box">
            <button
              className={`mode-btn ${mode === 'academic' ? 'active' : ''}`}
              onClick={() => setMode('academic')}
            >
              Academic Mode (P0)
            </button>
            <button
              className={`mode-btn ${mode === 'student_friendly' ? 'active' : ''}`}
              onClick={() => setMode('student_friendly')}
            >
              Student-Friendly (P1)
            </button>
          </div>
        </div>

        <div className="toolbar-controls-group">
          {/* Quick STEM Sample Selector */}
          <select
            className="sample-selector"
            onChange={(e) => handleLoadSample(e.target.value as any)}
            defaultValue="mechanics"
          >
            <option value="mechanics">Physics: Classical Mechanics (Newton's Laws)</option>
            <option value="thermodynamics">Chemistry/Physics: Thermodynamics & Gases</option>
            <option value="ai">Computer Science: Neural Networks & Gradient Descent</option>
          </select>

          {/* Unified Upload Button with Dropdown for PDF & Image */}
          <div style={{ position: 'relative' }} ref={uploadMenuRef}>
            {/* Hidden native file inputs */}
            <input
              type="file"
              ref={pdfInputRef}
              accept=".pdf"
              style={{ display: 'none' }}
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) handleFileUpload(f);
              }}
            />
            <input
              type="file"
              ref={imageInputRef}
              accept="image/png,image/jpeg,image/webp,image/bmp"
              style={{ display: 'none' }}
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) handleFileUpload(f);
              }}
            />
            <input
              type="file"
              ref={anyFileInputRef}
              accept=".pdf,image/png,image/jpeg,image/webp,image/bmp"
              style={{ display: 'none' }}
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) handleFileUpload(f);
              }}
            />

            <button
              className="btn-secondary"
              style={{ padding: '0.45rem 0.85rem', fontSize: '0.82rem', gap: '0.4rem' }}
              onClick={() => setShowUploadMenu(!showUploadMenu)}
              disabled={isUploading}
            >
              {isUploading ? (
                <>
                  <RefreshCw size={14} className="spin" style={{ animation: 'spin 1s linear infinite' }} />
                  Extracting...
                </>
              ) : (
                <>
                  <Upload size={14} color="#06b6d4" />
                  Upload
                  <ChevronDown size={13} color="#94a3b8" />
                </>
              )}
            </button>

            {/* Upload Options Menu */}
            {showUploadMenu && (
              <div
                style={{
                  position: 'absolute',
                  top: '115%',
                  right: 0,
                  width: '240px',
                  background: 'var(--bg-card)',
                  border: '1px solid var(--border-card)',
                  borderRadius: '8px',
                  boxShadow: 'var(--shadow-md)',
                  zIndex: 50,
                  padding: '0.4rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.25rem',
                }}
              >
                <div
                  style={{
                    fontSize: '0.72rem',
                    color: '#94a3b8',
                    padding: '0.3rem 0.6rem',
                    fontWeight: 600,
                    textTransform: 'uppercase',
                    borderBottom: '1px solid rgba(255,255,255,0.06)',
                  }}
                >
                  Select File Type
                </div>

                <button
                  type="button"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.6rem',
                    background: 'transparent',
                    border: 'none',
                    color: '#f8fafc',
                    padding: '0.6rem 0.75rem',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '0.85rem',
                    textAlign: 'left',
                    transition: 'background 0.15s ease',
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = 'var(--bg-card-hover)')}
                  onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
                  onClick={() => {
                    setShowUploadMenu(false);
                    pdfInputRef.current?.click();
                  }}
                >
                  <FileText size={16} color="#ef4444" />
                  <div>
                    <div style={{ fontWeight: 600 }}>PDF Document</div>
                    <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Academic papers (.pdf)</div>
                  </div>
                </button>

                <button
                  type="button"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.6rem',
                    background: 'transparent',
                    border: 'none',
                    color: '#f8fafc',
                    padding: '0.6rem 0.75rem',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '0.85rem',
                    textAlign: 'left',
                    transition: 'background 0.15s ease',
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = 'var(--bg-card-hover)')}
                  onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
                  onClick={() => {
                    setShowUploadMenu(false);
                    imageInputRef.current?.click();
                  }}
                >
                  <ImageIcon size={16} color="#06b6d4" />
                  <div>
                    <div style={{ fontWeight: 600 }}>Image / Diagram</div>
                    <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Formulas & figures (PNG, JPG)</div>
                  </div>
                </button>
              </div>
            )}
          </div>

          {/* Clear button */}
          <button
            className="btn-secondary"
            style={{ padding: '0.45rem 0.85rem', fontSize: '0.82rem' }}
            onClick={handleClear}
          >
            <RotateCcw size={14} />
            Clear
          </button>

          {/* Translate and Verify CTA */}
          <button
            className="btn-primary"
            style={{ padding: '0.55rem 1.35rem', fontSize: '0.88rem' }}
            onClick={handleTranslate}
            disabled={isLoading || !content.trim()}
          >
            {isLoading ? (
              <>
                <RefreshCw size={16} className="spin" style={{ animation: 'spin 1s linear infinite' }} />
                Preserving & Translating...
              </>
            ) : (
              <>
                <Sparkles size={16} />
                Translate & Verify ({targetLang === 'bho' ? 'भोजपुरी' : 'हिंदी'})
              </>
            )}
          </button>
        </div>
      </div>

      {/* Uploading Status Banner */}
      {isUploading && (
        <div style={{
          background: 'rgba(6, 182, 212, 0.12)',
          border: '1px solid rgba(6, 182, 212, 0.35)',
          borderRadius: '8px',
          padding: '0.75rem 1.25rem',
          marginBottom: '1rem',
          color: '#67e8f9',
          display: 'flex',
          alignItems: 'center',
          gap: '0.6rem',
          fontSize: '0.88rem',
        }}>
          <RefreshCw size={16} className="spin" style={{ animation: 'spin 1s linear infinite' }} />
          <span>{uploadStatusText}</span>
        </div>
      )}

      {/* Error Callout */}
      {errorMessage && (
        <div style={{
          background: 'rgba(239, 68, 68, 0.12)',
          border: '1px solid rgba(239, 68, 68, 0.35)',
          borderRadius: '8px',
          padding: '0.85rem 1.25rem',
          marginBottom: '1rem',
          color: '#f87171',
          display: 'flex',
          alignItems: 'center',
          gap: '0.6rem',
          fontSize: '0.9rem',
        }}>
          <AlertCircle size={18} />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* Dual Side-by-Side Panels */}
      <div className="dual-panels-grid">
        {/* Left Side: Original Technical Document */}
        <div className="workspace-panel">
          <div className="panel-header">
            <div className="panel-header-title">
              <FileText size={16} color="#06b6d4" />
              <span>Original STEM Document (English)</span>
            </div>
            <div style={{ fontSize: '0.78rem', color: '#94a3b8', fontFamily: 'var(--font-mono)' }}>
              {analysis.words} words • {analysis.characters} chars
            </div>
          </div>

          <textarea
            className="workspace-textarea"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Paste your STEM paper, Markdown, equations, numbers, code, or citations here..."
          />

          {/* Live Detected Technical Element Badges */}
          <div className="detected-badges-bar">
            <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#94a3b8', marginRight: '0.25rem' }}>
              Detected Elements:
            </div>
            <span className="elem-badge eq">
              Equations: {analysis.equations}
            </span>
            <span className="elem-badge num">
              Numbers: {analysis.numbers}
            </span>
            <span className="elem-badge unit">
              Units: {analysis.units}
            </span>
            <span className="elem-badge code">
              Code: {analysis.codeBlocks}
            </span>
            <span className="elem-badge cit">
              Citations: {analysis.citations}
            </span>
            <span className="elem-badge term">
              Glossary Terms: {analysis.technicalTerms}
            </span>
          </div>
        </div>

        {/* Right Side: Translation with KaTeX */}
        <div className="workspace-panel">
          <div className="panel-header">
            <div className="panel-header-title">
              <Sparkles size={16} color="#38bdf8" />
              <span>Technical Translation — {targetLangLabel}</span>
            </div>

            <div className="panel-header-actions">
              {translationResult && (
                <>
                  <button className="icon-btn" onClick={handleCopy} title="Copy to clipboard">
                    {copied ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
                    {copied ? 'Copied' : 'Copy'}
                  </button>

                  <button className="icon-btn" onClick={handleDownload} title="Download Markdown file">
                    <Download size={14} />
                    Download
                  </button>
                </>
              )}
            </div>
          </div>

          <div className="workspace-output-view">
            {isLoading ? (
              <div style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                color: '#94a3b8',
                gap: '1rem',
              }}>
                <div style={{
                  width: '40px',
                  height: '40px',
                  border: '3px solid rgba(6, 182, 212, 0.2)',
                  borderTopColor: '#06b6d4',
                  borderRadius: '50%',
                  animation: 'spin 1s linear infinite',
                }} />
                <div>
                  <div style={{ fontWeight: 600, color: '#f8fafc', textAlign: 'center' }}>
                    Protecting Technical Elements & Translating into {targetLangLabel}...
                  </div>
                  <div style={{ fontSize: '0.82rem', color: '#64748b', textAlign: 'center', marginTop: '0.2rem' }}>
                    Equations, numbers, units, code, and citations are isolated and verified.
                  </div>
                </div>
              </div>
            ) : translationResult ? (
              <LaTeXRenderer content={translationResult.translatedContent} />
            ) : (
              <div style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                color: '#64748b',
                textAlign: 'center',
                padding: '2rem',
              }}>
                <ShieldCheck size={42} color="#1e293b" style={{ marginBottom: '1rem' }} />
                <h4 style={{ color: '#94a3b8', fontSize: '1rem', fontWeight: 600, marginBottom: '0.4rem' }}>
                  No Translation Generated Yet
                </h4>
                <p style={{ fontSize: '0.86rem', maxWidth: '340px' }}>
                  Click <strong>Translate & Verify</strong> above to run deterministic protection, translation into {targetLangLabel}, restoration, and automated integrity validation.
                </p>
              </div>
            )}
          </div>

          {/* Validation Status Footer */}
          {translationResult && (
            <div className="detected-badges-bar" style={{ background: 'rgba(12, 19, 34, 0.95)' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#94a3b8', marginRight: '0.25rem' }}>
                Preservation Status:
              </div>
              <span className="elem-badge eq">
                Equations: {translationResult.validation.equations.preserved}/{translationResult.validation.equations.original} ✓
              </span>
              <span className="elem-badge num">
                Numbers: {translationResult.validation.numbers.preserved}/{translationResult.validation.numbers.original} ✓
              </span>
              <span className="elem-badge unit">
                Units: {translationResult.validation.units.preserved}/{translationResult.validation.units.original} ✓
              </span>
              <span className="elem-badge code">
                Code: {translationResult.validation.codeBlocks.preserved}/{translationResult.validation.codeBlocks.original} ✓
              </span>
              <span className="elem-badge cit">
                Citations: {translationResult.validation.citations.preserved}/{translationResult.validation.citations.original} ✓
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Technical Integrity Panel */}
      {translationResult && (
        <IntegrityPanel
          validation={translationResult.validation}
          analysis={translationResult.analysis}
          warnings={translationResult.warnings}
          onTriggerCorruptionDemo={handleTriggerCorruptionDemo}
          isTestingCorruption={isTestingCorruption}
        />
      )}
    </div>
  );
};
