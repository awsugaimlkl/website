// Photos live in src/assets/photos. Refer to one by its file name without the extension,
// for example photo: "2026-05-meetup" in an event's frontmatter.
// Astro resizes and converts them when the site is built.

const files = import.meta.glob("/src/assets/photos/*.{jpg,jpeg,png,webp}", { eager: true });

const photos = Object.fromEntries(
  Object.entries(files).map(([path, mod]) => [
    path.split("/").pop().replace(/\.[^.]+$/, ""),
    mod.default,
  ])
);

export function getPhoto(name) {
  const photo = photos[name];
  if (!photo) {
    throw new Error(
      `Photo "${name}" not found in src/assets/photos. Available: ${Object.keys(photos).join(", ")}`
    );
  }
  return photo;
}
