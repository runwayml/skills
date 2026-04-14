# Marketing Video Script: Runway API Skills

**Duration:** 2:30  
**Format:** Screen recording with minimal voiceover  
**Goal:** Show an agent generating 20 product video ads from a single Shopify URL

---

## SCENE 1: The Hook (0:00 - 0:08)

**Visual:** Full-screen text on dark background, typed out character by character:

> "Generate a video ad for every product in your Shopify store."
> "One command. 20 videos. Zero production."

**Audio:** Subtle keyboard click sound effect.

---

## SCENE 2: Install (0:08 - 0:18)

**Visual:** Clean terminal. Type the install command.

```
$ npx skills add runwayml/skills
```

Show the skill list appearing, all selected, press Enter. Installation completes in 3 seconds.

**Voiceover:** "Install Runway API Skills in one command. Works with Claude Code, Cursor, and Codex."

---

## SCENE 3: Setup (0:18 - 0:28)

**Visual:** Set the API key.

```
$ export RUNWAYML_API_SECRET="rw_..."
```

**Voiceover:** "Set your API key. That's it -- you're ready."

---

## SCENE 4: The Ask (0:28 - 0:38)

**Visual:** Open Claude Code (or Cursor). Type the natural language prompt:

```
Generate a video ad for every product in my Shopify store
at demo-store.myshopify.com. Use gen4_turbo with the product
images. TikTok format (vertical). Save to output/shopify-ads/.
```

Press Enter. The agent starts working.

**Voiceover:** "Ask the agent to generate ads for your entire product catalog."

---

## SCENE 5: Agent Fetches Products (0:38 - 0:55)

**Visual:** The agent's output in the terminal, showing it working:

```
> Running: uv run scripts/shopify_products.py --store "demo-store.myshopify.com" --output products.json
  Fetched 20 products...
  Saved 20 products to /Users/demo/products.json
```

The agent reads the JSON, lists the products:
```
Found 20 products:
  1. Classic Canvas Sneaker ($89)
  2. Leather Weekender Bag ($245)
  3. Merino Wool Sweater ($135)
  ...
```

Then builds the pipeline:
```
> Writing pipeline to shopify-ads-pipeline.json
> Dry run first...
  Step 1 (fan_out x 20): generate_video [gen4_turbo] ~25 x 20 = ~500 credits
  Estimated total: ~500 credits
```

**Voiceover:** "The agent fetches every product from your store, reads the product data, and builds a batch pipeline."

---

## SCENE 6: Generation in Progress (0:55 - 1:25)

**Visual:** The pipeline runs. Speed up the recording (4x). Show the progress ticking:

```
> Running pipeline...

[Step 1/1] fan_out (gen4_turbo)
  --- fan_out 1/20 (parallel) ---
  [task_a1b2c3d4] PENDING (5s)...
  [task_a1b2c3d4] RUNNING (15s)...
  --- fan_out 2/20 (parallel) ---
  --- fan_out 3/20 (parallel) ---
  [task_a1b2c3d4] SUCCEEDED
  Saved: output/shopify-ads/product-ad-1.mp4
  Saved: output/shopify-ads/product-ad-2.mp4
  ...
  Saved: output/shopify-ads/product-ad-20.mp4

=== Pipeline Complete ===
  20 files saved
```

**Voiceover:** "20 products. 20 video ads. Generated in parallel. Each one uses the product's real image as the starting frame."

---

## SCENE 7: Show the Results (1:25 - 1:55)

**Visual:** Open Finder/file explorer. Show the `output/shopify-ads/` folder with 20 .mp4 files.

Play 4 of them in quick succession (5 seconds each, picture-in-picture layout showing 4 videos playing simultaneously):
- A sneaker ad (product rotating, studio lighting)
- A bag ad (camera orbit, leather texture)
- A sweater ad (lifestyle feel, warm tones)
- A watch ad (premium reveal, reflections)

**Voiceover:** "Every video is production-ready. Vertical format for TikTok and Reels. Starting from your actual product photos."

---

## SCENE 8: The Localization Demo (1:55 - 2:15)

**Visual:** Back in the terminal. Type another prompt:

```
Now localize the sneaker ad for New York, Tokyo, Paris, London, and Dubai.
```

The agent generates 5 city-specific variants. Show sped-up progress, then play 3 of the results:
- Sneaker with NYC skyline backdrop
- Sneaker with Tokyo neon lights
- Sneaker with Parisian architecture

**Voiceover:** "Same product, five markets. Each ad features local landmarks and atmosphere. Global campaign, zero location shoots."

---

## SCENE 9: CTA (2:15 - 2:30)

**Visual:** Dark background with clean text:

> **Runway API Skills**
> Agent-first media generation at scale.
>
> `npx skills add runwayml/skills`
>
> docs.dev.runwayml.com

**Voiceover:** "Runway API Skills. Install today. Generate everything."

---

## Production Notes

**Recording setup:**
- Screen recording at 4K, 60fps
- Use a clean terminal theme (dark background, monospace font)
- Speed up generation polling at 4x (the actual wait is 30-60 sec per video)
- Pre-generate the output videos so you can show real results

**Alternative shorter version (60 sec for Twitter/X):**
- Cut directly from install (Scene 2) to the ask (Scene 4) to results (Scene 7)
- Skip the agent's intermediate output
- Focus on: "One prompt. 20 videos." + playing the results

**Demo store:**
- Set up a Shopify dev store with 20 photogenic products
- Ensure each product has a high-quality featured image
- Categories: fashion, accessories, home goods (visually diverse)

**Key metrics to show on screen:**
- 20 products
- 20 videos
- ~500 credits ($X cost)
- < 10 minutes total generation time (with parallel execution)
