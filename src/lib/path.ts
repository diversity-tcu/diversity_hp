// Prepend Astro's BASE_URL to root-absolute paths.
// BASE_URL always ends with "/" (e.g. "/diversity_hp/").
const BASE = import.meta.env.BASE_URL;

export function withBase(path: string): string {
  if (!path) return path;
  if (!path.startsWith('/')) return path; // external or relative
  if (path.startsWith('//')) return path; // protocol-relative
  const trimmed = BASE.endsWith('/') ? BASE.slice(0, -1) : BASE;
  if (path === trimmed || path.startsWith(trimmed + '/')) return path;
  return trimmed + path;
}

export const base = BASE;
