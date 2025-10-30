#!/usr/bin/env python3
"""
Download images and icons from Figma design file.

Usage:
    1. Get your Figma personal access token from: https://www.figma.com/settings
    2. Set environment variable: export FIGMA_TOKEN="your-token-here"
    3. Run: python3 download_figma_assets.py
"""

import os
import sys
from pathlib import Path

import requests

# Configuration
FILE_KEY = "2qlSGUeAZO0Mp2ZxTTu9nF"
NODE_ID = "34:1491"
OUTPUT_DIR = Path("figma_images")

# Get Figma token from environment
FIGMA_TOKEN = os.getenv("FIGMA_TOKEN", "")

if not FIGMA_TOKEN:
    print("❌ Error: FIGMA_TOKEN environment variable not set")
    print("\n📝 To get your token:")
    print("   1. Visit: https://www.figma.com/settings")
    print("   2. Scroll to 'Personal access tokens'")
    print("   3. Generate a new token")
    print("   4. Run: export FIGMA_TOKEN='your-token-here'")
    print("   5. Run this script again")
    sys.exit(1)

HEADERS = {"X-Figma-Token": FIGMA_TOKEN}


def get_node_data(file_key: str, node_id: str) -> dict:
    """Fetch node data from Figma API."""
    url = f"https://api.figma.com/v1/files/{file_key}/nodes"
    params = {"ids": node_id}

    print(f"🔍 Fetching node data for {node_id}...")
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"❌ Error {response.status_code}: {response.text}")
        sys.exit(1)

    return response.json()


def find_image_nodes(node: dict, images: list[dict], path: str = "") -> None:
    """Recursively find all image nodes in the design tree."""
    node_type = node.get("type", "")
    node_name = node.get("name", "Unnamed")
    current_path = f"{path}/{node_name}" if path else node_name

    # Check if this node contains an image or is an exportable component
    if node_type in ["RECTANGLE", "FRAME", "COMPONENT", "INSTANCE", "GROUP"]:
        # Check for image fills
        fills = node.get("fills", [])
        for fill in fills:
            if fill.get("type") == "IMAGE":
                images.append(
                    {
                        "id": node.get("id"),
                        "name": node_name,
                        "path": current_path,
                        "type": "image_fill",
                    }
                )
                break

    # For frames and components, also add them as exportable
    if node_type in ["FRAME", "COMPONENT", "INSTANCE"] and "children" in node:
        images.append(
            {
                "id": node.get("id"),
                "name": node_name,
                "path": current_path,
                "type": node_type.lower(),
            }
        )

    # Recurse into children
    if "children" in node:
        for child in node["children"]:
            find_image_nodes(child, images, current_path)


def export_images(
    file_key: str, node_ids: list[str], format: str = "png", scale: int = 2
) -> dict:
    """Export images from Figma."""
    url = f"https://api.figma.com/v1/images/{file_key}"
    params = {"ids": ",".join(node_ids), "format": format, "scale": scale}

    print(f"📥 Requesting export for {len(node_ids)} nodes...")
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"❌ Export error {response.status_code}: {response.text}")
        return {}

    return response.json()


def download_image(url: str, filepath: Path) -> bool:
    """Download image from URL to file."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filepath.write_bytes(response.content)
            return True
        return False
    except Exception as e:
        print(f"❌ Error downloading {filepath.name}: {e}")
        return False


def sanitize_filename(name: str) -> str:
    """Convert name to valid filename."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, "_")
    name = name.strip(". ")
    return name or "unnamed"


def main():
    """Main execution function."""
    print("🎨 Figma Asset Downloader")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print(f"🔑 File: {FILE_KEY}")
    print(f"🎯 Node: {NODE_ID}\n")

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Get node data
    data = get_node_data(FILE_KEY, NODE_ID)

    # Extract node information
    nodes = data.get("nodes", {})
    if not nodes:
        print("❌ No nodes found")
        sys.exit(1)

    node_data = nodes.get(NODE_ID, {})
    if not node_data:
        print(f"❌ Node {NODE_ID} not found")
        sys.exit(1)

    document = node_data.get("document", {})

    # Find all image nodes
    images = []
    find_image_nodes(document, images)

    print(f"✅ Found {len(images)} exportable nodes\n")

    if not images:
        print("ℹ️  No images found in this section")
        return

    # Show what we found
    print("📋 Nodes to export:")
    for i, img in enumerate(images, 1):
        print(f"   {i}. {img['name']} ({img['type']})")
    print()

    # Export images
    node_ids = [img["id"] for img in images]
    export_data = export_images(FILE_KEY, node_ids)

    if "err" in export_data:
        print(f"❌ Export error: {export_data['err']}")
        sys.exit(1)

    image_urls = export_data.get("images", {})

    # Download each image
    print("💾 Downloading images...")
    success_count = 0

    for img in images:
        node_id = img["id"]
        url = image_urls.get(node_id)

        if not url:
            print(f"⚠️  No URL for {img['name']}")
            continue

        # Create filename
        safe_name = sanitize_filename(img["name"])
        filename = f"{safe_name}.png"
        filepath = OUTPUT_DIR / filename

        # Handle duplicate filenames
        counter = 1
        while filepath.exists():
            filename = f"{safe_name}_{counter}.png"
            filepath = OUTPUT_DIR / filename
            counter += 1

        # Download
        if download_image(url, filepath):
            print(f"   ✅ {filename}")
            success_count += 1
        else:
            print(f"   ❌ Failed: {filename}")

    print(
        f"\n🎉 Done! Downloaded {success_count}/{len(images)} images to {OUTPUT_DIR}/"
    )


if __name__ == "__main__":
    main()
