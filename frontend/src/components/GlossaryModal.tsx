import React, { useState, useEffect } from 'react';
import { X, Search, Plus, Trash2, BookOpen } from 'lucide-react';
import { GlossaryItem } from '../types';
import { getGlossary, addGlossaryTerm, deleteGlossaryTerm } from '../api';

interface GlossaryModalProps {
  isOpen: boolean;
  onClose: () => void;
  onTermAdded?: () => void;
}

export const GlossaryModal: React.FC<GlossaryModalProps> = ({ isOpen, onClose, onTermAdded }) => {
  const [terms, setTerms] = useState<GlossaryItem[]>([]);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [isAdding, setIsAdding] = useState(false);
  const [newSource, setNewSource] = useState('');
  const [newTarget, setNewTarget] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadTerms();
    }
  }, [isOpen]);

  const loadTerms = async () => {
    setLoading(true);
    try {
      const data = await getGlossary();
      setTerms(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSource.trim() || !newTarget.trim()) return;

    try {
      await addGlossaryTerm(newSource.trim(), newTarget.trim(), 'custom');
      setNewSource('');
      setNewTarget('');
      setIsAdding(false);
      await loadTerms();
      if (onTermAdded) onTermAdded();
    } catch (err) {
      alert('Failed to add custom glossary term');
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteGlossaryTerm(id);
      await loadTerms();
      if (onTermAdded) onTermAdded();
    } catch (err) {
      alert('Failed to delete term');
    }
  };

  if (!isOpen) return null;

  const filtered = terms.filter((item) => {
    const matchesSearch =
      item.sourceTerm.toLowerCase().includes(search.toLowerCase()) ||
      item.targetTerm.toLowerCase().includes(search.toLowerCase());
    const matchesCat = categoryFilter === 'all' || item.category === categoryFilter;
    return matchesSearch && matchesCat;
  });

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <BookOpen size={20} color="#06b6d4" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc' }}>
              STEM Terminology Glossary
            </h3>
            <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
              ({terms.length} verified terms)
            </span>
          </div>
          <button className="icon-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        <div className="modal-body">
          <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
            <div style={{ position: 'relative', flex: 1, minWidth: '200px' }}>
              <Search
                size={16}
                color="#64748b"
                style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)' }}
              />
              <input
                type="text"
                className="form-input"
                style={{ paddingLeft: '2.2rem' }}
                placeholder="Search English or Hindi term..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            <select
              className="sample-selector"
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              <option value="all">All Disciplines</option>
              <option value="physics">Physics & Mechanics</option>
              <option value="math">Mathematics</option>
              <option value="ai">AI & Machine Learning</option>
              <option value="cs">Computer Science</option>
              <option value="biology">Biology & Life Sciences</option>
              <option value="chemistry">Chemistry</option>
              <option value="custom">Custom Terms</option>
            </select>

            <button className="btn-primary" style={{ padding: '0.45rem 0.9rem', fontSize: '0.85rem' }} onClick={() => setIsAdding(!isAdding)}>
              <Plus size={16} />
              Add Custom Term
            </button>
          </div>

          {isAdding && (
            <form
              onSubmit={handleAdd}
              style={{
                background: 'var(--bg-input)',
                border: '1px solid var(--border-card)',
                borderRadius: '8px',
                padding: '1rem',
                marginBottom: '1.25rem',
              }}
            >
              <h4 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: '0.75rem', color: '#38bdf8' }}>
                Add Custom Scientific Terminology
              </h4>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '0.75rem' }}>
                <div>
                  <label className="form-label">English Source Term</label>
                  <input
                    type="text"
                    required
                    className="form-input"
                    placeholder="e.g. quantum superposition"
                    value={newSource}
                    onChange={(e) => setNewSource(e.target.value)}
                  />
                </div>
                <div>
                  <label className="form-label">Hindi Target Term</label>
                  <input
                    type="text"
                    required
                    className="form-input"
                    placeholder="e.g. क्वांटम सुपरपोजिशन"
                    value={newTarget}
                    onChange={(e) => setNewTarget(e.target.value)}
                  />
                </div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
                <button type="button" className="btn-secondary" onClick={() => setIsAdding(false)} style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}>
                  Cancel
                </button>
                <button type="submit" className="btn-primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}>
                  Save Term
                </button>
              </div>
            </form>
          )}

          {loading ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#94a3b8' }}>Loading glossary...</div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {filtered.map((item) => (
                <div
                  key={item.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '0.75rem 1rem',
                    background: 'var(--bg-input)',
                    border: '1px solid var(--border-card)',
                    borderRadius: '6px',
                  }}
                >
                  <div>
                    <div style={{ fontWeight: 600, fontSize: '0.9rem', color: '#f8fafc' }}>
                      {item.sourceTerm}
                    </div>
                    <div style={{ fontFamily: 'var(--font-hindi)', color: '#38bdf8', fontSize: '0.95rem' }}>
                      {item.targetTerm}
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <span
                      style={{
                        fontSize: '0.72rem',
                        padding: '0.2rem 0.5rem',
                        borderRadius: '4px',
                        background: 'rgba(255,255,255,0.06)',
                        color: '#94a3b8',
                        textTransform: 'uppercase',
                        fontFamily: 'var(--font-mono)',
                      }}
                    >
                      {item.category}
                    </span>
                    {item.id.startsWith('custom-') && (
                      <button
                        className="icon-btn"
                        style={{ color: '#ef4444' }}
                        onClick={() => handleDelete(item.id)}
                        title="Delete custom term"
                      >
                        <Trash2 size={15} />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
