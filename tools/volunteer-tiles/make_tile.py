"""Make a Community Day volunteer tile from an ordinary photo.

The person is cut out of the photo, turned black and white, and placed in front
of the Kuala Lumpur skyline (background.jpg, the volunteer placeholder art with
its silhouette taken out). The face is scaled and placed where the silhouette's
face was, so every tile matches.

    python3 make_tile.py PHOTO OUT.jpg [--crop X0,Y0,X1,Y1] [--face X,Y,H]

  --crop   crop the photo first (pixels in the original photo). Use it when the
           photo is wide or has other people in it.
  --face   the face centre and face height, in pixels of the original photo,
           when the face is not found automatically.

Needs: pip install rembg onnxruntime pillow numpy "opencv-python-headless<5"
(OpenCV 5 no longer has the face finder used here). The first run downloads
the cut-out model (about 170 MB). The larger BiRefNet models give finer hair
but need more than 8 GB of memory.

Save the result in src/assets/volunteers/ and set the volunteer's photo to its
file name without the extension.
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))

# Where the silhouette's face was, as fractions of the background's size.
FACE_X, FACE_Y, FACE_H = 0.500, 0.403, 0.239
OUT_SIZE = 840


def find_face(rgb):
    import cv2

    if not hasattr(cv2, "CascadeClassifier"):
        sys.exit('This OpenCV has no face finder: install "opencv-python-headless<5", or pass --face.')
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    faces = casc.detectMultiScale(gray, 1.1, 6, minSize=(60, 60))
    if len(faces) == 0:
        sys.exit("No face found. Pass --face X,Y,H (face centre and height in the original photo).")
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    return x + w / 2, y + h / 2, h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("out")
    ap.add_argument("--crop")
    ap.add_argument("--face")
    args = ap.parse_args()

    photo = ImageOps.exif_transpose(Image.open(args.photo)).convert("RGB")
    x0 = y0 = 0
    if args.crop:
        x0, y0, x1, y1 = (int(v) for v in args.crop.split(","))
        photo = photo.crop((x0, y0, x1, y1))
    # Work at a sensible size: the cut-out model sees about 1000 pixels anyway.
    shrink = min(1.0, 1400 / max(photo.size))
    if shrink < 1:
        photo = photo.resize((round(photo.width * shrink), round(photo.height * shrink)), Image.LANCZOS)

    from rembg import new_session, remove

    cut = remove(photo, session=new_session("isnet-general-use")).convert("RGBA")

    if args.face:
        fx, fy, fh = (float(v) for v in args.face.split(","))
        fx, fy, fh = (fx - x0) * shrink, (fy - y0) * shrink, fh * shrink
    else:
        fx, fy, fh = find_face(np.array(cut.convert("RGB")))

    bg = Image.open(os.path.join(HERE, "background.jpg")).convert("RGB")
    W, H = bg.size
    k = FACE_H * H / fh
    cut = cut.resize((max(1, round(cut.width * k)), max(1, round(cut.height * k))), Image.LANCZOS)
    ox, oy = round(FACE_X * W - fx * k), round(FACE_Y * H - fy * k)

    # A photo cropped tight (at the chest or through the shoulders) would end in a
    # hard straight line inside the tile. Fade the person out towards any photo
    # edge they touch, when that edge falls inside the tile.
    alpha = np.array(cut.split()[3]).astype(np.float32)
    ch, cw = alpha.shape
    ramp = 0.5 * FACE_H * H
    yy = np.arange(ch, dtype=np.float32)[:, None]
    xx = np.arange(cw, dtype=np.float32)[None, :]
    fade = np.ones_like(alpha)

    def touches(edge):
        return (edge > 128).mean() > 0.02

    def smooth(t):
        t = np.clip(t, 0, 1)
        return t * t * (3 - 2 * t)

    if oy + ch < H and touches(alpha[-1, :]):
        fade = np.minimum(fade, smooth((ch - 1 - yy) / ramp))
    if ox > 0 and touches(alpha[:, 0]):
        fade = np.minimum(fade, smooth(xx / ramp))
    if ox + cw < W and touches(alpha[:, -1]):
        fade = np.minimum(fade, smooth((cw - 1 - xx) / ramp))
    if oy > 0 and touches(alpha[0, :]):
        fade = np.minimum(fade, smooth(yy / ramp))
    cut.putalpha(Image.fromarray((alpha * fade).astype(np.uint8)))

    # Black and white, with a touch of contrast. Only the person, not the skyline.
    a = np.array(cut).astype(np.float32)
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255.0
    lum = np.clip((lum - 0.5) * 1.08 + 0.52, 0, 1) * 255
    person = Image.fromarray(np.dstack([lum, lum, lum, a[..., 3]]).astype(np.uint8), "RGBA")

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(person, (max(ox, 0), max(oy, 0)), (max(-ox, 0), max(-oy, 0)))

    # A soft lavender glow around the person, like the silhouette's rim light.
    glow = Image.new("RGBA", (W, H), (190, 160, 255, 0))
    glow.putalpha(layer.split()[3].filter(ImageFilter.GaussianBlur(0.0144 * W)).point(lambda p: int(p * 0.55)))

    out = bg.convert("RGBA")
    out.alpha_composite(glow)
    out.alpha_composite(layer)

    # Fade the bottom of the frame into the dark, as the placeholder art does.
    t = np.linspace(0, 1, H)[:, None]
    fade = (np.clip((t - 0.78) / 0.22, 0, 1) ** 1.4 * 0.75)[..., None]
    o = np.array(out.convert("RGB")).astype(np.float32)
    o = o * (1 - fade) + np.array([16, 14, 60], np.float32) * fade

    Image.fromarray(o.astype(np.uint8)).resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS).save(
        args.out, quality=88, optimize=True, progressive=True
    )
    print(f"face at {fx / shrink + x0:.0f},{fy / shrink + y0:.0f} height {fh / shrink:.0f} (original photo pixels)")


if __name__ == "__main__":
    main()
