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
  --circle the photo is a round avatar: fill outside the circle with the photo's
           background colour before cutting the person out.
  --body   draw shoulders and a body behind the person in the colour of their
           clothes (the placeholder silhouette's shape, body-mask.png) instead of
           stretching their clothes. Best with dark, plain clothes; use it when
           stretching shows skin or a collar, as with a round avatar.
  --model  the cut-out model (default isnet-general-use). Use u2net_human_seg when
           clothing or a headscarf is close in colour to the background and the
           default keeps only the face.

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


def fill_outside_circle(photo):
    """A round avatar: replace whatever is outside the circle (often black) with
    the photo's own background colour, so it is not taken for clothing."""
    a = np.array(photo).astype(np.float32)
    h, w, _ = a.shape
    cx, cy, r = (w - 1) / 2, (h - 1) / 2, min(w, h) / 2
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.hypot(xx - cx, yy - cy)
    ring = (dist < r - 4) & (dist > r - 14) & (yy < cy)      # just inside the circle, top half
    bg = np.median(a[ring], axis=0)
    a[dist > r - 2.5] = bg
    return Image.fromarray(a.astype(np.uint8))


def drawn_body(cut, oy, W, H, chin, face_px):
    """Shoulders and body for a photo that shows too little of them (a round avatar,
    a tight crop): the placeholder silhouette's shoulders, below the person's chin,
    in the colour of their clothes with soft shading. It goes behind the person."""
    import cv2

    a = np.array(cut).astype(np.float32)
    al = a[..., 3]
    ch = al.shape[0]
    low = slice(max(0, int(ch * 0.85)), ch)
    sel = al[low] > 230
    cloth = np.median(a[low][..., :3][sel], axis=0) if sel.any() else np.array([30, 30, 34], np.float32)

    mask = np.array(Image.open(os.path.join(HERE, "body-mask.png")).convert("L").resize((W, H))).astype(np.float32)
    # The silhouette's shoulders are broad: narrow them a little.
    narrow = int(W * 0.9)
    squeezed = np.array(Image.fromarray(mask.astype(np.uint8)).resize((narrow, H), Image.BILINEAR)).astype(np.float32)
    mask = np.zeros((H, W), np.float32)
    mask[:, (W - narrow) // 2:(W - narrow) // 2 + narrow] = squeezed
    # The silhouette frays out before the bottom of the frame: below its widest row,
    # carry that row straight down.
    widest = int(np.argmax((mask > 127).sum(axis=1)))
    mask[widest:] = mask[widest]
    top = int(oy + chin)
    mask[: max(0, top)] = 0
    ramp = int(0.15 * face_px)                       # ease the body in below the chin
    for i in range(ramp):
        r = top + i
        if 0 <= r < H:
            mask[r] *= i / ramp
    inside = (mask > 127).astype(np.uint8)
    dist = cv2.distanceTransform(inside, cv2.DIST_L2, 5)
    shade = 0.82 + 0.18 * np.clip(dist / (0.4 * face_px), 0, 1)
    rgb = cloth[None, None, :] * shade[..., None]
    alpha = cv2.GaussianBlur(mask, (0, 0), 2)
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), alpha]).astype(np.uint8), "RGBA")


def fade_bottom_edge(cut, face_px):
    """With a drawn body behind, let the lower edge of the photo (wherever it was cut)
    melt into it instead of showing a line."""
    a = np.array(cut).astype(np.float32)
    al = a[..., 3]
    h, w = al.shape
    inside = al > 128
    has = inside.any(axis=0)
    bottom = np.where(has, h - 1 - np.argmax(inside[::-1], axis=0), 0).astype(np.float32)
    ramp = 0.05 * face_px
    yy = np.arange(h, dtype=np.float32)[:, None]
    t = np.clip((bottom[None, :] - yy) / ramp, 0, 1)
    al = al * (t * t * (3 - 2 * t))
    cut.putalpha(Image.fromarray(al.astype(np.uint8)))
    return cut


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("out")
    ap.add_argument("--crop")
    ap.add_argument("--face")
    ap.add_argument("--zoom", type=float, default=1.0)
    ap.add_argument("--lower", type=float, default=0.0)
    ap.add_argument("--circle", action="store_true")
    ap.add_argument("--body", action="store_true")
    ap.add_argument("--model", default="isnet-general-use")
    args = ap.parse_args()

    photo = ImageOps.exif_transpose(Image.open(args.photo)).convert("RGB")
    x0 = y0 = 0
    if args.crop:
        x0, y0, x1, y1 = (int(v) for v in args.crop.split(","))
        photo = photo.crop((x0, y0, x1, y1))
    if args.circle:
        photo = fill_outside_circle(photo)
    # Work at a sensible size: the cut-out model sees about 1000 pixels anyway.
    shrink = min(1.0, 1400 / max(photo.size))
    if shrink < 1:
        photo = photo.resize((round(photo.width * shrink), round(photo.height * shrink)), Image.LANCZOS)

    from rembg import new_session, remove

    cut = remove(photo, session=new_session(args.model)).convert("RGBA")

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

    chin = (fy + 0.6 * fh) * k
    body = None
    if args.body:
        body = drawn_body(cut, oy, W, H, chin, fh * k)
        cut = fade_bottom_edge(cut, fh * k)
    else:
        cut, ox, oy = extend_body(cut, ox, oy, W, H, fh * k, chin)

    # Natural colour, a little brighter and livelier so the person stands out on the dark blue.
    alpha = cut.split()[3]
    rgb = cut.convert("RGB")
    rgb = ImageEnhance.Brightness(rgb).enhance(1.06)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.05)
    rgb = ImageEnhance.Color(rgb).enhance(1.12)
    person = rgb.convert("RGBA")
    person.putalpha(alpha)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if body is not None:
        layer.alpha_composite(body)
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
