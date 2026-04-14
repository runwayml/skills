# Runway API -- Cookbook

Real-world recipes that show what's possible when you combine AI agent reasoning with Runway's generation API. Each recipe is a complete, runnable example.

---

## Recipe 1 -- 100 Product Ads from a Shopify Store

**What it does:** Give the agent a Shopify store URL. It fetches every product, crafts a video prompt from each product's title and image, then generates a video ad for every single SKU.

**Why this is powerful:** One URL in, full product video catalog out. Replaces weeks of creative production.

**What you say to the agent:**
```
Generate a video ad for every product in my Shopify store at myshop.myshopify.com.
Use gen4_turbo with the product images. Save to output/shopify-ads/.
```

**Step 1 -- Fetch all products:**
```bash
uv run scripts/shopify_products.py --store "myshop.myshopify.com" --output products.json
```

**Step 2 -- The agent reads products.json, extracts titles and featured images, then builds a pipeline:**

```json
{
  "steps": [{
    "action": "fan_out",
    "parallel": true,
    "sources": [
      "https://cdn.shopify.com/product-1.jpg",
      "https://cdn.shopify.com/product-2.jpg",
      "https://cdn.shopify.com/product-3.jpg"
    ],
    "step": {
      "action": "generate_video",
      "model": "gen4_turbo",
      "prompt": "Professional product advertisement, camera slowly reveals the product with a gentle orbit, studio lighting, clean white background, premium feel",
      "ratio": "720:1280",
      "duration": 5,
      "filename": "product-ad-{i}"
    }
  }]
}
```

**Step 3 -- Estimate cost, then run:**
```bash
uv run scripts/batch_generate.py --pipeline shopify-ads.json --dry-run
uv run scripts/batch_generate.py --pipeline shopify-ads.json --output-dir output/shopify-ads --max-parallel 3 --notify
```

**Cost planning:**
- 50 products x 5 sec x 5 credits/sec (gen4_turbo) = **1,250 credits**
- 50 products x 5 sec x 12 credits/sec (gen4.5) = **3,000 credits**

**Tips:**
- `gen4_turbo` requires an image but is the cheapest video model -- perfect for product ads
- Use `--max-parallel` based on your API tier (Tier 1: 1-2, Tier 3: 5)
- If interrupted, re-run with `--resume` to pick up where you left off

---

## Recipe 2 -- Localized Campaign: Same Product, 50 Cities

**What it does:** Take a single product and generate video ads set in different cities around the world. Each ad features local landmarks and atmosphere.

**Why this is powerful:** Global ad campaigns usually require location shoots or expensive CGI. This generates city-specific creatives programmatically.

**What you say to the agent:**
```
Generate a video ad for Acme Watch localized for every major city:
New York, Tokyo, London, Paris, Dubai, Sydney, Mumbai, Berlin, Sao Paulo, Seoul,
Singapore, Toronto, Amsterdam, Barcelona, Milan. Use gen4.5, 1280:720, 5 seconds.
```

**Pipeline -- localize.json:**
```json
{
  "steps": [{
    "action": "fan_out",
    "parallel": true,
    "sources": [
      "New York", "Tokyo", "London", "Paris", "Dubai",
      "Sydney", "Mumbai", "Berlin", "Sao Paulo", "Seoul",
      "Singapore", "Toronto", "Amsterdam", "Barcelona", "Milan"
    ],
    "step": {
      "action": "generate_video",
      "model": "gen4.5",
      "prompt": "{{product}} advertisement set in {i}, iconic local architecture in background, golden hour cinematic lighting, premium product showcase",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "{{product_handle}}-{i}"
    }
  }]
}
```

```bash
uv run scripts/batch_generate.py --pipeline localize.json \
  --var product="Acme Watch" \
  --var product_handle="acme-watch" \
  --output-dir output/localized \
  --max-parallel 5 \
  --notify
```

**Cost:** 15 cities x 5 sec x 12 credits/sec = **900 credits**

**Tips:**
- Include the city name in the prompt, not just "city {i}" -- the model generates better results with specific city names
- For multi-language voiceovers, chain with `generate_audio --type tts` for each language
- Use `--dry-run` first to verify the total cost

---

## Recipe 3 -- Product Photo to Video Pipeline

**What it does:** Take a product photo (what every brand already has), generate a hero image variation, then animate it into a cinematic video reveal.

**Why this is powerful:** Turns any existing product photo into a polished video ad with zero production.

**What you say to the agent:**
```
Take this product image and create a cinematic reveal video.
Image: https://cdn.example.com/product-hero.jpg
```

**Pipeline -- product-to-video.json:**
```json
{
  "steps": [
    {
      "action": "generate_video",
      "model": "gen4_turbo",
      "image_url": "{{product_image}}",
      "prompt": "Camera slowly orbits the product revealing every angle, studio lighting with subtle highlights, premium product showcase, smooth motion",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "product-orbit"
    },
    {
      "action": "generate_video",
      "model": "gen4.5",
      "image_url": "{{product_image}}",
      "prompt": "Dramatic product reveal: product emerges from darkness into spotlight, cinematic, premium feel",
      "ratio": "720:1280",
      "duration": 5,
      "filename": "product-reveal-vertical"
    }
  ]
}
```

```bash
uv run scripts/batch_generate.py --pipeline product-to-video.json \
  --var product_image="https://cdn.example.com/product-hero.jpg" \
  --output-dir output/product-videos
```

**For batch product photos (5 products, 2 variants each = 10 videos):**
```json
{
  "steps": [{
    "action": "fan_out",
    "parallel": true,
    "sources": [
      "https://cdn.example.com/product-1.jpg",
      "https://cdn.example.com/product-2.jpg",
      "https://cdn.example.com/product-3.jpg",
      "https://cdn.example.com/product-4.jpg",
      "https://cdn.example.com/product-5.jpg"
    ],
    "step": {
      "action": "generate_video",
      "model": "gen4_turbo",
      "prompt": "Cinematic product reveal, camera orbit, studio lighting, clean background",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "product-video-{i}"
    }
  }]
}
```

---

## Recipe 4 -- Storyboard to Video Ad

**What it does:** Write a multi-scene script, generate an image for each scene, then animate each image into a video clip. Produces a complete narrative ad from text alone.

**Why this is powerful:** Go from a creative brief to a produced video ad without a camera, crew, or editing software.

**What you say to the agent:**
```
Produce a 30-second ad for Acme Skincare with this script:
Scene 1: Person looking frustrated at their skin in a mirror
Scene 2: They discover the Acme Serum on their phone
Scene 3: Close-up of the elegant serum bottle
Scene 4: Person applying the serum, smiling
Scene 5: Before/after transformation
Scene 6: Product on clean background with logo
```

**Pipeline -- storyboard.json:**
```json
{
  "steps": [
    {
      "action": "generate_image",
      "model": "gen4_image",
      "prompt": "Person looking frustrated at their skin in bathroom mirror, cinematic 16:9, warm indoor lighting",
      "ratio": "1280:720",
      "filename": "scene-1-frame"
    },
    {
      "action": "generate_video",
      "use_previous": true,
      "model": "gen4.5",
      "prompt": "Person sighs and touches their face, looks concerned, ambient bathroom sounds",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "scene-1-clip"
    },
    {
      "action": "generate_image",
      "model": "gen4_image",
      "prompt": "Close-up of elegant skincare serum bottle, frosted glass, studio lighting, product photography",
      "ratio": "1280:720",
      "filename": "scene-3-frame"
    },
    {
      "action": "generate_video",
      "use_previous": true,
      "model": "gen4.5",
      "prompt": "Camera slowly orbits the serum bottle, light reflections dance across the glass, premium reveal",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "scene-3-clip"
    }
  ]
}
```

**Assemble with ffmpeg after generation:**
```bash
ls output/storyboard/scene-*-clip.mp4 | sort > clips.txt
ffmpeg -f concat -safe 0 -i <(awk '{print "file \x27" $0 "\x27"}' clips.txt) -c copy output/final-ad.mp4
```

**Tips:**
- Write motion prompts that describe *camera movement* and *action*, not just the scene
- Keep scene prompts consistent: same character description, lighting style, color grading
- Use `gen4_image` for frames (highest quality stills), `gen4.5` for animation

---

## Recipe 5 -- Data-Driven Creative Iteration

**What it does:** Generate many ad variants, measure performance, then regenerate winners with targeted variations. Programmatic creative optimization.

**Why this is powerful:** Most creative iteration is a guess. This makes it a system.

**Phase 1 -- Generate 20 variants:**

```json
{
  "steps": [{
    "action": "fan_out",
    "parallel": true,
    "sources": ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"],
    "step": {
      "action": "generate_video",
      "model": "veo3.1_fast",
      "prompt": "{{product}} creative variant {i} -- each with unique mood, lighting, composition, and camera angle",
      "ratio": "720:1280",
      "duration": 5,
      "filename": "variant-{i}"
    }
  }]
}
```

```bash
uv run scripts/batch_generate.py --pipeline variants.json --var product="Acme Serum" --output-dir output/round-1 --notify
```

**Cost:** 20 x 5 sec x 10 credits/sec (veo3.1_fast) = **1,000 credits** for 20 variants

**Phase 2 -- After measuring performance (CTR, thumbstop rate), tell the agent:**

```
Variants 3, 7, and 12 performed best. Generate 10 new variations for each winner:
vary the lighting (warm/cool/dramatic), background (studio/outdoor/abstract),
and camera movement (orbit/zoom/pan).
```

The agent generates 30 targeted variants based on the winning creative direction.

**Phase 3 -- Final production quality:**

Switch the winning variant to `gen4.5` for maximum quality:

```bash
uv run scripts/generate_video.py \
  --prompt "Same composition as winning variant, cinematic quality, 4K feel" \
  --model gen4.5 \
  --duration 10 \
  --filename "final-winner.mp4"
```

**Tips:**
- Start with `veo3.1_fast` (cheapest) to explore the creative space
- Only use `gen4.5` or `veo3` for the final winning variants
- Track variants in a `variants-log.json` alongside generations
- The most impactful variable to test is usually the *creative angle* (what story the video tells), not the model

---

## Quick Reference

| Goal | Recipe | Recommended Model | Est. Credits |
|------|--------|-------------------|--------------|
| Catalog all products | #1 Shopify Ads | `gen4_turbo` | 25/product |
| Global localization | #2 City Variants | `gen4.5` | 60/city |
| Product photo to video | #3 Photo Pipeline | `gen4_turbo` | 25/video |
| Narrative video ad | #4 Storyboard | `gen4.5` | 60/scene |
| Find winning creative | #5 Iteration | `veo3.1_fast` | 50/variant |
