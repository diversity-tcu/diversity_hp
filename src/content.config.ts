import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const pageSchema = z.object({
  title: z.string().optional().default(''),
  date: z.string().optional(),
  author: z.string().optional(),
  original_url: z.string().optional(),
  status: z.string().optional(),
  topic: z.enum(['environment', 'reform', 'nextgen']).optional(),
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
