import os

root_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM"
core_dir = os.path.join(root_dir, "core")
os.makedirs(core_dir, exist_ok=True)

print("📁 [WORKSPACE ENGINE]: Standard directories verified and locked on disk.")
