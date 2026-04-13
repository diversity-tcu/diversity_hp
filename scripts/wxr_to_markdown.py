#!/usr/bin/env python3
"""Convert WordPress WXR export XML into Astro content collection Markdown files."""
import os
import re
import sys
from pathlib import Path
from lxml import etree

try:
    from markdownify import markdownify as md
    HAS_MD = True
except Exception:
    HAS_MD = False

BASE = Path("/home/sekiguchi/GitHub/diversity_hp")
XML_PATH = BASE / "WordPress.2026-04-13.xml"
OUT_DIRS = {
    "page": BASE / "src/content/pages",
    "news": BASE / "src/content/news",
    "events": BASE / "src/content/events",
}

NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}

SITE = "https://www.diversity.tcu.ac.jp"


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^\w\-\.]+", "-", name, flags=re.UNICODE)
    name = name.strip("-._")
    return name or "untitled"


def clean_html(html: str) -> str:
    if not html:
        return ""
    # Strip WordPress block comments
    html = re.sub(r"<!--\s*/?wp:[^>]*?-->", "", html)
    html = re.sub(r"<!--\s*more\s*-->", "", html)
    # Replace image/internal URLs
    html = html.replace(f"{SITE}/wp-content/uploads", "/uploads")
    html = html.replace("http://www.diversity.tcu.ac.jp/wp-content/uploads", "/uploads")
    html = html.replace(SITE, "")
    html = html.replace("http://www.diversity.tcu.ac.jp", "")
    return html


def html_to_md(html: str) -> str:
    html = clean_html(html)
    if not html.strip():
        return ""
    if HAS_MD:
        try:
            out = md(html, heading_style="ATX", bullets="-")
            # collapse excessive blank lines
            out = re.sub(r"\n{3,}", "\n\n", out)
            return out.strip() + "\n"
        except Exception:
            return html
    return html


def yaml_escape(s: str) -> str:
    if s is None:
        s = ""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def text_of(item, xpath, default=""):
    r = item.xpath(xpath, namespaces=NS)
    if not r:
        return default
    v = r[0]
    if hasattr(v, "text"):
        return v.text or default
    return v or default


def main():
    counts = {"page": 0, "news": 0, "events": 0}
    other_types = {}

    ctx = etree.iterparse(str(XML_PATH), events=("end",), tag="item")
    for _, item in ctx:
        post_type = text_of(item, "wp:post_type/text()")
        status = text_of(item, "wp:status/text()")
        if post_type not in OUT_DIRS or status != "publish":
            if post_type and post_type not in OUT_DIRS:
                other_types[post_type] = other_types.get(post_type, 0) + 1
            item.clear()
            continue

        title = text_of(item, "title/text()", "")
        slug = text_of(item, "wp:post_name/text()", "")
        post_id = text_of(item, "wp:post_id/text()", "")
        pub_date = text_of(item, "wp:post_date/text()", "")
        date_only = pub_date.split(" ")[0] if pub_date else ""
        author = text_of(item, "dc:creator/text()", "")
        link = text_of(item, "link/text()", "")
        content_html = text_of(item, "content:encoded/text()", "")

        if not slug:
            slug = post_id or sanitize_filename(title)
        # slug may be URL-encoded Japanese; keep as-is but sanitize for filename
        filename = sanitize_filename(slug) + ".md"

        body = html_to_md(content_html)

        frontmatter = (
            "---\n"
            f'title: "{yaml_escape(title)}"\n'
            f'slug: "{yaml_escape(slug)}"\n'
            f'date: "{date_only}"\n'
            f'author: "{yaml_escape(author)}"\n'
            f'original_url: "{yaml_escape(link)}"\n'
            f'status: "publish"\n'
            "---\n\n"
        )

        out_path = OUT_DIRS[post_type] / filename
        # Handle duplicate filenames
        if out_path.exists():
            out_path = OUT_DIRS[post_type] / f"{sanitize_filename(slug)}-{post_id}.md"

        out_path.write_text(frontmatter + body, encoding="utf-8")
        counts[post_type] += 1
        item.clear()

    print(f"pages: {counts['page']}")
    print(f"news:  {counts['news']}")
    print(f"events:{counts['events']}")
    if other_types:
        print(f"(skipped post_types): {other_types}")


if __name__ == "__main__":
    main()
