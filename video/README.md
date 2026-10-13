# Orbit 소개 영상(30초) — 콘티 · Blender 초안

최종 영상은 Higgsfield로 만들고, 이 폴더는 그 전 단계인 **구성 콘티**와 **Blender 구도·타이밍 초안**입니다.
Blender 씬은 [blender-mcp](https://github.com/ahujasid/mcp-for-blender)의 `execute_blender_code` 도구로 만들었습니다.

| 산출물 | 경로 |
| --- | --- |
| 콘티(이 문서) | `video/README.md` |
| 샷별 기준 프레임 1920×1080(자막 없음 = Higgsfield 입력용, `_clean`) | `video/renders/keyframes/` |
| 콘티 시트(9샷 한 장) | `video/renders/storyboard.jpg` |
| 30초 애니매틱(960×540, 24fps, 자막 포함) | `video/renders/orbit_animatic.mp4` |
| Blender 파일 | `video/blender/orbit_intro.blend` |
| 씬 빌드 스크립트(샷별) | `video/blender/shots/s1_phone.py` … `s9_end.py`, 공통 `orbit_lib.py` |

## 1. 기획 요약

- **서비스**: Orbit — 설비·시공 현장 작업을 다루는 발주사(사무실)와 현장 기사를 잇는 업무 관리 플랫폼. 사무실은 웹(타임테이블·작업 목록·진행 보드·조직 설정·알림함), 기사는 모바일 앱에서 배정을 받고 수락·작업 시작·완료 보고를 한다.
- **해결하는 문제**: 배정·일정 변경·진행 확인·완료 확인이 전화·메신저·엑셀로 흩어져 있다. 같은 시간대 이중 배정이 생기고, 기사가 지금 어디서 무엇을 하는지는 전화해야만 알 수 있다.
- **핵심 메시지**(랜딩 카피 그대로): "현장을 위한 스마트한 업무 관리 플랫폼" / "담당 기사 배치부터 작업 완료까지, 전화 없이 한눈에 관리하세요"
- **영상에서 따라가는 작업 하나**: 대기함의 *가스보일러 점검* → 김태훈 기사 09:00 배정(배정됨) → 기사 앱에서 수락(작업전) → 진행 보드에서 작업중·완료 → 사진이 담긴 완료 보고 도착. 실제 상태 6종(등록·배정됨·작업전·작업중·완료·취소) 표기와 색을 그대로 쓴다.

## 2. 구성(30초 = 720프레임 @24fps)

| 막 | 샷 | 시간 | 프레임 | 한 줄 |
| --- | --- | --- | --- | --- |
| 문제 제기 | S1 | 0:00–0:03 | 1–72 | 쉬지 않고 울리는 전화 |
| | S2 | 0:03–0:06.3 | 73–150 | 전화·메신저·엑셀에 흩어진 일정, 일정 충돌 |
| | S3 | 0:06.3–0:09 | 151–216 | 기사는 지금 어디서 무엇을? |
| 전환 | S4 | 0:09–0:12 | 217–288 | 흩어진 것들이 하나의 궤도로 → Orbit |
| 기능 | S5 | 0:12–0:16 | 289–384 | 타임테이블에서 드래그 한 번으로 배정 |
| | S6 | 0:16–0:19.5 | 385–468 | 기사는 앱에서 바로 확인·수락 |
| | S7 | 0:19.5–0:23 | 469–552 | 진행 상황을 실시간으로 한눈에 |
| | S8 | 0:23–0:26 | 553–624 | 완료 보고까지, 전화 없이 |
| 엔딩 | S9 | 0:26–0:30 | 625–720 | Orbit 로고 + 헤드라인 |

**톤 전환**: S1–S3는 따뜻한 텅스텐 조명·노랑/빨강 경고색·좁은 화각으로 답답하게, S4에서 그 조각들이 보라색으로 바뀌며 궤도에 정렬되고, S5–S9는 브랜드 남색(#1c1b2a) 스튜디오와 보라(#4f3bfe·#a99fff) 림 라이트로 정돈된 느낌으로 간다. S4의 *궤도(Orbit)* 고리는 S9 엔딩에서 다시 제품을 감싸며 수미상관을 만든다.

**같은 사물로 잇기**: S1의 휴대폰·S2의 포스트잇과 말풍선·S3의 위치 핀이 S4에서 궤도에 올라타고, S5에서 떠오른 카드가 S6 기사 폰 화면과 S7 보드 행으로 이어진다. 문제의 사물이 해결 화면의 요소로 바뀌는 흐름이다.

## 3. 샷별 콘티

각 샷의 *기준 프레임*은 `renders/keyframes/S#_<frame>_clean.jpg`(자막 없음)와 `S#_<frame>.jpg`(자막 있음)입니다. Higgsfield 프롬프트는 이미지→영상(시작 프레임 = 첫 번째 기준 프레임)을 전제로 썼습니다.

### S1 0:00–0:03 · 쉬지 않고 울리는 전화
- **화면**: 어두운 사무실 책상. 가운데 휴대폰에 "김민수 기사 · 수신 중 / 부재중 전화 12", 양옆 폰 2대는 "카톡 37". 뒤 모니터에는 수기로 관리하는 엑셀 배정표(`현장배정_10월_최종_진짜최종(2).xlsx`, 빈칸·물음표·빨간 수정 흔적).
- **동작**: 폰 3대가 번갈아 진동. 메인 폰 옆으로 알림 카드 5장이 하나씩 튀어 올라 쌓인다(부재중 전화 이민준 기사 (3) → 메시지 "기사님 몇 시 도착하세요?" → 고객 윤서아 (2) → "오후 일정 바뀌었어요!!" → 김태훈 기사 (5)).
- **카메라**: 하이 앵글 3/4, 40mm, 3초 동안 천천히 밀어 들어감(dolly in).
- **자막**: 오늘도 전화로 시작되는 현장 배정 / "기사님, 지금 어디세요?"
- **사운드**: 진동음·벨소리가 겹쳐 점점 커짐.
- **Higgsfield**: `Dark office desk at night, three smartphones vibrating and buzzing, stacked missed-call and chat notification cards popping up one after another, warm desk lamp, cluttered spreadsheet on monitor behind, tense mood, slow dolly in, shallow depth of field, cinematic 3D product render` · 카메라 프리셋: Dolly In(느리게)

### S2 0:03–0:06.3 · 흩어진 일정
- **화면**: 코르크보드에 엑셀 출력물, 포스트잇("김민수 9시 배관", "이철호?? 2시", "보일러 교체 → 누구?", "13시 겹침!!" …), 정보를 잇는 빨간 실. 카톡색 말풍선 5개가 차례로 튀어나온다("기사님 몇 시 도착?", "작업 끝나셨나요?", "사진 보내주세요", "일정 바뀌었어요!", "주소 다시 알려주세요").
- **동작**: 앞쪽에서 *보일러 수리 14:00*과 *에어컨 점검 14:00*(둘 다 이민준 기사) 카드가 양쪽에서 밀려와 겹치고, 빨간 "일정 충돌" 태그가 튀어나와 흔들린다.
- **카메라**: 32mm, 보드를 따라 좌→우 트럭.
- **자막**: 전화 · 메신저 · 엑셀에 흩어진 일정 / 겹치는 배정, 놓치는 연락
- **Higgsfield**: `Cork board covered with sticky notes, printed spreadsheet and red strings, yellow chat bubbles popping in front, two schedule cards slide in from both sides and collide, red "schedule conflict" warning badge shakes, chaotic office, camera trucks left to right, stylized 3D` · 프리셋: Truck Right / Pan

### S3 0:06.3–0:09 · 보이지 않는 현장
- **화면**: 밤의 도시 미니어처. 기사 6명(김민수·이민준·홍길동·김태훈·박서연·이철호)의 위치 핀 위에 "?"가 떠 있고, 핀마다 빨간 파동이 퍼진다.
- **카메라**: 30mm 하이 앵글, 천천히 선회하며 내려옴.
- **자막**: 기사님은 지금 어디서, 무엇을? / 현장 상황은 전화해야만 알 수 있다
- **Higgsfield**: `Miniature night city diorama from above, glowing location pins with question marks over each pin, red pulse rings spreading, dark moody blue light, slow orbiting aerial camera, tilt-shift, 3D render` · 프리셋: Arc / Orbit(느리게)

### S4 0:09–0:12 · 하나의 궤도로(전환)
- **화면**: 앞 샷의 포스트잇·말풍선·폰·핀 조각이 사방에서 날아와 기울어진 세 개의 궤도 고리에 올라탄다. 날아오는 동안 노랑·빨강·카톡색이 라벤더·보라·흰색으로 바뀐다. 중심에 Orbit 마크(둥근 사각형)가 켜지고, 왼쪽으로 비켜서며 "Orbit" 워드마크와 락업을 만든다.
- **카메라**: 24mm로 혼란 한가운데서 시작해 32mm로 빠지며 롤 -6° → 0°(정돈).
- **자막**: 흩어진 현장을, 하나의 궤도로
- **사운드**: 소음이 빨려 들어가듯 사라지고(리버스 스윕) 맑은 톤 하나.
- **Higgsfield**: `Scattered sticky notes, chat bubbles, smartphones and map pins fly inward and snap into three glowing tilted orbit rings, colors shift from yellow and red to lavender and violet, a white rounded-square logo lights up in the center, dark navy background, camera pulls back, satisfying motion design` · 프리셋: Dolly Out / Super Dolly Out. 끝 프레임(`S4_282_clean.jpg`)을 End frame으로 지정하면 로고 락업 구도가 유지됩니다.

### S5 0:12–0:16 · 드래그 한 번으로 배정
- **화면**: 남색 스튜디오의 모니터에 실제 Orbit 타임테이블(편집 모드) 화면. 오른쪽 대기함의 *가스보일러 점검*(점검·기사 미정) 카드가 3D로 떠올라 커서를 따라 호를 그리며 *김태훈 기사 09:00* 칸에 내려앉는다. 착지 순간 보라 파동, 카드가 회색 블록으로 바뀌고 칩이 "점검" → "배정됨", 부제가 "09:00 - 11:00 · 김태훈 기사"로 바뀐다. 빈 대기함 자리는 패널색으로 비워진다.
- **카메라**: 35mm 3/4 앵글에서 40mm 정면 쪽으로 밀어 들어감.
- **자막**: 드래그 한 번으로 기사 배정 / 타임테이블 · 대기함
- **Higgsfield**: `Sleek monitor on a desk in a dark navy studio with violet rim light, scheduling app on screen, a task card lifts out of the screen in 3D, follows a cursor in an arc and snaps into an empty time slot with a soft purple ripple, clean UI motion, slow push in` · 프리셋: Dolly In. **화면 UI 글자는 AI가 뭉개므로** 편집 단계에서 실제 화면 캡처(`blender/assets/ui/timetable-edit.png`)나 화면 녹화를 모니터에 합성하는 것을 권장합니다.

### S6 0:16–0:19.5 · 기사는 앱에서 바로 수락
- **화면**: 모니터의 배정 카드에서 보라색 신호가 기사 폰으로 날아간다. 폰 상단에 "새 작업이 배정되었어요 · 가스보일러 점검 · 09:00" 푸시가 뜨고, 작업 카드(09:00–11:00 · 서초구 반포동 · "보일러 E-02 오류, 점검 요청")에 거절/수락 버튼. 수락을 탭하면 칩이 "배정됨" → "작업전"(보라)으로 바뀌고 "수락 완료 · 사무실에 바로 반영돼요". 신호가 모니터로 되돌아가고 뒤 모니터의 카드도 같은 순간 보라(작업전)로 바뀐다.
- **카메라**: 40mm, 폰을 전경 오른쪽, 모니터를 배경 왼쪽에 둔 투샷. 살짝 밀어 들어감.
- **자막**: 기사는 앱에서 바로 확인 · 수락 / 배정 알림 → 수락 → 사무실 화면에 즉시 반영
- **Higgsfield**: `Smartphone floating beside a desktop monitor, glowing violet signal dots travel from the monitor to the phone, a push notification drops in, a finger taps the accept button, status badge turns purple, synced update on the monitor behind, dark navy studio, gentle push in` · 프리셋: Dolly In / Focus change(폰 → 모니터)

### S7 0:19.5–0:23 · 진행 상황을 실시간으로
- **화면**: 모니터가 실제 진행 보드 화면으로 바뀐다. 앞에 작업 행 4개가 떠 있고 상태 칩이 차례로 바뀐다 — 가스보일러 점검 작업전→작업중, 식기세척기 설치 작업중→완료, 세탁기 설치 배정됨→작업전, 보일러 배관 교체 작업중→완료. 오른쪽 "오늘 완료" 카드(초록 실시간 점)가 4건 → 5건 → 6건.
- **카메라**: 38mm 낮은 3/4 앵글, 좌→우로 천천히 트럭.
- **자막**: 진행 상황을 실시간으로 한눈에 / 배정됨 · 작업전 · 작업중 · 완료
- **Higgsfield**: `Floating task rows in front of a dashboard monitor, status pills flip one after another from purple to orange to green, a KPI card counter ticks up, live green dot pulsing, clean modern SaaS motion graphics, dark navy studio with violet glow, slow lateral camera move` · 프리셋: Truck Right

### S8 0:23–0:26 · 완료 보고까지, 전화 없이
- **화면**: 기사 폰이 "완료 보고" 화면(작업 전·후 사진 2장, 메모 "배관 세척 후 정상 작동 확인", 보고 제출 버튼). 제출을 누르면 사진 카드 두 장이 모니터로 날아가고, 모니터는 실제 알림함 화면으로 바뀌며 "완료 보고가 도착했어요 · 가스보일러 점검 · 김태훈 기사 · 사진 2장" 토스트가 뜬다.
- **카메라**: 32mm, 폰 쪽 어깨 너머에서 모니터를 바라보며 살짝 빠짐.
- **자막**: 완료 보고까지, 전화 없이 / 사진 · 메모 · 알림이 한 곳에
- **Higgsfield**: `Over-the-shoulder view from a smartphone showing a completion report with before and after photos, photo cards fly from the phone to the desktop monitor, a dark notification toast pops up with a green check, dark navy studio, smooth camera pull back` · 프리셋: Dolly Out

### S9 0:26–0:30 · 엔딩
- **화면**: 카메라가 크게 빠지며 모니터(실제 타임테이블)와 기사 폰을 세 개의 궤도 고리가 감싸고 빛나는 점이 돈다. 위로 Orbit 로고 락업, 헤드라인 "현장을 위한 스마트한 업무 관리 플랫폼", 서브 "담당 기사 배치부터 작업 완료까지, 전화 없이 한눈에"가 차례로 떠오른다.
- **카메라**: 35mm, 2초 동안 크게 dolly out 후 정지(마지막 2초는 로고 홀드).
- **Higgsfield**: `Wide shot of a desk with a monitor and a smartphone encircled by three glowing lavender orbit rings with light particles orbiting, a white logo and headline text rise above, dark navy studio with violet glow, calm confident ending, camera pulls back and settles` · 프리셋: Super Dolly Out. 로고·헤드라인 글자는 AI 생성 대신 편집 툴에서 벡터(`front/src/assets/logo/*.svg`)로 올리는 것을 권장합니다.

## 4. Higgsfield 작업 가이드

1. 샷마다 `keyframes/S#_<시작>_clean.jpg`를 시작 프레임으로, 필요하면 `S#_<끝>_clean.jpg`를 끝 프레임으로 넣고 위 프롬프트와 카메라 프리셋을 씁니다. 길이는 표의 샷 길이에 맞춰 3–4초로 생성하고 편집에서 잘라 씁니다.
2. 자막·로고·UI 글자는 생성 결과에 맡기지 말고 편집 단계에서 올립니다. 자막 위치·타이밍은 애니매틱(`orbit_animatic.mp4`)을 기준으로 합니다.
3. 화면 속 UI(S5–S9)는 실제 화면 캡처나 화면 녹화로 교체 합성하는 것이 안전합니다. 캡처 원본은 `blender/assets/ui/`(1920×1080, 실제 앱 `/timetable?mode=edit`, `/board`, `/notifications`, `/timetable`).
4. 브랜드 색: Primary `#1c1b2a`, Secondary `#4f3bfe`, Primary100 `#a99fff`, 상태색 작업전 `#4f3bfe`·작업중 `#eea216`·완료 `#277d02`·경고 `#d71a29`(`front/src/styles/tokens.css`).

## 5. Blender 씬 다시 만들기

- Blender 5.2(또는 `pip install bpy==5.2.2`)에서 `video/blender/build_all.py`를 실행하면 S1–S9를 다시 만들고 `orbit_intro.blend`로 저장합니다. blender-mcp를 쓸 때는 이 파일 내용을 `execute_blender_code`로 보냅니다.
- 샷 하나만 고치려면 `shots/s#_*.py`를 수정하고 `build_all.py`를 다시 실행합니다(세트는 X축 0·20·40·60·80m에 떨어져 있고, 타임라인 마커 S1–S9가 카메라를 전환합니다).
- 컬렉션 `CAPTIONS`를 렌더에서 끄면 자막 없는 클린 프레임이 나옵니다.
- 렌더: `python render.py keyframes`(1920×1080 기준 프레임) → `python make_storyboard.py`(JPG 변환 + 콘티 시트), `python render.py animatic`(960×540 PNG 시퀀스) 후 `ffmpeg -framerate 24 -i renders/animatic/%04d.png -c:v libx264 -pix_fmt yuv420p renders/orbit_animatic.mp4`. 문제 제기 파트 텍스처는 `python gen_textures.py`로 다시 만듭니다.
- 폰트: Pretendard(SIL OFL 1.1) — `blender/assets/fonts/`.

## 6. 확인이 필요한 것

- **기사 앱 화면**: 이 저장소에는 기사용 모바일 앱이 없어서 S6·S8의 폰 화면은 웹의 상태·용어(배정 알림, 수락/거절, 완료 보고, 사진)를 바탕으로 단순화해 만들었습니다. Figma `앱UI` 페이지의 실제 화면으로 바꿔야 합니다.
- **로고**: 3D 락업은 마크(둥근 사각형) + Pretendard ExtraBold "Orbit"으로 근사했습니다. 최종 편집에서는 `orbit-lockup.svg`를 씁니다.
- **화면 캡처의 날짜·데이터**는 목업 시드(실행한 날 기준)입니다.
- 애니매틱은 구도·타이밍 확인용 저해상도(EEVEE 8샘플)입니다.
