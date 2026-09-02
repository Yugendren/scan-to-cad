# 16 — Kill research II: market reality, iteration speed, STL reframe (2026-09-02)

Method: ~36 fetch/search attempts via API/proxy (search quota
exhausted). Mandate: test whether the market is real and the product
iterable.

## 1. Demand quantification
- Amazon US (via jina proxy): Revopoint POP 4 $828, 165 ratings;
  INSPIRE 2 $467, 177; MetroY Ultra $1,899, 54; Creality Ferret Pro
  $359, 255; newer Creality Pika/Otter <10 each. At ~1–2% review rate
  → low tens of thousands of units per SKU on Amazon US. Kickstarter
  pages delisted; Bing News confirms Revopoint MetroX "$1M from 1,200+
  backers in 4 hours" (Oct 2024).
- Community sizes (subredditstats, Dec 2022–23 snapshots): r/3DScanning
  19,039 vs r/3Dprinting 1,984,771 vs r/functionalprint 421,900 vs
  r/Machinists 209,141. Scanning ≈1% of printing; even tripled, a
  ~60k pond.
- Paid demand (Fiverr via proxy): "stl to step" 13,000+ gigs;
  "reverse engineering 3d scan" 1,100+. Top sellers: Tran Tung 887
  reviews @$25+, Charithcmp 817 @$83+, Sathish Kumar 446, Jacob R 357,
  Letuan9 280; prices $9–$264. Review counts understate orders ~3–5x
  → top ~10 sellers ≈ 10–20k paid conversions. Strongest signal in the
  exercise: people pay $15–80 today, repeatedly, to turn meshes into
  STEP. Most gig titles say "STL/OBJ to STEP," not scanner output.
- Pro-tier: QuickSurface 94 resellers in ~35 countries; Backflip Aug
  4, 2026 covers "3D scans, STLs, and other mesh files."
- Trends JS-walled; Google autocomplete: "stl to step" → converter,
  online, free, solidworks, fusion 360, freecad; "3d scan to cad" →
  software/ai/service/free. Free converters (imagetostl.com: STL→STEP
  up to 500MB, 200-file batches, ~5 s) = naive tessellated conversion
  is a zero-price commodity; only true feature-tree reconstruction +
  accuracy report is defensible.

## 2. Iteration speed — workable
OrcaSlicer (15.5k stars) ships monthly stable + nightlies; HueForge
iterated publicly through 0.x via devlog/Discord. Scan files 50–500MB;
imagetostl proves 500MB browser uploads work and its 4-hour retention
defuses privacy worries. Scan-derived test data harder to crowdsource
(users guard proprietary/personal parts); multi-surface fitting to
noisy data is genuinely hard (HN: "very NP-hard"; "$5B/yr of manual
labor" framing). Verdict: iteration possible (web demo + Discord +
Fiverr-arbitrage dogfooding); algorithmic cycles are weeks, not days.

## 3. The reframe — STL→parametric is the bigger door, same tech
Every proxy agrees: mesh-to-parametric need is ~10–100x broader than
scan-specific. r/3Dprinting 100x r/3DScanning; Fiverr "stl to step" 10x
"reverse engineering 3d scan"; autocomplete shows everyman intent;
pullpush "stl to step" mentions across r/3Dprinting, r/Onshape,
r/functionalprint, r/forhire ("$50/hr to alter STL or STEP files") —
downloaded models people want to MODIFY, no scanner. Same core (mesh →
segmented primitives → feature tree) minus the noise/registration/
accuracy layer; clean STLs are the easier input, ideal for early
iteration; scan support = premium upsell. Backflip covers STLs too.

## 4. Frank verdict
Market meaningless? No — but the scan-first framing nearly is: a
tens-of-thousands-person market served by QuickSurface Personal (free),
Fiverr humans at $25, and a funded AI incumbent at $20/mo. Verifiable
paid demand (thousands of Fiverr transactions) is overwhelmingly
"convert/modify this mesh," source-agnostic.
Recommended pivot: "make this downloaded STL editable/parametric" for
the ~2M printing community (free tier → paid feature-tree export),
distributed on Printables/MakerWorld/r/3Dprinting with a web demo;
dogfood by fulfilling Fiverr gigs ourselves; add scan/accuracy layer
after the mesh core wins. Must articulate why we beat Backflip's
$20/mo web app on the hobbyist end (price, offline/privacy,
printing-specific features like "split into printable, editable
bodies") — or don't start.

Sources: amazon.com/s?k=3d+scanner, fiverr.com/search/gigs?query=stl
to step, subredditstats API, quicksurface.com/resellers, backflip.ai,
Bing News RSS, imagetostl.com, HN Algolia, api.pullpush.io, GitHub
API (OrcaSlicer), shop.thehueforge.com, Google autocomplete API.
Caveats: subreddit counts are 2022–23 snapshots; Trends unfetchable;
Fiverr result counts fuzzy-inflated — review counts are the trustworthy
core.
