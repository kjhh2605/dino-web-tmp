"""S4 0:09–0:12 (f217–288) 전환: 흩어진 것들이 하나의 궤도로.

앞 샷의 포스트잇·말풍선·휴대폰·위치 핀이 사방에서 날아와 세 개의 궤도에 올라타고,
색이 경고색(노랑·빨강)에서 브랜드색(보라·흰색)으로 바뀐다. 중심에 Orbit 마크가 켜진다.
"""
import math
import random

F0, F1 = 217, 289
X = 60.0
CENTER = (X, 0.0, 1.5)
COLL = 'S4_ORBIT'


def build(L):
    random.seed(5)
    objs = []
    # 혼란(노랑·빨강·카톡) → 질서(보라·흰색)로 바뀌는 공유 머티리얼
    m_a = L.mat('m_deb_a', L.C['sticky'], 0.5)
    m_b = L.mat('m_deb_b', L.C['warning'], 0.4)
    m_c = L.mat('m_deb_c', L.C['kakao'], 0.5)
    for m, c0, c1 in ((m_a, L.C['sticky'], L.C['primary100']), (m_b, L.C['warning'], L.C['secondary']),
                      (m_c, L.C['kakao'], '#ffffff')):
        L.key_color(m, F0 + 16, c0)
        L.key_color(m, F0 + 38, c1)

    rings = [(70, 0, 1.25), (62, 38, 1.6), (78, -34, 1.95)]
    m_ring = L.emit_mat('e_orbit_ring', L.C['primary100'], 1.4)
    for k, (rx, ry, radius) in enumerate(rings):
        tilt = L.empty(f's4_tilt_{k}', CENTER, COLL)
        tilt.rotation_euler = (math.radians(rx), math.radians(ry), 0)
        spin = L.empty(f's4_spin_{k}', (0, 0, 0), COLL)
        spin.parent = tilt
        L.key(spin, F0, rot=(0, 0, k * 40))
        L.key(spin, F1, rot=(0, 0, k * 40 + (110 if k % 2 == 0 else -110)))
        ring = L.torus(f's4_ring_{k}', radius, 0.006, (0, 0, 0), m_ring, COLL)
        ring.parent = tilt
        L.pop_in(ring, F0 + 20 + k * 3, dur=10, overshoot=1.05)
        objs += [tilt, spin, ring]

        # 궤도에 올라탈 조각들
        n = 11
        for j in range(n):
            a = 2 * math.pi * j / n
            kind = (j + k) % 4
            if kind == 0:
                o = L.rbox(f's4_deb_{k}_{j}', (0.16, 0.16, 0.006), (0, 0, 0), m_a, COLL, bevel=0.004)
            elif kind == 1:
                o = L.rbox(f's4_deb_{k}_{j}', (0.22, 0.1, 0.03), (0, 0, 0), m_c, COLL, bevel=0.04, segments=6)
            elif kind == 2:
                o = L.rbox(f's4_deb_{k}_{j}', (0.075, 0.155, 0.01), (0, 0, 0), m_c, COLL,
                           bevel=0.009)
            else:
                o = L.sphere(f's4_deb_{k}_{j}', 0.05, (0, 0, 0), m_b, COLL, seg=16)
            o.parent = spin
            far = random.uniform(1.9, 3.0)
            fz = random.uniform(-1.1, 1.1)
            fa = a + random.uniform(-0.6, 0.6)
            L.key(o, F0, loc=(math.cos(fa) * far, math.sin(fa) * far, fz),
                  rot=(random.uniform(-90, 90), random.uniform(-90, 90), random.uniform(0, 360)))
            L.key(o, F0 + 30 + random.randint(0, 6), loc=(math.cos(a) * radius, math.sin(a) * radius, 0),
                  rot=(0, 0, math.degrees(a)))
            L.key(o, F1, loc=(math.cos(a) * radius, math.sin(a) * radius, 0), rot=(0, 0, math.degrees(a)))
            objs.append(o)

    # 중심 마크(둥근 사각형) + 워드마크
    mark = L.rbox('s4_mark', (0.62, 0.12, 0.62), CENTER, L.emit_mat('e_mark', '#ffffff', 1.4), COLL, bevel=0.17,
                  segments=10)
    L.pop_in(mark, F0 + 26, dur=10, overshoot=1.2)
    glow = L.point_light('s4_glow', (X, -0.6, 1.5), 0, L.C['secondary'], radius=0.6, coll=COLL)
    glow.data.energy = 0
    glow.data.keyframe_insert('energy', frame=F0 + 24)
    glow.data.energy = 900
    glow.data.keyframe_insert('energy', frame=F0 + 34)
    # 마크가 왼쪽으로 비켜서며 워드마크와 로고 락업을 만든다
    L.key(mark, F0 + 40, loc=CENTER, scale=1.0)
    L.key(mark, F0 + 50, loc=(X - 0.78, 0, 1.5), scale=0.62)
    word = L.text('s4_word', 'Orbit', (X + 0.3, -0.08, 1.5), 0.62, L.emit_mat('e_word', '#ffffff', 1.2), COLL,
                  weight='ExtraBold')
    L.pop_in(word, F0 + 46, dur=10, overshoot=1.06)
    objs += [mark, word]

    L.area_light('s4_back', (X, 4, 3), CENTER, 600, 6, L.C['secondary'], coll=COLL)
    L.area_light('s4_front', (X - 1.5, -4.5, 3.0), CENTER, 400, 4, '#ffffff', coll=COLL)
    L.show_between(objs, F0, F1)

    cam = L.camera('CAM_S4', 24)
    L.cam_key(cam, F0, (X + 0.4, -3.0, 1.75), CENTER, lens=24, roll=-6)
    L.cam_key(cam, F1 - 1, (X, -6.6, 1.55), (X, 0, 1.25), lens=32, roll=0)
    L.cut(cam, F0, 'S4')
    L.caption(cam, 's4_cap', '흩어진 현장을, 하나의 궤도로', F0 + 44, F1)
    return cam
