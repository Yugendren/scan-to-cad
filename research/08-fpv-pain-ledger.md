# 08 — FPV customer pain ledger (2026-09-02)

Method: 24 searches by a research agent. Purpose: customer-perspective
pain evidence in the FPV community. Kept as benchmark vertical (P5 in
the Pain Ledger).

## Pain 1 — tuning/vibration hell (deepest, most monetized)
IntoFPV threads read like therapy: quads "fly away at the slightest
encounter of propwash"; "a lot of wasted hours troubleshooting."
Community wisdom defeatist ("Perfect propwash-free freestyle on 5" is
a gradient, not a checkbox"). FPVTune founder: "Record a flight, pull
the blackbox log, open PIDtoolbox, stare at gyro traces for an hour,
change one number, fly again… repeat forever" — ~15 interacting
parameters; copied Discord tunes fail on hardware differences.
Frequency: universal, chronic; most pilots never do blackbox analysis
(EmuFlight's pitch; Betaflight presets; Oscar Liang: "you can never get
filtering perfect").
Paid: Fiverr PID tuning $30/$40/$50; eBay "CUSTOM Quad Tuning PRO
LEVEL"; SupaFly FPV paid tunes; PIDtoolbox author 1:1 sessions;
FPVTune $9.90/analysis; Chris Rosser Patreon + Betaflight course + a
2026.06 chirp-tuning course. "Do it for me" tuning = real cottage
industry at $10–50.

## Pain 2 — DJI O4 Pro gyro scandal (Aug 2026)
DJI silently swapped the O4 Pro's MP66 gyro for the cheaper 1469D in
Feb-2026 units; Gyroflow stabilization "broken"; "do not buy" panic.
Workarounds: Gyroflow complementary integration + 5 Hz LPF; units in
frames with proper soft-mount platforms (Flywoo Firefly) showed zero
jello. Signal: mount design quality now determines whether a $250 air
unit works — a printed-part fix for an electronics pain.

## Pain 3 — printed-parts failure normalized
"A camera mount that snaps on the first pack wasn't designed wrong — it
was designed for the wrong material"; 2mm TPU arms flex; sharp internal
corners crack. Long-tail hunt on Printables/Thingiverse (frame × camera
× angle); paid STLs on Gumroad; pre-printed TPU mounts $10–20/pair on
eBay/Etsy; "can someone design X for my frame" requests scattered
across Discords.

## Pain 4 — industry shipped auto-tuning, half-baked (Aug–Sept 2026)
Betaflight 2026.6 (CalVer) ships an Autotune tab: chirp test flight →
closed-loop frequency response (Welch) from blackbox → recommended
slider values, one-button apply. Gated behind Expert Mode; issue #5258
reports instability/flyaway on arm; community verdict "excellent as a
measurement tool, dangerous as a one-click fix." Nobody sells
custom-tuned hardware at scale; the trusted-application gap is where
FPVTune, Fiverr tuners, and Rosser's courses live.

## Pain 5 — adjacent niches with the same loop
INAV fixed-wing (over-parameterization complaints, autotune "may never
succeed"); rocketry (Eggtimer/Altus Metrum telemetry + printed AV bays;
design contests); combat robots (printed antweights mainstream; no
telemetry-tuning equivalent).

## Bottom line
FPV already pays $10–50 repeatedly for tuning outcomes and $10–20 for
frame-specific TPU parts; the O4 Pro fiasco fused vibration and
mounting pains; Betaflight's Autotune legitimized automated tuning
while leaving the safe one-click experience unclaimed.

Sources: IntoFPV threads, FPV Grind, dev.to/fpvtune, EmuFlight wiki,
Oscar Liang (blackbox guide; O4 Pro issue; 2026.6), Fiverr gigs, eBay
listing 326361863951, SupaFly FPV, FPVTune.com, AOS RC Thinkific,
Unmanned Tech blog, LUCEED FPV, UAVMODEL 2026 guide, Betaflight
2026.6 release notes, configurator issue #5258, GitHub
betaflight-pid-autotuning, inav issue #9392, RocketryForum,
Printables (antweight bot).
