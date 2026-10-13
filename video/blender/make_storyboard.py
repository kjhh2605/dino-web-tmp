"""기준 프레임으로 9샷 콘티 시트(renders/storyboard.jpg)를 만들고 키프레임 PNG를 JPG로 줄인다. Pillow 필요."""
import glob
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
KF = os.path.join(ROOT, '..', 'renders', 'keyframes')
FONT = os.path.join(ROOT, 'assets', 'fonts', 'Pretendard-Bold.otf')
SHOTS = [('S1', 64, '0:00–0:03', '쉬지 않고 울리는 전화'), ('S2', 140, '0:03–0:06', '흩어진 일정 · 일정 충돌'),
         ('S3', 210, '0:06–0:09', '보이지 않는 현장'), ('S4', 282, '0:09–0:12', '하나의 궤도로 → Orbit'),
         ('S5', 360, '0:12–0:16', '드래그 한 번으로 배정'), ('S6', 452, '0:16–0:19.5', '기사 앱에서 바로 수락'),
         ('S7', 545, '0:19.5–0:23', '진행 상황을 실시간으로'), ('S8', 612, '0:23–0:26', '완료 보고까지, 전화 없이'),
         ('S9', 718, '0:26–0:30', '엔딩 · 로고 + 헤드라인')]

# 1) PNG → JPG(저장소 용량)
for p in glob.glob(os.path.join(KF, '*.png')):
    Image.open(p).convert('RGB').save(p[:-4] + '.jpg', quality=90)
    os.remove(p)

# 2) 3×3 콘티 시트
tw, th, pad, lab = 640, 360, 24, 64
sheet = Image.new('RGB', (3 * tw + 4 * pad, 3 * (th + lab) + 4 * pad + 80), '#1c1b2a')
d = ImageDraw.Draw(sheet)
d.text((pad, pad), 'Orbit 소개 영상 30s — 콘티', font=ImageFont.truetype(FONT, 40), fill='#ffffff')
f1, f2 = ImageFont.truetype(FONT, 26), ImageFont.truetype(FONT, 22)
for i, (shot, frame, tc, title) in enumerate(SHOTS):
    x = pad + (i % 3) * (tw + pad)
    y = 80 + pad + (i // 3) * (th + lab + pad)
    im = Image.open(os.path.join(KF, f'{shot}_{frame:03d}.jpg')).resize((tw, th), Image.LANCZOS)
    sheet.paste(im, (x, y))
    d.text((x, y + th + 10), f'{shot}  {title}', font=f1, fill='#ffffff')
    d.text((x + tw, y + th + 14), tc, font=f2, fill='#a99fff', anchor='ra')
sheet.save(os.path.join(KF, '..', 'storyboard.jpg'), quality=90)
print('storyboard.jpg')
