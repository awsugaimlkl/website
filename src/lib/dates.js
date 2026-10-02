// Date helpers shared by the event pages and the event lists.
//
// An event counts as upcoming until the end of its day in Malaysia time (UTC+8).
// This runs when the site is built. public/scripts/site.js repeats the same check
// in the visitor's browser, so labels stay right between deploys.

export function endOfEventDay(date) {
  return new Date(`${date}T23:59:59+08:00`);
}

export function isPast(date, now = new Date()) {
  return endOfEventDay(date).getTime() < now.getTime();
}
