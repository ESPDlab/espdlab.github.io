"""소식 목록에 쓰는 작은 사진을 만든다.
쓰는 법(저장소 폴더에서):  python tools/make_thumbs.py
media/news/ 아래의 사진마다 media/thumb/news/…/<같은 이름>.jpg (긴 변 800px)를 만든다. 이미 있는 것은 건너뛴다.
작은 사진이 없어도 사이트는 원래 사진을 대신 보여 주므로, 이 스크립트를 돌리지 않아도 고장 나지는 않는다(조금 느릴 뿐이다)."""
import os
from PIL import Image, ImageOps

SRC, DST, SIZE = "media/news", "media/thumb/news", 800
made = 0
for d, _, files in os.walk(SRC):
    for f in sorted(files):
        if not f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        src = os.path.join(d, f)
        dst = os.path.join(DST, os.path.relpath(d, SRC), f + ".jpg")
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            continue
        im = ImageOps.exif_transpose(Image.open(src))
        if im.mode in ("RGBA", "LA", "P"):                     # 투명한 곳은 흰색으로 채운다
            im = im.convert("RGBA")
            im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im)
        im = im.convert("RGB")
        im.thumbnail((SIZE, SIZE), Image.LANCZOS)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        im.save(dst, quality=80, optimize=True, progressive=True)
        made += 1
# 원래 사진이 없어진 작은 사진은 지운다
for d, _, files in os.walk(DST):
    for f in files:
        if not os.path.exists(os.path.join(SRC, os.path.relpath(d, DST), f[:-4])):
            os.remove(os.path.join(d, f))
print("made", made)
