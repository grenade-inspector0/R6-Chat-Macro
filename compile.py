"""Compiles the application"""

import os
import time
import shutil
import pathlib
import PyInstaller.__main__ as pyinstaller

EXE_NAME = "R6_Chat_Macro"
ROOT_DIR = pathlib.Path(__file__).parent.resolve()

def compile_main(name, source):
    pyinstaller.run([
        f"--name={name}",
        '--onefile',
        '--console',
        '--clean',
        '--add-data=assets/config.json;assets',
        str(source),
    ])

# Delete the old exe if it exits
target_path = os.path.join(ROOT_DIR, f"{EXE_NAME}.exe")
if os.path.exists(target_path):
    os.remove(target_path)

# Compile the exe
compile_main(EXE_NAME, os.path.join("main.py"))

# Delete any Pycache files
for root, dirs, files in os.walk(ROOT_DIR):
    for dir_name in dirs:
        if dir_name == '__pycache__':
            shutil.rmtree(os.path.join(root, dir_name))
    for file_name in files:
        if file_name.endswith(('.pyc', '.pyo')):
            os.remove(os.path.join(root, file_name))

# Delete build directory
build_dir = os.path.join(ROOT_DIR, "build")
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

# Delete the spec file
spec_file = os.path.join(ROOT_DIR, f"{EXE_NAME}.spec")
if os.path.exists(spec_file):
    os.remove(spec_file)

dist_dir = ROOT_DIR / "dist"

# Move exe to the current directory
exe_file = os.path.join(dist_dir, f"{EXE_NAME}.exe")
if os.path.exists(exe_file):
    shutil.move(str(exe_file), str(target_path))

# Remove the Dist directory
if os.path.exists(dist_dir):
    shutil.rmtree(dist_dir)

os.system("cls")