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
src/layouts/EventLayout.astro    How a meetup page looks
src/layouts/CommunityDayLayout.astro  How the Community Day page looks
src/components/                  Header, footer, event card, team member, speaker
src/lib/site.js                  Group name, the Meetup, LinkedIn, Facebook links, the Google Analytics ID and the event button in the menu
src/lib/team.js                  The organizing team shown on the home page
src/assets/logo.png              The logo. Astro resizes it where it is used
src/assets/photos/               Event photos. Astro resizes and compresses them
src/assets/team/                 Team photos, one per person
src/assets/speakers/             Speaker photos for Community Day
src/assets/sponsors/             Sponsor and partner logos for Community Day
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

## Update the Community Day page

Everything on the page comes from the top of `src/pages/events/community-day-2026.md`. The file has a commented example for each list, so remove the `#` signs and fill in the details.

- **Call for speakers.** `callForSpeakersUrl` is the application form. While the line is there, the page shows "Apply to speak" buttons. Put a `#` in front of it when the call closes.
- **Speakers.** Add an entry under `speakers` with `name`, `role`, `talk`, `linkedin` and `photo`. Photos go in `src/assets/speakers/`. A speaker without a photo is shown with their initials.
- **Speaker placeholders.** `speakerSlots` is how many profiles the page shows. Slots without a speaker yet are shown as "Speaker to be announced", and each speaker you add takes one over. Set it to `0` to show only confirmed speakers.
- **Schedule.** `agenda` has one entry per slot with `time`, `title` and, for a talk, `speaker`. It starts as a placeholder outline: an entry with `placeholder: true` is marked "To be announced". Replace the outline with the real slots when the agenda is set, and remove `agendaNote`, the line that tells visitors it is an outline.
- **Registration.** Add `registrationUrl` and a Register button appears at the top of the page and in the Registration section.
- **Sponsors and partners.** Add an entry under `sponsors` with `name`, `tier`, `url` and `logo`. Entries with the same `tier` are grouped under one heading. Logos go in `src/assets/sponsors/`.
- **Countdown.** It runs to `startTime` on `date`, in Malaysia time, and disappears once the event starts.
- **Venue.** `venueNote` and `gettingThere` hold the room note and the travel directions.

The organizing team on the page is the same list as the home page, from `src/lib/team.js`. If the date or time changes, update `public/community-day-2026.ics` as well, which is the file behind the "Add to calendar" button.

To use the same page for a later event, copy the file and keep `layout: ../../layouts/CommunityDayLayout.astro`.

## The event button in the menu

The outlined button in the menu at the top of every page ("Community Day 2026") is set by `highlight` in `src/lib/site.js`: its label, the page it opens and the event date. It disappears by itself once the date has passed. To remove it sooner, replace the block with `highlight: null,`. To promote a different event, change the three values.

On phones the button is the first item behind the Menu button. On tablets it stays in the bar next to Menu.

## Update the organizing team

The team shown on the home page is listed in `src/lib/team.js`: name, role, LinkedIn link, initials and photo name. Add, remove or reorder entries there.

Photos go in `src/assets/team/`, named to match the `photo` value, for example `src/assets/team/kuan-hoong.jpg`. Use a square photo of about 600 by 600 pixels with the face near the centre. Until a photo is added, the card shows the person's initials.

## Add a photo

Put a JPG in `src/assets/photos/`, about 2400 pixels wide. Remove location data from phone photos first; the ones in the repo have had all metadata stripped. Refer to it by file name, as in `photo: "2026-12-meetup"`.

## One-time Cloudflare settings

These are set in the Cloudflare dashboard, not in this repo.

- **Send www to the main address.** Both `awsugaimlkl.com` and `www.awsugaimlkl.com` currently show the site. Under Rules, Redirect Rules, create a rule from the "Redirect from WWW to root" template so search engines see one address.
- **robots.txt.** Cloudflare can replace or extend `public/robots.txt` with its own managed version. Check the setting under Security, Bots if you want search and AI crawlers handled a particular way.

## Things worth knowing

- `public/_headers` sets a strict Content-Security-Policy. It allows only files from this site plus the Google Analytics addresses, so an embedded video, another script or a font from another site needs a matching entry there.
- Google Analytics is loaded on every page by `src/layouts/BaseLayout.astro`. The measurement ID is `googleAnalyticsId` in `src/lib/site.js`; set it to `""` to switch tracking off. The setup code is in `public/scripts/analytics.js` rather than inline in the page, because the Content-Security-Policy blocks inline scripts.
- `public/_redirects` holds short links: `/meetup`, `/linkedin`, `/facebook` and `/community-day`.
- The link-preview image is `public/og.png` (1200 by 630).
