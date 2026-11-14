/* ESPD Lab 홈페이지 공통 스크립트. 빌드 과정이 없으므로 이 파일을 그대로 올린다.
   1. 언어 전환   2. 상단 메뉴와 하단 정보   3. 눌러서 펼치는 카드, 사진 넘기기
   4. data/*.json 을 읽어 소식·과제·논문·구성원 목록 그리기   5. 첫 화면 영상과 전력망 불빛
   글과 사진은 이 파일이 아니라 data/ 와 media/ 에서 고친다(README.md 참고). */
(() => {
  'use strict';
  const root = document.documentElement;

  /* ── 1. 언어 ── */
  const lang = () => root.dataset.lang;
  let rerender = () => {};            // 목록이 있는 화면이 자기 그리기 함수를 여기에 건다
  function setLang(v) {
    root.dataset.lang = root.lang = v;
    try { localStorage.setItem('espd-lang', v); } catch (e) {}
    rerender();
  }
  try { if (localStorage.getItem('espd-lang') === 'en') root.dataset.lang = root.lang = 'en'; } catch (e) {}

  /* ── 2. 상단 메뉴와 하단 정보: MENU를 고치면 모든 화면의 상단 메뉴와 휴대폰 메뉴가 바뀐다. 하단의 링크 목록은 아래 site-footer 에 따로 적혀 있으니 함께 고친다 ── */
  const MENU = [['research.html', 'Research'], ['members.html', 'Research Team'], ['projects.html', 'Projects'], ['news.html', 'News &amp; Gallery'], ['publications.html', 'Publication'], ['contact.html', 'Contact']];
  const t = (ko, en) => `<span lang="ko">${ko}</span><span lang="en">${en}</span>`;
  const links = (cls) => MENU.map(([href, label]) => `<a${cls} href="${href}">${label}</a>`);
  const define = (tag, html) => customElements.define(tag, class extends HTMLElement { connectedCallback() { this.innerHTML = html; } });

  define('site-header', `
<header class="lab-gnav" data-surface="black">
<nav class="lab-gnav-inner nav-link" aria-label="Main">
<a href="index.html"><img class="site-logo" src="media/logo-white.svg" alt="ESPD Lab"></a>
<ul class="lab-gnav-links">${links('').map((a) => `<li>${a}</li>`).join('')}</ul>
<div class="lab-gnav-actions">
<button class="lab-btn lab-btn-utility button-utility" type="button" data-act="lang"><span class="only-ko">English</span><span class="only-en">한국어</span></button>
<button class="lab-gnav-icon lab-gnav-menu" type="button" aria-label="Menu" aria-expanded="false" data-act="menu"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="M2 5h12M2 11h12"></path></svg></button>
</div>
</nav>
</header>
<nav class="site-menu" data-surface="black" aria-label="Menu" hidden>${links(' class="body"').join('')}</nav>`);

  define('site-footer', `
<footer class="lab-footer">
<div class="lab-footer-inner">
<div class="lab-footer-cols">
<div>
<h4 class="caption-strong">Research</h4>
<ul class="dense-link">
<li><a href="research.html">Research</a></li>
<li><a href="projects.html">Projects</a></li>
<li><a href="publications.html">Publication</a></li>
</ul>
</div>
<div>
<h4 class="caption-strong">Lab</h4>
<ul class="dense-link">
<li><a href="members.html">Research Team</a></li>
<li><a href="news.html">News &amp; Gallery</a></li>
<li><a href="contact.html">Contact</a></li>
</ul>
</div>
<div>
<h4 class="caption-strong">Contact</h4>
<ul class="dense-link">
<li><a href="mailto:jpromo8@cau.ac.kr">jpromo8@cau.ac.kr</a></li>
<li><a href="tel:+8228205233">02-820-5233</a></li>
<li><a href="https://www.youtube.com/@EnergySystemPDLab">YouTube</a></li>
</ul>
</div>
</div>
<div class="lab-footer-legal fine-print">
<p>© ${new Date().getFullYear()} Energy System Prognostics &amp; Diagnostics Lab</p>
<p>${t('중앙대학교 에너지시스템공학부', 'School of Energy Systems Engineering, Chung-Ang University')}</p>
<p>${t('서울특별시 동작구 흑석로 84, 중앙대학교 교수연구동(305관) 603호', '603, 305, 84 Heukseok-ro, Dongjak-gu, Seoul, South Korea')}</p>
</div>
</div>
</footer>`);

  /* ── 3. 누르는 것들: 언어, 메뉴, 거르기 버튼, 카드, 사진 넘기기 ── */
  const state = {};                   // 거르기 버튼이 고른 값. 예: { cat: 'award' }

  // 카드(<dialog>)를 그 자리에서 떼어 화면 가운데 시트로 띄운다. 닫히면 아래 close 처리에서 제자리로 돌아간다.
  function openCard(d) {
    if (d.matches(':modal')) return;
    d.close();
    d.showModal();
    d.querySelectorAll('img[data-full]').forEach((i) => { if (i.getAttribute('src') !== i.dataset.full) i.src = i.dataset.full; });   // 열면 작은 사진을 큰 사진으로 바꾼다
    d.scrollTop = 0;
    const strip = d.querySelector('.strip');
    if (strip) strip.scrollLeft = 0;
  }

  // 시트 안에서 글을 긁다가 바깥에서 손을 떼도 닫히지 않게, 누르기 시작한 곳이 바깥이었는지 적어 둔다.
  let downOutside = false;
  document.addEventListener('pointerdown', (e) => { downOutside = !!e.target.matches && e.target.matches('dialog.xcard:modal'); }, true);

  document.addEventListener('click', (e) => {
    const el = e.target.closest('[data-act], .lab-chip[data-key], .stretch, .xclose, .carousel .nav, dialog.xcard');
    if (!el) return;
    if (el.dataset.act === 'lang') return setLang(lang() === 'ko' ? 'en' : 'ko');
    if (el.dataset.act === 'menu') {
      const menu = document.querySelector('.site-menu');
      menu.hidden = !menu.hidden;
      return el.setAttribute('aria-expanded', !menu.hidden);
    }
    if (el.matches('.lab-chip')) {
      state[el.dataset.key] = el.dataset.val;
      document.querySelectorAll(`.lab-chip[data-key="${el.dataset.key}"]`).forEach((b) => b.setAttribute('aria-pressed', b === el));
      return rerender();
    }
    const d = el.closest('dialog.xcard');
    if (!d) return;
    if (el.matches('.stretch')) openCard(d);
    else if (el.matches('.xclose')) d.close();
    else if (el.matches('.nav')) {     // 사진 띠를 한 장만큼 옆으로 민다
      const strip = el.parentElement.querySelector('.strip');
      strip.scrollBy({ left: (el.matches('.prev') ? -1 : 1) * strip.clientWidth, behavior: 'smooth' });
    } else if (!d.matches(':modal')) {
      if (e.target.closest('.carousel')) openCard(d);     // 닫힌 카드의 사진을 눌러도 열린다(사진은 넘길 수 있게 덮개 위에 있어서 따로 받는다)
    } else if (e.target === d && downOutside) {           // 시트 바깥(어두운 부분)을 누르면 닫는다
      const r = d.getBoundingClientRect();
      if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) d.close();
    }
  });

  // close 이벤트는 위로 올라오지 않으므로 캡처 단계에서 받는다.
  document.addEventListener('close', (e) => {
    const d = e.target;
    if (!d.matches || !d.matches('dialog.xcard') || d.matches(':modal')) return;   // 띄우려고 잠깐 닫은 것이면 그대로 둔다
    d.open = true;                    // show() 를 부르면 포커스가 카드 안으로 옮겨 간다. 속성만 켜서, 카드를 열었던 단추로 포커스가 돌아가게 둔다.
    const strip = d.querySelector('.strip');
    if (strip) strip.scrollLeft = 0;
    d.querySelectorAll('video').forEach((v) => v.pause());
  }, true);

  /* ── 4. 목록 화면 ── */
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const src = (p) => esc(String(p || '').replace(/^\//, ''));      // "/media/a.jpg" 와 "media/a.jpg" 를 모두 받는다
  // 목록에서는 작은 사진(media/thumb/… 에 같은 이름 + ".jpg")을 먼저 보여 준다. 작은 사진이 없으면 원래 사진이 대신 나온다.
  // 작은 사진은 tools/make_thumbs.py 로 만든다.
  const thumb = (p) => esc('media/thumb/' + String(p || '').replace(/^\/?media\//, '') + '.jpg');
  // data/*.json 은 { "items": [ … ] } 모양이다(Pages CMS가 항목 제목을 보여 주려면 목록이 칸 하나에 담겨야 한다).
  // cache: 'no-cache' = 열 때마다 서버에 새 내용이 있는지 묻는다. 없으면 브라우저가 10분 동안 예전 목록을 보여 준다.
  const load = (name) => fetch('data/' + name + '.json', { cache: 'no-cache' }).then((r) => { if (!r.ok) throw new Error(name + '.json ' + r.status); return r.json(); }).then((j) => (Array.isArray(j) ? j : j.items || []));
  const fill = (fn) => document.querySelectorAll('[data-n]').forEach((el) => { el.textContent = fn(el.dataset.n); });
  const CLOSE = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8"></path></svg>';
  const PI = ['Seung Jin Chang', '장승진'];   // 교수님 이름(논문 목록에서 굵게 표시). 나머지 구성원은 members.json 에서 읽는다.

  // 소식: data/news.json
  async function initNews(grid) {
    const items = (await load('news')).slice().sort((a, b) => String(b.date).localeCompare(String(a.date)));
    grid.innerHTML = items.map((n) => {
      const photos = n.photos || [];
      const videos = n.videos || [];          // 영상(mp4)은 사진 뒤에 차례로 놓인다
      const many = photos.length + videos.length > 1;
      return `<article class="cell" data-c="${esc(n.category)}">
<dialog open class="lab-card lift xcard" aria-label="${esc(n.title)}">
<button class="lab-btn lab-btn-icon xclose when-open" type="button" aria-label="Close"></button>
${photos.length || videos.length ? `<div class="carousel${many ? '' : ' single'} above"><div class="strip">${photos.map((p) => `<img src="${thumb(p)}" data-full="${src(p)}" alt="" loading="lazy" decoding="async" onerror="this.onerror=null;this.src=this.dataset.full">`).join('')}${videos.map((v) => `<video src="${src(v)}#t=0.1" controls playsinline preload="metadata"></video>`).join('')}</div>${many ? '<button class="lab-btn lab-btn-icon nav prev" type="button" aria-label="Previous photo"></button><button class="lab-btn lab-btn-icon nav next" type="button" aria-label="Next photo"></button>' : ''}</div>` : ''}
<h3 class="body-strong clamp2" style="margin-top: var(--space-md); min-height: 42px"><button class="stretch" type="button">${esc(n.title)}</button></h3>
<p class="lab-card-meta caption lab-muted">${esc(String(n.date).replace(/-/g, '. '))}${photos.length > 1 ? t(` · 사진 ${photos.length}장`, ` · ${photos.length} photos`) : ''}${videos.length ? t(` · 영상 ${videos.length}개`, ` · ${videos.length} video${videos.length > 1 ? 's' : ''}`) : ''}</p>
${n.body ? `<p class="body when-open" style="margin-top: var(--space-sm); white-space: pre-line">${esc(n.body)}</p>` : ''}
</dialog>
</article>`;
    }).join('');
    fill((c) => items.filter((n) => c === 'all' || n.category === c).length);
    rerender = () => grid.querySelectorAll('[data-c]').forEach((el) => { el.hidden = !!state.cat && state.cat !== 'all' && el.dataset.c !== state.cat; });
    rerender();                       // 목록이 오기 전에 누른 거르기 버튼도 반영한다
  }

  // 과제: data/projects.json. 종료 연월이 이번 달 이후면 "진행 중", 지났거나 비어 있으면 "완료"로 자동 분류한다.
  async function initProjects(box) {
    const now = new Date();
    const thisMonth = now.getFullYear() + '.' + String(now.getMonth() + 1).padStart(2, '0');
    const all = (await load('projects')).slice().sort((a, b) => (b.start || '0').localeCompare(a.start || '0'));   // 시작이 늦은 것부터, 기간이 없으면 맨 뒤
    const on = all.filter((p) => p.end && p.end >= thisMonth);
    const done = all.filter((p) => on.indexOf(p) === -1);
    fill((k) => ({ all: all.length, on: on.length, done: done.length })[k]);
    const card = (live) => (p) => `<article class="lab-card lift" style="display: flex; flex-direction: column">
<p class="caption-strong${live ? '' : ' lab-muted'}" style="margin: 0${live ? '; color: var(--primary)' : ''}">${[p.start, p.end].filter(Boolean).map(esc).join(' – ') || '—'}</p>
<h3 class="body-strong clamp4" style="margin: var(--space-xs) 0 0; min-height: 84px">${esc(p.title)}</h3>
<p class="caption lab-muted clamp2" style="margin: var(--space-xs) 0 0; min-height: 40px">${esc(p.program ? p.org + ' · ' + p.program : p.org)}</p>
${p.logo ? `<img class="plogo-img" src="${src(p.logo)}" alt="" loading="lazy">` : `<div class="tagline lab-muted" aria-hidden="true" style="height: 120px; margin: var(--space-sm) 0; display: grid; place-items: center">${esc(p.abbr)}</div>`}
<p class="body-strong" style="margin: auto 0 0; min-height: 21px">${esc(p.amount)}</p>
</article>`;
    const block = (list, live, ko, en) => list.length ? `<h2 class="display-md" style="max-width: var(--content-grid); margin: var(--space-xl) auto 0; padding: 0 var(--space-lg)">${t(ko, en)} <span style="color: var(--ink-muted-48)">${list.length}</span></h2>
<div class="lab-grid eq" style="grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); padding-top: var(--space-sm)">${list.map(card(live)).join('')}</div>` : '';
    rerender = () => {
      const f = state.status || 'all';
      box.innerHTML = (f !== 'done' ? block(on, true, '진행 중인 과제', 'Ongoing Projects') : '') + (f !== 'on' ? block(done, false, '완료한 과제', 'Past Projects') : '');
    };
    rerender();
  }

  // 논문: data/publications.json. 검색, 국내외·종류 거르기, 연도별 막대.
  async function initPubs(list) {
    const [all, members] = await Promise.all([load('publications'), load('members').catch(() => [])]);   // 구성원 파일이 깨져도 논문 목록은 나온다(이름만 굵게 안 된다)
    const key = (n) => String(n).replace(/[¹*\s-]/g, '').toLowerCase();          // 이름 견주기: 기호, 띄어쓰기, 붙임표 무시
    const lab = new Set(PI.concat(...members.map((m) => [m.name, m.nameEn])).filter(Boolean).map(key));
    const norm = (s) => String(s).toLowerCase().replace(/[\s\-¹*]/g, '');
    const KIND = { journal: ['저널', 'Journal'], conf: ['학회', 'Conference'], patent: ['특허', 'Patent'] };
    const years = all.map((p) => +p.year).filter(Boolean);
    const y0 = Math.min(...years), y1 = Math.max(...years);
    const $ = (id) => document.getElementById(id);
    const input = $('pub-q'), chart = $('pub-chart');
    input.addEventListener('input', () => rerender());
    chart.addEventListener('click', (e) => {
      const b = e.target.closest('[data-year]');
      if (!b) return;
      state.year = state.year === +b.dataset.year ? 0 : +b.dataset.year;
      rerender();
    });
    $('pub-clear').addEventListener('click', () => { state.year = 0; rerender(); });
    fill((k) => all.filter((p) => p.region === k || p.kind === k).length);
    rerender = () => {
      const en = lang() === 'en';
      const region = state.region || 'all', kind = state.kind || 'all', year = state.year || 0;
      const needle = norm(input.value);
      // 연도를 뺀 조건으로 먼저 거르고(막대가 이 수를 센다), 그다음 연도로 거른다.
      const base = all.filter((p) => (region === 'all' || p.region === region) && (kind === 'all' || p.kind === kind)
        && (!needle || norm([p.title, p.venue, p.when, p.authors].join(' ')).indexOf(needle) !== -1));
      const shown = base.filter((p) => !year || +p.year === year).sort((a, b) => b.year - a.year);
      const counts = {};
      base.forEach((p) => { counts[p.year] = (counts[p.year] || 0) + 1; });
      const peak = Math.max(1, ...Object.keys(counts).map((k) => counts[k]));
      const focused = document.activeElement && document.activeElement.dataset.year;
      let bars = '';
      for (let y = y0; y <= y1; y++) {
        const n = counts[y] || 0, on = year === y, tip = en ? y + ': ' + n : y + '년 ' + n + '건';
        bars += `<button class="ybar" type="button" title="${tip}" aria-label="${tip}" aria-pressed="${on}" data-year="${y}"><span style="height: ${n ? Math.max(6, Math.round(140 * n / peak)) : 2}px; opacity: ${!year || on ? 1 : 0.3}"></span><span class="caption" style="color: ${on ? 'var(--ink)' : 'var(--ink-muted-80)'}; font-weight: ${on ? 600 : 400}"><span class="yl-full">${y}</span><span class="yl-short">'${String(y).slice(2)}</span></span></button>`;
      }
      chart.innerHTML = bars;
      if (focused) { const b = chart.querySelector(`[data-year="${focused}"]`); if (b) b.focus(); }
      input.placeholder = en ? 'Search by title, author or venue' : '제목, 저자, 학술지로 찾기';
      $('pub-chart-label').innerHTML = year ? t(year + '년 실적', 'In ' + year) : t(y0 + '–' + y1 + ' 연도별 실적', y0 + '–' + y1 + ', by year');
      $('pub-chart-value').innerHTML = shown.length + t('건', '');
      $('pub-clear').hidden = !year;
      $('pub-result').innerHTML = t(shown.length + '건 표시', shown.length + ' shown');
      $('pub-empty').hidden = shown.length > 0;
      list.innerHTML = shown.map((p) => `<article class="lab-card lift" style="display: flex; flex-direction: column">
<h3 class="body-strong" style="margin: 0">${p.url ? `<a class="lab-link" href="${esc(p.url)}" style="display: inline; margin: 0">${esc(p.title)}</a>` : `<span>${esc(p.title)}</span>`}</h3>
<p class="lab-card-meta body" style="margin: var(--space-xs) 0 0">${esc(p.venue)}</p>
<p class="caption lab-muted" style="margin: var(--space-xxs) 0 0">${[t(...(KIND[p.kind] || [p.kind, p.kind])), esc(p.when), p.jcr && t('JCR 상위 ', 'JCR top ') + esc(p.jcr)].filter(Boolean).join(' · ')}</p>
<p class="caption lab-muted" style="margin: auto 0 0; padding-top: var(--space-sm)">${String(p.authors).split(', ').map((n) => lab.has(key(n)) ? `<span style="font-weight: 600; color: var(--ink)">${esc(n)}</span>` : esc(n)).join(', ')}</p>
</article>`).join('');
    };
    rerender();
  }

  // 구성원: data/members.json. 경력·논문·과제·수상 중 하나라도 적혀 있으면 눌러서 펼치는 카드가 된다.
  async function initMembers(box) {
    const GROUPS = [['postdoc', '박사후연구원', 'Post Doctoral'], ['phd', '박사과정', 'Ph.D. Students'], ['ms', '석사과정', 'M.S. Students'], ['undergrad', '학부 연구생', 'Undergraduate Students'], ['alumni', '졸업생', 'Alumni']];
    const LISTS = [['career', '경력', 'Career'], ['publications', '논문', 'Publications'], ['projects', '수행 과제', 'Projects'], ['awards', '수상 이력', 'Awards']];
    const bold = (s, names) => names.filter(Boolean).reduce((h, n) => h.split(esc(n)).join('<strong>' + esc(n) + '</strong>'), esc(s));   // 본인 이름을 굵게
    const all = await load('members');
    const card = (m) => {
      const lists = LISTS.filter(([k]) => (m[k] || []).length);
      const head = `<div style="display: flex; gap: var(--space-lg); align-items: flex-start">
${m.photo ? `<img src="${src(m.photo)}" alt="" loading="lazy" style="flex: none; width: 120px; aspect-ratio: 3 / 4; object-fit: cover; object-position: top; border-radius: var(--rounded-sm)">` : ''}
<div style="min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: var(--space-xxs)">
<p class="caption lab-muted" style="margin: 0">${t(esc(m.roleKo), esc(m.roleEn || m.roleKo))}</p>
<h3 class="tagline" style="margin: 0">${esc(m.name)}</h3>
<p class="caption" style="margin: 0">${esc(m.nameEn)}</p>
<p class="caption lab-muted clamp3" style="margin: var(--space-xs) 0 0; min-height: 60px">${m.interests ? t('관심 분야', 'Interests') + ': ' + esc(m.interests) : t(esc(m.noteKo), esc(m.noteEn || m.noteKo))}</p>
${m.email ? `<a class="lab-link caption above" href="mailto:${esc(m.email)}" style="margin: 0; padding: var(--space-xs) 0">${esc(m.email)}</a>` : ''}
${lists.length ? `<button class="stretch when-closed" type="button"><span class="lab-link caption">${t('경력 및 연구실적', 'Career &amp; achievements')}</span></button>` : ''}
</div>
</div>`;
      if (!lists.length) return `<article class="lab-card lift">${head}</article>`;
      return `<article class="cell">
<dialog open class="lab-card lift xcard" aria-label="${esc(m.name)}">
<button class="lab-btn lab-btn-icon xclose when-open" type="button" aria-label="Close">${CLOSE}</button>
${head}
<div class="when-open" style="margin-top: var(--space-xl); display: flex; flex-direction: column; gap: var(--space-xl)">
${lists.map(([k, ko, en]) => `<section>
<h4 class="body-strong" style="margin: 0 0 var(--space-xs)">${t(ko, en)}</h4>
<ul class="caption" style="margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: var(--space-xxs)">${m[k].map((s) => `<li>${k === 'publications' ? bold(s, [m.nameEn, m.name]) : esc(s)}</li>`).join('')}</ul>
</section>`).join('')}
</div>
</dialog>
</article>`;
    };
    box.innerHTML = GROUPS.map(([id, ko, en]) => {
      const group = all.filter((m) => m.group === id);
      return group.length ? `<section style="display: flex; flex-wrap: wrap; gap: var(--space-lg)">
<h2 class="tagline" style="margin: 0; flex: 0 0 200px">${t(ko, en)}</h2>
<div style="flex: 999 1 420px; min-width: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 400px), 1fr)); gap: var(--space-lg)">${group.map(card).join('')}</div>
</section>` : '';
    }).join('');
  }

  /* ── 5. 첫 화면 ── */
  const still = !!window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;   // 움직임 줄이기를 켠 사람

  // 영상: 화면에 들어오면 소리 없이 재생하고, 화면 밖으로 나가면 멈춘다.
  function autoplay(v) {
    if (still || !window.IntersectionObserver) return;
    v.muted = true;
    v.loop = true;
    new IntersectionObserver(([e]) => {
      if (!e.isIntersecting) return v.pause();
      const p = v.play();
      if (p && p.catch) p.catch(() => {});
    }, { threshold: 0.3 }).observe(v);
  }

  // 전력망 불빛: 밝게 그린 그림을 동그란 창(.hero-glow)으로만 드러낸다. 포인터가 쉬면 불빛이 한반도 위를 천천히 돈다.
  // 창은 한쪽으로, 창 안의 그림은 그 반대쪽으로 같은 만큼 옮긴다(transform). 그러면 그림은 제자리에 있고 창만 움직이는 것처럼 보인다.
  // transform 만 바꾸므로 브라우저가 매번 다시 그리지 않아 가볍다.
  function glow(win) {
    const stage = win.parentElement, lit = win.firstElementChild;
    let W = 1, H = 1, r = 0, x = 0.7, y = 0.5;
    const place = () => {
      const cx = Math.round(x * W), cy = Math.round(y * H);
      win.style.transform = `translate3d(${cx}px,${cy}px,0)`;
      lit.style.transform = `translate3d(${r - cx}px,${r - cy}px,0)`;
    };
    const size = () => {
      W = stage.clientWidth; H = stage.clientHeight; r = win.offsetWidth / 2;
      lit.style.width = W + 'px'; lit.style.height = H + 'px';
      place();
    };
    size();
    window.addEventListener('resize', size);
    win.classList.add('on');
    if (still || !window.IntersectionObserver) return;       // 움직임 줄이기를 켠 사람에게는 불빛이 한자리에 머문다
    let tx = x, ty = y, moved = -1e9, seen = false, raf = 0;
    stage.parentElement.addEventListener('pointermove', (e) => {
      const b = stage.getBoundingClientRect();
      tx = (e.clientX - b.left) / b.width;
      ty = (e.clientY - b.top) / b.height;
      moved = performance.now();
    });
    const tick = (now) => {
      if (now - moved > 2500) {        // 한반도 위치를 그림 비율로 적어 둔 값. 그림 구도를 바꾸면 이 숫자도 바꾼다.
        tx = 0.7 + 0.08 * Math.cos(now / 3600);
        ty = 0.55 + 0.27 * Math.sin(now / 5200);
      }
      x += (tx - x) * 0.08;
      y += (ty - y) * 0.08;
      place();
      raf = seen ? requestAnimationFrame(tick) : 0;
    };
    new IntersectionObserver(([e]) => {
      seen = e.isIntersecting;
      if (seen && !raf) raf = requestAnimationFrame(tick);
    }).observe(stage);
  }

  document.addEventListener('DOMContentLoaded', () => {
    const pages = { 'news-list': initNews, 'project-list': initProjects, 'pub-list': initPubs, 'member-list': initMembers };
    Object.keys(pages).forEach((id) => {
      const el = document.getElementById(id);
      if (el) pages[id](el).catch((err) => {
        console.error(err);
        el.innerHTML = `<p class="body lab-muted" style="grid-column: 1 / -1; margin: 0; padding: var(--space-lg); text-align: center">${t('내용을 불러오지 못했습니다.', 'Could not load the content.')}</p>`;
      });
    });
    document.querySelectorAll('video[data-autoplay]').forEach(autoplay);
    document.querySelectorAll('.hero-glow').forEach(glow);
  });
})();
