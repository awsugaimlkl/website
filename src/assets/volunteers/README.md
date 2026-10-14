# Volunteer photos

One finished tile per volunteer, named to match the `photo` value in the event's `.md` file. For example, `photo: "jane-tan"` uses `jane-tan.jpg`.

Each tile is a square JPG of 840 by 840 pixels: the volunteer cut out of their photo, in colour, standing in front of the Kuala Lumpur skyline where the placeholder silhouette was. Make them with `tools/volunteer-tiles/make_tile.py` so every tile has the same background, size and position. The site shows the file as it is.

A volunteer whose file is not here yet is shown with the skyline silhouette (`src/assets/volunteer-placeholder.jpg`) above their name, so a name can go up before the photo arrives.
