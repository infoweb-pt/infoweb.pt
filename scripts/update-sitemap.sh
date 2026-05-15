#!/bin/bash
# Auto-update sitemap.xml when new free tools are added
# Run this after adding a new free tool

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITEMAP="$REPO_ROOT/sitemap.xml"
BASE_URL="https://infoweb.sousadev.com"

echo "🗺️  Updating sitemap.xml..."

# Start XML
cat > "$SITEMAP" << 'XMLEOF'
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Homepage -->
  <url>
    <loc>https://infoweb.sousadev.com/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>

  <!-- Free Tools Hub -->
  <url>
    <loc>https://infoweb.sousadev.com/free-tools/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>

  <!-- Portuguese Hub -->
  <url>
    <loc>https://infoweb.sousadev.com/free-tools/pt/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
XMLEOF

# Function to add URL
add_url() {
    local path="$1"
    local priority="${2:-0.8}"
    echo "  <url>" >> "$SITEMAP"
    echo "    <loc>${BASE_URL}${path}</loc>" >> "$SITEMAP"
    echo "    <changefreq>monthly</changefreq>" >> "$SITEMAP"
    echo "    <priority>${priority}</priority>" >> "$SITEMAP"
    echo "  </url>" >> "$SITEMAP"
}

# Add English tools
echo "  <!-- Free Tools (English) -->" >> "$SITEMAP"
for dir in "$REPO_ROOT"/free-tools/*/; do
    # Skip pt/ directory and files
    [[ "$dir" == */pt/ ]] && continue
    [[ ! -d "$dir" ]] && continue
    # Check if it has an index.html
    [[ ! -f "$dir/index.html" ]] && continue
    slug=$(basename "$dir")
    # Skip non-tool directories
    [[ "$slug" == "index.html" ]] && continue
    add_url "/free-tools/${slug}/"
done

# Add Portuguese tools
echo "  <!-- Free Tools (Portuguese) -->" >> "$SITEMAP"
for dir in "$REPO_ROOT"/free-tools/pt/*/; do
    [[ ! -d "$dir" ]] && continue
    [[ ! -f "$dir/index.html" ]] && continue
    slug=$(basename "$dir")
    add_url "/free-tools/pt/${slug}/"
done

# Close XML
echo "</urlset>" >> "$SITEMAP"

echo "✅ Sitemap updated with $(grep -c '<loc>' "$SITEMAP") URLs"
echo "📄 $SITEMAP"