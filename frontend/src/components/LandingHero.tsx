import React from 'react';
import { ShieldCheck, ArrowRight, Sparkles, BookOpenCheck, CheckCircle2, Cpu, FileCode2 } from 'lucide-react';

interface LandingHeroProps {
  onStartTranslating: () => void;
  onSeeHowItWorks: () => void;
  onLoadPhysicsDemo: () => void;
}

export const LandingHero: React.FC<LandingHeroProps> = ({
  onStartTranslating,
  onSeeHowItWorks,
  onLoadPhysicsDemo,
}) => {
  return (
    <section className="hero-section">
      <div className="hero-pill">
        <Sparkles size={14} />
        <span>Next-Gen STEM Localization for Indian Languages</span>
      </div>

      <h1 className="hero-heading">
        Translate Knowledge.<br />Preserve Science.
      </h1>

      <p className="hero-subheading">
        Understand complex scientific and technical content in your language — without losing equations,
        numbers, units, code, citations, or technical meaning.
      </p>

      <div className="core-principle-card">
        <ShieldCheck size={20} color="#38bdf8" />
        <span>
          Core Principle: <strong className="core-principle-highlight">The language can change. The science must not.</strong>
        </span>
      </div>

      <div className="hero-actions">
        <button className="btn-primary" onClick={onStartTranslating}>
          Start Translating
          <ArrowRight size={18} />
        </button>

        <button className="btn-secondary" onClick={onLoadPhysicsDemo}>
          <FileCode2 size={18} color="#06b6d4" />
          Load Classical Mechanics Demo
        </button>

        <button className="btn-secondary" onClick={onSeeHowItWorks}>
          See How It Works
        </button>
      </div>

      {/* Visual Pipeline Bar */}
      <div className="pipeline-bar">
        <div className="pipeline-step active">
          <span className="pipeline-step-badge">1</span>
          Detect
        </div>
        <span className="pipeline-arrow">→</span>
        <div className="pipeline-step active">
          <span className="pipeline-step-badge">2</span>
          Protect
        </div>
        <span className="pipeline-arrow">→</span>
        <div className="pipeline-step active">
          <span className="pipeline-step-badge">3</span>
          Translate
        </div>
        <span className="pipeline-arrow">→</span>
        <div className="pipeline-step active">
          <span className="pipeline-step-badge">4</span>
          Restore
        </div>
        <span className="pipeline-arrow">→</span>
        <div className="pipeline-step active">
          <span className="pipeline-step-badge">5</span>
          Verify
        </div>
      </div>

      {/* Why TechSetu? 3 Pillars */}
      <div style={{ marginTop: '3.5rem', marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1.4rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.4rem' }}>
          Why TechSetu?
        </h3>
        <p style={{ color: '#94a3b8', fontSize: '0.92rem' }}>
          Engineered specifically for engineering students, researchers, and scientific learners.
        </p>
      </div>

      <div className="pillars-grid">
        <div className="pillar-card">
          <div className="pillar-icon-box" style={{ background: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8' }}>
            <BookOpenCheck size={22} />
          </div>
          <h4 className="pillar-title">Understand</h4>
          <p className="pillar-desc">
            Complex technical STEM prose becomes lucid and accessible in formal Hindi without cognitive overload.
          </p>
        </div>

        <div className="pillar-card">
          <div className="pillar-icon-box" style={{ background: 'rgba(129, 140, 248, 0.15)', color: '#818cf8' }}>
            <Cpu size={22} />
          </div>
          <h4 className="pillar-title">Preserve</h4>
          <p className="pillar-desc">
            Equations, numerical constants, SI units, citations, and code remain protected with deterministic placeholders.
          </p>
        </div>

        <div className="pillar-card">
          <div className="pillar-icon-box" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#10b981' }}>
            <CheckCircle2 size={22} />
          </div>
          <h4 className="pillar-title">Verify</h4>
          <p className="pillar-desc">
            Every output undergoes automated algorithmic validation to certify that not a single number or equation changed.
          </p>
        </div>
      </div>
    </section>
  );
};
