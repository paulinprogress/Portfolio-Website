import frontmatter
import re
from pathlib import Path
import shutil
from datetime import datetime

OBSIDIAN_ROOT = Path("~/Obsidian/Main").expanduser()
CONTENT_ROOT = Path("~/Repositories/Website/content").expanduser()

ALLOWED_KEYS = {"anchors", "created", "last updated", "year", "published",
                "publish", "title", "description", "image", "project-type"}

SOURCES = [
    {
        "source": OBSIDIAN_ROOT / "projects" / "portfolio",
        "target_subdir": "portfolio",
        "include_subdirs": True,
    },
    {
        "source": OBSIDIAN_ROOT / "z",
        "target_subdir": "notes",
        "include_subdirs": False,
    },
    {
        "source": OBSIDIAN_ROOT / "projects" / "posts",
        "target_subdir": "feed",
        "include_subdirs": False,
    },
]

def collect_md_files(source_dir: Path):
    """Collect all markdown files recursively from given source directory."""
    return list(source_dir.rglob("*.md"))

def clean_comments(text: str) -> str:
    """Remove all %% comments, multiline or inline."""
    return re.sub(r"%%.*?%%", "", text, flags=re.DOTALL)

def filter_frontmatter(post: frontmatter.Post) -> frontmatter.Post:
    """Keep only allowed frontmatter keys."""
    keys_to_remove = set(post.metadata.keys()) - ALLOWED_KEYS
    for key in keys_to_remove:
        del post.metadata[key]
    return post

def ensure_frontmatter(post: frontmatter.Post, filepath: Path) -> frontmatter.Post:
    """Ensure minimum required frontmatter fields exist."""
    if "title" not in post.metadata:
        post.metadata["title"] = filepath.stem
    if "date" not in post.metadata:
        post.metadata["date"] = datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
    if "publish" not in post.metadata:
        post.metadata["publish"] = False
    return post

def clean_target_dir(target_dir: Path, preserve_patterns):
    """
    Delete all files and folders in target_dir except those matching preserve_patterns.
    Patterns can be:
      - "_index.md"
      - "sidebars-left/*"
    """
    for item in target_dir.rglob("*"):
        rel_path = item.relative_to(target_dir).as_posix()

        # Falls Pfad durch preserve_patterns geschützt ist
        if any(Path(rel_path).match(pat) for pat in preserve_patterns):
            continue

        # Löschen
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item, ignore_errors=True)

def export_notes():
    for group in SOURCES:
        src = group["source"]
        dst_root = CONTENT_ROOT / group["target_subdir"]
        dst_root.mkdir(parents=True, exist_ok=True)

        # Clean target directory, preserving specific files
        preserve = ["_index.md", "sidebars-left/*"]
        clean_target_dir(dst_root, preserve)

        for file in collect_md_files(src):
            rel_path = file.relative_to(src)
            post = frontmatter.load(file)

            # Clean body and frontmatter
            post.content = clean_comments(post.content)
            post = filter_frontmatter(post)
            post = ensure_frontmatter(post, file)

            if post.metadata.get("publish", False):
                if group["include_subdirs"]:
                    target_file = dst_root / rel_path
                else:
                    target_file = dst_root / file.name

                target_file.parent.mkdir(parents=True, exist_ok=True)

                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(frontmatter.dumps(post))

                print(f"Exported: {file.relative_to(OBSIDIAN_ROOT)} → {target_file.relative_to(CONTENT_ROOT)}")
            else:
                print(f"Skipped (publish: false): {file.relative_to(OBSIDIAN_ROOT)}")

if __name__ == "__main__":
    export_notes()
