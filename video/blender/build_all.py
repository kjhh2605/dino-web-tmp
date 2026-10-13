"""전체 씬(S1–S9)을 다시 만들고 orbit_intro.blend로 저장한다.

- blender-mcp: execute_blender_code에 이 파일 내용을 보내거나 `exec(open(path).read())`
- 단독 실행: blender -b -P build_all.py  (또는 bpy 모듈: python build_all.py)
"""
import importlib
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else \
    '/home/user/dino-web-tmp/video/blender'
sys.path.insert(0, ROOT)

import bpy  # noqa: E402

import orbit_lib as L  # noqa: E402

SHOTS = ['s1_phone', 's2_chaos', 's3_city', 's4_orbit', 's5_assign', 's6_accept', 's7_board', 's8_report', 's9_end']

importlib.reload(L)
L.reset_scene()
for name in SHOTS:
    mod = importlib.import_module('shots.' + name)
    importlib.reload(mod)
    mod.build(L)
s = bpy.context.scene
s.camera = bpy.data.objects['CAM_S1']
s.eevee.taa_render_samples = 32
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, 'orbit_intro.blend'), relative_remap=True)
print('saved', os.path.join(ROOT, 'orbit_intro.blend'), 'markers:',
      [(m.name, m.frame) for m in sorted(s.timeline_markers, key=lambda m: m.frame)])
