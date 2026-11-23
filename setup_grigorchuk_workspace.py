import os
base_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
target_dir = os.path.join(base_path, "grigorchuk_planning_space")
os.makedirs(target_dir, exist_ok=True)
with open(os.path.join(target_dir, "bk.pl"), "w") as f: f.write("grigorchuk_generator(alpha, 0, 1).\ngrigorchuk_generator(beta, 1, 2).\ngrigorchuk_generator(gamma, 2, 3).\n")
with open(os.path.join(target_dir, "bias.pl"), "w") as f: f.write("head_pred(validate_tactical_step,2).\n")
with open(os.path.join(target_dir, "exs.pl"), "w") as f: f.write("pos(validate_tactical_step(0,0)).\n")
print("✅ Workspace seeded.")
