# Volunteer tiles

Makes the Community Day volunteer photos: the person cut out of an ordinary photo, in black and white, in front of the Kuala Lumpur skyline. The face is scaled and placed where the placeholder silhouette's face was, so all tiles match.

- `background.jpg` is the volunteer placeholder art (`src/assets/volunteer-placeholder.jpg`) with the silhouette taken out.
- `make_tile.py` makes one tile. Its first lines explain the options and what to install.

```
python3 tools/volunteer-tiles/make_tile.py photo.jpg src/assets/volunteers/jane-tan.jpg
python3 tools/volunteer-tiles/make_tile.py wide-photo.jpg src/assets/volunteers/jane-tan.jpg --crop 1200,600,3000,2700
```

Use `--crop` when the photo is wide or has other people in it, and `--face` when the face is not found by itself. A photo cropped tight at the chest or shoulders is faded out towards those edges, so the person does not end in a hard line; a photo showing the shoulders and some of the body looks best. Check each tile by eye before publishing.

These files are not part of the website build.
