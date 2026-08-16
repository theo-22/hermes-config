---
name: Image Factory Mixed Replacement Batch Generation
description: Generate clean mixed-subject native-16:9 replacement candidates as separately described images without contaminating the image prompt with batch counts, exhibit language, replacement language, or workflow metadata.
owner: Image Factory
status: active
---

# Mixed Replacement Batch Generation

Use this when Ted asks Image Factory for another mixed batch of replacement candidates and wants the reliable generation technique proven on 2026-08-15.

## Core prompt shape

Describe every requested image independently and concretely, in sequence: “Make [subject A] …”, then “Make [subject B] …”, then “Make [subject C] …”. Each image description must stand alone as a complete photographic brief.

Do **not** mention the number of images anywhere in the generation prompt. Do not say “batch of four,” “four images,” “set,” “grid,” “collection,” or similar.

Do **not** mention exhibits, Image Factory, Museum, replacements, source assets, target filenames, categories, or workflow mechanics in the image-generation prompt. Those belong outside the visual request and can cause the generator to interpret the task as a composite presentation or UI/document layout.

## Visual brief for each image

- Native 16:9 landscape.
- One clear subject or coherent natural scene.
- Photorealistic or highly realistic unless Ted asks otherwise.
- Subject-forward, structure-first composition.
- Appropriate natural or controlled studio lighting.
- Background supports the subject without competing with it.
- No text, labels, borders, arrows, UI, montage, cards, captions, or decorative layout elements.
- For animals/plants/materials, preserve plausible anatomy, texture, coloration, and physical structure.

## Variation

Choose subjects from different visual families when making a mixed run: for example wildlife, mineral/material, botanical/food, underwater, landscape, or macro natural history. Avoid repeatedly choosing near-duplicates from the immediately prior run.

## Proven interaction pattern

Ted’s successful instruction: describe the requested images separately—“make X, and then make Y, and then make Z”—with no stated image count and no exhibit/workflow framing. Two consecutive native-16:9 runs produced individually rendered images that Ted accepted and saved in full.

Treat this as the preferred generation technique for mixed 16:9 replacement work unless a later test supersedes it.
