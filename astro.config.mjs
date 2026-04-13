import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

const BASE = '/diversity_hp';

/**
 * Rehype plugin that prepends BASE to root-absolute URLs in migrated markdown
 * (e.g. /uploads/..., /assets/..., /news/..., /events/...). Skips external
 * URLs, fragments, mailto/tel, and URLs already prefixed with BASE.
 */
function rehypeBasePath() {
  const base = BASE;
  const rewrite = (url) => {
    if (typeof url !== 'string' || url.length === 0) return url;
    if (!url.startsWith('/')) return url;
    if (url.startsWith('//')) return url;
    if (url === base || url.startsWith(base + '/')) return url;
    return base + url;
  };
  const visit = (node) => {
    if (!node || typeof node !== 'object') return;
    if (node.type === 'element' && node.properties) {
      const p = node.properties;
      if (node.tagName === 'a' && p.href) p.href = rewrite(p.href);
      if ((node.tagName === 'img' || node.tagName === 'source') && p.src) p.src = rewrite(p.src);
      if (p.style && typeof p.style === 'string') {
        p.style = p.style.replace(/url\((['"]?)(\/[^'")]+)\1\)/g, (_m, q, u) => `url(${q}${rewrite(u)}${q})`);
      }
    }
    if (Array.isArray(node.children)) node.children.forEach(visit);
  };
  return () => (tree) => visit(tree);
}

export default defineConfig({
  site: 'https://kasekiguchi.github.io',
  base: BASE,
  trailingSlash: 'always',
  output: 'static',
  integrations: [mdx()],
  markdown: {
    rehypePlugins: [rehypeBasePath()],
  },
  vite: {
    build: {},
  },
});
