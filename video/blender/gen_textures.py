"""문제 제기 파트용 보조 텍스처(엑셀 일정표·현장 사진)를 만든다. Pillow 필요.

usage: python gen_textures.py   → assets/gen/*.png
"""
import os
import random

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'assets', 'gen')
FONT = os.path.join(ROOT, 'assets', 'fonts', 'Pretendard-SemiBold.otf')
os.makedirs(OUT, exist_ok=True)
random.seed(7)


def f(size):
    return ImageFont.truetype(FONT, size)


def excel():
    """수기로 관리하는 엑셀 배정표: 빈칸·물음표·빨간 수정 흔적."""
    w, h = 1600, 900
    im = Image.new('RGB', (w, h), '#ffffff')
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, 56], fill='#217346')
    d.text((24, 12), '현장배정_10월_최종_진짜최종(2).xlsx', font=f(28), fill='#ffffff')
    cols = ['기사', '09시', '10시', '11시', '12시', '13시', '14시', '15시', '비고']
    rows = ['김민수', '김민준', '이민준', '홍길동', '김태훈', '박서연', '이철호', '이준혁', '???']
    cw, rh, x0, y0 = 170, 82, 20, 80
    for i, c in enumerate(cols):
        d.rectangle([x0 + i * cw, y0, x0 + (i + 1) * cw, y0 + rh], fill='#e8eef7', outline='#b7c3d0')
        d.text((x0 + i * cw + 16, y0 + 24), c, font=f(30), fill='#333333')
    notes = {
        (0, 1): '인덕션', (0, 5): '에어컨?', (1, 1): '에어컨 설치', (2, 2): '보일러', (2, 6): '냉장고',
        (3, 1): '정수기', (3, 3): '욕실', (5, 5): '보일러 수리', (5, 6): '보일러 수리', (6, 1): '식기세척기',
        (6, 5): '세탁기', (8, 2): '전화 요망', (4, 8): '연락 안됨', (2, 8): '현장 늦음', (7, 4): '배관??',
    }
    for r, name in enumerate(rows):
        y = y0 + (r + 1) * rh
        for i in range(len(cols)):
            d.rectangle([x0 + i * cw, y, x0 + (i + 1) * cw, y + rh], fill='#ffffff', outline='#d0d7de')
        d.text((x0 + 16, y + 24), name, font=f(30), fill='#222222')
        for (rr, cc), t in notes.items():
            if rr == r:
                warn = '?' in t or '안됨' in t or '늦음' in t or '요망' in t
                if warn:
                    d.rectangle([x0 + cc * cw + 2, y + 2, x0 + (cc + 1) * cw - 2, y + rh - 2], fill='#fde2e2')
                d.text((x0 + cc * cw + 14, y + 24), t, font=f(26), fill='#c62828' if warn else '#333333')
    # 겹친 배정(같은 칸 두 줄)과 취소선
    d.line([x0 + 5 * cw + 10, y0 + 6 * rh + 41, x0 + 6 * cw - 10, y0 + 6 * rh + 41], fill='#c62828', width=4)
    d.ellipse([x0 + 5 * cw - 10, y0 + 6 * rh - 8, x0 + 7 * cw + 10, y0 + 7 * rh + 8], outline='#c62828', width=5)
    im.save(os.path.join(OUT, 'excel.png'))


def photo(name, clean):
    """완료 보고 사진(보일러 전·후) 일러스트."""
    w, h = 600, 600
    im = Image.new('RGB', (w, h), '#d9d4cc' if not clean else '#e9edf2')
    d = ImageDraw.Draw(im)
    d.rectangle([0, 420, w, h], fill='#b8afa3' if not clean else '#cfd6df')
    d.rounded_rectangle([170, 90, 430, 470], 18, fill='#f3f3f3' if clean else '#d8d2c4', outline='#888888', width=4)
    d.rounded_rectangle([210, 140, 390, 220], 10, fill='#2b2b35')
    d.text((232, 162), '45°C' if clean else 'E-02', font=f(40), fill='#7CFC9A' if clean else '#ff5252')
    for i in range(4):
        d.rectangle([215 + i * 45, 470, 235 + i * 45, 560], fill='#9aa3ad' if clean else '#8a6a4a')
    if not clean:
        for _ in range(40):
            x, y = random.randint(175, 425), random.randint(250, 465)
            r = random.randint(4, 14)
            d.ellipse([x - r, y - r, x + r, y + r], fill=random.choice(['#a0522d', '#8b5a2b', '#6b4423']))
    else:
        d.ellipse([440, 40, 560, 160], fill='#277d02')
        d.line([470, 100, 495, 128, 535, 72], fill='#ffffff', width=12, joint='curve')
    tag = '작업 후' if clean else '작업 전'
    d.rounded_rectangle([20, 20, 170, 74], 12, fill='#1c1b2a')
    d.text((40, 28), tag, font=f(30), fill='#ffffff')
    im.save(os.path.join(OUT, name))


if __name__ == '__main__':
    excel()
    photo('photo_before.png', False)
    photo('photo_after.png', True)
    print('textures ->', OUT)
