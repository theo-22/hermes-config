---
name: image-factory-mixed-replacement-batch-generation
description: Generate clean mixed-subject native-16:9 collection or replacement candidates from one operator request while keeping every image-generation request isolated from batch counts, neighboring subjects, exhibit language, replacement language, and workflow metadata.
metadata:
  category: gpt
  write_mode: none
  one_line_use: compose independent mixed-subject native-16:9 image briefs
  fast_pick: "yes"
  owner: Image Factory
  status: active
---

# Mixed Collection Batch Generation

Use this when Ted asks Image Factory for a mixed batch of up to ten new images,
including the older replacement use case. New collection generation is the
default; use replacement framing only when Ted explicitly names predecessors.

## Operator order versus generator request

The operator-level work order may contain the numbered subjects together so
Image Factory can execute them in one bounded run. It must explicitly require
one independent image-generation request per subject. The count and workflow
instruction stay at this operator layer; they do not pass into any individual
generator request.

Ten-image operator frame proposed 2026-09-03, extending the six-image frame
incorporated after the 2026-09-01 affected Image Factory hearing:

> Generate ten images by making exactly ten independent native 16:9 image-generation requests, one for each numbered subject, in numbered order. Each request must contain only that subject's literal visual description and must produce one standalone image. Do not combine subjects into one generation request or create a collage, contact sheet, grid, or composite. Present all ten outputs separately, in numbered order, so each can be downloaded independently.

Disposition: `pending affected-GPT hearing` for the count increase and new
Collection Generation mode. The isolation boundary itself remains incorporated.

The installed worker may recognize the prior operator frame only when recovering
an already-completed, exact-subject browser turn. It must never use that legacy
frame for a new generation send.

## Core prompt shape

Describe every requested image independently and concretely, in sequence: “Make [subject A] …”, then “Make [subject B] …”, then “Make [subject C] …”. Each image description must stand alone as a complete photographic brief.

Do **not** mention the number of images anywhere in an individual generator
request. Do not say “batch of four,” “four images,” “set,” “grid,” “collection,”
or similar. A count is allowed only in the operator-level work order that tells
Image Factory how many independent requests to execute.

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

Choose subjects from different visual families when making a mixed run. For a
ten-image delegated roster, use no more than two subjects from one broad family,
avoid exact repeats from the prior 30 images, and cap the predictable defaults:
at most one marine/kelp/reef/bioluminescent subject and at most one common
produce macro such as red onion. Maintain this roster outside the generator.

## Proven interaction pattern

Ted’s successful instruction: describe the requested images separately—“make X, and then make Y, and then make Z”—with no stated image count and no exhibit/workflow framing. Two consecutive native-16:9 runs produced individually rendered images that Ted accepted and saved in full.

Treat this as the preferred generation technique for mixed 16:9 collection work unless a later test supersedes it.
