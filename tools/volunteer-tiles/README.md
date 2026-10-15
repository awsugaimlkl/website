# Volunteer tiles

Makes the Community Day volunteer photos: the person cut out of an ordinary photo, in colour and slightly brightened, in front of the Kuala Lumpur skyline. The face is scaled and placed where the placeholder silhouette's face was, so all tiles match.

- `background.jpg` is the volunteer placeholder art (`src/assets/volunteer-placeholder.jpg`) with the silhouette taken out.
- `body-mask.png` is the placeholder silhouette's shape, used by `--body` to draw shoulders behind a person.
- `make_tile.py` makes one tile. Its first lines explain the options and what to install.

```
python3 tools/volunteer-tiles/make_tile.py photo.jpg src/assets/volunteers/jane-tan.jpg
python3 tools/volunteer-tiles/make_tile.py wide-photo.jpg src/assets/volunteers/jane-tan.jpg --crop 1200,600,3000,2700
python3 tools/volunteer-tiles/make_tile.py chest-up-photo.jpg src/assets/volunteers/jane-tan.jpg --zoom 1.5 --lower 0.05
python3 tools/volunteer-tiles/make_tile.py round-avatar.jpg src/assets/volunteers/jane-tan.jpg --circle --body --zoom 1.4
python3 tools/volunteer-tiles/make_tile.py passport-photo.jpg src/assets/volunteers/jane-tan.jpg --zoom 1.6 --lower 0.09 --band 0
python3 tools/volunteer-tiles/make_tile.py trimmed-cutout.png src/assets/volunteers/jane-tan.jpg --cutout --face 215,320,300 --edge 0.18
```

Use `--crop` when the photo is wide or has other people in it, and `--face` when the face is not found by itself. A photo cut off at the chest has its clothes stretched down to the bottom of the tile so the person does not float; add `--zoom 1.5 --lower 0.05` for such a photo so less has to be stretched. A side cut by the photo edge is faded out. For a round avatar, `--circle` ignores everything outside the circle, and `--body` draws shoulders and a body behind the person in the colour of their clothes instead of stretching; this works best with dark, plain clothes. The face finder sometimes takes in hair or a headscarf and makes a person too small: compare each new tile with the others and use `--zoom` to match. If the cut-out keeps only the face (clothing or a headscarf close in colour to the background), add `--model u2net_human_seg`. `--body` suits dark plain clothes; with light clothes it looks like a flat block, so stretch instead. For a passport-style photo that stops at the upper chest with an open collar, stretching drags the neck down: use `--band 0` (no stretching, the lower edge fades softly) with `--zoom` and `--lower` so the photo ends near the bottom. When the cut-out keeps background clutter, trim it by hand to a PNG with a transparent background and pass it with `--cutout` (and `--face` if the face is not found, for example with a tilted head). `--edge` sets how wide a side cut by the photo's edge fades; use less than the default 0.25 when the edge runs close to the face. Do not draw clothes or bodies for light clothing or to change what someone wears: it looks fake. Use the person's own photo. A photo showing the shoulders and some of the body looks best. Check each tile by eye before publishing.

These files are not part of the website build.
