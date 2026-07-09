#!/usr/bin/env python3
"""Render 2026-archaeology.md as a single self-contained reading page.

No external CSS, no fonts, no images. Output opens from file://.
Read state and notes persist in localStorage, keyed per section.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "_Documentation" / "2026-archaeology.md"
OUT = ROOT / "_Documentation" / "2026-archaeology.html"


def inline(text):
    """Inline markdown on already-escaped text.

    Code spans are masked out before emphasis runs. The essay writes things
    like `lat * -800`; an unmasked italic pass pairs those asterisks across
    the code-span boundary and emits interleaved <em>/<code>.
    """
    spans = []

    def stash(m):
        spans.append(m.group(1))
        return f"\x00{len(spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{spans[int(m.group(1))]}</code>", text)


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "section"


def convert(md):
    """Markdown -> (body_html, toc) where toc is a list of top-level sections."""
    lines = md.split("\n")
    out, toc = [], []
    i = 0
    in_code = False
    open_section = False
    list_stack = []  # 'ul' | 'ol'

    def close_lists():
        while list_stack:
            out.append(f"</{list_stack.pop()}>")

    def close_section():
        nonlocal open_section
        if open_section:
            close_lists()
            out.append("</section>")
            open_section = False

    while i < len(lines):
        line = lines[i]

        # fenced code
        m = re.match(r"^```(\w*)\s*$", line)
        if m:
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                close_lists()
                lang = m.group(1) or "text"
                out.append(f'<pre class="code" data-lang="{html.escape(lang)}"><code>')
                in_code = True
            i += 1
            continue
        if in_code:
            out.append(html.escape(line))
            i += 1
            continue

        # tables
        if line.startswith("|"):
            close_lists()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            cells = [
                [c.strip() for c in r.strip().strip("|").split("|")] for r in rows
            ]
            body = [r for r in cells if not all(re.fullmatch(r":?-{2,}:?", c or "-") for c in r)]
            if body:
                out.append("<table>")
                head, rest = body[0], body[1:]
                out.append("<thead><tr>" + "".join(
                    f"<th>{inline(html.escape(c))}</th>" for c in head) + "</tr></thead>")
                if rest:
                    out.append("<tbody>")
                    for r in rest:
                        out.append("<tr>" + "".join(
                            f"<td>{inline(html.escape(c))}</td>" for c in r) + "</tr>")
                    out.append("</tbody>")
                out.append("</table>")
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_lists()
            level, text = len(m.group(1)), m.group(2).strip()
            esc = inline(html.escape(text))
            if level == 1:
                close_section()
                out.append(f"<h1>{esc}</h1>")
            elif level == 2:
                close_section()
                sid = slug(text)
                toc.append({"id": sid, "title": text})
                out.append(f'<section id="{sid}" data-title="{html.escape(text)}">')
                out.append(f'<div class="shead"><h2>{esc}</h2>{controls(sid)}</div>')
                open_section = True
            else:
                out.append(f'<h{level} id="{slug(text)}">{esc}</h{level}>')
            i += 1
            continue

        # hr
        if re.fullmatch(r"-{3,}", line.strip()):
            close_lists()
            i += 1
            continue

        # blockquote
        if line.startswith(">"):
            close_lists()
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip(">").strip())
                i += 1
            joined = inline(html.escape(" ".join(b for b in buf if b)))
            out.append(f"<blockquote>{joined}</blockquote>")
            continue

        # lists
        m_ul = re.match(r"^(\s*)[-*]\s+(.*)$", line)
        m_ol = re.match(r"^(\s*)\d+\.\s+(.*)$", line)
        if m_ul or m_ol:
            m = m_ul or m_ol
            want = "ul" if m_ul else "ol"
            if not list_stack:
                out.append(f"<{want}>")
                list_stack.append(want)
            elif list_stack[-1] != want:
                out.append(f"</{list_stack.pop()}>")
                out.append(f"<{want}>")
                list_stack.append(want)
            out.append(f"<li>{inline(html.escape(m.group(2)))}</li>")
            i += 1
            continue

        # blank
        if not line.strip():
            close_lists()
            i += 1
            continue

        # paragraph (soft-wrapped: gather until blank / block start)
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(
            r"^(#{1,6}\s|```|>|\||\s*[-*]\s|\s*\d+\.\s|-{3,}$)", lines[i]
        ):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            close_lists()
            out.append(f"<p>{inline(html.escape(' '.join(buf)))}</p>")

    close_section()
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out), toc


def controls(sid):
    return (
        f'<div class="ctl" data-for="{sid}">'
        f'<button class="read" type="button" aria-pressed="false">Mark read</button>'
        f'<button class="note-open" type="button">Note</button>'
        f"</div>"
    )


CSS = """
:root{
  --bg:#0d0e10; --ink:#f2f0ec; --dim:#8b8880; --faint:#3a3a3d;
  --accent:#e8a33d; --panel:#141519; --code:#111216;
  --body:18px; --head:36px;
  --font:"SF Pro Display","SF Pro Text",-apple-system,BlinkMacSystemFont,system-ui,sans-serif;
  --mono:"SF Mono",ui-monospace,Menlo,monospace;
  --measure:34rem;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;background:var(--bg);color:var(--ink);
  font:600 var(--body)/1.62 var(--font);
  -webkit-font-smoothing:antialiased;
}
#bar{position:fixed;top:0;left:0;height:2px;background:var(--accent);width:0;z-index:50}
.wrap{display:grid;grid-template-columns:16rem minmax(0,var(--measure)) 1fr;gap:3rem;
  max-width:76rem;margin:0 auto;padding:3rem 2rem 8rem}
nav{position:sticky;top:3rem;align-self:start;max-height:80vh;overflow-y:auto;
  font-size:var(--body);line-height:1.45}
nav h3{margin:0 0 1rem;font-size:var(--body);color:var(--dim)}
nav a{display:block;color:var(--faint);text-decoration:none;padding:.28rem 0}
nav a:hover{color:var(--dim)}
nav a.on{color:var(--ink)}
nav a.done{color:var(--accent)}
nav a.done::after{content:"  read";font-size:.72em;color:var(--faint)}
main{min-width:0}
h1{font-size:var(--head);line-height:1.15;margin:0 0 3rem;color:var(--ink)}
h2{font-size:var(--head);line-height:1.2;margin:0;color:var(--ink)}
h3{font-size:var(--body);margin:2.6rem 0 .6rem;color:var(--accent)}
h4{font-size:var(--body);margin:2rem 0 .5rem;color:var(--dim)}
section{margin:0 0 5rem;scroll-margin-top:2rem}
section.read h2{color:var(--dim)}
.shead{display:flex;align-items:baseline;justify-content:space-between;gap:1rem;
  margin:0 0 1.6rem;flex-wrap:wrap}
p{margin:0 0 1.2rem;color:var(--ink)}
li{margin:0 0 .4rem}
ul,ol{margin:0 0 1.2rem;padding-left:1.2rem}
blockquote{margin:1.4rem 0;padding-left:1.2rem;border-left:2px solid var(--faint);color:var(--dim)}
code{font:400 .88em/1.5 var(--mono);color:var(--dim);background:none;word-break:break-word}
pre.code{background:var(--code);padding:1rem 1.1rem;overflow-x:auto;margin:1.4rem 0;border-radius:4px}
pre.code code{color:var(--dim);font-size:.84em}
table{border-collapse:collapse;width:100%;margin:1.4rem 0;font-size:.9em}
th{text-align:left;color:var(--dim);font-weight:600;padding:.4rem .8rem .4rem 0;vertical-align:top}
td{padding:.35rem .8rem .35rem 0;color:var(--ink);vertical-align:top}
a{color:var(--accent)}
button{font:600 .84em var(--font);color:var(--dim);background:var(--panel);
  border:none;border-radius:3px;padding:.4rem .8rem;cursor:pointer}
button:hover{color:var(--ink)}
button.read[aria-pressed="true"]{color:var(--bg);background:var(--accent)}
.ctl{display:flex;gap:.4rem;flex:0 0 auto}
.note{display:none;width:100%;margin:0 0 1.6rem}
.note.open{display:block}
.note textarea{width:100%;min-height:5rem;background:var(--panel);color:var(--ink);
  border:none;border-radius:4px;padding:.9rem;font:600 .92em/1.5 var(--font);resize:vertical}
.note textarea:focus{outline:1px solid var(--faint)}
.note .hint{color:var(--faint);font-size:.8em;margin:.4rem 0 0}
#foot{position:fixed;bottom:0;left:0;right:0;background:var(--panel);
  padding:.9rem 2rem;display:flex;align-items:center;gap:1.4rem;z-index:40}
#foot .count{color:var(--dim);font-size:.9em}
#foot .count b{color:var(--ink);font-weight:600}
#foot .spacer{flex:1}
#copy{background:var(--accent);color:var(--bg)}
#copy:hover{color:var(--bg);opacity:.85}
#reset{background:none}
@media(max-width:900px){
  .wrap{grid-template-columns:1fr;padding:2rem 1.2rem 8rem}
  nav{position:static;max-height:none;margin-bottom:2rem}
}
"""

JS = """
const KEY='timeland-archaeology-read-v1';
const SECS=__TOC__;
let state=JSON.parse(localStorage.getItem(KEY)||'{}');

function save(){localStorage.setItem(KEY,JSON.stringify(state))}
function st(id){return state[id]||(state[id]={read:false,note:''})}

function paint(){
  let n=0;
  SECS.forEach(s=>{
    const d=st(s.id), sec=document.getElementById(s.id);
    const btn=sec.querySelector('button.read');
    const link=document.querySelector(`nav a[href="#${s.id}"]`);
    btn.setAttribute('aria-pressed',d.read?'true':'false');
    btn.textContent=d.read?'Read':'Mark read';
    sec.classList.toggle('read',d.read);
    link.classList.toggle('done',d.read);
    const ta=sec.querySelector('textarea');
    if(ta&&ta.value!==d.note)ta.value=d.note;
    const nb=sec.querySelector('.note-open');
    nb.textContent=d.note.trim()?'Note ·':'Note';
    if(d.read)n++;
  });
  document.querySelector('#foot .count b').textContent=n;
  document.getElementById('copy').disabled=false;
}

// build note panels
SECS.forEach(s=>{
  const sec=document.getElementById(s.id);
  const box=document.createElement('div');
  box.className='note';
  box.innerHTML='<textarea placeholder="What you thought about this section."></textarea>'+
    '<p class="hint">A note on its own records nothing. Mark read when you have read it.</p>';
  sec.querySelector('.shead').after(box);
  sec.querySelector('.note-open').addEventListener('click',()=>{
    box.classList.toggle('open');
    if(box.classList.contains('open'))box.querySelector('textarea').focus();
  });
  box.querySelector('textarea').addEventListener('input',e=>{
    st(s.id).note=e.target.value; save();
    sec.querySelector('.note-open').textContent=e.target.value.trim()?'Note ·':'Note';
  });
  sec.querySelector('button.read').addEventListener('click',()=>{
    const d=st(s.id); d.read=!d.read; save(); paint();
  });
});

// scroll progress + current section
const bar=document.getElementById('bar');
function onScroll(){
  const h=document.documentElement;
  const p=h.scrollTop/Math.max(1,h.scrollHeight-h.clientHeight);
  bar.style.width=(p*100)+'%';
  let cur=SECS[0]&&SECS[0].id;
  for(const s of SECS){
    const r=document.getElementById(s.id).getBoundingClientRect();
    if(r.top<=120)cur=s.id;
  }
  document.querySelectorAll('nav a').forEach(a=>
    a.classList.toggle('on',a.getAttribute('href')==='#'+cur));
}
addEventListener('scroll',onScroll,{passive:true});
addEventListener('resize',onScroll);

document.getElementById('copy').addEventListener('click',()=>{
  const read=SECS.filter(s=>st(s.id).read);
  const notes=SECS.filter(s=>st(s.id).note.trim());
  const L=[];
  L.push('Timeland archaeology essay — my pass, '+SECS.length+' sections.');
  L.push('');
  L.push('Read '+read.length+' of '+SECS.length+'.');
  if(read.length===SECS.length)L.push('I have read the whole essay.');
  else{
    const left=SECS.filter(s=>!st(s.id).read).map(s=>s.title);
    L.push('Still to read: '+left.join('; '));
  }
  if(notes.length){
    L.push('');L.push('Notes:');
    notes.forEach(s=>L.push('- '+s.title+': '+st(s.id).note.trim()));
  }
  const txt=L.join('\\n');
  navigator.clipboard.writeText(txt).then(()=>{
    const b=document.getElementById('copy');
    b.textContent='Copied';setTimeout(()=>b.textContent='Copy for Claude',1400);
  });
});

document.getElementById('reset').addEventListener('click',()=>{
  if(!confirm('Clear read marks and notes on this page?'))return;
  state={};save();paint();
});

paint();onScroll();
"""


def main():
    if not SRC.exists():
        sys.exit(f"missing {SRC}")
    md = SRC.read_text(encoding="utf-8")
    body, toc = convert(md)
    words = len(re.findall(r"\S+", re.sub(r"```.*?```", "", md, flags=re.S)))

    nav = "\n".join(
        f'<a href="#{s["id"]}">{html.escape(s["title"])}</a>' for s in toc
    )
    page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Timeland — the 2026 archaeology</title>
<style>{CSS}</style>
</head><body>
<div id="bar"></div>
<div class="wrap">
<nav><h3>Contents</h3>{nav}</nav>
<main>{body}</main>
</div>
<div id="foot">
  <span class="count"><b>0</b> of {len(toc)} sections read</span>
  <span class="count">{words:,} words</span>
  <span class="spacer"></span>
  <button id="reset" type="button">Reset</button>
  <button id="copy" type="button">Copy for Claude</button>
</div>
<script>{JS.replace("__TOC__", json.dumps(toc))}</script>
</body></html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(toc)} sections, {words:,} words, {len(page):,} bytes)")


if __name__ == "__main__":
    main()
