import os
import shutil

def move_images(src_dir, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    moved = []
    for root, _, files in os.walk(src_dir):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg')):
                src = os.path.join(root, f)
                dst = os.path.join(dest_dir, f)
                try:
                    shutil.move(src, dst)
                    moved.append(dst)
                except Exception:
                    # try copy if move fails
                    try:
                        shutil.copy2(src, dst)
                        moved.append(dst)
                    except Exception:
                        pass
    return len(moved), moved
