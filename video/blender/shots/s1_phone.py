"""S1 0:00–0:03 (f1–72) 문제 제기: 쉬지 않고 울리는 전화.

책상 위 휴대폰 3대가 번갈아 진동하고, 부재중·메시지 알림 카드가 쌓여 올라간다.
뒤 모니터에는 수기로 관리하는 엑셀 배정표. 카메라는 메인 폰으로 천천히 다가간다.
"""
import math
import os

F0, F1 = 1, 73
X = 0.0
COLL = 'S1_PHONE'


def build(L):
    m_desk = L.mat('m_desk', L.C['desk'], 0.55)
    m_card = L.mat('m_notif', '#d9d9e2', 0.5)
    m_txt = L.emit_mat('t_dark', L.C['gray900'])
    m_txt_sub = L.emit_mat('t_gray', L.C['gray700'])
    m_red = L.emit_mat('e_red', L.C['warning'], 1.6)
    m_white = L.emit_mat('t_white', L.C['white'])
    m_call = L.emit_mat('scr_call', '#20203a', 1.0)
    objs = []

    desk = L.rbox('s1_desk', (3.2, 1.8, 0.05), (X, 0.1, -0.025), m_desk, COLL, bevel=0.01)
    wall = L.plane('s1_wall', (6, 3), (X, 1.2, 1.2), L.mat('m_wall', '#2c2a33', 0.9), COLL)
    objs += [desk, wall]

    excel = L.image_mat('img_excel', os.path.join(L.ASSETS, 'gen', 'excel.png'), 0.9)
    mon, _ = L.monitor('s1_monitor', (X + 0.35, 0.95, 0.5), excel, COLL, width=1.1, rot_z=-6)
    objs += [mon] + list(mon.children)

    # 메인 폰: 수신 화면
    ph, scr = L.phone('s1_phone_main', (X, -0.12, 0.006), COLL, rot=(-90, 0, 12), screen_mat=m_call)
    objs += [ph] + list(ph.children)
    lines = [('김민수 기사', 0.03, 0.011, m_white), ('휴대전화 · 수신 중', 0.015, 0.0055, m_txt_sub),
             ('부재중 전화 12', -0.045, 0.0075, m_red)]
    for i, (body, z, size, m) in enumerate(lines):
        t = L.text(f's1_call_{i}', body, (0, -0.0062, z), size, m, COLL)
        t.parent = ph
        objs.append(t)
    for i, (dx, col) in enumerate(((-0.018, '#d71a29'), (0.018, '#27ae60'))):
        b = L.cyl(f's1_btn_{i}', 0.009, 0.002, (dx, -0.0062, -0.06), L.emit_mat(f'e_btn{i}', col, 1.5), COLL,
                  rot=(math.radians(90), 0, 0))
        b.parent = ph
        objs.append(b)
    L.shake(ph, 6, 30, amp=3)
    L.shake(ph, 40, 66, amp=3)

    # 보조 폰 2대
    for i, (dx, dy, rz, f) in enumerate(((-0.42, 0.08, -25, 14), (0.38, 0.12, 30, 26))):
        p, s = L.phone(f's1_phone_{i}', (X + dx, dy, 0.006), COLL, rot=(-90, 0, rz),
                       screen_mat=L.emit_mat(f'scr_p{i}', '#30304a', 1.0))
        objs += [p] + list(p.children)
        t = L.text(f's1_p{i}_txt', '카톡 37', (0, -0.0062, 0.02), 0.009, L.emit_mat('e_kakao', L.C['kakao'], 1.3),
                   COLL)
        t.parent = p
        objs.append(t)
        L.shake(p, f, f + 22, amp=4)

    # 쌓여 올라가는 알림 카드
    notes = [('부재중 전화', '이민준 기사 (3)'), ('메시지', '기사님 몇 시 도착하세요?'),
             ('부재중 전화', '고객 윤서아 (2)'), ('메시지', '오후 일정 바뀌었어요!!'), ('부재중 전화', '김태훈 기사 (5)')]
    for i, (title, body) in enumerate(notes):
        z = 0.07 + i * 0.05
        root = L.empty(f's1_note_{i}', (X + 0.2, -0.02, z), COLL)
        card = L.rbox(f's1_note_{i}_bg', (0.22, 0.006, 0.042), (0, 0, 0), m_card, COLL, bevel=0.012)
        dot = L.cyl(f's1_note_{i}_dot', 0.009, 0.004, (-0.088, -0.004, 0), m_red if '부재' in title else
                    L.emit_mat('e_kakao', L.C['kakao']), COLL, rot=(math.radians(90), 0, 0))
        t1 = L.text(f's1_note_{i}_t', title, (-0.072, -0.0035, 0.008), 0.0095, m_txt_sub, COLL, align='LEFT',
                    weight='SemiBold')
        t2 = L.text(f's1_note_{i}_b', body, (-0.072, -0.0035, -0.008), 0.013, m_txt, COLL, align='LEFT')
        for o in (card, dot, t1, t2):
            o.parent = root
        root.rotation_euler = (math.radians(-6), 0, math.radians(-14))
        L.pop_in(root, 8 + i * 11, dur=7)
        objs += [root, card, dot, t1, t2]

    L.point_light('s1_lamp', (X - 0.9, -0.3, 1.0), 120, '#ffb36b', radius=0.3, coll=COLL)
    L.point_light('s1_fill', (X + 0.8, -1.2, 0.7), 25, '#8fa2ff', radius=0.5, coll=COLL)
    L.point_light('s1_phoneglow', (X, -0.2, 0.08), 3, '#9aa0ff', radius=0.05, coll=COLL)
    L.show_between(objs, F0, F1)

    cam = L.camera('CAM_S1', 40)
    L.cam_key(cam, F0, (X + 0.3, -1.0, 0.62), (X + 0.1, -0.02, -0.02))
    L.cam_key(cam, F1 - 1, (X + 0.22, -0.74, 0.5), (X + 0.1, -0.04, 0.0))
    L.cut(cam, F0, 'S1')
    L.caption(cam, 's1_cap', '오늘도 전화로 시작되는 현장 배정', 10, F1, sub='“기사님, 지금 어디세요?”')
    return cam
