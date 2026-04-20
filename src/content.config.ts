import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const pageSchema = z.object({
  title: z.string().optional().default(''),
  date: z.string().optional(),
  author: z.string().optional(),
  status: z.string().optional(),
  topic: z.enum(['environment', 'reform', 'nextgen']).optional(),
  thumb: z.string().optional(),
  // ロールモデル用（frontmatterで指定すればMarkdownだけで記事が書ける）
  name: z.string().optional(),
  affiliation: z.string().optional(),
  role: z.string().optional(),
  photo_main: z.string().optional(),
  photo_style: z.string().optional(),
  theme: z.string().optional(),
  workplace: z.string().optional(),
  career: z.string().optional(),
  education: z.string().optional(),
  high_school: z.string().optional(),
  published_date: z.string().optional(),
});

const pages = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/pages' }),
  schema: pageSchema,
});

const news = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/news' }),
  schema: pageSchema,
});

const events = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/events' }),
  schema: pageSchema,
});

const communication = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/communication' }),
  schema: z.object({
    title: z.string(),
    date: z.string(),
    pdf: z.string(),
    thumb: z.string().optional(),
  }),
});

export const collections = { pages, news, events, communication };
