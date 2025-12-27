import os
import subprocess

# Input and output directories
input_dir = r"C:\Users\j0m_\AppData\Local\Feral Interactive\Total War ROME REMASTERED\Mods\My Mods\MVE\data\characters\textures"
output_dir = os.path.join(input_dir, "unit_textures_resized")

# Make output folder if missing
os.makedirs(output_dir, exist_ok=True)

# Path to texconv (set full path if not in same folder or PATH)
texconv_path = r"texconv.exe"

# Loop through .dds files
for file in os.listdir(input_dir):
    if file.lower().endswith(".dds"):
        input_file = os.path.join(input_dir, file)
        
        # texconv command:
        # -w 256 -h 256 = resize
        # -o output_dir = save in new folder
        cmd = [
            texconv_path,
            "-w", "512",
            "-h", "512",
            "-o", output_dir,
            input_file
        ]
        
        print("Resizing:", file)
        subprocess.run(cmd, check=True)

print("✅ All DDS files resized to 256x256 and saved in:", output_dir)
