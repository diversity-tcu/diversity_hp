// Shared extraction helpers for auto-generated tile listings.
// Pulls thumbnail, vol label, affiliation/name/role from content body/title.

// Ordered longest-first so compound role names (学生支援部長, 事務局長, 副学長, 学部長,
// 准教授, 准教授) take precedence over their substrings (部長, 学長, 教授).
const ROLE_WORDS = [
  '学生支援部長', '事務局長', '副学長', '学部長',
  '准教授', '助教', '講師', '教員', '教授', '先生',
  '室員', '部長', '学長',
];

const IMG_RE = /\/uploads\/[^\s"')\]]+?\.(?:jpg|jpeg|png|gif|webp)/i;

export function extractFirstImage(body: string | undefined): string | null {
  if (!body) return null;
  const m = body.match(IMG_RE);
  return m ? m[0] : null;
}

// Extract volume label: "Vol.XX", "第XX回", or "最終回" from a title.
export function extractVolLabel(title: string | undefined): string {
  if (!title) return '';
  // explicit vol pattern in title
  let m = title.match(/Vol\.?\s*0*(\d+)/i);
  if (m) {
    const n = parseInt(m[1], 10);
    return `Vol.${String(n).padStart(2, '0')}`;
  }
  m = title.match(/第\s*0*(\d+)\s*回/);
  if (m) {
    const n = parseInt(m[1], 10);
    return `第${String(n).padStart(2, '0')}回`;
  }
  if (/最終回/.test(title)) return '最終回';
  return '';
}

// Try to extract {affiliation, name, role} from the first bold/highlighted chunk.
// Handles both markdown "**...**" and WordPress-migrated HTML where the name is
// in <span class="font-15em">...</span> surrounded by affiliation text.
export function extractPerson(body: string | undefined): {
  affiliation: string;
  name: string;
  role: string;
} {
  const empty = { affiliation: '', name: '', role: '' };
  if (!body) return empty;

  // 1) WordPress pattern: "<affiliation text><br/>\n<span class=\"font-15em\">NAME</span> ROLE<br/>"
  const wpRe =
    /([^<>\n]{2,60})<br\s*\/?>[\s\S]{0,40}?<span[^>]*class=\"font-15em\"[^>]*>\s*([^<]+?)\s*<\/span>\s*([^<\n]{0,20}?)(?:<br|$)/;
  const wp = body.match(wpRe);
  if (wp) {
    const affiliation = wp[1].replace(/\s+/g, ' ').trim();
    const name = wp[2].replace(/\s+/g, ' ').trim();
    let role = (wp[3] || '').replace(/\s+/g, ' ').trim();
    // normalize "さん" etc; keep only meaningful role words or leave empty
    if (role && !ROLE_WORDS.some((w) => role.includes(w)) && !/さん/.test(role)) {
      role = '';
    }
    return { affiliation, name, role };
  }

  // 2) Markdown bold pattern: **...役職ワード...**
  const boldMatches = body.match(/\*\*([^*]{2,120})\*\*/g);
  if (boldMatches) {
    for (const bm of boldMatches) {
      const inner = bm.slice(2, -2).trim();
      // Normalize whitespace (full-width space too)
      const norm = inner.replace(/[\u3000\s]+/g, ' ').trim();
      const roleWord = ROLE_WORDS.find((w) => norm.includes(w));
      if (!roleWord) continue;
      // Split around role word
      const idx = norm.indexOf(roleWord);
      const before = norm.slice(0, idx).trim();
      // role: from idx to end of that word; trailing text (if any) appended too.
      const role = norm.slice(idx).trim();
      // "before" typically contains "AFFILIATION NAME" separated by space.
      // Heuristic: affiliation is everything before the last space; name is last token(s).
      const tokens = before.split(' ');
      let name = '';
      let affiliation = '';
      if (tokens.length >= 2) {
        // name likely is last 1-2 tokens (family + given)
        // If token[-2] looks like a name (short, no 学科/部/室), take last 2 as name.
        const last2 = tokens.slice(-2).join(' ');
        const last1 = tokens.slice(-1).join(' ');
        const hasAffixInLast2 = /学科|学部|学系|研究科|部$|室$|センター/.test(tokens[tokens.length - 2]);
        if (!hasAffixInLast2 && tokens.length >= 2 && tokens[tokens.length - 2].length <= 4) {
          name = last2;
          affiliation = tokens.slice(0, -2).join(' ');
        } else {
          name = last1;
          affiliation = tokens.slice(0, -1).join(' ');
        }
      } else {
        name = before;
      }
      return { affiliation, name, role };
    }
  }

  return empty;
}

export interface TileInfo {
  vol: string;
  affiliation: string;
  name: string;
  role: string;
  thumb: string | null;
}

export function extractTileInfo(title: string | undefined, body: string | undefined): TileInfo {
  const person = extractPerson(body);
  return {
    vol: extractVolLabel(title),
    affiliation: person.affiliation,
    name: person.name,
    role: person.role,
    thumb: extractFirstImage(body),
  };
}
