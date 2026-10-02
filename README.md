# awsugaimlkl.com

Website for AWS User Group AI/ML Kuala Lumpur. Built with [Astro](https://astro.build) and served as static files by Cloudflare. Every push to `main` is built and deployed by Cloudflare.

## Run it on your computer

You need Node.js 22.12 or newer.

```sh
npm install
npm run dev        # live preview at http://localhost:4321
npm run build      # builds the site into ./dist
npx wrangler dev   # serves ./dist the way Cloudflare does, at http://localhost:8787
```

`npx wrangler dev` is the closest match to the live site: it applies the headers in `public/_headers`, the short links in `public/_redirects` and the 404 page.

## Where things are

```text
src/pages/index.astro            Home page
src/pages/events/index.astro     Events list (upcoming and past)
src/pages/events/*.md            One file per event
src/layouts/EventLayout.astro    How an event page looks
src/components/                  Header, footer, event card
src/lib/site.js                  Group name and the Meetup, LinkedIn, Facebook links
src/assets/logo.png              The logo. Astro resizes it where it is used
src/assets/photos/               Event photos. Astro resizes and compresses them
public/                          Files copied as they are: favicons, og.png, _headers, _redirects
```

## Add an event

Copy one of the files in `src/pages/events/` and change the details at the top. The file name becomes the address: `2026-12-meetup.md` is served at `/events/2026-12-meetup/`.

```yaml
---
layout: ../../layouts/EventLayout.astro
title: "December 2026 meetup"
description: "One sentence shown under the title and in search results."
number: 7                      # meetup number, leave out for other events
date: "2026-12-10"             # decides upcoming or past
dateDisplay: "Thursday, 10 December 2026"
time: "7:00 PM – 9:00 PM"
startTime: "19:00"             # 24-hour, Malaysia time
endTime: "21:00"
venue: "Company name, building"
address: "Full address, used by search engines"
summary: "One line shown on the event card."
registrationUrl: "https://..." # shows a Register button while the event is upcoming
meetupUrl: "https://www.meetup.com/awsug-aiml-my/events/123/"
---
```

After the event you can add what happened:

```yaml
signups: 160
albumUrl: "https://photos.app.goo.gl/..."
photo: "2026-12-meetup"        # file name in src/assets/photos, without .jpg
photoAlt: "What the photo shows, for people who cannot see it"
talks:
  - title: "Talk title"
    speaker: "Speaker name"
```

Text below the second `---` is the body of the page and is written in Markdown.

An event is listed as upcoming until the end of its day in Malaysia time. The home page highlights the next upcoming event that has `featured: true`, or simply the next one. Remember to update the meetup count in the "facts" block on the home page.

## Add a photo

Put a JPG in `src/assets/photos/`, about 2400 pixels wide. Remove location data from phone photos first; the ones in the repo have had all metadata stripped. Refer to it by file name, as in `photo: "2026-12-meetup"`.

## One-time Cloudflare settings

These are set in the Cloudflare dashboard, not in this repo.

- **Send www to the main address.** Both `awsugaimlkl.com` and `www.awsugaimlkl.com` currently show the site. Under Rules, Redirect Rules, create a rule from the "Redirect from WWW to root" template so search engines see one address.
- **robots.txt.** Cloudflare can replace or extend `public/robots.txt` with its own managed version. Check the setting under Security, Bots if you want search and AI crawlers handled a particular way.

## Things worth knowing

- `public/_headers` sets a strict Content-Security-Policy. It allows only files from this site, so an embedded video, an analytics script or a font from another site needs a matching entry there.
- `public/_redirects` holds short links: `/meetup`, `/linkedin`, `/facebook` and `/community-day`.
- The link-preview image is `public/og.png` (1200 by 630).
