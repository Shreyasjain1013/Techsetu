import React, { useState } from 'react';
import { Header } from './components/Header';
import { LandingHero } from './components/LandingHero';
import { TranslatorWorkspace } from './components/TranslatorWorkspace';
import { GlossaryModal } from './components/GlossaryModal';
import { HistoryModal } from './components/HistoryModal';
import { HistoryItem } from './types';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'translator' | 'pipeline' | 'glossary' | 'history'>('translator');
  const [isGlossaryOpen, setIsGlossaryOpen] = useState<boolean>(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState<boolean>(false);

  const handleStartTranslating = () => {
    setActiveTab('translator');
    const el = document.getElementById('workspace-container');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSeeHowItWorks = () => {
    setActiveTab('pipeline');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="app-wrapper">
      <div className="scientific-grid-bg" />

      {/* Main Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenGlossary={() => setIsGlossaryOpen(true)}
        onOpenHistory={() => setIsHistoryOpen(true)}
      />

      <main style={{ flex: 1, paddingBottom: '3rem' }}>
        {/* Landing Hero displayed if on 'pipeline' tab or top of translator */}
        {activeTab === 'pipeline' && (
          <LandingHero
            onStartTranslating={handleStartTranslating}
            onSeeHowItWorks={handleSeeHowItWorks}
            onLoadPhysicsDemo={() => {
              setActiveTab('translator');
            }}
          />
        )}

        {/* Translator Workspace */}
        <div id="workspace-container">
          <TranslatorWorkspace />
        </div>
      </main>

      {/* Footer */}
      <footer
        style={{
          borderTop: '1px solid var(--border-subtle)',
          padding: '1.5rem',
          textAlign: 'center',
          fontSize: '0.8rem',
          color: '#64748b',
          background: 'rgba(11, 15, 23, 0.95)',
        }}
      >
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
          <div>
            <strong>TechSetu</strong> — Translate Knowledge. Preserve Science.
          </div>
          <div>
            PS 2.4: Multi-Lingual Technical Translator for Complex Science • Smart Education
          </div>
          <div>
            Deterministic Protection & Verification Engine
          </div>
        </div>
      </footer>

      {/* Glossary Modal */}
      <GlossaryModal
        isOpen={isGlossaryOpen}
        onClose={() => setIsGlossaryOpen(false)}
      />

      {/* History Modal */}
      <HistoryModal
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        onSelectHistory={(item: HistoryItem) => {
          // Handled via workspace or reloads
        }}
      />
    </div>
  );
};
