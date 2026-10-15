# Volunteer tiles

Makes the Community Day volunteer tiles. Every volunteer is shown as a comic-book superhero: the person redrawn from their photo in one comic style and one matching suit, in front of the Kuala Lumpur skyline. Use the same steps and the same prompt for a new volunteer so all the tiles match. The suit is our own design: do not use Marvel or any other existing characters, names, emblems or logos.

- `background.jpg` is the volunteer placeholder art (`src/assets/volunteer-placeholder.jpg`) with the silhouette taken out.
- `body-mask.png` is the placeholder silhouette's shape, used by `--body` to draw shoulders behind a person.
- `make_tile.py` cuts the person out and places them on the skyline. Its first lines explain the options and what to install.
- `upscale.py` enlarges a small comic portrait four times. Its first lines explain what to download.

## Superhero tiles

1. **Redraw the photo in Canva.** Generate an image (square) with the volunteer's photo as the reference image and the prompt below. Use her/she or his/he to match the person.

   > Redraw the person in this image as an original comic-book superhero portrait. Keep her face, facial features, skin tone, hairstyle and expression the same so she is clearly recognisable. Head and shoulders, facing the viewer, centred, cropped at mid-chest with both shoulders fully in frame, no hands. She wears an original sleek superhero suit in midnight navy with bright orange-gold panels on the shoulders and a high collar, long sleeves, no logos, no letters, no emblems, no symbols, no cape, no mask. Bold clean ink outlines, cel shading, vibrant saturated colours, modern comic-book illustration style. Plain flat light grey background with nothing else in it.

   Add what makes the person recognisable to the "Keep" sentence: glasses, grey hair, curly or long hair, a smile. For a headscarf, add: "and keep her headscarf (hijab) exactly as in the photo, fully covering her hair and neck, with the suit's high collar under it", with its colour. Name things in the photo to leave out after "no hands" (a backpack, a laptop, a hand gesture). Compare the result with the photo and generate again if the face is not a good likeness.

2. **Enlarge it if it is small.** A portrait downloaded from Canva at full size can be used as it is. The 200 by 200 pixel version the Canva connector returns is enlarged to 800 by 800 first:

   ```
   python3 tools/volunteer-tiles/upscale.py portrait.jpg portrait-800.png path/to/models
   ```

3. **Place it on the skyline.** Most tiles use `--zoom 1.35 --lower 0.04`. Compare the new tile with the others at tile size and change `--zoom` until the face matches theirs: a headscarf or big hair makes the face finder's box too large, so the person needs more zoom.

   ```
   python3 tools/volunteer-tiles/make_tile.py portrait-800.png src/assets/volunteers/jane-tan.jpg --zoom 1.35 --lower 0.04
   ```

   Settings used on 15 October 2026: `--zoom 1.35 --lower 0.04` for Yap Hock Seng, Chong Hun Yee, Jerry Chong, Lavanesswary and Edelyn Seah; 1.25 for Chan Kar Fong; 1.45 for Tuan Nur Sumayyah Binti Roseli; 1.5 for Muhammad Fikhri; 1.6 for Fatin Najdah; 1.25 with `--face 395,290,320` for Ruben Chong, whose tilted head is not found by the face finder.

## make_tile.py options

```
python3 tools/volunteer-tiles/make_tile.py photo.jpg src/assets/volunteers/jane-tan.jpg
python3 tools/volunteer-tiles/make_tile.py wide-photo.jpg src/assets/volunteers/jane-tan.jpg --crop 1200,600,3000,2700
python3 tools/volunteer-tiles/make_tile.py chest-up-photo.jpg src/assets/volunteers/jane-tan.jpg --zoom 1.5 --lower 0.05
python3 tools/volunteer-tiles/make_tile.py round-avatar.jpg src/assets/volunteers/jane-tan.jpg --circle --body --zoom 1.4
python3 tools/volunteer-tiles/make_tile.py passport-photo.jpg src/assets/volunteers/jane-tan.jpg --zoom 1.6 --lower 0.09 --band 0
python3 tools/volunteer-tiles/make_tile.py trimmed-cutout.png src/assets/volunteers/jane-tan.jpg --cutout --face 215,320,300 --edge 0.18
```

The script also works on an ordinary photo, which is how the tiles were made before the superhero look. Use `--crop` when the photo is wide or has other people in it, and `--face` when the face is not found by itself. A photo cut off at the chest has its clothes stretched down to the bottom of the tile so the person does not float; add `--zoom 1.5 --lower 0.05` for such a photo so less has to be stretched. A side cut by the photo edge is faded out. For a round avatar, `--circle` ignores everything outside the circle, and `--body` draws shoulders and a body behind the person in the colour of their clothes instead of stretching; this works best with dark, plain clothes. The face finder sometimes takes in hair or a headscarf and makes a person too small: compare each new tile with the others and use `--zoom` to match. If the cut-out keeps only the face (clothing or a headscarf close in colour to the background), add `--model u2net_human_seg`. `--body` suits dark plain clothes; with light clothes it looks like a flat block, so stretch instead. For a passport-style photo that stops at the upper chest with an open collar, stretching drags the neck down: use `--band 0` (no stretching, the lower edge fades softly) with `--zoom` and `--lower` so the photo ends near the bottom. When the cut-out keeps background clutter, trim it by hand to a PNG with a transparent background and pass it with `--cutout` (and `--face` if the face is not found, for example with a tilted head). `--edge` sets how wide a side cut by the photo's edge fades; use less than the default 0.25 when the edge runs close to the face. Do not draw clothes onto an ordinary photo or change what someone wears by hand: it looks fake. Check each tile by eye before publishing.

These files are not part of the website build.
