# DualSense: phone scan vs reference scans (108.3 s)

Spec (sorted): [160.0, 106.0, 66.0] mm

Phone scan bbox: [158.01, 108.6, 56.46] (minus spec: [-1.99, 2.6, -9.54])

- ref kabliga: 149982 faces, bbox [160.51, 112.35, 60.57] (minus spec [0.51, 6.35, -5.43]), watertight=False
- ref v3design: 150000 faces, bbox [159.69, 109.28, 60.45] (minus spec [-0.31, 3.28, -5.55]), watertight=True
- ref printables1508424: 143132 faces, bbox [159.65, 105.75, 65.77] (minus spec [-0.35, -0.25, -0.23]), watertight=True

## Phone vs reference (rigid alignment, mm)
- vs kabliga: median 2.932, p95 7.104, max 13.199, >0.5mm 93%, >1mm 86%; best-fit scale 0.9189 → phone scale error 8.82%
- vs v3design: median 2.896, p95 6.796, max 12.836, >0.5mm 91%, >1mm 81%; best-fit scale 0.9279 → phone scale error 7.77%
- vs printables1508424: median 2.957, p95 7.028, max 12.621, >0.5mm 90%, >1mm 82%; best-fit scale 0.9292 → phone scale error 7.62%

## Reference vs reference (consensus quality, mm)
- kabliga_vs_v3design: median 0.15, p95 0.569, max 3.576, >0.5mm 8%
- kabliga_vs_printables1508424: median 0.177, p95 0.589, max 7.313, >0.5mm 7%
