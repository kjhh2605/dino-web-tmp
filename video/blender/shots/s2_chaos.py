"""S2 0:03–0:06 (f73–150) 문제 심화: 흩어진 정보와 일정 충돌.

코르크보드에 엑셀 출력물·포스트잇이 뒤엉켜 있고, 메신저 말풍선이 계속 튀어나온다.
같은 기사·같은 시간의 작업 카드 두 장이 양쪽에서 밀려와 겹치며 '일정 충돌' 경고가 뜬다.
카메라는 보드를 따라 좌→우로 트럭.
"""
import math
import os
import random

F0, F1 = 73, 151
X = 20.0
COLL = 'S2_CHAOS'


def build(L):
    random.seed(3)
    objs = []
    m_txt = L.emit_mat('t_dark', L.C['gray900'])
    m_red = L.emit_mat('e_red', L.C['warning'], 1.6)
    m_white = L.emit_mat('t_white', L.C['white'])

    objs.append(L.plane('s2_wall', (8, 4), (X, 0.6, 1.6), L.mat('m_wall2', '#34323d', 0.9), COLL))
    board = L.rbox('s2_board', (2.8, 0.04, 1.5), (X, 0.5, 1.5), L.mat('m_cork', '#a77b52', 0.85), COLL, bevel=0.02)
    objs.append(board)
    sheet = L.plane('s2_excel', (1.25, 0.70), (X - 0.55, 0.47, 1.62), L.image_mat('img_excel_p', os.path.join(
        L.ASSETS, 'gen', 'excel.png'), 0.85), COLL)
    sheet.rotation_euler = (math.radians(90), math.radians(-2.5), 0)
    objs.append(sheet)

    stickies = ['김민수\n9시 배관', '이철호??\n2시', '보일러 교체\n→ 누구?', '13시 겹침!!', '고객 재방문\n요청', '사진 아직',
                '박서연\n연락X', '자재 확인']
    colors = [L.C['sticky'], L.C['sticky2'], L.C['sticky3']]
    for i, body in enumerate(stickies):
        x = X + 0.25 + (i % 4) * 0.27 + random.uniform(-0.04, 0.04)
        z = 1.95 - (i // 4) * 0.42 + random.uniform(-0.05, 0.05)
        root = L.empty(f's2_sticky_{i}', (x, 0.465, z), COLL)
        n = L.rbox(f's2_sticky_{i}_bg', (0.22, 0.004, 0.22), (0, 0, 0), L.mat(f'm_sticky{i % 3}', colors[i % 3], 0.8),
                   COLL, bevel=0.003)
        t = L.text(f's2_sticky_{i}_t', body, (0, -0.004, 0), 0.032, m_txt, COLL)
        for o in (n, t):
            o.parent = root
        root.rotation_euler = (0, math.radians(random.uniform(-9, 9)), 0)
        objs += [root, n, t]
    # 빨간 실(연결이 꼬인 정보)
    for i, (a, b) in enumerate((((-0.9, 1.9), (0.6, 1.5)), ((-0.2, 1.2), (0.9, 1.9)), ((-1.1, 1.3), (0.35, 1.95)))):
        ax, az = a
        bx, bz = b
        ln = math.hypot(bx - ax, bz - az)
        r = L.rbox(f's2_thread_{i}', (ln, 0.004, 0.006), (X + (ax + bx) / 2, 0.445, (az + bz) / 2),
                   L.mat('m_thread', '#c62828', 0.6), COLL, bevel=0)
        r.rotation_euler = (0, -math.atan2(bz - az, bx - ax), 0)
        objs.append(r)

    # 메신저 말풍선
    bubbles = [('기사님 몇 시 도착?', -0.95, 1.05), ('작업 끝나셨나요?', 0.15, 2.05), ('사진 보내주세요', 0.95, 1.12),
               ('일정 바뀌었어요!', -0.35, 2.12), ('주소 다시 알려주세요', -1.2, 1.7)]
    m_bub = L.mat('m_kakao', L.C['kakao'], 0.5)
    for i, (body, bx, bz) in enumerate(bubbles):
        root = L.empty(f's2_bub_{i}', (X + bx, 0.05 - i * 0.06, bz), COLL)
        w = 0.11 + len(body) * 0.034
        b = L.rbox(f's2_bub_{i}_bg', (w, 0.03, 0.15), (0, 0, 0), m_bub, COLL, bevel=0.06, segments=8)
        tail = L.rbox(f's2_bub_{i}_tail', (0.06, 0.03, 0.06), (-w / 2 + 0.07, 0, -0.075), m_bub, COLL, bevel=0.01,
                      rot=(0, math.radians(45), 0))
        t = L.text(f's2_bub_{i}_t', body, (0, -0.017, 0), 0.05, m_txt, COLL)
        for o in (b, tail, t):
            o.parent = root
        L.pop_in(root, F0 + 4 + i * 9, dur=8, overshoot=1.18)
        L.key(root, F0 + 12 + i * 9, loc=tuple(root.location))
        L.key(root, F1, loc=(root.location.x, root.location.y - 0.15, root.location.z + 0.08))
        objs += [root, b, tail, t]

    # 같은 시간대 작업 두 장이 겹치며 충돌
    m_card = L.mat('m_card_w', '#f4f4f7', 0.45)
    cards = []
    for i, (title, side) in enumerate((('보일러 수리 14:00', -1), ('에어컨 점검 14:00', 1))):
        root = L.empty(f's2_conf_{i}', (X + side * 1.7, -0.55, 1.35 + i * 0.05), COLL)
        c = L.rbox(f's2_conf_{i}_bg', (0.62, 0.02, 0.2), (0, 0, 0), m_card, COLL, bevel=0.03)
        bar = L.rbox(f's2_conf_{i}_bar', (0.02, 0.022, 0.2), (-0.3, 0, 0), L.mat('m_bar_o', L.C['progress'], 0.4), COLL,
                     bevel=0.005)
        t1 = L.text(f's2_conf_{i}_t', title, (-0.26, -0.012, 0.03), 0.052, m_txt, COLL, align='LEFT')
        t2 = L.text(f's2_conf_{i}_s', '담당: 이민준 기사', (-0.26, -0.012, -0.05), 0.036,
                    L.emit_mat('t_gray', L.C['gray700']), COLL, align='LEFT', weight='SemiBold')
        for o in (c, bar, t1, t2):
            o.parent = root
        L.key(root, F0 + 20, loc=tuple(root.location), rot=(0, 0, 0))
        L.key(root, F0 + 44, loc=(X + side * 0.16, -0.55 - i * 0.03, 1.38 + i * 0.07), rot=(0, side * -6, 0))
        cards.append(root)
        objs += [root, c, bar, t1, t2]
    warn = L.empty('s2_warn', (X + 0.02, -0.66, 1.62), COLL)
    wb = L.rbox('s2_warn_bg', (0.42, 0.02, 0.11), (0, 0, 0), L.mat('m_warn', L.C['warning'], 0.4, emit=0.6), COLL,
                bevel=0.05, segments=8)
    wt = L.text('s2_warn_t', '⚠ 일정 충돌', (0, -0.012, 0), 0.05, m_white, COLL)
    wt.data.body = '일정 충돌'
    for o in (wb, wt):
        o.parent = warn
    L.pop_in(warn, F0 + 46, dur=8, overshoot=1.3)
    L.shake(warn, F0 + 54, F0 + 66, amp=5, step=2)
    objs += [warn, wb, wt]

    L.area_light('s2_key', (X - 1.5, -2.5, 3.0), (X, 0.4, 1.5), 170, 2.0, '#fff1de', coll=COLL)
    L.point_light('s2_red', (X + 0.1, -1.0, 1.7), 30, '#ff4040', radius=0.2, coll=COLL)
    L.show_between(objs, F0, F1)

    cam = L.camera('CAM_S2', 32)
    L.cam_key(cam, F0, (X - 0.9, -2.9, 1.55), (X - 0.5, 0.4, 1.5))
    L.cam_key(cam, F1 - 1, (X + 0.5, -2.75, 1.6), (X + 0.15, 0.4, 1.48))
    L.cut(cam, F0, 'S2')
    L.caption(cam, 's2_cap', '전화 · 메신저 · 엑셀에 흩어진 일정', F0 + 6, F1, sub='겹치는 배정, 놓치는 연락')
    return cam
