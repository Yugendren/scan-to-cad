"""JSON + HTML report. The HTML summary block is written for a hobbyist: plain words,
verdict first, then the full disclosure of every action and every decision."""

from __future__ import annotations

import html
import json
from pathlib import Path


def write_json(report: dict, path: Path) -> Path:
    path.write_text(json.dumps(report, indent=2))
    return path


def _row(k, v):
    return f"<tr><th>{html.escape(str(k))}</th><td>{html.escape(str(v))}</td></tr>"


def _table(d: dict) -> str:
    return "<table>" + "".join(_row(k, v) for k, v in d.items()) + "</table>"


def write_html(report: dict, path: Path) -> Path:
    r = report
    verdict = r["verdict"]
    dev = r["deviation"]
    th = r["thickness"]
    ide = r["idealize"]
    ori = r["orientation"]
    before, after = r["before"], r["after"]

    summary_lines = [
        f"<li><b>Printable file:</b> {'yes' if verdict['printable'] else 'no'} — {html.escape(verdict['printable_reason'])}</li>",
        f"<li><b>Restored model changed the original surface by:</b> up to {dev['max_mm']} mm "
        f"(95% of the surface within {dev['p95_mm']} mm; your budget was {dev['budget_mm']} mm) — "
        f"{'within budget' if dev['within_budget'] else 'OVER budget — check the flagged regions'}</li>",
        f"<li><b>Thin walls:</b> {th['below_min_wall_frac']*100:.1f}% of the surface is thinner than "
        f"{th['min_wall_mm']} mm (thinnest sample {th['min_mm']} mm); {th['thin_region_count']} thin region(s)</li>",
        f"<li><b>Flat-surface idealization:</b> "
        + (f"{ide['accepted']} region(s) flattened, {ide['refused']} refused (deviation too large)"
           if ide['enabled'] else f"not applied — {html.escape(ide['note'])}") + "</li>",
        f"<li><b>Suggested print orientation:</b> {html.escape(ori['suggested'])} "
        f"({ori['overhang_area_frac']*100:.1f}% overhang area)</li>",
        f"<li><b>Size:</b> {' × '.join(str(x) for x in after['bbox_mm'])} mm"
        + (" — <b>check units</b>" if any('units' in n for n in before.get('notes', [])) else "") + "</li>",
    ]

    actions_html = "".join(
        f"<tr><td>{html.escape(a['step'])}</td><td><code>{html.escape(json.dumps(a['params']))}</code></td>"
        f"<td><code>{html.escape(json.dumps(a.get('result', {})))}</code></td></tr>"
        for a in r["actions"])
    decisions_html = "".join(
        f"<tr><td>{d['region_id']}</td><td>{d['faces']}</td><td>{d['area_mm2']}</td><td>{d['max_dev_mm']}</td>"
        f"<td>{d['p95_dev_mm']}</td><td>{'ACCEPTED' if d['accepted'] else 'refused'}</td>"
        f"<td>{html.escape(d['reason'])}</td><td>{d['vertices_moved']}</td></tr>"
        for d in ide.get("decisions", []))
    flagged_html = "".join(
        f"<li>at {f['center_mm']} mm: {f['samples']} samples, max {f['max_dev_mm']} mm — {html.escape(f['likely'])}</li>"
        for f in dev.get("flagged_regions", [])) or "<li>none</li>"

    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>scanfix report — {html.escape(r['input_name'])}</title>
<style>
body{{font-family:-apple-system,system-ui,Segoe UI,Roboto,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#1a1915;line-height:1.5}}
h1{{font-size:1.4rem}} h2{{font-size:1.1rem;margin-top:2rem;border-bottom:1px solid #ddd;padding-bottom:.3rem}}
.summary{{background:#f4f2ec;border-left:4px solid #1a1915;padding:1rem 1.2rem}} .summary li{{margin:.4rem 0}}
table{{border-collapse:collapse;width:100%;font-size:.9rem}} th,td{{text-align:left;border-bottom:1px solid #e5e2da;padding:.35rem .5rem;vertical-align:top}}
th{{width:34%;font-weight:600}} code{{font-size:.8rem;word-break:break-all}} .muted{{color:#5c5950;font-size:.85rem}}
.ok{{color:#2d6a4a}} .bad{{color:#a03d22}}
</style></head><body>
<h1>scanfix report — {html.escape(r['input_name'])}</h1>
<p class="muted">scanfix v{html.escape(r['version'])} · {html.escape(r['timestamp'])} · runtime {r['runtime_s']} s · class: {html.escape(r['mesh_class'])} ({html.escape(r['class_source'])})</p>
<div class="summary"><b>What you got</b><ul>{''.join(summary_lines)}</ul>
<p class="muted">Every change made to your file is listed below. Nothing was changed that is not listed here.</p></div>

<h2>Files</h2>{_table(r['outputs'])}
<h2>Before → after</h2>
<table><tr><th></th><th>before</th><th>after</th></tr>
{''.join(f"<tr><th>{html.escape(k)}</th><td>{html.escape(str(before.get(k)))}</td><td>{html.escape(str(after.get(k)))}</td></tr>" for k in ['vertices','faces','components','watertight','boundary_edges','nonmanifold_edges','bbox_mm','volume_mm3','noise_envelope_mm'])}
</table>
<p class="muted">Notes on input: {html.escape('; '.join(before.get('notes', [])) or 'none')}</p>

<h2>Every action taken</h2>
<table><tr><th>step</th><th>parameters</th><th>result</th></tr>{actions_html}</table>

<h2>Deviation certificate (restored vs original)</h2>{_table({k: v for k, v in dev.items() if k != 'flagged_regions'})}
<p>Flagged regions:</p><ul>{flagged_html}</ul>

<h2>Flat-surface idealization decisions</h2>
<p>{html.escape(ide.get('note', ''))} Budget: {ide['budget_mm']} mm.</p>
{('<table><tr><th>region</th><th>faces</th><th>area mm²</th><th>max dev</th><th>p95 dev</th><th>decision</th><th>reason</th><th>vertices moved</th></tr>' + decisions_html + '</table>') if decisions_html else '<p class="muted">no decisions (not applied)</p>'}

<h2>Wall thickness</h2>{_table(th)}
<h2>Orientation</h2>{_table({k: v for k, v in ori.items() if k != 'candidates'})}
<h2>Verdict</h2>{_table(verdict)}
<p class="muted">scanfix is an integration of well-known mesh-repair and geometry-fitting methods with a disclosure discipline; it is not an AI model and it makes no claim beyond the numbers above.</p>
</body></html>"""
    path.write_text(doc)
    return path
