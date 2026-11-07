#!/usr/bin/env python3
# 불편이즘 상품 링크 페이지 빌드 (로컬 초안). data/products.csv -> docs/index.html
# 가격·재고는 넣지 않는다. partners_url이 비어 있으면 '링크 준비중' 비활성 버튼이 된다.
import csv, html, pathlib

R = pathlib.Path(__file__).resolve().parent
DISC = '이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.'
NUM = '①②③④⑤⑥⑦⑧⑨⑩'
h = html.escape

rows = list(csv.DictReader(open(R / 'data/products.csv', encoding='utf-8')))
series = {}
for r in rows:
    series.setdefault(r['series'], []).append(r)

secs = []
for name_s, items in series.items():
    lis = []
    for it in sorted(items, key=lambda x: int(x['slot'])):
        u = it['partners_url'].strip()
        if u.startswith('https://link.coupang.com/'):
            btn = f'<a class="btn" href="{h(u)}" target="_blank" rel="sponsored noopener">쿠팡에서 보기 ›</a>'
        else:
            btn = '<span class="btn off">링크 준비중</span>'
        lis.append(f'<li class="item" data-q="{h(it["name"].lower())}"><span class="no">{NUM[int(it["slot"]) - 1]}</span>'
                   f'<div class="txt"><b>{h(it["name"])}</b><small>{h(it["benefit"])}</small>{btn}</div></li>')
    secs.append(f'<section class="ser"><h2>{h(name_s)}</h2><ul>{"".join(lis)}</ul></section>')

page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>불편이즘 상품 모음</title>
<meta name="description" content="불편이즘 쇼츠에 나온 상품을 모아 둔 페이지예요.">
<style>
:root{{--p:#ff8fab;--bg:#fff7f0;--ink:#3b2f2f}}
*{{box-sizing:border-box}}body{{margin:0;font-family:-apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;background:var(--bg);color:var(--ink)}}
.disc{{position:sticky;top:0;z-index:9;background:#3b2f2f;color:#fff;font-size:13px;line-height:1.45;padding:9px 14px;text-align:center;font-weight:600}}
header{{text-align:center;padding:22px 16px 6px}}header h1{{margin:8px 0 2px;font-size:24px}}header p{{margin:0;color:#8a7272}}
.search{{max-width:480px;margin:16px auto;padding:0 16px}}
.search input{{width:100%;font-size:18px;padding:12px 16px;border:3px solid var(--p);border-radius:18px;outline:none}}
main{{max-width:520px;margin:0 auto;padding:0 12px 40px}}
.ser{{background:#fff;border-radius:22px;padding:14px;margin:14px 0;box-shadow:0 3px 0 #f3d9cf}}
.ser h2{{font-size:18px;margin:4px 0 6px;color:var(--p)}}
ul{{list-style:none;margin:0;padding:0}}.item{{display:flex;gap:10px;align-items:center;padding:10px 0;border-top:1px dashed #f0d6cc}}
.no{{font-size:22px;color:var(--p);font-weight:800;min-width:26px}}
.txt{{flex:1;display:flex;flex-direction:column;gap:3px}}.txt small{{color:#8a7272}}
.btn{{align-self:flex-start;background:#ff6b6b;color:#fff;text-decoration:none;font-weight:700;padding:7px 12px;border-radius:12px;font-size:14px}}
.btn.off{{background:#ccc}}footer{{text-align:center;font-size:12px;color:#a08b8b;padding:20px}}
</style></head><body>
<div class="disc">📢 {h(DISC)}</div>
<header><h1>불편이즘 상품 모음</h1><p>쇼츠에 나온 상품을 모아 둔 페이지예요</p></header>
<div class="search"><input id="q" type="search" placeholder="상품 이름으로 찾기 (예: 랩)" autocomplete="off"></div>
<main>{"".join(secs)}</main>
<footer>가격과 재고는 쿠팡 페이지에서 확인해 주세요.<br>📢 {h(DISC)}</footer>
<script>
document.getElementById('q').addEventListener('input', function (e) {{
  var q = e.target.value.trim().toLowerCase();
  document.querySelectorAll('.item').forEach(function (li) {{
    li.style.display = (!q || li.dataset.q.indexOf(q) !== -1) ? '' : 'none';
  }});
}});
</script></body></html>
'''
(R / 'docs').mkdir(exist_ok=True)
(R / 'docs/index.html').write_text(page, encoding='utf-8')
(R / 'docs/.nojekyll').write_text('', encoding='utf-8')
print(f'built {len(series)} series, {len(rows)} products')
