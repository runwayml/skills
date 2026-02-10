# Prompting Guide

## Core Principles

**Gen-4 thrives on simplicity.** Start with minimal prompts and iterate.

### Do's

- Describe single scenes (5-10 seconds max)
- Use clear physical descriptions
- Reference subjects generically: "the subject", "she", "he"
- Describe motion and camera movement explicitly

### Don'ts

- Avoid negative phrasing ("no blur", "without artifacts")
- Don't describe multiple scenes or cuts
- Don't use conceptual/abstract language

### Bad vs Good Examples

| Bad | Good |
|-----|------|
| "No camera movement" | "Locked camera. Static shot." |
| "The subject embodies joyful greeting" | "The woman smiles and waves." |
| "The tall man with black hair in a blue suit reaches out" | "The man extends his arm to shake hands." |

## Camera Movements

Use these terms for predictable camera motion:

| Movement | Description |
|----------|-------------|
| `push in` | Camera moves toward subject |
| `pull out` | Camera moves away from subject |
| `pan left/right` | Camera rotates horizontally |
| `tilt up/down` | Camera rotates vertically |
| `tracking shot` | Camera follows subject movement |
| `static` | No camera movement |
| `handheld` | Subtle realistic shake |
| `crane shot` | Vertical camera movement |
| `dolly` | Smooth horizontal movement |

## Prompt Structure

**Recommended formula:**

```
[subject motion] + [camera motion] + [scene motion] + [style descriptor]
```

**Example:**

```
The mechanical bull runs across the desert. A handheld camera tracks the movement. Dust trails behind the creature. Cinematic live-action.
```

## Example Prompts

### Good Prompts

```
"Camera slowly pushes in on the subject, wind gently moving her hair"

"A timelapse of clouds moving across a blue sky, static camera"

"The subject walks toward camera, tracking shot follows from behind"
```

### Bad Prompts

```
"A beautiful scene without any blur or artifacts"  # Negative phrasing

"First we see a mountain, then cut to a river, then to a bird"  # Multiple scenes

"An ethereal representation of human emotion"  # Too abstract
```

## Motion Intensity

Control motion amount with descriptive language:

- **Subtle**: "gentle breeze", "slight movement", "barely perceptible"
- **Moderate**: "steady motion", "natural movement"
- **Dynamic**: "rapid movement", "energetic", "dramatic"

## Style Transfer with References

When using reference images, describe how to apply the style:

```python
prompt_text="@subject painted in the bold brushstrokes and swirling patterns of @style"
```

Be specific about which visual elements to transfer (colors, textures, composition).

## Quick Reference

**Motion verbs:** walks, runs, turns, reaches, waves, nods, smiles, blinks, breathes, jumps, falls, rises, spins, gestures

**Camera terms:** locked, static, handheld, dolly, pan, tilt, tracking, crane, zoom, push in, pull back

**Speed modifiers:** slowly, gradually, quickly, suddenly, gently, smoothly

**Style terms:** cinematic, live-action, animated, dreamlike, documentary, stop-motion

## Links

- [Gen-4 Video Prompting Guide](https://help.runwayml.com/hc/en-us/articles/39789879462419)
- [Creating with Gen-4](https://help.runwayml.com/hc/en-us/articles/37327109429011)
- [Camera Control Guide](https://help.runwayml.com/hc/en-us/articles/34926468947347)
- [Aleph Prompting Guide](https://help.runwayml.com/hc/en-us/articles/43277392678803)
