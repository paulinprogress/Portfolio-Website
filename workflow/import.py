import frontmatter
import re
from pathlib import Path
import shutil
from PIL import Image
from datetime import datetime
import fnmatch
import unicodedata

"""
This script imports markdown files from an Obsidian vault into a Hugo-based portfolio website.

- Cleans up target directories before import (removing all files)
- Exports Markdown files from specified Obsidian directories, given that `publish` is set to true
- Cleans up frontmatter (allowing only specified keys, ensuring required fields)
- Removes comments from content (%% ... %%)
- Collects and copies linked images to a static directory
- Sets new filename (and thus URL) based on the "title" frontmatter property
"""

# Define directories
OBSIDIAN_ROOT = Path("~/Obsidian/Notebook").expanduser()
WEBSITE_ROOT = Path("~/Repositories/Portfolio-Website").expanduser()

CONTENT_DIR = WEBSITE_ROOT / "content"

ATTACHMENTS_SOURCE_DIR = OBSIDIAN_ROOT / "+" / "media"
ATTACHMENTS_TARGET_DIR = WEBSITE_ROOT / "static" / "attachments"

# Define content to be imported
SOURCES = [
    {
        # PORTFOLIO
        "publish": True,
        "source_dir": OBSIDIAN_ROOT / "projects" / "portfolio",
        "target_dir": CONTENT_DIR / "projects",
        "include_subdirs": True,
    },
    {
        # NOTES
        "publish": False,
        "source_dir": OBSIDIAN_ROOT / "z",
        "target_dir": CONTENT_DIR / "notes",
        "include_subdirs": False,
    },
    {
        # POSTS
        "publish": False,
        "source_dir": OBSIDIAN_ROOT / "projects" / "writing",
        "target_dir": CONTENT_DIR / "posts",
        "include_subdirs": False,
    },
]

# Define frontmatter properties/keys that should be imported; rest will be removed
ALLOWED_KEYS = {"anchors", "created", "last updated", "year", "published", "date", "opened", "closed",
                "publish", "title", "description", "image", "feature-image", "thumb-image", "project-type"}

# Define media link patterns for handling attached media files
IMAGE_LINK_PATTERN = re.compile(r'\[\[(.+?\.(?:webp|jpg|jpeg|png|svg))\]\]', re.IGNORECASE)
VIDEO_LINK_PATTERN = re.compile(r'\[\[(.+?\.(?:webm|mp4|gif))\]\]', re.IGNORECASE)
PDF_LINK_PATTERN = re.compile(r'\[\[(.+?\.(?:pdf))\]\]', re.IGNORECASE)



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
        if any(fnmatch.fnmatch(rel_path, pattern) for pattern in preserve_patterns):
            continue

        # Delete
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item, ignore_errors=True)



def clean_attachments_dir():
    """
    Delete all files and folders in attachments dir.
    """
    for item in ATTACHMENTS_TARGET_DIR.glob("*"):
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)



def collect_md_files(source_dir: Path):
    """Collect all markdown files recursively from given source directory."""
    return list(source_dir.rglob("*.md"))



def collect_attachment_filenames(frontmatter, content):
    """Extract all image filenames from content and frontmatter."""
    filenames = set()

    # From content
    wikilink_images = re.findall(r'!\[\[([^\]]+)\]\]', content)
    filenames.update(wikilink_images)

    # From frontmatter
    for property in frontmatter:
        raw = str(frontmatter[property] or "")
        image_match = re.match(IMAGE_LINK_PATTERN, raw)
        video_match = re.match(VIDEO_LINK_PATTERN, raw)
        pdf_match = re.match(PDF_LINK_PATTERN, raw)
        if image_match:
            filenames.add(image_match.group(1))
        elif video_match:
            filenames.add(video_match.group(1))
        elif pdf_match:
            filenames.add(pdf_match.group(1))  

    return filenames



def find_and_copy_attachments(filenames):
    """Find and copy images from source to target dir."""
    for filename in filenames:
        # Recursively look through attachments folder to find file
        found = None
        for source_path in ATTACHMENTS_SOURCE_DIR.rglob("*"):
            if source_path.name.lower() == filename.lower():
                found = source_path
                break

        if not found:
            print(f"⚠ File not found: {filename}")
            continue
    
        extension = source_path.suffix.lower()

        # --- Images ---
        if extension in [".jpg", ".jpeg", ".png", ".svg", ".webp"]:
            target_path = ATTACHMENTS_TARGET_DIR / f"{source_path.stem}.webp"

            if extension != ".webp":
                try:
                    img = Image.open(source_path)
                    img.save(target_path, "webp")
                    print(f"→ Image converted & imported: {source_path.name} → {target_path.name}")
                except Exception as e:
                    print(f"Error converting image {source_path}: {e}")
            else:
                shutil.copy2(source_path, target_path)
                print(f"→ Image imported: {filename}")

        # --- Videos ---
        elif extension in [".mp4", ".gif", ".webm"]:
            target_path = ATTACHMENTS_TARGET_DIR / f"{source_path.stem}.webm"

            if extension == ".webm":
                shutil.copy2(source_path, target_path)
                print(f"→ Video imported: {filename}")
            else:
                # TODO: needs ffmpeg for real conversion
                print(f"⚠ Skipping video conversion (requires ffmpeg): {source_path.name}")
        
        # --- PDFs ---
        elif extension == ".pdf":
            target_path = ATTACHMENTS_TARGET_DIR / f"{source_path.name}"
            shutil.copy2(source_path, target_path)
            print(f"→ PDF imported: {filename}")



def prepare_content(text: str) -> str:
    """Prepare & clean up content."""
    # Remove all %% comments, multiline or inline
    text = re.sub(r"%%.*?%%", "", text, flags=re.DOTALL)

    # Convert attachment links (ensure WebP/WebM)
    def replace_image(match):
        filename = Path(match.group(1))
        new_filename = f"{filename.stem}.webp"
        return f"[[{new_filename}]]"

    def replace_video(match):
        filename = Path(match.group(1))
        new_filename = f"{filename.stem}.webm"
        return f"[[{new_filename}]]"

    text = re.sub(IMAGE_LINK_PATTERN, replace_image, text)
    text = re.sub(VIDEO_LINK_PATTERN, replace_video, text)

    return text



def prepare_frontmatter(post: frontmatter.Post, filepath: Path) -> frontmatter.Post:
    """Prepare & clean up frontmatter."""
    # Keep only allowed frontmatter keys
    keys_to_remove = set(post.metadata.keys()) - ALLOWED_KEYS
    for key in keys_to_remove:
        del post.metadata[key]
    
    # Ensure minimum required frontmatter fields exist
    if "title" not in post.metadata:
        post.metadata["title"] = filepath.stem
    if "publish" not in post.metadata:
        post.metadata["publish"] = False
    
    # Convert attachment links
    relative_attach_dir = ATTACHMENTS_TARGET_DIR.relative_to(WEBSITE_ROOT / "static")

    for property in list(post.metadata.keys()):
        # Get the raw value
        raw = post.metadata[property]
        raw_str = str(raw)

        image_match = re.match(IMAGE_LINK_PATTERN, raw_str)
        video_match = re.match(VIDEO_LINK_PATTERN, raw_str)

        filename = None
        if image_match:
            f = Path(image_match.group(1))
            filename = f"{f.stem}.webp"
        elif video_match:
            f = Path(video_match.group(1))
            filename = f"{f.stem}.webm"

        if filename:
            if not raw_str.startswith(str(relative_attach_dir)):
                post.metadata[property] = "/" + str((relative_attach_dir / filename).as_posix())


    return post



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

                post = frontmatter.load(file)
                
                if post.metadata.get("publish", False):
                    # Copy attached media files
                    attachment_filenames = collect_attachment_filenames(post.metadata, post.content)
                    find_and_copy_attachments(attachment_filenames)

                    # Remove comments & convert links
                    post.content = prepare_content(post.content)
                    # Filter properties & convert links
                    post = prepare_frontmatter(post, file)

                    # Gerenrate new file names from "title" property
                    safe_title = post.metadata["title"].strip().lower()
                    safe_title = unicodedata.normalize("NFKD", safe_title)
                    safe_title = safe_title.replace(" ", "-")
                    safe_title = re.sub(r"[^\w\-]", "", safe_title)
                    target_file = dst_root / f"{safe_title}.md"

                    # Set target file path based on whether subdirectories are included
                    rel_path = file.relative_to(src)

                    if group["include_subdirs"]:
                        rel_path = file.relative_to(src)
                        target_file = dst_root / rel_path.parent / f"{safe_title}.md"
                    else:
                        target_file = dst_root / f"{safe_title}.md"

                    target_file.parent.mkdir(parents=True, exist_ok=True)

                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(frontmatter.dumps(post))

                    print(f"Exported: {file.relative_to(OBSIDIAN_ROOT)} → {target_file.relative_to(CONTENT_DIR)}")
                else:
                    print(f"Skipped (publish: false): {file.relative_to(OBSIDIAN_ROOT)}")


if __name__ == "__main__":
    export_notes()
