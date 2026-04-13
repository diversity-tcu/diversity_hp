import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://www.diversity.tcu.ac.jp',
  base: '/',
  output: 'static',
  integrations: [mdx()],
  markdown: {
    // Be lenient about odd HTML in migrated content
  },
  vite: {
    build: {
      // Avoid failing entire build on single asset issues
    },
  },
});
