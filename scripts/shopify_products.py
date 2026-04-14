# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""Fetch all products from a Shopify store via the GraphQL Admin API."""

import argparse
import json
import os
import sys
import requests

PRODUCTS_QUERY = """
query ($cursor: String) {
  products(first: 50, after: $cursor) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        title
        descriptionHtml
        handle
        productType
        vendor
        tags
        featuredImage {
          url
          altText
        }
        images(first: 5) {
          edges {
            node {
              url
              altText
            }
          }
        }
        variants(first: 10) {
          edges {
            node {
              id
              title
              sku
              price
              inventoryQuantity
              image {
                url
              }
            }
          }
        }
      }
    }
  }
}
"""


def fetch_all_products(store, token):
    url = f"https://{store}/admin/api/2024-10/graphql.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": token,
    }

    products = []
    cursor = None

    while True:
        variables = {"cursor": cursor} if cursor else {}
        r = requests.post(url, headers=headers, json={"query": PRODUCTS_QUERY, "variables": variables})

        if not r.ok:
            print(f"Error: Shopify API returned {r.status_code}: {r.text[:500]}", file=sys.stderr)
            sys.exit(1)

        data = r.json()
        errors = data.get("errors")
        if errors:
            print(f"Error: GraphQL errors: {json.dumps(errors)}", file=sys.stderr)
            sys.exit(1)

        products_data = data["data"]["products"]
        for edge in products_data["edges"]:
            node = edge["node"]
            product = {
                "id": node["id"],
                "title": node["title"],
                "description": node.get("descriptionHtml", ""),
                "handle": node["handle"],
                "type": node.get("productType", ""),
                "vendor": node.get("vendor", ""),
                "tags": node.get("tags", []),
                "featured_image": node.get("featuredImage", {}).get("url") if node.get("featuredImage") else None,
                "images": [
                    {"url": img["node"]["url"], "alt": img["node"].get("altText", "")}
                    for img in node.get("images", {}).get("edges", [])
                ],
                "variants": [
                    {
                        "id": v["node"]["id"],
                        "title": v["node"]["title"],
                        "sku": v["node"].get("sku", ""),
                        "price": v["node"].get("price", ""),
                        "inventory": v["node"].get("inventoryQuantity"),
                        "image_url": v["node"].get("image", {}).get("url") if v["node"].get("image") else None,
                    }
                    for v in node.get("variants", {}).get("edges", [])
                ],
            }
            products.append(product)

        page_info = products_data["pageInfo"]
        print(f"  Fetched {len(products)} products...", file=sys.stderr)

        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]

    return products


def main():
    parser = argparse.ArgumentParser(description="Fetch all products from a Shopify store")
    parser.add_argument("--store", required=True, help="Shopify store domain (e.g. myshop.myshopify.com)")
    parser.add_argument("--token", help="Shopify Admin API access token (or set SHOPIFY_ACCESS_TOKEN)")
    parser.add_argument("--output", default="products.json", help="Output JSON file (default: products.json)")
    parser.add_argument("--output-dir", help="Output directory")
    args = parser.parse_args()

    token = args.token or os.environ.get("SHOPIFY_ACCESS_TOKEN")
    if not token:
        print(
            "Error: No Shopify token. Set SHOPIFY_ACCESS_TOKEN or pass --token.\n"
            "Create a custom app at https://<store>/admin/settings/apps/development",
            file=sys.stderr,
        )
        sys.exit(1)

    store = args.store
    if not store.endswith(".myshopify.com") and "." not in store:
        store = f"{store}.myshopify.com"

    print(f"Fetching products from {store}...", file=sys.stderr)
    products = fetch_all_products(store, token)

    out = args.output
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        out = os.path.join(args.output_dir, os.path.basename(out))

    with open(out, "w") as f:
        json.dump(products, f, indent=2)

    abs_path = os.path.abspath(out)
    print(abs_path)
    print(f"Saved {len(products)} products to {abs_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
