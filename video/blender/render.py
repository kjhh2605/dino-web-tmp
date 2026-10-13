"""orbit_intro.blend 렌더.

python render.py keyframes  → ../renders/keyframes/S#_<frame>[_clean].png (1920×1080, Higgsfield 시작·끝 프레임)
python render.py animatic   → ../renders/animatic/####.png (960×540, 자막 포함) — ffmpeg로 mp4 합성
"""
import os
import sys

import bpy

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, '..', 'renders')
mode = sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, 'orbit_intro.blend'))
s = bpy.context.scene
caps = bpy.data.collections['CAPTIONS']

# 샷별 Higgsfield 기준 프레임(시작·핵심)
KEYFRAMES = {'S1': (2, 64), 'S2': (78, 140), 'S3': (156, 210), 'S4': (222, 282), 'S5': (292, 360),
             'S6': (392, 452), 'S7': (474, 545), 'S8': (556, 612), 'S9': (630, 718)}


def cam_at(f):
    cam = None
    for m in sorted(s.timeline_markers, key=lambda m: m.frame):
        if m.frame <= f:
            cam = m.camera
    return cam


if mode == 'keyframes':
    os.makedirs(os.path.join(OUT, 'keyframes'), exist_ok=True)
    s.render.resolution_percentage = 100
    s.eevee.taa_render_samples = 32
    for shot, frames in KEYFRAMES.items():
        for f in frames:
            s.frame_set(f)
            s.camera = cam_at(f)
            for clean in (True, False):
                caps.hide_render = clean
                s.render.filepath = os.path.join(OUT, 'keyframes', f'{shot}_{f:03d}{"_clean" if clean else ""}.png')
                bpy.ops.render.render(write_still=True)
            print(shot, f, flush=True)
elif mode == 'animatic':
    os.makedirs(os.path.join(OUT, 'animatic'), exist_ok=True)
    s.render.resolution_percentage = 50
    s.eevee.taa_render_samples = 8
    caps.hide_render = False
    start = int(os.environ.get('FROM', 1))
    for f in range(start, s.frame_end + 1):
        path = os.path.join(OUT, 'animatic', f'{f:04d}.png')
        if os.path.exists(path):
            continue
        s.frame_set(f)
        s.camera = cam_at(f)
        s.render.filepath = path
        bpy.ops.render.render(write_still=True)
        print('frame', f, flush=True)
