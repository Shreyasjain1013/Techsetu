import React from 'react';
import katex from 'katex';

interface LaTeXRendererProps {
  content: string;
}

export const LaTeXRenderer: React.FC<LaTeXRendererProps> = ({ content }) => {
  if (!content) return null;

  // Split into paragraphs / lines
  const lines = content.split('\n');
  const elements: React.ReactNode[] = [];
  let inCodeBlock = false;
  let codeBlockBuffer: string[] = [];
  let codeBlockLang = '';

  const renderMathSafely = (mathStr: string, displayMode: boolean) => {
    try {
      const html = katex.renderToString(mathStr, {
        displayMode,
        throwOnError: false,
      });
      return <span dangerouslySetInnerHTML={{ __html: html }} />;
    } catch {
      return <code>{mathStr}</code>;
    }
  };

  const parseInlineElements = (text: string): React.ReactNode[] => {
    // Look for $$...$$ display, $...$ inline, `...` inline code, **bold**
    const parts: React.ReactNode[] = [];
    let remaining = text;
    let keyIdx = 0;

    while (remaining.length > 0) {
      // 1. Display math $$...$$
      const displayMathMatch = remaining.match(/^\$\$([\s\S]*?)\$\$/);
      if (displayMathMatch) {
        parts.push(
          <div key={`disp-${keyIdx++}`} className="katex-display">
            {renderMathSafely(displayMathMatch[1], true)}
          </div>
        );
        remaining = remaining.slice(displayMathMatch[0].length);
        continue;
      }

      // 2. Inline math $...$
      const inlineMathMatch = remaining.match(/^\$([^\$\n]+?)\$/);
      if (inlineMathMatch) {
        parts.push(
          <span key={`inline-math-${keyIdx++}`} style={{ margin: '0 2px' }}>
            {renderMathSafely(inlineMathMatch[1], false)}
          </span>
        );
        remaining = remaining.slice(inlineMathMatch[0].length);
        continue;
      }

      // 3. Inline code `...`
      const inlineCodeMatch = remaining.match(/^`([^`\n]+)`/);
      if (inlineCodeMatch) {
        parts.push(
          <code
            key={`inline-code-${keyIdx++}`}
            style={{
              background: 'rgba(255,255,255,0.08)',
              padding: '0.15rem 0.4rem',
              borderRadius: '4px',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.85em',
              color: '#38bdf8',
            }}
          >
            {inlineCodeMatch[1]}
          </code>
        );
        remaining = remaining.slice(inlineCodeMatch[0].length);
        continue;
      }

      // 4. Bold text **...**
      const boldMatch = remaining.match(/^\*\*([^\*\n]+)\*\*/);
      if (boldMatch) {
        parts.push(<strong key={`bold-${keyIdx++}`}>{boldMatch[1]}</strong>);
        remaining = remaining.slice(boldMatch[0].length);
        continue;
      }

      // Regular text up to next special character ($, `, *)
      const nextSpecial = remaining.search(/[\$`\*]/);
      if (nextSpecial === -1) {
        parts.push(remaining);
        break;
      } else if (nextSpecial > 0) {
        parts.push(remaining.slice(0, nextSpecial));
        remaining = remaining.slice(nextSpecial);
      } else {
        parts.push(remaining[0]);
        remaining = remaining.slice(1);
      }
    }

    return parts;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Handle fenced code blocks
    if (line.startsWith('```')) {
      if (inCodeBlock) {
        elements.push(
          <pre key={`code-${i}`}>
            <code>{codeBlockBuffer.join('\n')}</code>
          </pre>
        );
        codeBlockBuffer = [];
        inCodeBlock = false;
      } else {
        inCodeBlock = true;
        codeBlockLang = line.replace('```', '').trim();
      }
      continue;
    }

    if (inCodeBlock) {
      codeBlockBuffer.push(line);
      continue;
    }

    // Markdown Headers
    if (line.startsWith('# ')) {
      elements.push(
        <h1 key={`h1-${i}`} style={{ fontSize: '1.6rem', fontWeight: 700, margin: '1rem 0 0.5rem', color: '#fff' }}>
          {parseInlineElements(line.replace('# ', ''))}
        </h1>
      );
      continue;
    }
    if (line.startsWith('## ')) {
      elements.push(
        <h2 key={`h2-${i}`} style={{ fontSize: '1.3rem', fontWeight: 600, margin: '0.9rem 0 0.4rem', color: '#38bdf8' }}>
          {parseInlineElements(line.replace('## ', ''))}
        </h2>
      );
      continue;
    }
    if (line.startsWith('### ')) {
      elements.push(
        <h3 key={`h3-${i}`} style={{ fontSize: '1.1rem', fontWeight: 600, margin: '0.75rem 0 0.35rem', color: '#e2e8f0' }}>
          {parseInlineElements(line.replace('### ', ''))}
        </h3>
      );
      continue;
    }

    // Blank line
    if (!line.trim()) {
      elements.push(<div key={`blank-${i}`} style={{ height: '0.65rem' }} />);
      continue;
    }

    // Regular line
    elements.push(
      <p key={`p-${i}`} style={{ marginBottom: '0.45rem', wordBreak: 'break-word' }}>
        {parseInlineElements(line)}
      </p>
    );
  }

  // Handle trailing unclosed code block
  if (inCodeBlock && codeBlockBuffer.length > 0) {
    elements.push(
      <pre key="code-unclosed">
        <code>{codeBlockBuffer.join('\n')}</code>
      </pre>
    );
  }

  return <div className="rendered-stem-content">{elements}</div>;
};
