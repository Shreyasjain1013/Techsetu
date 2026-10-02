import React from 'react';
import { Atom, BookOpen, Clock, Sparkles, CheckCircle2 } from 'lucide-react';

interface HeaderProps {
  activeTab: 'translator' | 'pipeline' | 'glossary' | 'history';
  setActiveTab: (tab: 'translator' | 'pipeline' | 'glossary' | 'history') => void;
  onOpenGlossary: () => void;
  onOpenHistory: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  onOpenGlossary,
  onOpenHistory,
}) => {
  return (
    <header className="app-header">
      <div className="header-container">
        <div className="brand-section" onClick={() => setActiveTab('translator')}>
          <div className="brand-icon-box">
            <Atom size={22} />
          </div>
          <div>
            <div className="brand-title">
              TechSetu
              <span className="brand-tagline">Academic</span>
            </div>
            <div style={{ fontSize: '0.72rem', color: '#64748b', fontWeight: 500 }}>
              Translate Knowledge. Preserve Science.
            </div>
          </div>
        </div>

        <nav className="nav-links">
          <button
            className={`nav-button ${activeTab === 'translator' ? 'active' : ''}`}
            onClick={() => setActiveTab('translator')}
          >
            <Sparkles size={16} />
            Workspace
          </button>

          <button
            className={`nav-button ${activeTab === 'pipeline' ? 'active' : ''}`}
            onClick={() => setActiveTab('pipeline')}
          >
            <Atom size={16} />
            How It Works
          </button>

          <button
            className="nav-button"
            onClick={onOpenGlossary}
          >
            <BookOpen size={16} />
            Glossary
          </button>

          <button
            className="nav-button"
            onClick={onOpenHistory}
          >
            <Clock size={16} />
            History
          </button>

          <div className="header-status-badge">
            <span className="status-dot" />
            Integrity Engine Ready
          </div>
        </nav>
      </div>
    </header>
  );
};
