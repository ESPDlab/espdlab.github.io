# ESPD Lab 홈페이지

중앙대학교 에너지시스템 예지 & 진단 연구실(Energy System Prognostics & Diagnostics Lab) 홈페이지입니다.
빌드 과정이 없는 정적 사이트입니다. 이 저장소의 파일이 그대로 GitHub Pages에 올라갑니다.

- 저장소: <https://github.com/ESPDlab/espdlab.github.io>
- 주소: <https://espdlab.github.io/> (학교 주소 `energypd.cau.ac.kr` 을 연결한 뒤에는 그쪽으로 넘어갑니다)
- 수정 화면: <https://app.pagescms.org>

## 내용을 고치는 방법

소식, 구성원, 과제, 논문은 코드를 건드리지 않고 고칩니다.

처음 한 번 준비할 것:

- 고칠 사람은 GitHub 계정이 있어야 하고, `ESPDlab` 조직의 Owner가 그 계정을 초대해야 합니다(조직 화면 → People → Invite member). 조직 Settings → Member privileges → Base permissions 가 Write 여야 구성원이 저장소를 고칠 수 있습니다.
- Pages CMS 앱이 `ESPDlab` 조직의 이 저장소에 설치되어 있어야 합니다. Owner가 app.pagescms.org 에 처음 로그인할 때 한 번 설치합니다(조직 Settings → GitHub Apps 에서 확인).
- 조직의 Owner는 항상 두 명 이상(교수님과 담당 학생)으로 둡니다. 담당 학생은 졸업하기 전에 후임을 Owner로 올린 뒤 조직에서 나갑니다.

고치는 순서:

1. <https://app.pagescms.org> 에 GitHub 계정으로 로그인하고 이 저장소를 엽니다.
2. 왼쪽에서 **소식 / 구성원 / 과제 / 논문·특허** 중 하나를 고릅니다.
3. 항목을 더하거나 고치고 저장합니다. 사진은 입력 화면에서 바로 올립니다.
4. 1~2분 뒤 홈페이지에 반영됩니다. 열어 둔 화면은 새로 고치면 바뀐 목록이 보입니다.

새 항목을 더하는 단추(Add an entry)는 목록 맨 아래에 있습니다(End 키를 누르면 바로 내려갑니다). 새 항목은 목록 맨 아래에 생기지만, 홈페이지에서는 소식은 날짜 순, 논문은 연도 순으로 다시 놓입니다.

알아 둘 것:

- **사진 크기**: 올리기 전에 긴 변을 2560px 이하로 줄입니다. 휴대폰 원본(장당 수 MB)을 그대로 올리면 저장소가 금방 무거워지고 소식 화면이 느려집니다. 휴대폰 사진에는 찍은 위치가 들어 있을 수 있으니, 크기를 줄여 새로 저장한 파일을 올립니다.
- **목록용 작은 사진**: 소식 목록은 `media/thumb/` 에 있는 작은 사진을 먼저 보여 주고, 카드를 열면 원래 사진으로 바꿉니다. 사진을 새로 올린 뒤 PC에서 `python tools/make_thumbs.py` 를 돌려 함께 올리면 목록이 가벼워집니다. 돌리지 않아도 원래 사진이 대신 나오므로 고장 나지는 않습니다.
- **영상**: 소식에는 mp4(H.264) 영상도 넣을 수 있습니다. 사진 뒤에 차례로 보입니다. 아이폰의 "고효율(HEVC)" 영상은 일부 브라우저에서 나오지 않으므로 H.264로 바꿔서 올립니다.
- **신분이 드러나는 번호**: 상장이나 확인서를 올릴 때는 학번, 연구자번호, 주민번호 같은 번호를 가린 뒤에 올립니다.
- **과제의 진행 여부**는 종료 연월로 자동 분류됩니다. 연월은 `2026.03` 형식으로 적습니다.
- **논문의 굵은 이름**은 구성원 목록의 이름·영문 이름과 같은 저자에게 자동으로 붙습니다. 졸업생도 구성원 목록(구분: 졸업생)에 남겨 두어야 굵게 나옵니다.
- **구성원이 졸업하면** 구분을 "졸업생"으로, 직함을 "졸업생 · 석사"처럼 바꿉니다.
- **논문의 저자 표시**: 제1저자 앞에 ¹, 교신저자 앞에 * 를 붙입니다(예: `¹홍길동, *장승진`). 링크 칸에는 DOI 주소나 DBpia 주소를 넣습니다.

Pages CMS를 쓸 수 없을 때는 GitHub 웹에서 `data/*.json` 을 직접 고쳐도 됩니다. 파일은 `{ "items": [ … ] }` 모양이고, 항목은 `items` 안에 차례로 들어 있습니다. 쉼표나 따옴표가 하나라도 틀리면 해당 화면의 목록이 통째로 안 나오므로, 고친 뒤 화면을 꼭 확인합니다.

## 그 밖의 글을 고치는 방법

| 고칠 것 | 파일 |
|---|---|
| 첫 화면, 연구 소개, 교수 소개, 문의·오시는 길의 글 | `index.html`, `research.html`, `members.html`, `contact.html` |
| 상단 메뉴, 하단 정보(주소·전화·메일) | `js/site.js` 의 "2. 상단 메뉴와 하단 정보" |
| 색, 글자 크기 등 디자인 값 | `css/tokens.css` |

글은 한국어와 영어가 나란히 들어 있습니다. `lang="ko"` 와 `lang="en"` 이 붙은 조각이 짝입니다(대부분 `<span>`, 교수 소개의 목록은 `<ul>`). 두 쪽을 함께 고칩니다.

## 폴더 구조

```
index.html, research.html, members.html, projects.html, publications.html, news.html, contact.html
404.html  없는 주소로 들어온 사람에게 보이는 안내 화면
css/      tokens.css(디자인 토큰) · bundle.css(디자인 시스템 컴포넌트) · site.css(이 사이트에서 더한 것)
js/       site.js (언어 전환, 메뉴, 카드, 목록 그리기, 첫 화면 효과)
data/     news.json · members.json · projects.json · publications.json
media/    사진, 로고, 영상, 첫 화면 그림
          news/(소식 사진·영상) · thumb/(목록용 작은 사진) · people/ · logos/ · research/ · video/
          logo-white.svg(상단 로고) · hero.jpg, hero-lit.jpg(첫 화면) · og.jpg(링크 미리보기)
.pages.yml   Pages CMS 입력 화면 설정
_config.yml  홈페이지 주소로 열리지 않게 할 파일 목록(이 README, tools/). 저장소에는 그대로 있다
tools/    make_thumbs.py(목록용 작은 사진 만들기) · gen_art.py(첫 화면 그림 다시 그리기). 사이트 동작에는 필요 없음
```

`README.md`, `tools/`, `.pages.yml`, `_config.yml` 은 저장소에서만 보이고 홈페이지 주소로는 열리지 않습니다. 이름이 밑줄(`_`)로 시작하는 파일이나 폴더도 공개되지 않으니, 사진이나 폴더 이름을 밑줄로 시작하지 않습니다.

## 내 PC에서 미리 보기

`data/*.json` 을 읽어 오기 때문에 파일을 더블클릭해서는 목록이 나오지 않습니다. 이 폴더에서 아래 명령을 실행하고 <http://localhost:8000> 을 엽니다.

```bash
python -m http.server 8000
```

## PC에서 고쳐서 올리기

새 PC에서는 먼저 [Git](https://git-scm.com)을 설치하고 저장소를 받아 옵니다(한 번만). 처음 `git push` 할 때 GitHub 로그인 창이 뜹니다.

```bash
git clone https://github.com/ESPDlab/espdlab.github.io.git
cd espdlab.github.io
```

화면의 글이나 디자인을 고칠 때의 순서입니다. Pages CMS에서 저장한 내용은 PC에 없으므로 항상 `git pull` 부터 합니다.

```bash
git pull
# 파일을 고치고, 위의 방법으로 미리 본다
git add .
git commit -m "무엇을 고쳤는지 한 줄"
git push
```

`git push` 가 거절되면 `git pull --rebase` 를 한 뒤 다시 `git push` 합니다. 1~2분 뒤 홈페이지에 반영됩니다. 잘못 올렸으면 `git log --oneline -5` 로 커밋을 찾아 `git revert --no-edit <커밋 앞 일곱 글자>` 로 되돌리고 `git push` 합니다.

## 배포

- GitHub 저장소 → Settings → Pages → "Deploy from a branch", `main` 브랜치의 `/ (root)`.
- `main` 에 올라간 내용이 곧 홈페이지입니다. 별도의 빌드나 Actions 설정은 없습니다.
- 저장소 이름이 `espdlab.github.io` 라서 사이트가 주소의 맨 위(`/`)에 놓입니다. 저장소 이름을 바꾸면 주소도 바뀝니다.

## 학교 주소(energypd.cau.ac.kr) 연결

순서를 지킵니다. GitHub에 먼저 적고, 학교 DNS를 나중에 바꿉니다. 다만 1번을 저장하는 순간부터 `espdlab.github.io` 는 `energypd.cau.ac.kr` 로 넘겨지고, 학교가 2번을 마칠 때까지 그 주소에는 예전 사이트가 나옵니다. 그 사이에는 새 홈페이지를 어느 주소로도 볼 수 없으므로, DNS 담당 부서와 바꿀 날짜를 먼저 정하고 1번은 그날 DNS를 바꾸기 직전에 합니다.

1. 저장소 Settings → Pages → Custom domain 에 `energypd.cau.ac.kr` 을 적고 Save. GitHub가 저장소에 `CNAME` 파일을 커밋합니다(PC에서는 `git pull` 로 받습니다).
2. 학교 DNS 담당 부서에 `energypd.cau.ac.kr` 의 CNAME 레코드를 `espdlab.github.io` 로 바꿔 달라고 요청합니다.
3. 같은 화면에 "DNS check successful" 이 뜨고 인증서가 나오면(최대 24시간) Enforce HTTPS 를 켭니다.

주소를 다른 것으로 바꿀 때도 같습니다. 1번 칸에 새 주소를 적고, 그 주소의 CNAME을 `espdlab.github.io` 로 맞춥니다. 사이트를 내릴 때는 학교에 이 CNAME 레코드도 지워 달라고 요청합니다. 남겨 두면 다른 사람이 이 주소로 사이트를 열 수 있습니다.

링크 미리보기 그림의 주소(HTML 일곱 개의 `og:image`)에는 `espdlab.github.io` 가 적혀 있습니다. 학교 주소를 연결한 뒤에도 GitHub가 새 주소로 넘겨 주므로 그대로 둡니다.

## 첫 화면의 전력망 그림

`media/hero.jpg`(평소)와 `media/hero-lit.jpg`(전력망이 밝게 켜진 상태) 두 장입니다. 화면에서는 포인터 둘레만 밝은 그림이 드러나고, 포인터가 쉬면 불빛이 한반도 위를 천천히 돕니다(`js/site.js` 의 `glow`).

다시 그리려면 Python과 Pillow가 필요합니다.

1. `tools/overpass-lines.txt`(남한 송전선), `tools/overpass-points.txt`(변전소·발전소)의 질의를 <https://overpass-turbo.eu> 또는 Overpass API로 실행해 `lines_kr.json`, `points.json` 으로 저장합니다. 북한 송전선은 첫 질의의 `KR` 을 `KP` 로 바꿔 `lines_kp.json` 으로 저장합니다.
2. Natural Earth의 `ne_10m_admin_0_countries.geojson` 을 받습니다.
3. `python tools/gen_art.py media herosite <1의 폴더> <2의 파일>`

링크 미리보기 그림 `media/og.jpg` 는 `media/hero-lit.jpg` 에서 한반도 둘레를 잘라 1200×630으로 줄이고 오른쪽 아래에 출처를 써 넣은 것입니다. 첫 화면 그림을 다시 그리면 이 그림도 같은 방법으로 다시 만듭니다.

## 출처와 사용 조건

- 전력망 자료(송전선, 변전소, 발전소): © OpenStreetMap contributors, ODbL. 첫 화면 오른쪽 아래의 출처 표기를 지우면 안 됩니다.
- 해안선: Natural Earth (퍼블릭 도메인).
- 디자인: "연구실 홈페이지" 디자인 시스템의 토큰과 컴포넌트(`css/tokens.css`, `css/bundle.css`).

## 남은 일 (2026년 11월 기준)

- 학교 주소 `energypd.cau.ac.kr` 은 아직 예전 Wix 사이트를 가리킵니다. 위의 "학교 주소 연결"을 마치면 Wix 요금제를 해지합니다.
- 연구 소개의 카드 두 개(동적 송전 용량, AI 시계열 예측)에 소개 글이 없습니다. `research.html` 에 글이 들어갈 자리를 주석으로 표시해 두었습니다.
- 학부 연구생 한 명의 관심 분야가 비어 있습니다.
- 2026년 11월에 한꺼번에 추가한 논문 42편(국내 학술대회 33편 등)에는 제1저자·교신저자 표시가 없습니다.
- 조직의 Owner가 아직 한 명입니다. 교수님 계정을 Owner로 초대해야 합니다.

## 알려진 한계

- 소식·구성원·과제·논문 목록은 브라우저에서 그려집니다. 검색 엔진이 목록 내용까지 읽어 가지 못할 수 있습니다. 문제가 되면 목록을 HTML에 미리 써 넣는 빌드 단계를 더합니다.
- 첫 화면 그림은 2026년 11월에 받은 자료로 그린 정지 그림 두 장입니다. 전력망이 바뀌어도 자동으로 갱신되지 않습니다.
