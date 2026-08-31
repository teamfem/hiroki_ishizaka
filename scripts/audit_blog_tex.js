#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {CHTML} = require('mathjax-full/js/output/chtml.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const {AllPackages} = require('mathjax-full/js/input/tex/AllPackages.js');

const root = path.join(process.cwd(), 'blog', 'posts');
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const tex = new TeX({packages: AllPackages});
const chtml = new CHTML();
const html = mathjax.document('', {InputJax: tex, OutputJax: chtml});

function decodeEntities(s) {
  return s
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x([0-9a-fA-F]+);/g, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#([0-9]+);/g, (_, d) => String.fromCodePoint(parseInt(d, 10)));
}

function lineNumber(text, index) {
  return text.slice(0, index).split('\n').length;
}

function removeIgnoredBlocks(source) {
  return source
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<pre\b[^>]*>[\s\S]*?<\/pre>/gi, '')
    .replace(/<code\b[^>]*>[\s\S]*?<\/code>/gi, '');
}

function isDelimiterAt(text, index, seq) {
  if (!text.startsWith(seq, index)) return false;
  // A delimiter beginning at the second slash of TeX line breaks such as \\[6pt]
  // is not a real MathJax delimiter.
  return index === 0 || text[index - 1] !== '\\';
}

function findDelimiter(text, seq, from) {
  let i = from;
  while (i < text.length) {
    const j = text.indexOf(seq, i);
    if (j < 0) return -1;
    if (isDelimiterAt(text, j, seq)) return j;
    i = j + 1;
  }
  return -1;
}

function extractMath(source, file, errors) {
  const cleaned = removeIgnoredBlocks(source);
  const out = [];
  let i = 0;
  while (i < cleaned.length) {
    let kind = null;
    let open = null;
    let close = null;
    if (isDelimiterAt(cleaned, i, '\\[')) {
      kind = 'display'; open = '\\['; close = '\\]';
    } else if (isDelimiterAt(cleaned, i, '\\(')) {
      kind = 'inline'; open = '\\('; close = '\\)';
    }
    if (!kind) { i++; continue; }

    const start = i;
    const end = findDelimiter(cleaned, close, i + 2);
    if (end < 0) {
      errors.push(`${file}:${lineNumber(cleaned, start)}: unmatched opening delimiter ${open}`);
      break;
    }

    const nested = findDelimiter(cleaned, open, i + 2);
    if (nested >= 0 && nested < end) {
      errors.push(`${file}:${lineNumber(cleaned, nested)}: nested ${open} before closing ${close}; likely a missing ${close} before this line`);
    }

    const raw = cleaned.slice(i + 2, end);
    out.push({kind, raw, start, line: lineNumber(cleaned, start)});
    i = end + 2;
  }

  // Detect unmatched closing delimiters by comparing all real delimiter positions
  // with the paired expressions collected above.
  for (const [seq, label] of [['\\]', 'display'], ['\\)', 'inline']]) {
    let pos = 0;
    while ((pos = findDelimiter(cleaned, seq, pos)) >= 0) {
      const belongsToPair = out.some(f => {
        const closeSeq = f.kind === 'display' ? '\\]' : '\\)';
        const end = findDelimiter(cleaned, closeSeq, f.start + 2);
        return end === pos;
      });
      if (!belongsToPair) {
        errors.push(`${file}:${lineNumber(cleaned, pos)}: unmatched closing ${label} delimiter ${seq}`);
      }
      pos += 2;
    }
  }
  return out;
}

function checkBalanced(math, file, line, errors) {
  let depth = 0;
  for (let i = 0; i < math.length; i++) {
    if (math[i] === '\\') { i++; continue; }
    if (math[i] === '{') depth++;
    if (math[i] === '}') {
      depth--;
      if (depth < 0) {
        errors.push(`${file}:${line}: extra closing brace in TeX: ${math.slice(0, 160).replace(/\s+/g, ' ')}`);
        break;
      }
    }
  }
  if (depth !== 0) {
    errors.push(`${file}:${line}: unbalanced braces (${depth}) in TeX: ${math.slice(0, 160).replace(/\s+/g, ' ')}`);
  }

  const envStack = [];
  const re = /\\(begin|end)\{([^}]+)\}/g;
  let m;
  while ((m = re.exec(math))) {
    if (m[1] === 'begin') envStack.push(m[2]);
    else {
      const expected = envStack.pop();
      if (expected !== m[2]) {
        errors.push(`${file}:${line}: environment mismatch: expected \\end{${expected || '?'}} but found \\end{${m[2]}}`);
        break;
      }
    }
  }
  if (envStack.length) {
    errors.push(`${file}:${line}: unclosed environment(s): ${envStack.join(', ')}`);
  }
}

function auditFile(filePath) {
  const rel = path.relative(process.cwd(), filePath).replace(/\\/g, '/');
  const source = fs.readFileSync(filePath, 'utf8');
  const errors = [];
  const formulas = extractMath(source, rel, errors);

  for (const f of formulas) {
    const math = decodeEntities(f.raw).trim();
    if (!math) continue;
    checkBalanced(math, rel, f.line, errors);
    try {
      const node = html.convert(math, {display: f.kind === 'display'});
      const output = adaptor.outerHTML(node);
      const err = output.match(/data-mjx-error="([^"]+)"/);
      if (err) {
        errors.push(`${rel}:${f.line}: MathJax: ${err[1]} :: ${math.slice(0, 180).replace(/\s+/g, ' ')}`);
      }
    } catch (e) {
      errors.push(`${rel}:${f.line}: MathJax exception: ${e && e.message ? e.message : e} :: ${math.slice(0, 180).replace(/\s+/g, ' ')}`);
    }
  }
  return {formulas: formulas.length, errors};
}

const files = fs.readdirSync(root)
  .filter(f => f.endsWith('.html'))
  .sort()
  .map(f => path.join(root, f));

let total = 0;
let allErrors = [];
for (const file of files) {
  const r = auditFile(file);
  total += r.formulas;
  allErrors.push(...r.errors);
}

console.log(`Audited ${files.length} blog post HTML files and ${total} TeX expressions.`);
if (allErrors.length) {
  console.log(`Found ${allErrors.length} issue(s):`);
  for (const e of allErrors) console.log(`ERROR ${e}`);
  process.exitCode = 1;
} else {
  console.log('No TeX syntax or delimiter errors detected.');
}
