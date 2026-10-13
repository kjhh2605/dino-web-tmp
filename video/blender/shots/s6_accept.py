"""S6 0:16–0:19.5 (f385–468) 기능 2: 기사는 앱에서 바로 확인·수락.

모니터의 배정 카드에서 보라색 신호가 기사 폰으로 날아가고, 폰 상단에 배정 알림이 내려온다.
작업 카드의 '수락'을 누르면 칩이 '배정됨' → '작업전'으로 바뀌고, 뒤 모니터의 카드도 같은 순간
보라색(작업전)으로 바뀐다(실시간 동기화). 폰은 S8·S9에서도 쓴다.
"""
import math

F0, F1 = 385, 469
X = 80.0
PHONE_LOC = (X + 1.3, -0.62, 1.28)
PHONE_SCALE = 2.6
COLL = 'STAGE'
ACCEPT = F0 + 56   # s5_assign의 accept와 같은 프레임


def ui(L, root, name, items, window):
    """폰 화면 로컬 좌표(가로 0.071, 세로 0.15, 화면 면 y=-0.0058)에 UI를 얹는다."""
    out = []
    for it in items:
        kind = it[0]
        if kind == 'box':
            _, nm, size, loc, col = it
            o = L.rbox(f'{name}_{nm}', (size[0], 0.0006, size[1]), (loc[0], -0.0060, loc[1]),
                       L.emit_mat(f'ui_{col}', col), COLL, bevel=min(size) * 0.25, segments=4)
        else:
            _, nm, body, loc, sz, col, align = it
            o = L.text(f'{name}_{nm}', body, (loc[0], -0.0066, loc[1]), sz, L.emit_mat(f'ui_{col}', col), COLL,
                       align=align, weight='Bold' if sz >= 0.005 else 'SemiBold')
        o.parent = root
        out.append(o)
    if window:
        L.show_windows(out, window)
    return {o.name.replace(name + '_', ''): o for o in out}


def build(L):
    ph, scr = L.phone('tech_phone', PHONE_LOC, COLL, rot=(0, 0, 28),
                      screen_mat=L.emit_mat('scr_app', '#f5f6f8'))
    ph.scale = (PHONE_SCALE,) * 3
    parts = [ph] + list(ph.children)
    L.show_windows(parts, [(F0, F1), (553, 721)])
    L.key(ph, F0, loc=(PHONE_LOC[0] + 0.25, PHONE_LOC[1], PHONE_LOC[2] - 0.15), rot=(8, 0, 40))
    L.key(ph, F0 + 14, loc=PHONE_LOC, rot=(0, 0, 28))

    W = [(F0, F1)]
    base = ui(L, ph, 'app', [
        ('box', 'status', (0.071, 0.012), (0, 0.068), '#1c1b2a'),
        ('text', 'hello', '오늘의 작업', (-0.03, 0.052), 0.0062, '#222222', 'LEFT'),
        ('text', 'date', '10월 14일 (수) · 김태훈 기사', (-0.03, 0.044), 0.0034, '#767676', 'LEFT'),
        ('box', 'card', (0.064, 0.05), (0, 0.006), '#ffffff'),
        ('box', 'card_bar', (0.0018, 0.046), (-0.0305, 0.006), '#4f3bfe'),
        ('text', 'card_title', '가스보일러 점검', (-0.027, 0.018), 0.0052, '#222222', 'LEFT'),
        ('text', 'card_time', '09:00 - 11:00 · 서초구 반포동', (-0.027, 0.009), 0.0031, '#767676', 'LEFT'),
        ('text', 'card_memo', '보일러 E-02 오류, 점검 요청', (-0.027, 0.002), 0.0031, '#767676', 'LEFT'),
        ('box', 'btn_no', (0.026, 0.011), (-0.0155, -0.011), '#e9e9ea'),
        ('text', 'btn_no_t', '거절', (-0.0155, -0.011), 0.0036, '#585858', 'CENTER'),
        ('box', 'btn_ok', (0.026, 0.011), (0.0155, -0.011), '#4f3bfe'),
        ('text', 'btn_ok_t', '수락', (0.0155, -0.011), 0.0036, '#ffffff', 'CENTER'),
        ('box', 'next', (0.064, 0.022), (-0.0, -0.038), '#ffffff'),
        ('text', 'next_t', '13:00  세탁기 설치 · 작업전', (-0.027, -0.038), 0.0032, '#585858', 'LEFT'),
    ], W)
    for k in ('card', 'card_bar', 'card_title', 'card_time', 'card_memo', 'btn_no', 'btn_no_t', 'btn_ok', 'btn_ok_t'):
        L.pop_in(base[k], F0 + 34, dur=8, overshoot=1.04)

    chips = ui(L, ph, 'app', [
        ('box', 'chip_a', (0.014, 0.0055), (0.023, 0.018), '#cecece'),
        ('text', 'chip_a_t', '배정됨', (0.023, 0.018), 0.0026, '#1f1f1f', 'CENTER'),
        ('box', 'chip_b', (0.014, 0.0055), (0.023, 0.018), '#4f3bfe'),
        ('text', 'chip_b_t', '작업전', (0.023, 0.018), 0.0026, '#ffffff', 'CENTER'),
        ('text', 'done', '수락 완료 · 사무실에 바로 반영돼요', (0, -0.011), 0.0031, '#4f3bfe', 'CENTER'),
    ], None)
    L.show_between([chips['chip_a'], chips['chip_a_t']], F0 + 34, ACCEPT - 4)
    L.show_between([chips['chip_b'], chips['chip_b_t'], chips['done']], ACCEPT - 4, F1)
    L.pop_in(chips['chip_b'], ACCEPT - 4, dur=6, overshoot=1.3)
    for k in ('btn_no', 'btn_no_t', 'btn_ok', 'btn_ok_t'):
        L.pop_out(base[k], ACCEPT - 5, dur=1)

    # 상단에서 내려오는 배정 알림
    banner = ui(L, ph, 'push', [
        ('box', 'bg', (0.066, 0.017), (0, 0.0), '#1c1b2a'),
        ('text', 't1', '새 작업이 배정되었어요', (-0.029, 0.0035), 0.0038, '#ffffff', 'LEFT'),
        ('text', 't2', '가스보일러 점검 · 09:00', (-0.029, -0.0035), 0.003, '#a99fff', 'LEFT'),
    ], None)
    broot = L.empty('push_root', (0, 0, 0), COLL)
    broot.parent = ph
    for o in banner.values():
        o.parent = broot
    broot.location = (0, 0, 0.058)
    L.pop_in(broot, F0 + 20, dur=6, overshoot=1.08)
    L.pop_out(broot, F0 + 47, dur=4)
    L.show_between(list(banner.values()), F0 + 20, F0 + 52)

    # 손가락 탭
    tap = L.torus('tap_ring', 0.006, 0.0009, (0.0155, -0.0066, -0.011), L.emit_mat('e_tap', '#a99fff', 2.0), COLL,
                  rot=(math.radians(90), 0, 0))
    tap.parent = ph
    L.key(tap, ACCEPT - 6, scale=0.3)
    L.key(tap, ACCEPT + 4, scale=2.2)
    L.show_between([tap], ACCEPT - 6, ACCEPT + 5)

    # 모니터 카드 → 폰으로 가는 신호
    src = (X - 0.16, -0.05, 1.63 - 0.18)
    for i in range(5):
        dot = L.sphere(f'signal_{i}', 0.018, src, L.emit_mat('e_signal', L.C['primary100'], 4.0), COLL, seg=16)
        f = F0 + 4 + i * 3
        mid = ((src[0] + PHONE_LOC[0]) / 2, -0.55, src[2] + 0.35)
        L.key(dot, f, loc=src, scale=0.4)
        L.key(dot, f + 8, loc=mid, scale=1.0)
        L.key(dot, f + 16, loc=PHONE_LOC, scale=0.3)
        L.show_between([dot], f, f + 17)
    # 수락 → 모니터로 되돌아가는 신호
    for i in range(4):
        dot = L.sphere(f'signal_back_{i}', 0.016, PHONE_LOC, L.emit_mat('e_signal', L.C['primary100'], 4.0), COLL,
                       seg=16)
        f = ACCEPT - 4 + i * 2
        L.key(dot, f, loc=PHONE_LOC, scale=0.3)
        L.key(dot, f + 5, loc=((src[0] + PHONE_LOC[0]) / 2, -0.5, src[2] + 0.3), scale=1.0)
        L.key(dot, f + 9, loc=src, scale=0.3)
        L.show_between([dot], f, f + 10)

    cam = L.camera('CAM_S6', 40)
    L.cam_key(cam, F0, (X + 2.15, -2.0, 1.42), (X + 0.95, -0.42, 1.2), lens=40)
    L.cam_key(cam, F1 - 1, (X + 1.95, -1.72, 1.4), (X + 1.0, -0.45, 1.2), lens=40)
    L.cut(cam, F0, 'S6')
    L.caption(cam, 's6_cap', '기사는 앱에서 바로 확인 · 수락', F0 + 6, F1, sub='배정 알림 → 수락 → 사무실 화면에 즉시 반영')
    return cam
