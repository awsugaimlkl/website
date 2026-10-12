// Structured data so search engines can list a page as an event.
// Used by both event layouts.

import { SITE } from "./site.js";

export function eventStructuredData(frontmatter, pageUrl, site) {
  const { title, description, date, startTime, endTime, venue, address, sponsors = [] } = frontmatter;

  return {
    "@context": "https://schema.org",
    "@type": "Event",
    name: title,
    description,
    startDate: startTime ? `${date}T${startTime}:00+08:00` : date,
    ...(endTime ? { endDate: `${date}T${endTime}:00+08:00` } : {}),
    eventStatus: "https://schema.org/EventScheduled",
    eventAttendanceMode: "https://schema.org/OfflineEventAttendanceMode",
    url: pageUrl,
    image: new URL("/og.png", site),
    location: {
      "@type": "Place",
      name: venue,
      ...(address ? { address } : {}),
    },
    organizer: {
      "@type": "Organization",
      name: SITE.name,
      url: site,
    },
    ...(sponsors.length > 0
      ? {
          sponsor: sponsors.map((s) => ({
            "@type": "Organization",
            name: s.name,
            ...(s.url ? { url: s.url } : {}),
          })),
        }
      : {}),
  };
}
