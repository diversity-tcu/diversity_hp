#!/usr/bin/env python3
"""Rewrite broken WordPress postID links in content/*.md to proper slug URLs."""
import re
import sys
import urllib.parse
from pathlib import Path
from collections import Counter, defaultdict
from lxml import etree

BASE = Path("/home/sekiguchi/GitHub/diversity_hp")
XML_PATH = BASE / "WordPress.2026-04-13.xml"

CONTENT_DIRS = {
    "pages": BASE / "src/content/pages",
    "news": BASE / "src/content/news",
    "events": BASE / "src/content/events",
}

NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def read_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
        if mm:
            fm[mm.group(1)] = mm.group(2)
    return fm


def build_postid_map():
    """Map post_id -> (type_dir, filename_stem)"""
    # First scan actual files and collect their original_url + slug
    # index by original_url path and by slug
    file_by_url = {}  # full URL -> (type_dir, stem)
    file_by_slug = defaultdict(dict)  # type_dir -> {slug: stem}

    for type_dir, d in CONTENT_DIRS.items():
        for md_file in d.glob("*.md"):
            stem = md_file.stem
            text = md_file.read_text(encoding="utf-8")
            fm = read_frontmatter(text)
            url = fm.get("original_url", "").rstrip("/")
            slug = fm.get("slug", "")
            if url:
                file_by_url[url] = (type_dir, stem)
                # normalize: also store path segment
            if slug:
                file_by_slug[type_dir][slug] = stem

    # Parse XML
    tree = etree.parse(str(XML_PATH))
    root = tree.getroot()

    postid_map = {}  # post_id -> (type_dir, stem)
    unmapped_types = Counter()
    for item in root.iter("item"):
        pid_el = item.find("wp:post_id", NS)
        pname_el = item.find("wp:post_name", NS)
        ptype_el = item.find("wp:post_type", NS)
        link_el = item.find("link")
        if pid_el is None or ptype_el is None:
            continue
        pid = pid_el.text
        ptype = ptype_el.text
        pname = urllib.parse.unquote(pname_el.text) if pname_el is not None and pname_el.text else ""
        link = link_el.text.rstrip("/") if link_el is not None and link_el.text else ""

        if ptype == "page":
            type_dir = "pages"
        elif ptype == "news":
            type_dir = "news"
        elif ptype == "events":
            type_dir = "events"
        else:
            continue

        # Try to find matching file
        stem = None
        # 1) match by link URL
        if link and link in file_by_url:
            td, stem = file_by_url[link]
            if td != type_dir:
                stem = None
        # 2) match by slug
        if stem is None and pname:
            stem = file_by_slug[type_dir].get(pname)
        # 3) match by raw post_name (possibly still url-encoded)
        if stem is None and pname_el is not None and pname_el.text:
            stem = file_by_slug[type_dir].get(pname_el.text)

        if stem:
            postid_map[pid] = (type_dir, stem)
        else:
            unmapped_types[ptype] += 1

    return postid_map, unmapped_types


def main():
    postid_map, unmapped_types = build_postid_map()
    print(f"Built postid map: {len(postid_map)} entries")
    print(f"Unmapped (no matching file): {dict(unmapped_types)}")

    # Regexes
    pat1 = re.compile(r'(\.\./)?index\.html%3Fp=(\d+)\.html', re.IGNORECASE)
    pat2 = re.compile(r'(\.\./)?index\.html\?p=(\d+)(\.html)?', re.IGNORECASE)
    # href="...?p=NNN..." catch (only when not already caught)
    pat3 = re.compile(r'href="([^"]*\?p=(\d+)[^"]*)"')
    # wp-content/uploads paths
    pat_wp1 = re.compile(r'\.\./wp-content/uploads/')
    pat_wp2 = re.compile(r'/wp-content/uploads/')
    pat_wp3 = re.compile(r'\.\./wp-content/')

    hit_by_type = Counter()
    miss_by_type = Counter()
    file_hits = Counter()
    missing_pids = Counter()
    wp_fixes = 0

    def resolve(pid):
        if pid in postid_map:
            td, stem = postid_map[pid]
            if td == "pages":
                return f"/{stem}/"
            return f"/{td}/{stem}/"
        return None

    for type_dir, d in CONTENT_DIRS.items():
        for md_file in d.glob("*.md"):
            text = md_file.read_text(encoding="utf-8")
            original = text
            file_hit = 0

            def repl_plain(m):
                nonlocal file_hit
                pid = m.group(2)
                url = resolve(pid)
                if url:
                    hit_by_type[type_dir] += 1
                    file_hit += 1
                    return url
                miss_by_type[type_dir] += 1
                missing_pids[pid] += 1
                file_hit += 1
                return f'#" data-missing-link="p={pid}'

            text = pat1.sub(repl_plain, text)
            text = pat2.sub(repl_plain, text)

            # pat3: replace only the URL inside href="..."
            def repl_href(m):
                nonlocal file_hit
                pid = m.group(2)
                url = resolve(pid)
                if url:
                    hit_by_type[type_dir] += 1
                    file_hit += 1
                    return f'href="{url}"'
                miss_by_type[type_dir] += 1
                missing_pids[pid] += 1
                file_hit += 1
                return f'href="#" data-missing-link="p={pid}"'

            text = pat3.sub(repl_href, text)

            # wp-content cleanup: ../wp-content/uploads/ -> /uploads/
            # /wp-content/uploads/ -> /uploads/
            new_text, n1 = pat_wp1.subn("/uploads/", text)
            new_text, n2 = pat_wp2.subn("/uploads/", new_text)
            new_text, n3 = pat_wp3.subn("/wp-content/", new_text)  # ../wp-content/xxx (non-uploads)
            wp_fixes += n1 + n2 + n3
            text = new_text

            if text != original:
                md_file.write_text(text, encoding="utf-8")
                file_hits[md_file.name] = file_hit

    print("\n=== Results ===")
    print(f"Hits by type: {dict(hit_by_type)}")
    print(f"Misses by type: {dict(miss_by_type)}")
    print(f"Total hits: {sum(hit_by_type.values())}, misses: {sum(miss_by_type.values())}")
    print(f"wp-content path fixes: {wp_fixes}")
    print(f"\nTop 10 files by rewrites:")
    for f, c in file_hits.most_common(10):
        print(f"  {c:4d}  {f}")
    print(f"\nMissing postIDs (top 20): {missing_pids.most_common(20)}")


if __name__ == "__main__":
    main()
