// Loads every event page in src/pages/events/*.md and sorts them into upcoming and past.
// Do not import this file from EventLayout.astro: the event pages use that layout,
// so it would import itself in a circle. Use ./dates.js there instead.

import { isPast } from "./dates.js";

const modules = import.meta.glob("/src/pages/events/*.md", { eager: true });

export function getEvents() {
  const events = Object.entries(modules).map(([path, mod]) => {
    const slug = path.split("/").pop().replace(".md", "");
    return {
      ...mod.frontmatter,
      slug,
      href: `/events/${slug}/`,
      past: isPast(mod.frontmatter.date),
    };
  });

  const byDate = (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime();

  return {
    all: [...events].sort(byDate),
    // Soonest first
    upcoming: events.filter((e) => !e.past).sort(byDate),
    // Most recent first
    past: events.filter((e) => e.past).sort(byDate).reverse(),
  };
}
