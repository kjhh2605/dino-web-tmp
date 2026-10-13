"""S8 0:23–0:26 (f553–624) 기능 4: 완료 보고까지 전화 없이.

기사 폰이 '완료 보고' 화면으로 바뀌고 '보고 제출'을 누르면 작업 전·후 사진 카드가
모니터로 날아간다. 모니터는 실제 알림함 캡처로 바뀌고 '완료 보고가 도착했어요' 토스트가 뜬다.
"""
import math
import os

F0, F1 = 553, 625
X = 80.0
COLL = 'STAGE'
END = 721


def build(L):
    import bpy
    import shots.s6_accept as s6
    scr = bpy.data.materials['m_monitor']
    L.show_screen(scr, 2, F0)
    ph = bpy.data.objects['tech_phone']
    W = [(F0, END)]
    ui = s6.ui(L, ph, 'rep', [
        ('box', 'status', (0.071, 0.012), (0, 0.068), '#1c1b2a'),
        ('text', 'title', '완료 보고', (-0.03, 0.052), 0.0062, '#222222', 'LEFT'),
        ('text', 'sub', '가스보일러 점검 · 작업중', (-0.03, 0.044), 0.0034, '#767676', 'LEFT'),
        ('text', 'memo', '배관 세척 후 정상 작동 확인', (-0.03, -0.012), 0.0034, '#404040', 'LEFT'),
        ('box', 'btn', (0.064, 0.012), (0, -0.032), '#4f3bfe'),
        ('text', 'btn_t', '보고 제출', (0, -0.032), 0.0040, '#ffffff', 'CENTER'),
    ], W)
    photos = []
    for i, name in enumerate(('photo_before.png', 'photo_after.png')):
        m = L.image_mat(f'img_{name}', os.path.join(L.ASSETS, 'gen', name))
        p = L.plane(f'rep_photo_{i}', (0.03, 0.03), (-0.016 + i * 0.032, -0.0062, 0.018), m, COLL)
        p.parent = ph
        photos.append(p)
    L.show_windows(photos, W)
    L.key(ui['btn'], F0 + 10, scale=1.0)
    L.key(ui['btn'], F0 + 13, scale=0.9)
    L.key(ui['btn'], F0 + 16, scale=1.0)

    # 모니터로 날아가는 사진 카드
    start = (X + 1.3, -0.66, 1.33)
    target = (X + 0.5, -0.06, 1.98)
    fly = []
    for i, name in enumerate(('photo_before.png', 'photo_after.png')):
        root = L.empty(f'fly_{i}', start, COLL)
        frame = L.rbox(f'fly_{i}_frame', (0.25, 0.006, 0.25), (0, 0.003, 0), L.mat('m_photo_frame', '#ffffff', 0.4),
                       COLL, bevel=0.01)
        img = L.plane(f'fly_{i}_img', (0.23, 0.23), (0, -0.001, 0), bpy.data.materials[f'img_{name}'], COLL)
        for o in (frame, img):
            o.parent = root
        f = F0 + 14 + i * 5
        L.key(root, f, loc=start, scale=0.3, rot=(0, 0, 20))
        L.key(root, f + 12, loc=((start[0] + target[0]) / 2 + 0.1 - i * 0.28, -0.75, 1.75), scale=1.0,
              rot=(0, (-8 if i else 8), 0))
        L.key(root, f + 26, loc=(target[0] - 0.13 + i * 0.1, -0.05, target[2] - 0.02), scale=0.25, rot=(0, 0, 0))
        L.show_between([root, frame, img], f, f + 27)
        fly += [root, frame, img]

    # 모니터 위 토스트
    toast = L.empty('toast', (X + 0.3, -0.08, 1.95), COLL)
    tb = L.rbox('toast_bg', (0.66, 0.02, 0.16), (0, 0, 0), L.emit_mat('e_toast', L.C['primary']), COLL, bevel=0.04)
    chk = L.cyl('toast_chk', 0.035, 0.006, (-0.27, -0.013, 0), L.emit_mat('e_done', L.C['completed'], 1.2), COLL,
                rot=(math.radians(90), 0, 0))
    t1 = L.text('toast_t1', '완료 보고가 도착했어요', (-0.215, -0.013, 0.025), 0.036, L.emit_mat('t_white', '#ffffff'),
                COLL, align='LEFT')
    t2 = L.text('toast_t2', '가스보일러 점검 · 김태훈 기사 · 사진 2장', (-0.215, -0.013, -0.03), 0.022,
                L.emit_mat('t_lav', L.C['primary100']), COLL, align='LEFT', weight='SemiBold')
    for o in (tb, chk, t1, t2):
        o.parent = toast
    toast.scale = (1.35, 1.35, 1.35)
    L.pop_in(toast, F0 + 40, dur=8, overshoot=1.1)
    L.show_between([toast, tb, chk, t1, t2], F0 + 39, F1)

    cam = L.camera('CAM_S8', 32)
    L.cam_key(cam, F0, (X + 1.95, -1.7, 1.5), (X + 0.75, -0.2, 1.62), lens=32)
    L.cam_key(cam, F1 - 1, (X + 1.75, -2.05, 1.62), (X + 0.6, -0.1, 1.72), lens=32)
    L.cut(cam, F0, 'S8')
    L.caption(cam, 's8_cap', '완료 보고까지, 전화 없이', F0 + 6, F1, sub='사진 · 메모 · 알림이 한 곳에')
    return cam
