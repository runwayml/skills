---
name: rw-shopify-product-ads
description: "Generate a video ad for every product in a Shopify store. Fetches products via Shopify API, generates video ads via Runway API."
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(uv run *), Bash(command -v uv)
---

# Shopify Product Ads

Generate a video ad for every product in a Shopify store. This skill fetches all products from the Shopify GraphQL Admin API, then generates video ads using the Runway API in batch.

## Prerequisites

1. `command -v uv` must succeed
2. `RUNWAYML_API_SECRET` must be set (Runway API key)
3. `SHOPIFY_ACCESS_TOKEN` must be set (Shopify Admin API token)
4. The Shopify store domain (e.g. `myshop.myshopify.com`)

### Getting a Shopify Access Token

1. Go to the store's admin: `https://<store>/admin/settings/apps/development`
2. Create a custom app with `read_products` scope
3. Install the app and copy the Admin API access token

## Workflow

### Step 1: Fetch Products

```bash
uv run scripts/shopify_products.py --store "myshop.myshopify.com" --output products.json
```

This saves a JSON file with all products, including:
- Product title, description, handle
- Featured image URL
- All image URLs
- Variant SKUs and prices

### Step 2: Generate Prompts

For each product, craft a video prompt from the product data:

```
[Product title] -- professional product advertisement, [product type] showcase,
cinematic lighting, clean background, camera slowly reveals the product
```

Use the product's featured image as `--image-url` for image-to-video generation with `gen4_turbo` (fastest, cheapest) or `gen4.5` (highest quality).

### Step 3: Build Pipeline

Create a pipeline JSON with a fan_out step. Example for a store with products already fetched:

```json
{
  "steps": [{
    "action": "fan_out",
    "parallel": true,
    "sources": ["product-1-image-url", "product-2-image-url", "..."],
    "step": {
      "action": "generate_video",
      "model": "gen4.5",
      "prompt": "Professional product advertisement, camera slowly reveals the product, studio lighting, clean background",
      "ratio": "720:1280",
      "duration": 5,
      "filename": "product-ad-{i}"
    }
  }]
}
```

### Step 4: Run Pipeline

```bash
uv run scripts/batch_generate.py --pipeline shopify-ads.json --output-dir output/shopify-ads --max-parallel 3 --notify
```

### Step 5: Localize (Optional)

To generate localized variants for each product:

```json
{
  "steps": [{
    "action": "fan_out",
    "parallel": true,
    "sources": ["New York", "Tokyo", "London", "Paris", "Dubai"],
    "step": {
      "action": "generate_video",
      "model": "gen4.5",
      "prompt": "{{product_name}} advertisement set in {i}, local landmarks, cinematic",
      "ratio": "1280:720",
      "duration": 5,
      "filename": "{{product_handle}}-{i}"
    }
  }]
}
```

```bash
uv run scripts/batch_generate.py --pipeline localize.json --var product_name="Acme Serum" --var product_handle="acme-serum" --output-dir output/localized --notify
```

## Complete Example: End to End

When the user says "Generate a video ad for every product in my Shopify store":

1. **Fetch products:**
```bash
uv run scripts/shopify_products.py --store "myshop.myshopify.com" --output products.json
```

2. **Read products.json** to get product titles and featured image URLs

3. **For each product**, build a pipeline entry using the product's image as the source and a prompt based on the product title/description

4. **Write the pipeline JSON** to `shopify-ads-pipeline.json`

5. **Dry-run first** to estimate costs:
```bash
uv run scripts/batch_generate.py --pipeline shopify-ads-pipeline.json --dry-run
```

6. **Run the pipeline:**
```bash
uv run scripts/batch_generate.py --pipeline shopify-ads-pipeline.json --output-dir output/shopify-ads --max-parallel 3 --notify
```

7. **Report results** -- list all generated files with their product names

## Model Selection for Product Ads

- **`gen4_turbo`** (5 credits/sec) -- best value for product ads when you have product images. Requires `--image-url`.
- **`gen4.5`** (12 credits/sec) -- highest quality, works with or without images.
- **`veo3.1_fast`** (10-15 credits/sec) -- fast text-only generation when no product images available.

## Cost Planning

For a store with 50 products, generating 5-second video ads:
- `gen4_turbo`: 50 x 5 sec x 5 credits = **1,250 credits**
- `gen4.5`: 50 x 5 sec x 12 credits = **3,000 credits**
- `veo3.1_fast`: 50 x 5 sec x 10 credits = **2,500 credits**

Always run `--dry-run` first.

## Tips

- Use `gen4_turbo` with the product's featured image for the best quality-to-cost ratio
- Set `--max-parallel` based on your API tier's concurrency limit (Tier 1: 1-2, Tier 3: 5)
- Use `--resume` if the pipeline is interrupted
- For TikTok/Reels, use `--ratio 720:1280` (vertical). For YouTube, use `1280:720` (landscape).
