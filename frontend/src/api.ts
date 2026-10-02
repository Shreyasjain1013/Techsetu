import { TranslateResponse, AnalysisCounts, ElementDetail, GlossaryItem, HistoryItem } from './types';

export async function translateAndValidate(
  content: string,
  mode: string = 'academic',
  targetLanguage: string = 'hi',
  tone: string = 'academic',
  customGlossary?: Record<string, string>
): Promise<TranslateResponse> {
  const response = await fetch('/api/translate-and-validate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      content,
      format: 'markdown',
      sourceLanguage: 'en',
      targetLanguage,
      mode,
      tone,
      customGlossary,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to translate' }));
    throw new Error(errorData.detail || `Server returned ${response.status}`);
  }

  return response.json();
}

export async function analyzeContent(content: string): Promise<{ analysis: AnalysisCounts; elements: ElementDetail[] }> {
  const response = await fetch('/api/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ content }),
  });

  if (!response.ok) {
    throw new Error('Analysis failed');
  }

  return response.json();
}

export async function uploadDocumentOrImage(file: File): Promise<{ extractedContent: string; filename: string; fileType: string }> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('/api/upload-file', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(err.detail || 'Failed to extract text from document or image');
  }

  return response.json();
}

// Backward compatible alias
export const uploadPdf = uploadDocumentOrImage;

export async function getGlossary(): Promise<GlossaryItem[]> {
  const response = await fetch('/api/glossary');
  if (!response.ok) {
    throw new Error('Failed to load glossary');
  }
  return response.json();
}

export async function addGlossaryTerm(sourceTerm: string, targetTerm: string, category: string = 'custom'): Promise<GlossaryItem> {
  const response = await fetch('/api/glossary', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ sourceTerm, targetTerm, category, language: 'hi', isStrict: true }),
  });

  if (!response.ok) {
    throw new Error('Failed to add custom term');
  }

  return response.json();
}

export async function deleteGlossaryTerm(termId: string): Promise<void> {
  const response = await fetch(`/api/glossary/${termId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to delete term');
  }
}

export async function testCorruption(content: string, corruptedValue: string = '9.18'): Promise<any> {
  const response = await fetch('/api/test-corruption', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ content, corruptedValue }),
  });

  if (!response.ok) {
    throw new Error('Failed to test corruption');
  }

  return response.json();
}

export async function getHistory(): Promise<HistoryItem[]> {
  const response = await fetch('/api/history');
  if (!response.ok) {
    throw new Error('Failed to load translation history');
  }
  return response.json();
}
