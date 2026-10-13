"""S5 0:12–0:16 (f289–384) 기능 1: 타임테이블에서 드래그 한 번으로 배정.

제품 무대(어두운 남색 스튜디오, 보라 림 라이트)와 모니터를 만든다. 모니터에는 실제 Orbit
타임테이블(편집 모드) 캡처. 대기함의 '가스보일러 점검' 카드가 3D로 떠올라 김태훈 기사
09:00 칸에 내려앉고, 칩이 '점검' → '배정됨'으로 바뀐다. 무대는 S9까지 이어 쓴다.
"""
import math
import os

F0, F1 = 289, 385
X = 80.0
MZ = 1.63          # 모니터 화면 중심 높이
SW = 1.8           # 화면 너비(16:9)
SH = SW * 9 / 16
STAGE_END = 721
COLL = 'STAGE'


def px(x, y, depth=-0.026):
    """1920×1080 캡처 픽셀 → 월드 좌표(모니터 화면 앞)."""
    return (X + (x / 1920 - 0.5) * SW, depth, MZ + (0.5 - y / 1080) * SH)


def build_stage(L):
    objs = []
    floor = L.plane('st_floor', (30, 30), (X, 0, 0), L.mat('m_floor', '#121119', 0.22, metal=0.2), COLL,
                    rot=(0, 0, 0))
    wall = L.plane('st_wall', (30, 10), (X, 3.5, 4), L.mat('m_stwall', '#191826', 0.8), COLL)
    desk = L.rbox('st_desk', (2.7, 1.0, 0.06), (X, 0.15, 0.72), L.mat('m_stdesk', '#24233a', 0.35), COLL, bevel=0.02)
    legs = [L.rbox(f'st_leg_{i}', (0.05, 0.05, 0.7), (X + dx, 0.15 + dy, 0.35), L.mat('m_stand', '#2b2b35'), COLL,
                   bevel=0.01) for i, (dx, dy) in enumerate(((-1.25, -0.4), (1.25, -0.4), (-1.25, 0.4), (1.25, 0.4)))]
    ui = os.path.join(L.ASSETS, 'ui')
    scr = L.screen_seq('m_monitor', [os.path.join(ui, n) for n in (
        'timetable-edit.png', 'board.png', 'notifications.png', 'timetable.png')])
    mon, _ = L.monitor('st_monitor', (X, 0.0, MZ), scr, COLL, width=SW)
    objs += [floor, wall, desk, mon] + legs + list(mon.children)
    L.show_screen(scr, 0, F0)

    L.area_light('st_key', (X - 1.8, -3.2, 3.4), (X, 0, 1.4), 520, 2.5, '#f3f1ff', coll=COLL)
    L.area_light('st_rim_l', (X - 3.0, 2.2, 2.2), (X - 0.6, 0, 1.4), 700, 1.5, L.C['secondary'], coll=COLL)
    L.area_light('st_rim_r', (X + 3.0, 2.2, 2.2), (X + 0.6, 0, 1.4), 700, 1.5, L.C['primary100'], coll=COLL)
    L.area_light('st_wallglow', (X, 1.6, 0.4), (X, 3.5, 2.6), 900, 3.0, L.C['secondary'], coll=COLL)
    L.show_between(objs, F0, STAGE_END)
    return scr


def build(L):
    build_stage(L)
    objs = []
    m_txt = L.emit_mat('t_dark', L.C['gray900'])
    m_gray = L.emit_mat('t_gray', L.C['gray700'])

    # 3D로 떠오르는 대기함 카드(이후 S6에서 '작업전'으로 바뀐다)
    w, h = 0.235, 0.105
    card = L.empty('task_card', px(1748, 312), COLL)
    m_body = L.mat('m_card_body', '#ffffff', 0.4)
    m_bar = L.mat('m_card_bar', '#ffffff', 0.4)
    m_chip = L.emit_mat('m_card_chip', '#d6e3fa')
    body = L.rbox('task_card_body', (w, 0.012, h), (0, 0, 0), m_body, COLL, bevel=0.012)
    bar = L.rbox('task_card_bar', (0.009, 0.014, h - 0.01), (-w / 2 + 0.008, 0, 0), m_bar, COLL, bevel=0.003)
    chip = L.rbox('task_card_chip', (0.062, 0.004, 0.026), (-w / 2 + 0.05, -0.007, 0.028), m_chip, COLL, bevel=0.012,
                  segments=6)
    title = L.text('task_card_title', '가스보일러 점검', (-w / 2 + 0.02, -0.008, -0.004), 0.024, m_txt, COLL,
                   align='LEFT')
    sub0 = L.text('task_card_sub0', '기사 미정 · 등록 5일 경과', (-w / 2 + 0.02, -0.008, -0.034), 0.014, m_gray, COLL,
                  align='LEFT', weight='SemiBold')
    sub1 = L.text('task_card_sub1', '09:00 - 11:00 · 김태훈 기사', (-w / 2 + 0.02, -0.008, -0.034), 0.014, m_gray,
                  COLL, align='LEFT', weight='SemiBold')
    chip_t = {}
    for key_, body_, col in (('a', '점검', L.C['secondary']), ('b', '배정됨', L.C['gray900']),
                             ('c', '작업전', '#ffffff')):
        chip_t[key_] = L.text(f'task_card_chip_{key_}', body_, (-w / 2 + 0.05, -0.0095, 0.028), 0.014,
                              L.emit_mat(f't_chip_{key_}', col), COLL, weight='SemiBold')
    parts = [body, bar, chip, title, sub0, sub1] + list(chip_t.values())
    for o in parts:
        o.parent = card

    land = F0 + 66
    start = px(1748, 312)
    target = px(535, 734)
    target = (target[0] + w / 2 + 0.005, target[1], target[2])
    path = [(F0, start, 1.0), (F0 + 14, start, 1.0), (F0 + 22, (start[0] - 0.02, -0.16, start[2] + 0.02), 1.08),
            (F0 + 44, ((start[0] + target[0]) / 2, -0.3, (start[2] + target[2]) / 2 + 0.1), 1.1),
            (F0 + 60, (target[0], -0.12, target[2]), 1.06), (land, target, 1.0)]
    for f, loc, sc in path:
        L.key(card, f, loc=loc, scale=sc, rot=(0, 0, 0))
    L.key(card, F0 + 44, rot=(0, -6, 0))
    L.key(card, F0 + 60, rot=(0, 0, 0))

    # 상태 변화: 등록(대기함) → 배정됨 → (S6) 작업전
    L.key_color(m_body, land - 1, '#ffffff')
    L.key_color(m_body, land, '#e4e4e8')
    L.key_color(m_bar, land - 1, '#ffffff')
    L.key_color(m_bar, land, L.C['gray500'])
    L.key_color(m_chip, land - 1, '#d6e3fa')
    L.key_color(m_chip, land, L.C['gray300'])
    accept = 385 + 56  # S6에서 기사가 수락한 순간
    L.key_color(m_body, accept - 1, '#e4e4e8')
    L.key_color(m_body, accept, L.C['confirmed'])
    L.key_color(m_bar, accept - 1, L.C['gray500'])
    L.key_color(m_bar, accept, L.C['secondary'])
    L.key_color(m_chip, accept - 1, L.C['gray300'])
    L.key_color(m_chip, accept, L.C['secondary'])
    card_end = 469
    L.show_between([card, body, bar, chip, title], F0, card_end)
    L.swap(sub0, sub1, land, F0, card_end)
    L.show_between([chip_t['a']], F0, land)
    L.show_between([chip_t['b']], land, accept)
    L.show_between([chip_t['c']], accept, card_end)

    # 들어 올린 자리를 대기함 배경색으로 덮는다
    cover = L.plane('task_slot_cover', (0.25, 0.12), px(1748, 312, -0.0195), L.emit_mat('e_panel', L.C['primary']),
                    COLL)
    L.show_between([cover], F0 + 16, card_end)

    # 커서
    cur = L.cyl('cursor', 0.022, 0.004, (0, 0, 0), L.emit_mat('e_cursor', '#ffffff', 1.3), COLL, verts=3,
                rot=(math.radians(90), 0, math.radians(0)))
    off = (0.07, -0.02, -0.03)
    L.key(cur, F0, loc=(X + 0.95, -0.35, MZ - 0.35))
    for f, loc, _ in path[1:]:
        L.key(cur, f, loc=(loc[0] + off[0], loc[1] + off[1], loc[2] + off[2]))
    L.key(cur, land + 10, loc=(target[0] + 0.25, -0.12, target[2] - 0.12))
    L.show_between([cur], F0, F1)

    # 내려앉을 때 보라 파동
    ripple = L.torus('task_ripple', 0.14, 0.004, target, L.emit_mat('e_ripple', L.C['primary100'], 2.5), COLL,
                     rot=(math.radians(90), 0, 0))
    L.key(ripple, land, scale=0.3)
    L.key(ripple, land + 14, scale=1.6)
    L.show_between([ripple], land, land + 15)

    objs += [cover, cur, ripple]
    cam = L.camera('CAM_S5', 35)
    L.cam_key(cam, F0, (X + 1.15, -2.35, 1.8), (X + 0.25, 0, MZ), lens=35)
    L.cam_key(cam, F1 - 1, (X + 0.1, -1.95, 1.72), (X - 0.1, 0, MZ - 0.08), lens=40)
    L.cut(cam, F0, 'S5')
    L.caption(cam, 's5_cap', '드래그 한 번으로 기사 배정', F0 + 8, F1, sub='타임테이블 · 대기함')
    return cam
