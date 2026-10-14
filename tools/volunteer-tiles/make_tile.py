"""Make a Community Day volunteer tile from an ordinary photo.

The person is cut out of the photo, brightened a little, and placed in front of
the Kuala Lumpur skyline (background.jpg, the volunteer placeholder art with its
silhouette taken out). The face is scaled and placed where the silhouette's face
was, so every tile matches.

    python3 make_tile.py PHOTO OUT.jpg [--crop X0,Y0,X1,Y1] [--face X,Y,H]

  --crop   crop the photo first (pixels in the original photo). Use it when the
           photo is wide or has other people in it.
  --face   the face centre and face height, in pixels of the original photo,
           when the face is not found automatically.

A photo cut off at the chest would leave the person floating. The script then
stretches the lowest part of their clothes down to the bottom of the tile. For
such a photo, make the person larger and lower too (--zoom 1.5 --lower 0.05),
so less has to be stretched. A photo showing the shoulders and some of the body
still looks best.

  --zoom   make the person larger than the standard size (1.0).
  --lower  move the person down, as a fraction of the tile's height.

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
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

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


def touches(edge):
    return (edge > 128).mean() > 0.02


def extend_body(cut, ox, oy, W, H, face_px, chin):
    """Keep a person cut off at the chest from floating: stretch the lowest part of
    their clothes (below the chin, folds and outline included) down to the bottom
    of the tile. Sides cut by the photo's edge are softened instead."""
    a = np.array(cut).astype(np.float32)
    al = a[..., 3]
    ch, cw = al.shape

    if oy + ch < H and touches(al[-1, :]):
        gap = H - (oy + ch) + 8
        band = int(max(2, min(ch - max(chin, 0), max(0.15 * face_px, gap / 3))))
        top = Image.fromarray(a[: ch - band].astype(np.uint8), "RGBA")
        low = Image.fromarray(a[ch - band :].astype(np.uint8), "RGBA").resize((cw, band + gap), Image.BICUBIC)
        out = Image.new("RGBA", (cw, ch + gap), (0, 0, 0, 0))
        out.paste(top, (0, 0))
        out.paste(low, (0, ch - band))
        cut = out
        a = np.array(cut).astype(np.float32)
        al = a[..., 3]
        ch, cw = al.shape

    # A side cut by the photo's edge, or the top, fades out instead of ending in a hard line.
    ramp = 0.25 * face_px
    yy = np.arange(ch, dtype=np.float32)[:, None]
    xx = np.arange(cw, dtype=np.float32)[None, :]

    def smooth(t):
        t = np.clip(t, 0, 1)
        return t * t * (3 - 2 * t)

    fade = np.ones_like(al)
    if ox > 0 and touches(al[:, 0]):
        fade = np.minimum(fade, smooth(xx / ramp))
    if ox + cw < W and touches(al[:, -1]):
        fade = np.minimum(fade, smooth((cw - 1 - xx) / ramp))
    if oy > 0 and touches(al[0, :]):
        fade = np.minimum(fade, smooth(yy / ramp))
    cut.putalpha(Image.fromarray((al * fade).astype(np.uint8)))
    return cut, ox, oy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("out")
    ap.add_argument("--crop")
    ap.add_argument("--face")
    ap.add_argument("--zoom", type=float, default=1.0)
    ap.add_argument("--lower", type=float, default=0.0)
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
    k = args.zoom * FACE_H * H / fh
    cut = cut.resize((max(1, round(cut.width * k)), max(1, round(cut.height * k))), Image.LANCZOS)
    ox, oy = round(FACE_X * W - fx * k), round((FACE_Y + args.lower) * H - fy * k)

    cut, ox, oy = extend_body(cut, ox, oy, W, H, fh * k, (fy + 0.6 * fh) * k)

    # Natural colour, a little brighter and livelier so the person stands out on the dark blue.
    alpha = cut.split()[3]
    rgb = cut.convert("RGB")
    rgb = ImageEnhance.Brightness(rgb).enhance(1.06)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.05)
    rgb = ImageEnhance.Color(rgb).enhance(1.12)
    person = rgb.convert("RGBA")
    person.putalpha(alpha)

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
