# TechSetu Database Schema

## Overview
TechSetu uses Supabase (PostgreSQL) for persistence with a local in-memory/SQLite cache fallback.
The design enforces high throughput and complete privacy: temporary placeholder replacements (`{{TECH_EQ_001}}`) are kept purely in backend memory and are never persisted to disk or external storage.

## Schema Definition

### 1. `documents` Table
Stores uploaded or pasted technical documents.
```sql
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
```

### 2. `translations` Table
Stores translated versions and overall integrity score.
```sql
CREATE TABLE IF NOT EXISTS translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    mode VARCHAR(30) NOT NULL DEFAULT 'academic',
    translated_content TEXT NOT NULL,
    integrity_score NUMERIC(5, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'completed',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 3. `glossary_terms` Table
Stores standard and user-defined STEM terminology mappings.
```sql
CREATE TABLE IF NOT EXISTS glossary_terms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NULL,
    source_term TEXT NOT NULL,
    target_term TEXT NOT NULL,
    language VARCHAR(10) NOT NULL DEFAULT 'hi',
    is_strict BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 4. `validation_results` Table
Records granular technical preservation metrics per translation.
```sql
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
```
