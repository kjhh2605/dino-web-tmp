"""S3 0:06–0:09 (f151–216) 문제 정점: 보이지 않는 현장.

어두운 도시 미니어처 위로 기사 위치 핀이 흩어져 있고 핀마다 '?'가 떠 있다.
빨간 파동만 퍼질 뿐 상태는 알 수 없다. 카메라는 높은 앵글에서 천천히 선회.
"""
import math
import random

F0, F1 = 151, 217
X = 40.0
COLL = 'S3_CITY'


def build(L):
    random.seed(11)
    objs = []
    objs.append(L.plane('s3_ground', (14, 14), (X, 0, 0), L.mat('m_ground', '#16151f', 0.9), COLL, rot=(0, 0, 0)))
    m_bld = [L.mat('m_bld1', '#2a2a3c', 0.7), L.mat('m_bld2', '#33334a', 0.7), L.mat('m_bld3', '#24243a', 0.7)]
    m_win = L.emit_mat('e_win', '#ffd28a', 1.2)
    for gx in range(-5, 6):
        for gy in range(-5, 6):
            if gx in (-2, 1, 4) or gy in (-3, 0, 3):  # 도로
                continue
            h = random.choice((0.2, 0.3, 0.45, 0.6, 0.9, 1.3)) * (1.4 if abs(gx) + abs(gy) < 4 else 1)
            b = L.rbox(f's3_b_{gx}_{gy}', (0.42, 0.42, h), (X + gx * 0.55, gy * 0.55, h / 2), m_bld[(gx + gy) % 3],
                       COLL, bevel=0.01, segments=1)
            objs.append(b)
            if random.random() < 0.35:
                w = L.plane(f's3_w_{gx}_{gy}', (0.08, 0.05), (X + gx * 0.55 + random.uniform(-0.1, 0.1),
                                                              gy * 0.55 - 0.212, h * random.uniform(0.3, 0.8)),
                            m_win, COLL)
                objs.append(w)
    m_road = L.emit_mat('e_road', '#3b3b55', 0.6)
    for gx in (-2, 1, 4):
        objs.append(L.plane(f's3_rx_{gx}', (0.06, 6.2), (X + gx * 0.55, 0, 0.002), m_road, COLL, rot=(0, 0, 0)))
    for gy in (-3, 0, 3):
        objs.append(L.plane(f's3_ry_{gy}', (6.2, 0.06), (X, gy * 0.55, 0.002), m_road, COLL, rot=(0, 0, 0)))

    m_pin = L.mat('m_pin', '#8a8aa0', 0.35)
    m_q = L.emit_mat('e_q', L.C['white'], 1.2)
    m_ring = L.emit_mat('e_ring', L.C['warning'], 2.0)
    pins = [(-1.1, -1.65), (0.55, -0.55), (2.2, 1.1), (-2.2, 1.65), (1.65, -2.2), (-0.55, 0.55)]
    names = ['김민수', '이민준', '홍길동', '김태훈', '박서연', '이철호']
    for i, ((px, py), nm) in enumerate(zip(pins, names)):
        root = L.empty(f's3_pin_{i}', (X + px, py, 0.0), COLL)
        head = L.sphere(f's3_pin_{i}_head', 0.17, (0, 0, 0.95), m_pin, COLL, seg=24)
        bpy_cone = L.cyl(f's3_pin_{i}_stem', 0.035, 0.85, (0, 0, 0.45), m_pin, COLL, verts=12)
        q = L.text(f's3_pin_{i}_q', '?', (0, -0.175, 0.95), 0.26, m_q, COLL)
        label = L.text(f's3_pin_{i}_n', nm + ' 기사', (0, -0.0, 1.3), 0.14, m_q, COLL, weight='SemiBold')
        ring = L.torus(f's3_pin_{i}_ring', 0.15, 0.008, (0, 0, 0.01), m_ring, COLL)
        for o in (head, bpy_cone, q, label, ring):
            o.parent = root
        L.pop_in(root, F0 + 3 + i * 4, dur=8)
        # 위아래로 떠 있음
        for k, f in enumerate(range(F0 + 12 + i * 4, F1, 18)):
            L.key(head, f, loc=(0, 0, 0.95 + (0.05 if k % 2 else 0)))
        # 퍼지는 빨간 파동
        for f in range(F0 + 10 + i * 5, F1, 26):
            L.key(ring, f, scale=0.2)
            L.key(ring, f + 24, scale=3.0)
        objs += [root, head, bpy_cone, q, label, ring]

    L.area_light('s3_moon', (X - 3, -4, 7), (X, 0, 0), 500, 6.0, '#8fa2ff', coll=COLL)
    L.point_light('s3_red', (X, 0, 2.5), 200, '#ff4a4a', radius=1.0, coll=COLL)
    L.show_between(objs, F0, F1)

    cam = L.camera('CAM_S3', 30)
    L.cam_key(cam, F0, (X + 3.2, -4.6, 6.4), (X, -0.2, 0.3))
    L.cam_key(cam, F1 - 1, (X + 0.9, -5.2, 5.6), (X, -0.1, 0.5))
    L.cut(cam, F0, 'S3')
    L.caption(cam, 's3_cap', '기사님은 지금 어디서, 무엇을?', F0 + 6, F1, sub='현장 상황은 전화해야만 알 수 있다')
    return cam
