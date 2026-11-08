#!/usr/bin/env python3
"""data/products.csv -> docs/index.html (GitHub Pages: main 브랜치 /docs).

- 에피소드(ep) 단위로 상품을 쌓는다. 새 편은 products.csv에 행만 추가한다.
- partners_url이 비어 있으면 '링크 준비중'(비활성) 버튼이 된다.
- 고지 문구는 data/disclosure.txt 한 곳에만 둔다. 여기서 옮겨 적지 않는다.
"""
import csv, html, pathlib, shutil

R = pathlib.Path(__file__).resolve().parent
h = html.escape
NUM = '①②③④⑤⑥⑦⑧⑨⑩'

disc_lines = [l.strip() for l in (R / 'data/disclosure.txt').read_text(encoding='utf-8').splitlines() if l.strip()]
DISC = '<br>'.join(h(l) for l in disc_lines)

rows = list(csv.DictReader(open(R / 'data/products.csv', encoding='utf-8')))
eps = {}
for r in rows:
    e = eps.setdefault(int(r['ep']), {'series': r['series'], 'title': r['title'], 'items': []})
    e['items'].append(r)

cards = []
for n in sorted(eps, reverse=True):
    e = eps[n]
    lis = []
    for it in sorted(e['items'], key=lambda x: int(x['slot'])):
        u = it['partners_url'].strip()
        btn = (f'<a class="btn" href="{h(u)}" target="_blank" rel="sponsored noopener">쿠팡에서 보기 ›</a>'
               if u.startswith('https://link.coupang.com/') else '<span class="btn off">링크 준비중</span>')
        lis.append(f'<li class="item"><span class="no">{NUM[int(it["slot"]) - 1]}</span>'
                   f'<div class="txt"><b>{h(it["name"])}</b><small>{h(it["benefit"])}</small>{btn}</div></li>')
    cards.append(f'<section class="ep" id="ep{n}"><div class="eph"><span class="tag">#{n}</span>'
                 f'<span class="ser">{h(e["series"])}</span></div><h2>{h(e["title"])}</h2>'
                 f'<ul>{"".join(lis)}</ul></section>')

PAGE = """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>줍줍이 장바구니 · @jubjub_pick</title>
<meta name="description" content="줍줍이 쇼츠에 나온 상품을 영상 번호로 찾아보세요.">
<style>
:root{--p:#ff8fab;--bg:#fff7f0;--ink:#3b2f2f}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;background:var(--bg);color:var(--ink)}
.disc{background:#3b2f2f;color:#fff;font-size:13px;line-height:1.5;padding:10px 14px;text-align:center;font-weight:600}
header{text-align:center;padding:22px 16px 6px}
header img{width:96px;height:96px;border-radius:50%;border:4px solid var(--p);background:#fff;object-fit:cover}
header h1{margin:8px 0 2px;font-size:24px}
header p{margin:0;color:#8a7272}
header .yt{margin-top:8px}
header .yt a{color:#c0392b;font-weight:700;text-decoration:none}
.search{max-width:480px;margin:16px auto;padding:0 16px;display:flex;gap:8px}
.search input{flex:1;min-width:0;font-size:22px;padding:14px 16px;border:3px solid var(--p);border-radius:18px;outline:none;text-align:center}
.search button{font-size:18px;padding:0 18px;border:0;border-radius:18px;background:var(--p);color:#fff;font-weight:700}
#msg{text-align:center;color:#c0392b;min-height:20px;font-size:14px}
main{max-width:520px;margin:0 auto;padding:0 12px 40px}
.ep{background:#fff;border-radius:22px;padding:14px;margin:14px 0;box-shadow:0 3px 0 #f3d9cf;scroll-margin-top:16px}
.ep.hit{outline:4px solid var(--p)}
.eph{display:flex;gap:8px;align-items:center}
.tag{background:var(--p);color:#fff;font-weight:800;border-radius:12px;padding:3px 10px}
.ser{font-size:13px;color:#8a7272}
.ep h2{font-size:17px;margin:8px 0}
ul{list-style:none;margin:0;padding:0}
.item{display:flex;gap:10px;align-items:center;padding:10px 0;border-top:1px dashed #f0d6cc}
.no{font-size:24px;color:var(--p);font-weight:800;min-width:28px}
.txt{flex:1;display:flex;flex-direction:column;gap:3px}
.txt small{color:#8a7272}
.btn{align-self:flex-start;background:#ff6b6b;color:#fff;text-decoration:none;font-weight:700;padding:7px 12px;border-radius:12px;font-size:14px}
.btn.off{background:#ccc}
footer{text-align:center;font-size:12px;color:#a08b8b;padding:20px}
footer .fd{display:block;color:#3b2f2f;font-weight:600;margin-top:8px}
</style></head><body>
<div class="disc">__DISC__</div>
<header><img src="img/profile.png" alt="줍줍이"><h1>줍줍이 장바구니 🐾</h1><p>@jubjub_pick · 쇼츠에 나온 상품 모음</p><p class="yt"><a href="https://www.youtube.com/@jjajeungnyang" target="_blank" rel="noopener">▶ 짜증냥 쇼츠 보러가기</a></p></header>
<form class="search" onsubmit="go();return false"><input id="q" type="number" inputmode="numeric" placeholder="영상 번호 입력 (예: 8)"><button>찾기</button></form>
<div id="msg"></div>
<main>__CARDS__</main>
<footer>가격·재고는 쿠팡 페이지에서 확인해 주세요. 상품 번호(①②③)는 영상 속 번호와 같아요.<span class="fd">__DISC__</span></footer>
<script>
function go(n){
  n = n || document.getElementById('q').value.trim();
  var el = document.getElementById('ep' + n), m = document.getElementById('msg');
  document.querySelectorAll('.ep.hit').forEach(function (e) { e.classList.remove('hit'); });
  if (!el) { m.textContent = n ? '#' + n + ' 영상은 아직 없어요냥 😿' : ''; return; }
  m.textContent = ''; el.classList.add('hit'); el.scrollIntoView({behavior: 'smooth'});
  history.replaceState(null, '', '#' + n);
}
var hs = location.hash.replace(/\D/g, ''); if (hs) go(hs);
</script></body></html>
"""

out = R / 'docs'
out.mkdir(exist_ok=True)
page = PAGE.replace('__DISC__', DISC).replace('__CARDS__', ''.join(cards))
(out / 'index.html').write_text(page, encoding='utf-8')
(out / '.nojekyll').write_text('', encoding='utf-8')
if (R / 'img').is_dir():
    shutil.copytree(R / 'img', out / 'img', dirs_exist_ok=True)
print(f'built {len(eps)} episodes, {len(rows)} products')
