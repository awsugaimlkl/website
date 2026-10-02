// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // The public address of the site. Used for canonical links, link previews and the sitemap.
  site: 'https://awsugaimlkl.com',
  integrations: [sitemap()],
  build: {
    // Keep all CSS in files so the Content-Security-Policy in public/_headers can stay strict.
    inlineStylesheets: 'never',
  },
});
