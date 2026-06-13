# Audio Sync Policy

Audio is the master timeline. Animation must follow the narration, not the other
way around.

## Hard Rules

- Visuals must not appear before the narration reaches the matching idea.
- Main visuals, labels, formulas, and diagrams must not disappear while narration
  is still explaining them.
- Do not fade out the whole scene at the end of a narrated scene.
- Do not leave the last narrated seconds on an empty background.
- Do not use `self.clear()` during narrated content.
- Scene transitions belong after the narration block, or inside an intentional
  silent gap.

## Required Final State

Each scene must end on a stable final visual state. If audio padding is needed,
`fit_audio_sync.py` may extend that final frame, so the final frame must contain
the scene's concluding visual, not a blank background.

## Allowed End Pattern

```python
self.play(Indicate(main_visual), run_time=1.0)
self.wait(1.0)  # Hold final visual state through audio end
```

## Disallowed End Pattern

```python
self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
```

## Future Voiceover Scenes

For new scenes using `manim-voiceover`, split narration into blocks and drive
animation inside each tracker:

```python
with self.voiceover(text="...") as tracker:
    total = tracker.duration
    self.play(FadeIn(visual), run_time=total * 0.25)
    self.play(Indicate(key_part), run_time=total * 0.25)
    self.wait(total * 0.50)

self.play(FadeOut(visual), run_time=0.5)  # only after the block
```

For existing scenes with audio files only, create or inspect a timing table:

| Start | End | Audio content | Visual allowed | Animation | Hold visual until |
|---|---|---|---|---|---|

The `Hold visual until` timestamp must be at least the end of the relevant audio
idea.
