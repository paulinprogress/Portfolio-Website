import frontmatter
from pathlib import Path
from datetime import datetime
import shutil

OBSIDIAN_ROOT = Path("~/Obsidian/Main").expanduser()
CONTENT_ROOT = Path("~/Repositories/Website/content").expanduser()

SOURCES = [
    {
        "source": OBSIDIAN_ROOT / "projects" / "portfolio",
        "target_subdir": "portfolio",
        "include_subdirs": True,
    },
    {
        "source": OBSIDIAN_ROOT / "z",
        "target_subdir": "docs",
        "include_subdirs": False,  # Don't copy subdirectory structure
    },
]

def collect_md_files(source_dir: Path, include_subdirs: bool):
    if include_subdirs:
        return list(source_dir.rglob("*.md"))
    else:
        return [f for f in source_dir.glob("*.md") if f.is_file()]
    
def ensure_frontmatter(file, filepath):
    modified = False
    if "title" not in file.metadata:
        file.metadata["title"] = filepath.stem
        modified = True
    if "date" not in file.metadata:
        file.metadata["date"] = datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
        modified = True
    if "publish" not in file.metadata:
        file.metadata["publish"] = False
        modified = True
    return file, modified

def export_notes():
    for group in SOURCES:
        src = group["source"]
        dst = CONTENT_ROOT / group["target_subdir"]
        dst.mkdir(parents=True, exist_ok=True)

        files = collect_md_files(src, group["include_subdirs"])

        for file in files:
            post = frontmatter.load(file)
            post, _ = ensure_frontmatter(post, file)

            if post.metadata.get("publish", False) is True:
                target_file = dst / file.name
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(frontmatter.dumps(post))
                print(f"Exportiert: {file.relative_to(OBSIDIAN_ROOT)} → {target_file.relative_to(CONTENT_ROOT)}")
            else:
                print(f"Übersprungen (publish: false): {file.relative_to(OBSIDIAN_ROOT)}")

if __name__ == "__main__":
    export_notes()