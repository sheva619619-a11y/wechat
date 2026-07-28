# -*- coding: utf-8 -*-
"""从素材库封面底图合成 1880×800 公众号封面（无角标 LOGO）。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

LIB = Path(r"f:/1.3/低空安全防护项目/公众号/素材库")
FONT = r"C:\Windows\Fonts\msyhbd.ttc"


def make_cover(
    bg_path: Path,
    out_path: Path,
    tag: str,
    title: str,
    sub: str,
    brightness: float = 0.52,
) -> None:
    W, H = 1880, 800
    src = Image.open(bg_path).convert("RGB")
    sw, sh = src.size
    tr, sr = W / H, sw / sh
    if sr > tr:
        nw = int(sh * tr)
        left = (sw - nw) // 2
        src = src.crop((left, 0, left + nw, sh))
    else:
        nh = int(sw / tr)
        top = max(0, (sh - nh) // 4)
        src = src.crop((0, top, sw, min(sh, top + nh)))
    src = src.resize((W, H), Image.Resampling.LANCZOS)
    src = ImageEnhance.Brightness(src).enhance(brightness)
    out = src.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle([180, 210, 1700, 560], radius=18, fill=(6, 24, 48, 185))
    out = Image.alpha_composite(out, ov)
    draw = ImageDraw.Draw(out)

    def font(s):
        return ImageFont.truetype(FONT, s)

    tf, sf, gf = font(26), font(58), font(32)
    cx = W // 2
    tb = draw.textbbox((0, 0), tag, font=tf)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad_x, pad_y = 22, 10
    tag_cy = 263
    box_w, box_h = tw + pad_x * 2, th + pad_y * 2
    r = box_h // 2
    x0, y0 = cx - box_w // 2, tag_cy - box_h // 2
    draw.rounded_rectangle(
        [x0, y0, x0 + box_w, y0 + box_h], radius=r, outline=(46, 166, 230), width=2
    )
    draw.text((cx, tag_cy), tag, font=tf, fill=(46, 166, 230), anchor="mm")
    draw.text((cx, 348), title, font=sf, fill=(255, 255, 255), anchor="mm")
    draw.text((cx, 448), sub, font=gf, fill=(46, 166, 230), anchor="mm")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.convert("RGB").save(out_path, "PNG", optimize=True)
    print("saved", out_path)


if __name__ == "__main__":
    # 示例：用新政底图试合成
    make_cover(
        LIB / "01-封面底图" / "政策速递" / "01-城市夜景雷达底图.png",
        LIB / "01-封面底图" / "政策速递" / "_示例合成-政策封面.png",
        "政策速递",
        "示例：城市低空治理",
        "飞得开 · 管得住",
    )
