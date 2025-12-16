import subprocess
import os

import re
import logging
from logger import setup_logging

DECOMPILE_DIR = "work/decompile/"
setup_logging()
log = logging.getLogger(__name__)

def diff() -> str:
    result = subprocess.run(
        ["git", "diff"],
        cwd=DECOMPILE_DIR,
        capture_output=True,
        text=True
    )
    return result.stdout

def main():
    git_exists = os.path.exists(DECOMPILE_DIR + ".git")
    if not git_exists:
        log.info("Decompile directory is not a git repository. Initializing git...")
        subprocess.run(["git", "init"], cwd=DECOMPILE_DIR)
    else:
        log.info("Git repository found in decompile directory.")

    diffs = diff()
    if diffs == "":
        log.info("No changes detected. No patches to create.")
        return
    
    patches_dir = "patches/"
    os.makedirs(patches_dir, exist_ok=True)

    file_pattern = r'diff --git a/(.+?) b/(.+?)(?:\n|$)'
    matches = re.findall(file_pattern, diffs)
    
    if not matches:
        log.warning("No file paths found in diff output")
        return
    
    for old_path, new_path in matches:
        patch_filename = re.sub(r'\.java$', '.patch', new_path)
        patch_path = os.path.join(patches_dir, patch_filename)
        
        patch_dir = os.path.dirname(patch_path)
        os.makedirs(patch_dir, exist_ok=True)
        
        with open(patch_path, 'w') as f:
            f.write(diffs)
        
        log.info(f"Created patch file: {patch_path}")


if __name__ == "__main__":
    main()