"""S9 0:26–0:30 (f625–720) 엔딩: 하나의 궤도 위의 현장.

카메라가 뒤로 빠지며 모니터·기사 폰을 감싸는 궤도 고리가 생기고, 위로 Orbit 로고와
랜딩 헤드라인('현장을 위한 스마트한 업무 관리 플랫폼')이 떠오른다.
"""
import math

F0, F1 = 625, 721
X = 80.0
CENTER = (X + 0.25, 0.0, 1.45)
COLL = 'STAGE'


def build(L):
    import bpy
    L.show_screen(bpy.data.materials['m_monitor'], 3, F0)
    objs = []
    m_ring = L.emit_mat('e_orbit_ring', L.C['primary100'], 1.4)
    m_dot = L.emit_mat('e_signal', L.C['primary100'], 4.0)
    for k, (rx, ry, radius) in enumerate(((80, 0, 1.75), (74, 22, 2.15), (84, -18, 2.55))):
        tilt = L.empty(f's9_tilt_{k}', CENTER, COLL)
        tilt.rotation_euler = (math.radians(rx), math.radians(ry), 0)
        spin = L.empty(f's9_spin_{k}', (0, 0, 0), COLL)
        spin.parent = tilt
        L.key(spin, F0, rot=(0, 0, k * 70))
        L.key(spin, F1, rot=(0, 0, k * 70 + (80 if k % 2 == 0 else -80)))
        ring = L.torus(f's9_ring_{k}', radius, 0.007, (0, 0, 0), m_ring, COLL)
        ring.parent = tilt
        L.pop_in(ring, F0 + 10 + k * 5, dur=12, overshoot=1.04)
        objs += [tilt, spin, ring]
        for j in range(3):
            a = 2 * math.pi * j / 3 + k
            d = L.sphere(f's9_dot_{k}_{j}', 0.03, (math.cos(a) * radius, math.sin(a) * radius, 0), m_dot, COLL, seg=16)
            d.parent = spin
            L.pop_in(d, F0 + 16 + k * 5, dur=8)
            objs.append(d)

    white = L.emit_mat('e_mark', '#ffffff', 1.4)
    mark = L.rbox('s9_mark', (0.3, 0.06, 0.3), (X - 0.62, 0, 3.02), white, COLL, bevel=0.08, segments=10)
    word = L.text('s9_word', 'Orbit', (X + 0.2, -0.04, 3.02), 0.4, L.emit_mat('e_word', '#ffffff', 1.2), COLL,
                  weight='ExtraBold')
    head = L.text('s9_head', '현장을 위한 스마트한 업무 관리 플랫폼', (X, -0.04, 2.6), 0.15, L.emit_mat('t_white', '#ffffff'),
                  COLL)
    sub = L.text('s9_sub', '담당 기사 배치부터 작업 완료까지, 전화 없이 한눈에', (X, -0.04, 2.4), 0.08,
                 L.emit_mat('t_lav', L.C['primary100']), COLL, weight='SemiBold')
    L.pop_in(mark, F0 + 30, dur=10, overshoot=1.2)
    L.pop_in(word, F0 + 34, dur=10, overshoot=1.06)
    for i, o in enumerate((head, sub)):
        base = tuple(o.location)
        L.key(o, F0 + 42 + i * 6, loc=(base[0], base[1], base[2] - 0.08))
        L.key(o, F0 + 52 + i * 6, loc=base)
        L.show_between([o], F0 + 42 + i * 6, F1)
    objs += [mark, word]
    L.show_between(objs, F0, F1)

    cam = L.camera('CAM_S9', 35)
    L.cam_key(cam, F0, (X + 0.9, -2.6, 1.6), (X + 0.3, 0, 1.6), lens=35)
    L.cam_key(cam, F0 + 50, (X + 0.15, -6.0, 2.05), (X + 0.05, 0, 2.05), lens=35)
    L.cam_key(cam, F1 - 1, (X + 0.05, -6.5, 2.1), (X, 0, 2.08), lens=35)
    L.cut(cam, F0, 'S9')
    return cam
