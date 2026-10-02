export interface AnalysisCounts {
  words: number;
  characters: number;
  equations: number;
  numbers: number;
  units: number;
  codeBlocks: number;
  citations: number;
  technicalTerms: number;
}

export interface ElementDetail {
  type: 'equation' | 'number' | 'unit' | 'code' | 'citation' | 'term';
  value: string;
  placeholder?: string;
  preserved?: boolean;
}

export interface ValidationCategory {
  original: number;
  preserved: number;
}

export interface ValidationResult {
  integrityScore: number;
  equations: ValidationCategory;
  numbers: ValidationCategory;
  units: ValidationCategory;
  codeBlocks: ValidationCategory;
  citations: ValidationCategory;
  technicalTerms: ValidationCategory;
}

export interface TranslateResponse {
  status: 'success' | 'warning' | 'error';
  translatedContent: string;
  originalContent: string;
  mode: string;
  tone?: string;
  sourceLanguage: string;
  targetLanguage: string;
  analysis: AnalysisCounts;
  validation: ValidationResult;
  details: {
    preservedElements?: Array<{
      type: string;
      value?: string;
      source?: string;
      target?: string;
      status: string;
    }>;
    placeholdersCount?: number;
  };
  warnings: string[];
  protectedContentPreview?: string;
}

export interface GlossaryItem {
  id: string;
  sourceTerm: string;
  targetTerm: string;
  language: string;
  isStrict: boolean;
  category: string;
}

export interface HistoryItem {
  id: string;
  original_content: string;
  translated_content: string;
  mode: string;
  tone?: string;
  integrity_score: number;
  created_at: string;
  analysis: AnalysisCounts;
  validation: ValidationResult;
}
