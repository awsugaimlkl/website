"""Enlarge a small comic-style portrait four times, keeping the ink lines sharp.

The superhero portraits come out of Canva at 200 by 200 pixels when downloaded
through its connector. This enlarges one to 800 by 800 with the Real-ESRGAN
anime model, which suits the comic style, before make_tile.py places it on the
skyline.

    python3 upscale.py PORTRAIT.jpg OUT.png [MODELS_DIR]

MODELS_DIR is the "models" folder from the Real-ESRGAN ncnn release
(realesrgan-ncnn-vulkan-20220424-ubuntu.zip, from the Real-ESRGAN GitHub
releases, version 0.2.5.0). It defaults to a "models" folder next to this
script. Runs on the processor, no graphics card needed, in a few seconds.

Needs: pip install ncnn pillow numpy
"""

import sys
from pathlib import Path

import ncnn
import numpy as np
from PIL import Image

MODEL = "realesrgan-x4plus-anime"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    models = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(__file__).parent / "models"

    net = ncnn.Net()
    net.opt.use_vulkan_compute = False
    net.opt.num_threads = 4
    net.load_param(str(models / f"{MODEL}.param"))
    net.load_model(str(models / f"{MODEL}.bin"))

    img = Image.open(src).convert("RGB")
    w, h = img.size
    mat = ncnn.Mat.from_pixels(np.asarray(img).tobytes(), ncnn.Mat.PixelType.PIXEL_RGB, w, h)
    mat.substract_mean_normalize([0.0, 0.0, 0.0], [1 / 255.0] * 3)

    ex = net.create_extractor()
    ex.input("data", mat)
    _, out = ex.extract("output")
    pixels = np.clip(np.array(out).transpose(1, 2, 0), 0, 1)
    Image.fromarray((pixels * 255 + 0.5).astype(np.uint8)).save(dst)
    print(f"{w}x{h} -> {pixels.shape[1]}x{pixels.shape[0]}")


if __name__ == "__main__":
    main()
