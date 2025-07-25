import frontmatter
import re
from pathlib import Path
import shutil
from datetime import datetime
import re

# Define directories
OBSIDIAN_ROOT = Path("D:/Meine Ablage/Notebook")
CONTENT_ROOT = Path("~/Repositories/Website/content").expanduser()

ATTACHMENTS_SOURCE_DIR = OBSIDIAN_ROOT / "+" / "attachments"

ATTACHMENTS_TARGET_DIR = Path("~/Repositories/Website/static/images/attachments").expanduser()

# Define content to be imported
SOURCES = [
    {
        "publish": True,
        "source_dir": OBSIDIAN_ROOT / "projects" / "portfolio",
        "target_dir": CONTENT_ROOT / "portfolio",
        "include_subdirs": True,
    },
    {
        "publish": False,
        "source_dir": OBSIDIAN_ROOT / "z",
        "target_dir": CONTENT_ROOT / "notes",
        "include_subdirs": False,
    },
    {
        "publish": False,
        "source_dir": OBSIDIAN_ROOT / "projects" / "posts",
        "target_dir": CONTENT_ROOT / "posts",
        "include_subdirs": False,
    },
]

# Define frontmatter properties/keys that should be imported; rest will be removed
ALLOWED_KEYS = {"anchors", "created", "last updated", "year", "published",
                "publish", "title", "description", "image", "project-type"}

# Define image link pattern for collecting attached image files
IMAGE_LINK_PATTERN = re.compile(r'!\[\[(.+?\.(?:png|jpg|jpeg|gif|webp|svg))\]\]', re.IGNORECASE)



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
    #if "date" not in post.metadata:
    #    post.metadata["date"] = datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
    if "publish" not in post.metadata:
        post.metadata["publish"] = False
    
    # Convert image links before hugo parsing
    if "image" in post.metadata:
        raw = post.metadata["image"]
        
        # Extract filename from [[...]]
        match = re.match(r"\[\[(.+?)\]\]", raw)
        if match:
            filename = match.group(1)
        else:
            filename = raw  # If no brackets
        
        # Update path if not already absolute
        if not filename.startswith("/images/attachments/"):
            post.metadata["image"] = f"/images/attachments/{filename}"

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

        # If path is protected through preserve_patterns
        if any(Path(rel_path).match(pat) for pat in preserve_patterns):
            continue

        # Delete
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item, ignore_errors=True)

def clean_attachments_dir():
    """
    Delete all files and folders in static/images/attachments dir.
    """
    for item in ATTACHMENTS_TARGET_DIR.glob("*"):
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

def collect_image_filenames(frontmatter, content):
    """Extract all image filenames from content and frontmatter 'image'."""
    filenames = set()

    # 1. From content: ![[filename.jpg]]
    wikilink_images = re.findall(r'!\[\[([^\]]+)\]\]', content)
    filenames.update(wikilink_images)

    # 2. From frontmatter: image: '[[filename.jpg]]'
    frontmatter_image = frontmatter.get("image", "")
    if isinstance(frontmatter_image, str):
        match = re.match(r"\[\[(.+?)\]\]", frontmatter_image)
        if match:
            filenames.add(match.group(1))

    return filenames

def find_and_copy_images(filenames):
    for filename in filenames:
        # Recursively look through attachments folder to find file
        for path in ATTACHMENTS_SOURCE_DIR.rglob(filename):
            target_path = ATTACHMENTS_TARGET_DIR / path.name
            shutil.copy2(path, target_path)
            print(f"→ Bild kopiert: {path.name}")
            break  # Only copy first match



def export_notes():
    # Check & clean target image attachments directory
    ATTACHMENTS_TARGET_DIR.mkdir(parents=True, exist_ok=True)
    clean_attachments_dir()
    print(f"Cleaned target attachments directory: {ATTACHMENTS_TARGET_DIR}")

    for group in SOURCES:
        src = group["source_dir"]
        dst_root = group["target_dir"]
        dst_root.mkdir(parents=True, exist_ok=True)

        # Clean target directory, preserving specific files
        preserve = ["_index.md", "sidebars-left/*"]
        clean_target_dir(dst_root, preserve)
        print(f"Cleaned target content directory: {dst_root}")

        if group["publish"]:
            for file in collect_md_files(src):
                rel_path = file.relative_to(src)
                post = frontmatter.load(file)

                # Remove comments
                post.content = clean_comments(post.content)
                # Copy image filenames (before potentially modifying frontmatter)
                image_filenames = collect_image_filenames(post.metadata, post.content)
                # Filter & prepare frontmatter
                post = filter_frontmatter(post)
                post = ensure_frontmatter(post, file)

                if post.metadata.get("publish", False):
                    if group["include_subdirs"]:
                        target_file = dst_root / rel_path
                    else:
                        target_file = dst_root / file.name

                    target_file.parent.mkdir(parents=True, exist_ok=True)

                    # Copy all attached images
                    find_and_copy_images(image_filenames)

                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(frontmatter.dumps(post))

                    print(f"Exported: {file.relative_to(OBSIDIAN_ROOT)} → {target_file.relative_to(CONTENT_ROOT)}")
                else:
                    print(f"Skipped (publish: false): {file.relative_to(OBSIDIAN_ROOT)}")



if __name__ == "__main__":
    export_notes()
