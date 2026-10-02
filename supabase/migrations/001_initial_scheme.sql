-- TechSetu Initial Schema Migration

CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NULL,
    filename TEXT NULL,
    source_language VARCHAR(10) NOT NULL DEFAULT 'en',
    target_language VARCHAR(10) NOT NULL DEFAULT 'hi',
    format VARCHAR(20) NOT NULL DEFAULT 'markdown',
    original_content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    mode VARCHAR(30) NOT NULL DEFAULT 'academic',
    translated_content TEXT NOT NULL,
    integrity_score NUMERIC(5, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'completed',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS glossary_terms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NULL,
    source_term TEXT NOT NULL,
    target_term TEXT NOT NULL,
    language VARCHAR(10) NOT NULL DEFAULT 'hi',
    is_strict BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS validation_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    translation_id UUID REFERENCES translations(id) ON DELETE CASCADE,
    equations_total INT NOT NULL DEFAULT 0,
    equations_preserved INT NOT NULL DEFAULT 0,
    numbers_total INT NOT NULL DEFAULT 0,
    numbers_preserved INT NOT NULL DEFAULT 0,
    units_total INT NOT NULL DEFAULT 0,
    units_preserved INT NOT NULL DEFAULT 0,
    code_total INT NOT NULL DEFAULT 0,
    code_preserved INT NOT NULL DEFAULT 0,
    citations_total INT NOT NULL DEFAULT 0,
    citations_preserved INT NOT NULL DEFAULT 0,
    glossary_total INT NOT NULL DEFAULT 0,
    glossary_compliant INT NOT NULL DEFAULT 0,
    integrity_score NUMERIC(5, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_translations_document_id ON translations(document_id);
CREATE INDEX IF NOT EXISTS idx_glossary_source_term ON glossary_terms(source_term);
