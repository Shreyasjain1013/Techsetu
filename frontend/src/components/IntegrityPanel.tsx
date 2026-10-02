import React from 'react';
import { ShieldCheck, AlertTriangle, CheckCircle2, Bug, Sparkles, BookOpen } from 'lucide-react';
import { ValidationResult, AnalysisCounts } from '../types';

interface IntegrityPanelProps {
  validation: ValidationResult;
  analysis: AnalysisCounts;
  warnings: string[];
  onTriggerCorruptionDemo: () => void;
  isTestingCorruption?: boolean;
}

export const IntegrityPanel: React.FC<IntegrityPanelProps> = ({
  validation,
  analysis,
  warnings,
  onTriggerCorruptionDemo,
  isTestingCorruption = false,
}) => {
  const isPerfect = validation.integrityScore >= 95.0 && warnings.length === 0;

  return (
    <div className="integrity-panel">
      <div className="integrity-panel-header">
        <div className="integrity-header-left">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <ShieldCheck size={26} color={isPerfect ? '#10b981' : '#f59e0b'} />
            <div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#f8fafc' }}>
                Technical Integrity Verification
              </h3>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
                Automated post-translation validation of all scientific constants, math, and units.
              </p>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <button
            className="btn-secondary"
            onClick={onTriggerCorruptionDemo}
            disabled={isTestingCorruption}
            title="Demonstrate the validator catching an intentional numerical corruption (e.g. 9.81 -> 9.18)"
            style={{ fontSize: '0.82rem', padding: '0.45rem 0.9rem' }}
          >
            <Bug size={15} color="#f59e0b" />
            {isTestingCorruption ? 'Simulating...' : 'Test Corruption Detection'}
          </button>

          <div className={`integrity-score-badge ${isPerfect ? 'perfect' : 'warning'}`}>
            <span>Score:</span>
            <strong>{validation.integrityScore.toFixed(1)}%</strong>
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="integrity-metrics-grid">
        {/* Equations */}
        <div className="metric-card">
          <div className="metric-label">Equations</div>
          <div className={`metric-value ${validation.equations.preserved >= validation.equations.original ? 'preserved' : 'warning'}`}>
            {validation.equations.preserved >= validation.equations.original ? (
              <CheckCircle2 size={16} color="#10b981" />
            ) : (
              <AlertTriangle size={16} color="#f59e0b" />
            )}
            <span>{validation.equations.preserved} / {validation.equations.original}</span>
          </div>
        </div>

        {/* Numbers */}
        <div className="metric-card">
          <div className="metric-label">Numbers</div>
          <div className={`metric-value ${validation.numbers.preserved >= validation.numbers.original ? 'preserved' : 'warning'}`}>
            {validation.numbers.preserved >= validation.numbers.original ? (
              <CheckCircle2 size={16} color="#10b981" />
            ) : (
              <AlertTriangle size={16} color="#f59e0b" />
            )}
            <span>{validation.numbers.preserved} / {validation.numbers.original}</span>
          </div>
        </div>

        {/* Units */}
        <div className="metric-card">
          <div className="metric-label">Scientific Units</div>
          <div className={`metric-value ${validation.units.preserved >= validation.units.original ? 'preserved' : 'warning'}`}>
            {validation.units.preserved >= validation.units.original ? (
              <CheckCircle2 size={16} color="#10b981" />
            ) : (
              <AlertTriangle size={16} color="#f59e0b" />
            )}
            <span>{validation.units.preserved} / {validation.units.original}</span>
          </div>
        </div>

        {/* Code Blocks */}
        <div className="metric-card">
          <div className="metric-label">Code Blocks</div>
          <div className={`metric-value ${validation.codeBlocks.preserved >= validation.codeBlocks.original ? 'preserved' : 'warning'}`}>
            {validation.codeBlocks.preserved >= validation.codeBlocks.original ? (
              <CheckCircle2 size={16} color="#10b981" />
            ) : (
              <AlertTriangle size={16} color="#f59e0b" />
            )}
            <span>{validation.codeBlocks.preserved} / {validation.codeBlocks.original}</span>
          </div>
        </div>

        {/* Citations */}
        <div className="metric-card">
          <div className="metric-label">Citations</div>
          <div className={`metric-value ${validation.citations.preserved >= validation.citations.original ? 'preserved' : 'warning'}`}>
            {validation.citations.preserved >= validation.citations.original ? (
              <CheckCircle2 size={16} color="#10b981" />
            ) : (
              <AlertTriangle size={16} color="#f59e0b" />
            )}
            <span>{validation.citations.preserved} / {validation.citations.original}</span>
          </div>
        </div>

        {/* Glossary Terms */}
        <div className="metric-card">
          <div className="metric-label">Technical Terms</div>
          <div className={`metric-value ${validation.technicalTerms.preserved >= validation.technicalTerms.original ? 'preserved' : 'warning'}`}>
            {validation.technicalTerms.preserved >= validation.technicalTerms.original ? (
              <CheckCircle2 size={16} color="#10b981" />
            ) : (
              <AlertTriangle size={16} color="#f59e0b" />
            )}
            <span>{validation.technicalTerms.preserved} / {validation.technicalTerms.original}</span>
          </div>
        </div>
      </div>

      {/* Warnings & Alerts */}
      {warnings.length > 0 && (
        <div className="integrity-warnings-box">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', fontWeight: 600, color: '#f59e0b' }}>
            <AlertTriangle size={17} />
            <span>Integrity Inconsistencies Detected ({warnings.length}):</span>
          </div>
          {warnings.map((w, idx) => (
            <div key={idx} className="integrity-warning-item">
              <span>•</span>
              <span>{w}</span>
            </div>
          ))}
        </div>
      )}

      {/* Educational Microcopy */}
      <div className="educational-callout">
        <Sparkles size={18} />
        <span>
          <strong>Technical meaning preserved:</strong> The integrity score measures mathematical and scientific accuracy. Your equations, SI units, and code remain identical to the peer-reviewed source.
        </span>
      </div>
    </div>
  );
};
