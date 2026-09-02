# Gate 0 data plan — where the 20 verified scans come from

The verification recipe per part: (physical part with known geometry)
+ (one real prosumer scan of it) + (caliper spot-checks). Ground truth
never comes from the scan itself.

## Part sourcing — four tiers, ~$150 total + $25 calipers

1. **Manufacturer-CAD parts (~8 parts).** Off-the-shelf hardware that
   ships with official STEP files: 2020 V-slot extrusion offcut, NEMA17
   stepper, KFL08/KP08 flange bearing, shaft coupler, corner brackets,
   GT2 pulley, DIN rail + clip. Ground truth = the manufacturer STEP
   (spot-checked with calipers, since clones deviate). Strongest tier:
   full reference CAD, not just dimensions.
2. **Machinist references (~4 parts).** 123 block, parallel, V-block,
   drill bushing. Certified flat/square/dimensioned to hundredths —
   ideal for testing plane/angle/symmetry snapping in isolation.
3. **Made-from-known-CAD (~4 parts).** Parts we design and have printed
   or cheaply CNC'd. Ground truth = calipers on the physical part (a
   print deviates from its CAD, so the CAD is the *intent* reference
   and calipers are the *dimension* reference — this tier is the only
   one that tests intent recovery where intent is perfectly known).
4. **Real-world messy parts (~4 parts).** The friend's actual broken
   brackets/mounts — no CAD exists, caliper-only key dimensions. The
   realistic cases; expected hardest; they keep the benchmark honest.

## Ground-truth protocol

Per part: choose 5–15 key dimensions (bore diameters, hole spacings,
thicknesses, overall envelope), measure with digital calipers
(±0.02 mm, ~$25), record in the manifest with per-dimension tolerance.
For tier-1/3 parts also attach the reference STEP. Manifest is frozen
with the gauntlet.

## Scan acquisition

- Primary: one session on the friend's prosumer scanner — all 20 parts
  in an afternoon; raw output only (no vendor cleanup), export mesh +
  point cloud. Record scanner model/settings per scan (seeds the
  per-scanner noise model later).
- Fallback/parallel: vendor sample scans and community-shared scans
  (real noise, usually no ground truth) go to DEV, never gauntlet.
- If neither materializes: used Revopoint/Creality unit (~$300–600) —
  needed eventually anyway for the noise-model flywheel.

## What each verification layer checks

- Fidelity: reconstruction vs caliper truth (per-dimension tolerance).
- Deviation certificate: reconstruction vs the raw scan (heatmap,
  self-consistency — catches hallucinated surfaces).
- Intent (tier 1/3 only): recovered feature structure vs reference
  STEP — did it find the same planes/bores/symmetry, not just close
  surfaces.
- Editability: kernel executes the emitted build123d; STEP re-imports
  cleanly.
