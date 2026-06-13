# Manim Layout Policy

All scenes must prioritize readability over text density.

## Safe Zones

- Top Title Zone: one title only, near the top edge, never touching visuals.
- Secondary Text Zone: at most one short subtitle under the title.
- Main Visual Zone: primary visual occupies roughly 55-70% frame width or 45-65% frame height.
- Side Annotation Zone: only short notes, labels, or legends.
- Bottom Formula / Caption Zone: formulas and captions live near the bottom, never over the main diagram.

## Hard Rules

- Do not overlap title, subtitle, formula, caption, label, annotation, or main visual.
- Do not show more than three labels at the same time unless they are widely separated.
- Prefer sequential reveal over dense simultaneous labels.
- If a label is longer than five words, move it to a side panel or voiceover.
- If the main visual is too small, scale it before adding more text.
- If content cannot fit cleanly, split it into multiple beats or scenes.

## Implementation

- Use `safe_layout.py` helpers for new or revised scenes:
  - `place_title`
  - `place_secondary`
  - `fit_main_visual`
  - `fit_split_layout`
  - `place_formula`
  - `place_caption`
- `VisualBeatScene` and `EduScene` already use the shared layout helpers.
- Hand-authored scenes should wrap their main diagram group with `fit_main_visual(...)`
  before the first animation that introduces the group.

## Acceptance

A scene is not acceptable if:

- the title touches or overlaps a visual,
- text crosses a shape, node, box, or connector,
- labels overlap each other,
- a formula sits on top of the diagram,
- the main visual is visibly tiny while the frame has large unused space.
