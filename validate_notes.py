"""Check source integrity, navigation, worked arithmetic, and optional browser rendering."""
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote
import argparse
import hashlib
import json
import math
import re
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parent


def main(browser_check=False):
    manifest=json.loads((ROOT/'sources/manifest.json').read_text(encoding='utf-8'))
    assert len(manifest)==13
    pages=[ROOT/'index.html',ROOT/'sources.html',*sorted(ROOT.glob('lecture-*.html'))]
    assert len(pages)==15
    soups={p.name:BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser') for p in pages}
    math_expected={}
    timestamps=0
    cached_chapters=0
    for m in manifest:
        i=m['position']
        cache=ROOT/f'sources/lecture-{i:02d}.json'
        segments=None
        if cache.exists():
            assert hashlib.sha256(cache.read_bytes()).hexdigest()==m['sha256']
            segments=json.loads(cache.read_text(encoding='utf-8'))
            assert len(segments)==m['segments']
            assert all(a['start']<=b['start'] for a,b in zip(segments,segments[1:]))
            assert not any(re.search(r'\*\*\[\d+:\d+:\d+\]',s['text']) for s in segments), 'Unparsed hour timestamp'
            cached_chapters+=1
        source=(ROOT/f'chapters/lecture-{i:02d}.md').read_text(encoding='utf-8')
        math_expected[f'lecture-{i:02d}.html']=len(re.findall(r'\$\$[\s\S]+?\$\$|(?<!\\)\$[^$\n]+?\$',source))
        soup=soups[f'lecture-{i:02d}.html']
        main_times = [int(parse_qs(urlparse(a['href']).query)['t'][0].rstrip('s'))
                      for a in soup.select('main h2 a[href*="youtube.com/watch"]')]
        assert main_times == sorted(main_times), (i, 'section order')
        questions = re.search(r'## Exercises[^\n]*\n(.*?)<details>',source,re.S)[1]
        exercise_count = len(re.findall(r'^\d+\. ', questions, re.M))
        assert len(soup.select('details:not(.mobile-toc) > ol > li'))==exercise_count, (i,'solutions missing')
        assert 'MATHPLACEHOLDER' not in str(soup)
        for a in soup.select('main a[href*="youtube.com/watch"]'):
            q=parse_qs(urlparse(a['href']).query)
            assert q['v'][0]==m['video_id']
            if 't' in q:
                t=int(q['t'][0].rstrip('s'))
                assert 0<=t<=m['duration_seconds'],(i,t)
                if segments is not None:
                    caption=min(segments,key=lambda s:abs(s['start']-t))
                    assert abs(caption['start']-t)<90,(i,t,'caption gap')
                # Mobile contents duplicate the same recording links only as text.
                timestamps+=1
    for name,soup in soups.items():
        assert len(soup.select('h1'))==1,name
        ids=[t['id'] for t in soup.select('[id]')]
        assert len(ids)==len(set(ids)),(name,'duplicate ids')
        for a in soup.select('a[href]'):
            url=urlparse(a['href'])
            if url.scheme or url.netloc:
                continue
            target=ROOT/unquote(url.path) if url.path else ROOT/name
            assert target.exists(),(name,a['href'])
            if url.fragment and target.suffix=='.html':
                assert soups[target.name].find(id=unquote(url.fragment)),(name,a['href'])
    # Independently recompute representative worked results and exercise answers.
    checks={
        'five_nines_minutes':8760*(1-.99999)*60,
        'checkpoint_minutes':math.sqrt(2*2*1000),
        'energy_twh':100*1.2*8760/1e6,
        'network_pairs':100*99/2,
        'experiment_precision_n':math.ceil(1.96**2*.4864/.02**2),
        'rollout_error_bound':.01*(1.1**20-1)/.1,
        'latent_scalars':64*64*4,
        'codec_bits_per_second':50*8*math.log2(1024),
        'verifier_precision':.285/(.285+.007),
    }
    assert math.isclose(checks['five_nines_minutes'],5.256,rel_tol=1e-8)
    assert math.isclose(checks['energy_twh'],1.0512)
    assert checks['experiment_precision_n']==4672
    assert .572<checks['rollout_error_bound']<.574
    assert checks['codec_bits_per_second']==4000
    assert math.isclose((.2+50*.05)/(.2+4*.05),6.75)
    section_count=len(json.loads((ROOT/'sources/section-map.json').read_text()))
    report=dict(structural='passed',chapters=13,html_pages=15,section_timestamps=section_count,
                recording_links_in_chapter_bodies=timestamps,worked_arithmetic=checks,browser=[],
                caption_cache_checks=dict(passed=cached_chapters,skipped=13-cached_chapters))
    (ROOT/'validation').mkdir(exist_ok=True)
    if browser_check:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser=pw.chromium.launch(channel='chrome',headless=True)
            page=browser.new_page(viewport=dict(width=1280,height=900))
            errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            for path in pages:
                page.goto(path.as_uri(),wait_until='load')
                page.evaluate('async () => {await MathJax.startup.promise;}')
                found=page.locator('mjx-container').count()
                assert found==math_expected.get(path.name,0),(path.name,found,math_expected.get(path.name,0))
                assert page.locator('mjx-merror, [data-mml-node="merror"]').count()==0,path.name
                for width in [1280,390]:
                    page.set_viewport_size(dict(width=width,height=900))
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(path.name,width,'overflow')
                if path.name.startswith('lecture-'):
                    answer=page.locator('details:not(.mobile-toc)')
                    answer.locator('summary').click()
                    assert answer.get_attribute('open') is not None
                    assert answer.locator('li').first.is_visible()
                    mobile=page.locator('.mobile-toc')
                    mobile.locator('summary').click()
                    assert mobile.locator('a').first.is_visible()
                report['browser'].append(dict(page=path.name,math_expressions=found,desktop_and_mobile='passed'))
                print(path.name,'math',found,'desktop/mobile passed',flush=True)
            assert not errors,errors
            page.set_viewport_size(dict(width=1280,height=900))
            page.goto((ROOT/'index.html').as_uri(),wait_until='load')
            page.screenshot(path=str(ROOT/'validation/browser-index.png'))
            page.goto((ROOT/'lecture-11.html').as_uri(),wait_until='load')
            page.evaluate('async () => {await MathJax.startup.promise;}')
            page.locator('h2').nth(1).scroll_into_view_if_needed()
            page.screenshot(path=str(ROOT/'validation/browser-math.png'))
            browser.close()
    (ROOT/'validation/report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('Local links, timestamp bounds, solution coverage, and numerical checks passed.')
    print(f'Caption integrity and proximity: {cached_chapters} chapters passed; {13-cached_chapters} skipped (cache absent).')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--browser',action='store_true')
    main(parser.parse_args().browser)
