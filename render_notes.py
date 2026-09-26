"""Render the authored Markdown textbook as a static site with local MathJax."""
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import html
import json
import re
import markdown
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
MANIFEST = json.loads((ROOT / 'sources/manifest.json').read_text(encoding='utf-8'))
DESCRIPTIONS = [
    'Ecosystems, evaluation, customer context, and local-model economics',
    'Scaling laws, compute allocation, forecasts, and demand elasticity',
    'Resilience, incident response, recovery objectives, and legal evidence',
    'Goodput, availability, checkpoints, networks, and capacity planning',
    'AI-native work, productivity bounds, feedback loops, and founder judgment',
    'Co-design, the Roofline model, inference memory, and agent latency',
    'Firm power, fuel supply, capacity factors, storage, and project economics',
    'Network effects, venture-firm design, defensibility, and governance',
    'Product discovery, causal experiments, evidence, and value of information',
    'Multimodal architectures, preference signals, world models, and control',
    'Latent diffusion, flow matching, Self-Flow, editing, and distillation',
    'Audio codecs, cascaded and fused systems, latency, and reliable actions',
    'The whole stack, reinforcement learning, context, sovereignty, and standards',
]


def render_body(source):
    saved = []
    def protect(match):
        saved.append(match[0])
        return f'MATHPLACEHOLDER{len(saved)-1}END'
    source = re.sub(r'\$\$[\s\S]+?\$\$|(?<!\\)\$[^$\n]+?\$', protect, source)
    source = source.replace('<details>', '<details markdown="1">')
    body = markdown.markdown(source, extensions=['tables', 'fenced_code', 'toc', 'sane_lists', 'md_in_html'])
    body = body.replace('<code class="language-python">', '<code>')
    for i, expression in enumerate(saved):
        body = body.replace(f'MATHPLACEHOLDER{i}END', html.escape(expression))
    return body


def page(title, body, sidebar=''):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | CS153 Frontier Systems</title>
<link rel="stylesheet" href="assets/style.css">
<script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script>
<script defer src="assets/mathjax-tex-svg.js"></script>
<script defer src="assets/code-copy.js"></script></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="shell"><a class="brand" href="index.html">CS153 · Frontier Systems</a>
<nav aria-label="Site"><a href="index.html#chapters">Chapters</a><a href="sources.html">Sources &amp; coverage</a></nav></div></header>
<div class="shell layout"><main id="main" class="main">{body}</main>
<aside class="side" aria-label="On this page"><strong>On this page</strong>{sidebar}</aside></div>
<footer class="foot shell">Independent study notes · 25 September 2026 · <a href="sources.html">Source limitations</a> · <a href="index.html">Reading guide</a><br>Not official Stanford course material or endorsed by the speakers.</footer></body></html>'''


def toc(soup):
    return '<ul>'+''.join(f'<li><a href="#{h["id"]}">{html.escape(h.get_text(" ",strip=True))}</a></li>' for h in soup.select('h2[id]'))+'</ul>'


def main():
    records, references, sections = [], {}, []
    exercises = 0
    for i, metadata in enumerate(MANIFEST, 1):
        slug = f'lecture-{i:02d}'
        source = (ROOT / 'chapters' / f'{slug}.md').read_text(encoding='utf-8')
        exercise_part = re.search(r'## Exercises[^\n]*\n(.*?)<details>',source,re.S)[1]
        exercises += len(re.findall(r'^\d+\. ',exercise_part,re.M))
        body = render_body(source)
        soup = BeautifulSoup(body, 'html.parser')
        title = soup.h1.get_text()
        words = len(re.findall(r'\b[\w’]+\b', soup.get_text(' ')))
        records.append(dict(position=i, title=title, file=f'{slug}.html', words=words, description=DESCRIPTIONS[i-1]))
        navigation = '<nav class="chapter-nav" aria-label="Chapter navigation">'
        navigation += f'<a href="lecture-{i-1:02d}.html">Previous chapter</a>' if i>1 else '<span></span>'
        navigation += '<a class="index" href="index.html">Reading guide</a>'
        navigation += f'<a class="next" href="lecture-{i+1:02d}.html">Next chapter</a>' if i<13 else '<span></span>'
        navigation += '</nav>'
        contents = toc(soup)
        mobile = f'<details class="mobile-toc"><summary>Chapter contents</summary>{contents}</details>'
        companion = f'<p class="tiny"><a href="chapters/{slug}.md">Editable Markdown</a> · {words:,} words including notation and references · <a href="sources.html#source-{i}">Transcript provenance</a></p>'
        (ROOT / f'{slug}.html').write_text(page(title,navigation+companion+mobile+body+navigation,contents),encoding='utf-8')
        for heading in soup.select('h2'):
            link = heading.find('a', href=re.compile('youtube.com/watch'))
            if link:
                query = parse_qs(urlparse(link['href']).query)
                seconds = int(query['t'][0].rstrip('s'))
                assert query['v'][0] == metadata['video_id']
                assert 0 <= seconds <= metadata['duration_seconds']
                sections.append(dict(chapter=i, heading=heading.get_text(' ',strip=True), anchor=heading['id'], seconds=seconds, recording=link['href']))
        for link in soup.select('a[href^="https://"]'):
            url = link['href']
            if 'youtube.com/' not in url and 'CS153-Frontier-Systems-Transcripts' not in url:
                ref = references.setdefault(url, dict(label=link.get_text(' ',strip=True), chapters=[]))
                if i not in ref['chapters']:
                    ref['chapters'].append(i)
    cards = ''.join(f'<a class="card" href="{r["file"]}"><div class="eyebrow">Playlist {r["position"]:02d}</div><b>{html.escape(r["title"].split(". ",1)[1])}</b><span>{r["description"]}</span></a>' for r in records)
    hours = sum(m['duration_seconds'] for m in MANIFEST)/3600
    body = f'''<div class="eyebrow">Transcript-grounded lecture notes · Research extensions</div>
<h1>From models to<br>frontier systems.</h1>
<p>Thirteen conversations about how AI systems learn, operate, reach users, and pay for their next iteration. These textbook chapters follow the supplied Stanford CS153 playlist through recurring cases, mathematical derivations, executable examples, exercises with worked solutions, and primary-source research.</p>
<div class="hero"><div class="metrics"><span><b>13</b> chapters</span><span><b>{hours:.1f} h</b> of recordings</span><span><b>{len(sections)}</b> section timestamps</span><span><b>{exercises}</b> exercises</span></div><p>Our contribution: substantial independent exposition, worked teaching cases, mathematical derivations, exercises, and primary-source research, with explicit assumptions and a clear boundary between lecture content and educational extensions.</p></div>
<h2 id="reading">Choose a reading path</h2>
<p><b>Playlist path:</b> read 1–13 below. The playlist snapshot is arranged newest first; these chapter numbers are playlist positions, not official lecture numbers.</p>
<p><b>Conceptual path:</b> begin with <a href="lecture-13.html">13 · Context and compute</a>; then study <a href="lecture-11.html">11 · Visual models</a>, <a href="lecture-12.html">12 · Voice</a>, and <a href="lecture-10.html">10 · Unified systems</a>. Continue through 4, 6, and 7 for infrastructure; 5, 8, and 9 for building and organizations; then 1, 2, and 3 for ecosystem, scaling, and resilience.</p>
<p><b>Prerequisites:</b> basic linear algebra, probability, derivatives, and familiarity with AI tools. Symbols are defined where introduced. For each chapter, follow a timestamp, work one numerical example by hand, and attempt the exercises before opening the solutions.</p>
<p><b>Executable companion:</b> each chapter contains a Python example with checks. From this folder, run <code>python labs/check_chapters.py</code> for all thirteen, or add a chapter number to run one. The <a href="labs/check_chapters.py">runner</a> executes the displayed code directly using Python's standard library. These are analytical teaching models; no API keys, model downloads, or paid inference are required. See the <a href="README.md">README</a> for files and regeneration.</p>
<h2 id="chapters">The complete playlist snapshot</h2><div class="cards">{cards}</div>
<h2 id="evidence">How to read the evidence</h2>
<p>The full available English transcript text was used for each recording. Ten caption sources were fetched directly from YouTube; three use explicitly identified third-party archives. Direct-caption metadata does not retain whether those tracks were manual or automatic. The archived sources describe automatic captions with light formatting.</p>
<p>Timestamp links locate the relevant lecture topic; they do not attribute every equation or research extension beneath the heading to the speaker. Captions do not establish continuous visual coverage: demonstrations and slides were not independently inspected frame by frame. Personal anecdotes and repetitive discussion are compressed.</p>
<p>These are independent study notes, not official Stanford notes. The <a href="https://cs153.stanford.edu/">official course site</a> and <a href="https://www.youtube.com/playlist?list=PLoROMvodv4rN447WKQ5oz_YdYbS74M5IA">recording playlist</a> remain authoritative. The earliest listed recording refers to a prior class not present in this snapshot. No chapter has been invented for an unavailable recording.</p>
<p><a href="sources.html">Open the source map, research bibliography, and claim qualifications</a>. Equations render offline from the bundled MathJax asset; recordings and external references require internet access.</p>'''
    (ROOT/'index.html').write_text(page('Reading guide',body,toc(BeautifulSoup(body,'html.parser'))),encoding='utf-8')
    source_body = '''<h1>Sources, coverage, and research</h1><p>Snapshot: 25 September 2026. This page records source provenance and section-level navigation. It is not a claim-level attribution ledger or a percentage measure of lecture-derived prose.</p>
<h2 id="method">Method and limits</h2><p>The supplied playlist was enumerated, every available caption source was read, and lecture arguments were reconstructed in independent prose. Mathematical developments, hypothetical numbers, and exercises are labeled as educational extensions. Primary papers and institutional documents support research additions and consequential corrections. Speaker opinions, predictions, and private commercial figures remain attributed claims.</p>
<p>Selected corrections include five-nines downtime (chapter 4), network pair counts (8), supplier nationality versus operating enrichment capacity (7), the Sullivan appellate outcome (3), and the scope of historical export controls and the CLOUD Act (8 and 13). These checks do not amount to verifying every biographical or commercial statement in the recordings.</p>
<p>Raw caption caches are local research inputs. The <a href="sources/manifest.json">machine-readable manifest</a> retains recording identifiers, source origins, quality notes, and SHA-256 hashes. The <a href="sources/section-map.json">section map</a> records each timestamped main heading. No raw captions are embedded in the reading pages.</p>'''
    for m,r in zip(MANIFEST,records):
        i=m['position']
        source_body += f'<h2 id="source-{i}">{html.escape(r["title"])}</h2><p><a href="{r["file"]}">Read chapter</a> · <a href="{m["url"]}">Recording</a> · <a href="{html.escape(m["retrieval_url"],quote=True)}">Caption source</a></p><p>{html.escape(m["origin"])}. {html.escape(m["quality_note"])}</p><ul>'
        for s in sections:
            if s['chapter']==i:
                source_body += f'<li><a href="{r["file"]}#{s["anchor"]}">{html.escape(s["heading"])}</a> · <a href="{html.escape(s["recording"],quote=True)}">Recording segment</a></li>'
        source_body += '</ul>'
    source_body += '<h2 id="research">Research and institutional references</h2><p>Aggregated from the chapters, where the purpose and limits of each citation are explained. Papers, official model repositories, court opinions, and agency materials are primary sources; they differ in what they can establish. A model card supports claims about that release, not independent comparative superiority.</p><ol>'
    for url,ref in references.items():
        links=' · '.join(f'<a href="lecture-{i:02d}.html">{i}</a>' for i in ref['chapters'])
        source_body += f'<li><a href="{html.escape(url,quote=True)}">{html.escape(ref["label"])}</a> — chapters {links}</li>'
    source_body += '</ol>'
    (ROOT/'sources.html').write_text(page('Sources and coverage',source_body,toc(BeautifulSoup(source_body,'html.parser'))),encoding='utf-8')
    (ROOT/'sources/section-map.json').write_text(json.dumps(sections,indent=2),encoding='utf-8')
    (ROOT/'sources/reading-manifest.json').write_text(json.dumps(dict(chapters=records,section_timestamps=len(sections),references=len(references)),indent=2),encoding='utf-8')
    print(f'Rendered {len(records)} chapters; {sum(r["words"] for r in records):,} words; {len(sections)} timestamped sections; {len(references)} distinct reference URLs.')


if __name__=='__main__':
    assert '<em>' not in render_body('Test $x_i+y_j$')
    assert '<li>' in render_body('<details><summary>Answer</summary>\n\n1. Example\n\n</details>')
    main()
