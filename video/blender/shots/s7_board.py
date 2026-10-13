"""S7 0:19.5–0:23 (f469–552) 기능 3: 진행 상황을 실시간으로 한눈에.

모니터가 실제 진행 보드 캡처로 바뀐다. 화면 앞에 작업 행 4개가 떠 있고 상태 칩이 차례로
작업전 → 작업중 → 완료로 바뀌며, 오른쪽 '완료' 집계 카드 숫자가 4 → 5 → 6으로 오른다.
"""
F0, F1 = 469, 553
X = 80.0
COLL = 'STAGE'

STATUS = {
    '배정됨': ('#cecece', '#1f1f1f'),
    '작업전': ('#4f3bfe', '#ffffff'),
    '작업중': ('#eea216', '#ffffff'),
    '완료': ('#277d02', '#ffffff'),
}


def build(L):
    import bpy
    scr = bpy.data.materials['m_monitor']
    L.show_screen(scr, 1, F0)

    m_txt = L.emit_mat('t_dark', L.C['gray900'])
    m_gray = L.emit_mat('t_gray', L.C['gray700'])
    rows = [('가스보일러 점검', '김태훈 기사 · 09:00', ['작업전', '작업중'], [F0 + 14]),
            ('식기세척기 설치', '이철호 기사 · 09:00', ['작업중', '완료'], [F0 + 26]),
            ('세탁기 설치', '이철호 기사 · 13:00', ['배정됨', '작업전'], [F0 + 38]),
            ('보일러 배관 교체', '이민준 기사 · 10:00', ['작업중', '완료'], [F0 + 50])]
    objs = []
    for i, (title, sub, states, frames) in enumerate(rows):
        z = 1.98 - i * 0.15
        root = L.empty(f's7_row_{i}', (X - 0.38, -0.42, z), COLL)
        card = L.rbox(f's7_row_{i}_bg', (0.8, 0.016, 0.12), (0, 0, 0), L.mat('m_row', '#ffffff', 0.45), COLL,
                      bevel=0.03)
        t1 = L.text(f's7_row_{i}_t', title, (-0.36, -0.01, 0.014), 0.036, m_txt, COLL, align='LEFT')
        t2 = L.text(f's7_row_{i}_s', sub, (-0.36, -0.01, -0.03), 0.022, m_gray, COLL, align='LEFT', weight='SemiBold')
        for o in (card, t1, t2):
            o.parent = root
        L.pop_in(root, F0 + 2 + i * 3, dur=8, overshoot=1.05)
        objs += [root, card, t1, t2]
        bounds = [F0] + frames + [F1]
        for j, st in enumerate(states):
            bg_c, fg_c = STATUS[st]
            pill = L.rbox(f's7_row_{i}_p{j}', (0.13, 0.006, 0.048), (0.28, -0.011, 0), L.emit_mat(f'e_st_{st}', bg_c),
                          COLL, bevel=0.0235, segments=8)
            pt = L.text(f's7_row_{i}_pt{j}', st, (0.28, -0.0145, 0), 0.024, L.emit_mat(f't_st_{st}', fg_c), COLL)
            for o in (pill, pt):
                o.parent = root
            L.show_between([pill, pt], bounds[j], bounds[j + 1])
            if j:
                L.pop_in(pill, bounds[j], dur=6, overshoot=1.25)
                L.pop_in(pt, bounds[j], dur=6, overshoot=1.25)

    # 완료 집계 카드
    kpi = L.empty('s7_kpi', (X + 0.72, -0.45, 1.86), COLL)
    kbg = L.rbox('s7_kpi_bg', (0.42, 0.02, 0.3), (0, 0, 0), L.mat('m_kpi', L.C['primary'], 0.4), COLL, bevel=0.04)
    kl = L.text('s7_kpi_l', '오늘 완료', (-0.17, -0.012, 0.09), 0.04, L.emit_mat('t_white', '#ffffff'), COLL,
                align='LEFT')
    live = L.sphere('s7_live', 0.011, (0.12, -0.014, 0.095), L.emit_mat('e_live', '#3dbc07', 2.5), COLL, seg=12)
    for o in (kbg, kl, live):
        o.parent = kpi
    nums = [('4', F0, F0 + 26), ('5', F0 + 26, F0 + 50), ('6', F0 + 50, F1)]
    for n, a, b in nums:
        t = L.text(f's7_kpi_n{n}', n + '건', (0.17, -0.012, -0.05), 0.11, L.emit_mat('t_white', '#ffffff'), COLL,
                   align='RIGHT')
        t.parent = kpi
        L.show_between([t], a, b)
        if a != F0:
            L.pop_in(t, a, dur=6, overshoot=1.2)
    for f in range(F0, F1, 12):
        L.key(live, f, scale=1.0)
        L.key(live, f + 6, scale=1.6)
    L.pop_in(kpi, F0 + 8, dur=8)
    objs += [kpi, kbg, kl, live]
    L.show_between(objs, F0, F1)

    cam = L.camera('CAM_S7', 38)
    L.cam_key(cam, F0, (X - 1.25, -2.35, 1.55), (X - 0.05, -0.3, 1.68), lens=38)
    L.cam_key(cam, F1 - 1, (X - 0.75, -2.25, 1.66), (X - 0.02, -0.3, 1.7), lens=38)
    L.cut(cam, F0, 'S7')
    L.caption(cam, 's7_cap', '진행 상황을 실시간으로 한눈에', F0 + 6, F1, sub='배정됨 · 작업전 · 작업중 · 완료')
    return cam
