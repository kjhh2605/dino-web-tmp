"""Orbit 소개 영상(30초) Blender 씬 공통 헬퍼.

blender-mcp의 execute_blender_code로 각 샷 스크립트를 보낼 때 이 모듈을 import 한다.
단위는 m, 24fps, 720프레임. 색은 front/src/styles/tokens.css의 브랜드 토큰을 쓴다.
"""
import math
import os

import bpy
from mathutils import Vector

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, 'assets')
FPS = 24
END = 720

# tokens.css
C = {
    'primary': '#1c1b2a',
    'secondary': '#4f3bfe',
    'primary100': '#a99fff',
    'white': '#ffffff',
    'gray50': '#f4f4f4',
    'gray100': '#e9e9ea',
    'gray300': '#cecece',
    'gray500': '#9b9b9b',
    'gray700': '#585858',
    'gray900': '#222222',
    'bg2': '#f1f1f6',
    'pending': '#1f1f1f',
    'accepted': '#4f3bfe',
    'confirmed': '#ece5fe',
    'progress': '#eea216',
    'progress_bg': '#ffebc5',
    'completed': '#277d02',
    'completed_bg': '#d8f2cd',
    'warning': '#d71a29',
    'warning_bg': '#feeded',
    'kakao': '#fee500',
    'paper': '#f6f1e4',
    'sticky': '#ffd966',
    'sticky2': '#ffb3c1',
    'sticky3': '#b5e3ff',
    'desk': '#3a302a',
    'city': '#2a2a3c',
}


def srgb(hex_):
    h = hex_.lstrip('#')
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


# ---------------------------------------------------------------- scene

def reset_scene():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.curves, bpy.data.cameras,
                 bpy.data.lights, bpy.data.images, bpy.data.actions):
        for b in list(coll):
            coll.remove(b)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)
    s = bpy.context.scene
    s.timeline_markers.clear()
    s.frame_start, s.frame_end = 1, END
    s.render.fps = FPS
    s.render.resolution_x, s.render.resolution_y = 1920, 1080
    s.render.engine = 'BLENDER_EEVEE'
    s.view_settings.view_transform = 'Standard'
    s.view_settings.look = 'None'
    w = bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
    s.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get('Background')
    bg.inputs[0].default_value = srgb(C['primary'])
    bg.inputs[1].default_value = 1.0
    return s


def collection(name):
    c = bpy.data.collections.get(name)
    if not c:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def _link(obj, coll):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    collection(coll).objects.link(obj)
    return obj


# ---------------------------------------------------------------- materials

def mat(name, color, rough=0.45, emit=0.0, metal=0.0, alpha=1.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    col = srgb(color) if isinstance(color, str) else color
    p.inputs['Base Color'].default_value = col
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if emit:
        p.inputs['Emission Color'].default_value = col
        p.inputs['Emission Strength'].default_value = emit
    if alpha < 1:
        p.inputs['Alpha'].default_value = alpha
    return m


def emit_mat(name, color, strength=1.0):
    """조명과 무관하게 같은 색으로 보이는 평면 색(글자·UI 칩)."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = srgb(color) if isinstance(color, str) else color
    em.inputs['Strength'].default_value = strength
    nt.links.new(em.outputs[0], out.inputs[0])
    return m


def image_mat(name, path, strength=1.0):
    """실제 서비스 화면 캡처를 화면 발광 텍스처로."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    img = bpy.data.images.load(path, check_existing=True)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    tex = nt.nodes.new('ShaderNodeTexImage')
    tex.image = img
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Strength'].default_value = strength
    nt.links.new(tex.outputs['Color'], em.inputs['Color'])
    nt.links.new(em.outputs[0], out.inputs[0])
    return m


def color_socket(m):
    """애니메이션할 색 입력(발광이면 Emission Color, 아니면 Base Color)."""
    nt = m.node_tree
    em = next((n for n in nt.nodes if n.type == 'EMISSION'), None)
    if em:
        return em.inputs['Color']
    return nt.nodes.get('Principled BSDF').inputs['Base Color']


def key_color(m, frame, color):
    s = color_socket(m)
    s.default_value = srgb(color)
    s.keyframe_insert('default_value', frame=frame)


def key_strength(m, frame, value):
    nt = m.node_tree
    em = next((n for n in nt.nodes if n.type == 'EMISSION'), None)
    sock = em.inputs['Strength'] if em else nt.nodes.get('Principled BSDF').inputs['Emission Strength']
    sock.default_value = value
    sock.keyframe_insert('default_value', frame=frame)


# ---------------------------------------------------------------- primitives

def _obj_from_op(name, coll, material=None):
    o = bpy.context.active_object
    o.name = name
    if material:
        o.data.materials.append(material)
    return _link(o, coll)


def rbox(name, size, loc, material, coll, bevel=0.02, rot=(0, 0, 0), segments=4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = _obj_from_op(name, coll, material)
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        b = o.modifiers.new('bevel', 'BEVEL')
        b.width = bevel
        b.segments = segments
        b.limit_method = 'NONE'
    return o


def plane(name, size, loc, material, coll, rot=(math.radians(90), 0, 0)):
    """기본은 -Y(카메라 쪽)를 보는 세로 평면."""
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = _obj_from_op(name, coll, material)
    o.scale = (size[0], size[1], 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o


def cyl(name, r, depth, loc, material, coll, rot=(0, 0, 0), verts=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    return _obj_from_op(name, coll, material)


def sphere(name, r, loc, material, coll, seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=seg // 2)
    o = _obj_from_op(name, coll, material)
    bpy.ops.object.shade_smooth()
    return o


def torus(name, major, minor, loc, material, coll, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, location=loc, rotation=rot,
                                     major_segments=96, minor_segments=12)
    o = _obj_from_op(name, coll, material)
    bpy.ops.object.shade_smooth()
    return o


def empty(name, loc, coll):
    o = bpy.data.objects.new(name, None)
    o.location = loc
    collection(coll).objects.link(o)
    return o


FONTS = {}


def font(weight='Bold'):
    if weight not in FONTS:
        FONTS[weight] = bpy.data.fonts.load(os.path.join(ASSETS, 'fonts', f'Pretendard-{weight}.otf'),
                                            check_existing=True)
    return FONTS[weight]


def text(name, body, loc, size, material, coll, weight='Bold', align='CENTER', rot=(math.radians(90), 0, 0),
         extrude=0.0, valign='CENTER'):
    cu = bpy.data.curves.new(name, 'FONT')
    cu.body = body
    cu.font = font(weight)
    cu.size = size
    cu.align_x = align
    cu.align_y = valign
    cu.extrude = extrude
    o = bpy.data.objects.new(name, cu)
    o.location = loc
    o.rotation_euler = rot
    cu.materials.append(material)
    collection(coll).objects.link(o)
    return o


# ---------------------------------------------------------------- animation

def key(o, frame, loc=None, rot=None, scale=None):
    if loc is not None:
        o.location = loc
        o.keyframe_insert('location', frame=frame)
    if rot is not None:
        o.rotation_euler = [math.radians(a) for a in rot]
        o.keyframe_insert('rotation_euler', frame=frame)
    if scale is not None:
        o.scale = (scale, scale, scale) if isinstance(scale, (int, float)) else scale
        o.keyframe_insert('scale', frame=frame)


def pop_in(o, frame, dur=8, overshoot=1.12, base=None):
    """0 → 과장 → 1 크기로 튀어나오기."""
    base = base or tuple(o.scale)
    o.scale = (0, 0, 0)
    o.keyframe_insert('scale', frame=frame - 1)
    o.scale = tuple(v * overshoot for v in base)
    o.keyframe_insert('scale', frame=frame + int(dur * 0.65))
    o.scale = base
    o.keyframe_insert('scale', frame=frame + dur)


def pop_out(o, frame, dur=6):
    base = tuple(o.scale)
    o.keyframe_insert('scale', frame=frame)
    o.scale = (0, 0, 0)
    o.keyframe_insert('scale', frame=frame + dur)
    o.scale = base


def show_between(objs, f_in, f_out):
    """샷 범위 밖에서는 렌더·뷰포트에서 숨긴다(세트 간 간섭 방지)."""
    for o in objs:
        for f, hidden in ((1, True), (f_in, False), (f_out, True)):
            if f < 1:
                continue
            o.hide_render = hidden
            o.hide_viewport = hidden
            o.keyframe_insert('hide_render', frame=f)
            o.keyframe_insert('hide_viewport', frame=f)


def shake(o, f0, f1, amp=4.0, step=2):
    """휴대폰 진동."""
    base = tuple(math.degrees(a) for a in o.rotation_euler)
    f, sign = f0, 1
    while f < f1:
        key(o, f, rot=(base[0], base[1], base[2] + amp * sign))
        sign *= -1
        f += step
    key(o, f1, rot=base)


# ---------------------------------------------------------------- camera

def look_rot(src, dst, roll=0.0):
    d = Vector(dst) - Vector(src)
    q = d.to_track_quat('-Z', 'Y')
    e = q.to_euler()
    e.rotate_axis('Z', math.radians(roll))
    return e


def camera(name, lens=35):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.clip_start = 0.01
    cd.clip_end = 400
    o = bpy.data.objects.new(name, cd)
    collection('CAMERAS').objects.link(o)
    return o


def cam_key(cam, frame, loc, target, lens=None, roll=0.0):
    cam.location = loc
    cam.rotation_euler = look_rot(loc, target, roll)
    cam.keyframe_insert('location', frame=frame)
    cam.keyframe_insert('rotation_euler', frame=frame)
    if lens:
        cam.data.lens = lens
        cam.data.keyframe_insert('lens', frame=frame)


def cut(cam, frame, label):
    s = bpy.context.scene
    m = s.timeline_markers.new(label, frame=frame)
    m.camera = cam
    return m


def caption(cam, name, lines, f_in, f_out, sub=None):
    """카메라에 붙는 자막(하단). CAPTIONS 컬렉션을 끄면 Higgsfield용 클린 프레임.

    렌즈 앞 5cm에 두고 화면 높이 비율로 크기를 정해 어떤 세트에서도 가려지지 않게 한다.
    """
    d = 0.05
    half_h = d * (cam.data.sensor_width * 9 / 16 / 2) / cam.data.lens
    size = half_h * 0.105
    y = -half_h * 0.66
    m_main = emit_mat('cap_main', C['white'], 1.0)
    m_sub = emit_mat('cap_sub', C['primary100'], 1.0)
    objs = []
    t = text(name, lines, (0, y, -d), size, m_main, 'CAPTIONS', weight='Bold', rot=(0, 0, 0))
    objs.append(t)
    if sub:
        objs.append(text(name + '_sub', sub, (0, y - size * 1.3, -d), size * 0.6, m_sub, 'CAPTIONS',
                         weight='SemiBold', rot=(0, 0, 0)))
    # 밝은 화면 위에서도 읽히도록 어두운 알약 배경
    bpy.context.view_layer.update()
    wmax = max(o.dimensions.x for o in objs)
    hh = size * (2.25 if sub else 1.5)
    cy = y - (size * 0.65 if sub else 0)
    bg = rbox(name + '_bg', (wmax + size * 1.6, hh, size * 0.05), (0, cy, -d - size * 0.1),
              emit_mat('cap_bg', C['primary'], 1.0), 'CAPTIONS', bevel=min(hh / 2 - 1e-5, size * 0.6), segments=8)
    objs.append(bg)
    for o in objs:
        o.parent = cam
        show_between([o], f_in, f_out)
        base = o.location.copy()
        key(o, f_in, loc=(base.x, base.y - size * 0.4, base.z))
        key(o, f_in + 8, loc=tuple(base))
    return objs


def area_light(name, loc, target, energy, size, color='#ffffff', coll='LIGHTS'):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy = energy
    ld.size = size
    ld.color = srgb(color)[:3]
    o = bpy.data.objects.new(name, ld)
    o.location = loc
    o.rotation_euler = look_rot(loc, target)
    collection(coll).objects.link(o)
    return o


def point_light(name, loc, energy, color='#ffffff', radius=0.1, coll='LIGHTS'):
    ld = bpy.data.lights.new(name, 'POINT')
    ld.energy = energy
    ld.shadow_soft_size = radius
    ld.color = srgb(color)[:3]
    o = bpy.data.objects.new(name, ld)
    o.location = loc
    collection(coll).objects.link(o)
    return o


# ---------------------------------------------------------------- props

def monitor(name, loc, screen_mat, coll, width=1.6, rot_z=0.0):
    """얇은 베젤 모니터 + 스탠드. 화면 비율 16:9."""
    h = width * 9 / 16
    root = empty(name, loc, coll)
    bezel = rbox(name + '_bezel', (width + 0.05, 0.035, h + 0.05), (0, 0, 0), mat('m_bezel', '#0e0e14', 0.3), coll,
                 bevel=0.015)
    scr = plane(name + '_screen', (width, h), (0, -0.0185, 0), screen_mat, coll)
    neck = rbox(name + '_neck', (0.08, 0.05, 0.42), (0, 0.06, -h / 2 - 0.18), mat('m_stand', '#2b2b35', 0.35, metal=0.6),
                coll, bevel=0.01)
    foot = rbox(name + '_foot', (0.5, 0.28, 0.025), (0, 0.06, -h / 2 - 0.39), mat('m_stand', '#2b2b35'), coll,
                bevel=0.01)
    for o in (bezel, scr, neck, foot):
        o.parent = root
    root.rotation_euler = (0, 0, math.radians(rot_z))
    return root, scr


def phone(name, loc, coll, rot=(70, 0, 0), screen_mat=None, scale=1.0):
    """세로형 스마트폰(가로 0.075 × 세로 0.155). 화면은 -Y 쪽."""
    root = empty(name, loc, coll)
    body = rbox(name + '_body', (0.078 * scale, 0.009 * scale, 0.158 * scale), (0, 0, 0),
                mat('m_phone', '#111118', 0.25, metal=0.4), coll, bevel=0.009 * scale, segments=6)
    scr = rbox(name + '_screen', (0.071 * scale, 0.002, 0.15 * scale), (0, -0.0046 * scale, 0),
               screen_mat or emit_mat('m_phone_scr', '#0f0f18'), coll, bevel=0.007 * scale, segments=6)
    for o in (body, scr):
        o.parent = root
    root.rotation_euler = [math.radians(a) for a in rot]
    return root, scr


def show_windows(objs, windows):
    """여러 구간에서만 보이게(예: S6와 S8에 같은 폰)."""
    for o in objs:
        o.hide_render = o.hide_viewport = True
        o.keyframe_insert('hide_render', frame=1)
        o.keyframe_insert('hide_viewport', frame=1)
        for a, b in windows:
            for f, hidden in ((a, False), (b, True)):
                o.hide_render = o.hide_viewport = hidden
                o.keyframe_insert('hide_render', frame=f)
                o.keyframe_insert('hide_viewport', frame=f)


def screen_seq(name, paths, strength=1.0):
    """여러 화면 캡처를 순서대로 전환하는 모니터 머티리얼. show_screen(m, i, frame)으로 전환."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Strength'].default_value = strength
    prev = None
    for i, p in enumerate(paths):
        tex = nt.nodes.new('ShaderNodeTexImage')
        tex.image = bpy.data.images.load(p, check_existing=True)
        if prev is None:
            prev = tex.outputs['Color']
            continue
        mix = nt.nodes.new('ShaderNodeMix')
        mix.data_type = 'RGBA'
        mix.name = f'mix{i}'
        a = next(s for s in mix.inputs if s.name == 'A' and s.type == 'RGBA')
        b = next(s for s in mix.inputs if s.name == 'B' and s.type == 'RGBA')
        nt.links.new(prev, a)
        nt.links.new(tex.outputs['Color'], b)
        mix.inputs['Factor'].default_value = 0.0
        prev = next(s for s in mix.outputs if s.type == 'RGBA')
    nt.links.new(prev, em.inputs['Color'])
    nt.links.new(em.outputs[0], out.inputs[0])
    m['screens'] = len(paths)
    return m


def show_screen(m, idx, frame):
    for i in range(1, m['screens']):
        sock = m.node_tree.nodes[f'mix{i}'].inputs['Factor']
        for f, v in ((frame - 1, sock.default_value), (frame, 1.0 if i <= idx else 0.0)):
            sock.default_value = v
            sock.keyframe_insert('default_value', frame=f)


def swap(o_out, o_in, frame, f_start, f_end):
    """같은 자리의 두 텍스트(상태 칩 등)를 frame에서 교체."""
    show_between([o_out], f_start, frame)
    show_between([o_in], frame, f_end)
