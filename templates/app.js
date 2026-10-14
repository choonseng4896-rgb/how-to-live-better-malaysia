// Text and URLs from contribution files are escaped before insertion into HTML.
const $ = id => document.getElementById(id);
const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const normalize = text => String(text).normalize('NFKC').toLowerCase().replace(/my\s*50/g, 'my50').trim();
const keywords = {
  epf: 'epf kwsp 公积金 退休 persaraan',
  pidm: 'pidm 存款保障 存款保险 deposit protection insurans deposit',
  rapid: 'my50 月票 交通 通勤 transport pengangkutan pas bulanan',
  health: '诊所 预约 mysejahtera klinik appointment tempahan',
  diet: '饮食 糖 盐 营养 diet sugar salt gula garam pemakanan',
  activity: '运动 身体活动 锻炼 exercise aktiviti fizikal senaman',
  'bnm-verify': '防诈骗 骗局 bnm bank negara scam penipuan',
  'bnm-app': '防诈骗 骗局 bnm apk otp bank negara scam penipuan'
};
let category = 'all';
let onlySaved = false;
let bookmarks = new Set();
let lastTerms = [];
document.body.classList.remove('no-js');
try {
  const stored = JSON.parse(localStorage.getItem('my-life-saved') || '[]');
  if (Array.isArray(stored)) bookmarks = new Set(stored.filter(id => items.some(i => i.id === id)));
  if (localStorage.getItem('my-life-theme') === 'dark') document.body.classList.add('dark');
} catch {
  $('storage-note').textContent = '浏览器未开放本地存储；收藏仍可在本次页面使用。';
}
function persist(key, value) {
  try { localStorage.setItem(key, value); }
  catch { $('storage-note').textContent = '本地存储不可用；本次收藏不会在关闭页面后保留。'; }
}
function highlight(text) {
  if (!lastTerms.length) return esc(text);
  const pattern = lastTerms.map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).sort((a,b) => b.length-a.length).join('|');
  return String(text).split(new RegExp(`(${pattern})`, 'ig')).map((part,n) => n % 2 ? `<mark>${esc(part)}</mark>` : esc(part)).join('');
}
function termMatches(text, term) {
  // Short Latin acronyms must be words: EPF must not match the middle of "deepfakes".
  return /^[a-z0-9]{1,3}$/.test(term)
    ? new RegExp(`(^|[^a-z0-9])${term}([^a-z0-9]|$)`).test(text)
    : text.includes(term);
}
function rankedMatches(query) {
  const terms = normalize(query).split(/\s+/).filter(Boolean).slice(0,20);
  return items.filter(i => category === 'all' || i.category === category)
    .filter(i => !onlySaved || bookmarks.has(i.id))
    .map(i => {
      const title = normalize(i.title);
      const corpus = normalize([i.title,i.body,i.action,i.scope,i.period,i.region,sources[i.source][0],keywords[i.source] || ''].join(' '));
      const match = terms.every(t => termMatches(corpus,t));
      const score = (title === normalize(query) ? 100 : 0) + terms.reduce((n,t) => n + (title.includes(t) ? 10 : 0),0);
      return {item:i,match,score};
    }).filter(row => row.match).sort((a,b) => b.score-a.score || a.item.id-b.item.id).map(row => row.item);
}
function renderCard(i) {
  const source = sources[i.source];
  const today = new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Kuala_Lumpur',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  const stale = today > i.review_after;
  const group = groups.find(g => g.key === i.category);
  return `<article class="card" id="tip-${i.id}">
    <div class="card-top"><span>#${String(i.id).padStart(2,'0')} · ${esc(group.title)}</span><button class="save" type="button" data-id="${i.id}" aria-pressed="${bookmarks.has(i.id)}" aria-label="${bookmarks.has(i.id) ? '取消收藏' : '收藏'}：${esc(i.title)}">${bookmarks.has(i.id) ? '★' : '☆'}</button></div>
    <h3><a class="permalink" href="#tip-${i.id}">${highlight(i.title)}</a></h3><p>${highlight(i.body)}</p>
    <details style="font-size:12px;margin-bottom:16px"><summary>来源、范围与核验记录</summary><p style="margin-top:8px">支持位置：${esc(i.claim_locator)}<br>适用范围：${esc(i.scope)}<br>资料版本：${esc(i.period)}<br>正文核对：${esc(i.last_verified)} · 建议复核期限：${esc(i.review_after)}<br>审核状态：${esc(i.review_status)}<br>${stale ? '⚠ 已到复核日期，使用前请确认最新规则。' : '尚未到建议复核日期；不保证政策没有变化。'}</p><a href="${esc(source[1])}" target="_blank" rel="noopener noreferrer">${esc(source[0])} ↗</a></details>
    <div class="action"><b>可选动作 · 编辑者建议</b>${highlight(i.action)}</div><div class="card-foot"><span>${esc(i.cost)} · ${esc(i.region)}</span><a class="source-type" href="${esc(source[1])}" target="_blank" rel="noopener noreferrer">一手来源 ↗</a></div></article>`;
}
function syncSearchUrl() {
  // Search states share the canonical reading page; they are not standalone SEO landing pages.
  if (!['http:','https:'].includes(location.protocol)) return;
  const url = new URL(location.href);
  const query = $('search').value.trim();
  if (query) url.searchParams.set('q',query); else url.searchParams.delete('q');
  history.replaceState(null,'',url);
}
function render() {
  const query = $('search').value.trim();
  lastTerms = normalize(query).split(/\s+/).filter(Boolean).slice(0,20);
  document.querySelectorAll('[data-category]').forEach(button => {
    const active = button.dataset.category === category;
    button.classList.toggle('active',active);
    button.setAttribute('aria-pressed',String(active));
  });
  const list = rankedMatches(query);
  const title = category === 'all' ? '全部主题' : groups.find(g => g.key === category).title;
  $('count').textContent = `${title}${onlySaved ? ' · 我的收藏' : ''}${query ? ` · 搜索“${query}”` : ''} · ${list.length} 条内容`;
  $('saved-count').textContent = bookmarks.size;
  $('clear-search').hidden = !query;
  $('clear-filters').hidden = category === 'all' && !onlySaved && !query;
  if (!list.length) {
    $('results').innerHTML = `<div class="empty"><b>没有找到匹配内容</b><p>${onlySaved ? '当前只搜索收藏内容。' : ''}${category !== 'all' ? '当前只搜索所选主题。' : ''}试试更短的关键词，或清除筛选查看全部内容。</p><button class="icon-btn" id="reset">清除全部筛选</button></div>`;
  } else if (query) {
    $('results').innerHTML = `<h2 class="match-heading">搜索结果</h2><div class="cards">${list.map(renderCard).join('')}</div>`;
  } else {
    $('results').innerHTML = groups.map(g => {
      const rows = list.filter(i => i.category === g.key);
      return rows.length ? `<section class="topic" id="topic-${esc(g.key)}"><div class="section-title"><span>${esc(g.number)} /</span><h2>${esc(g.headline)}</h2></div><div class="cards">${rows.map(renderCard).join('')}</div></section>` : '';
    }).join('');
  }
  syncSearchUrl();
}
function showReading() {
  $('reading-start').focus({preventScroll:true});
  $('reading-start').scrollIntoView({behavior:'instant',block:'start'});
}
function clearFilters() {
  category = 'all'; onlySaved = false; $('search').value = '';
  $('saved').setAttribute('aria-pressed','false'); render();
}
$('nav').innerHTML = [{key:'all',number:'↗',title:'全部生活建议'},...groups].map(g => `<button type="button" data-category="${esc(g.key)}" aria-pressed="false"><small>${esc(g.number)}</small>${esc(g.title)}</button>`).join('');
$('nav').addEventListener('click',event => {
  const button = event.target.closest('[data-category]');
  if (button) { category = button.dataset.category; render(); showReading(); }
});
$('results').addEventListener('click',event => {
  const button = event.target.closest('[data-id]');
  if (button) {
    const id = Number(button.dataset.id);
    bookmarks.has(id) ? bookmarks.delete(id) : bookmarks.add(id);
    persist('my-life-saved',JSON.stringify([...bookmarks])); render();
    document.querySelector(`[data-id="${id}"]`)?.focus({preventScroll:true});
  }
  if (event.target.closest('#reset')) { clearFilters(); showReading(); }
});
$('search').addEventListener('input',render);
$('search').addEventListener('keydown',event => { if(event.key === 'Escape') { $('search').value = ''; render(); } });
$('search-form').addEventListener('submit',event => { event.preventDefault(); render(); showReading(); });
$('clear-search').onclick = () => { $('search').value = ''; render(); $('search').focus(); };
$('clear-filters').onclick = () => { clearFilters(); $('search').focus(); };
document.querySelector('.quick-searches').addEventListener('click',event => {
  const button = event.target.closest('[data-query]');
  if (button) { clearFilters(); $('search').value = button.dataset.query; render(); showReading(); }
});
$('saved').onclick = () => { onlySaved = !onlySaved; $('saved').setAttribute('aria-pressed',String(onlySaved)); render(); };
$('theme').onclick = () => { document.body.classList.toggle('dark'); persist('my-life-theme',document.body.classList.contains('dark') ? 'dark' : 'light'); };
$('print').onclick = () => window.print();
document.addEventListener('keydown',event => {
  if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !event.target.matches('input,textarea,select,[contenteditable="true"]')) {
    event.preventDefault(); $('search').focus();
  }
});
if (['http:','https:'].includes(location.protocol)) $('search').value = new URL(location.href).searchParams.get('q') || '';
render();
// Preserve shared item anchors after client-side enhancement replaces the static cards.
if (/^#tip-\d+$/.test(location.hash)) document.getElementById(location.hash.slice(1))?.scrollIntoView();
