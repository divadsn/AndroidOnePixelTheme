#!/usr/bin/env python3
import os
import json
import shutil
import subprocess
from pprint import pprint
from templates import generate_manifest, generate_gradle

DEVNULL = open(os.devnull, "w")
EXEC = ["bash", "gradlew", "app:assembleDebug"]
OUTPUT = "build/app/build/outputs/apk/debug/app-debug.apk"
MANIFEST = "build/app/src/main/AndroidManifest.xml"
GRADLE = "build/app/build.gradle"
OVERLAY_DIR = "system/vendor/overlay"
PACKAGE_BASE = "com.android.theme."
LABEL = "Pixel Theme "


def generate_filename(label):
    return label.replace(" ", "") + ".apk"

print("Android One Pixel Theme Buildscript")

# Loop for every file in every directory, subdirectory etc.
overlays = {}
for subdir, dirs, files in os.walk("overlays", topdown=True):
    for file in files:
        if file == "overlay.json":
            path = os.path.join(subdir, file)
            with open(path, "r") as json_file:
                overlays[subdir] = json.load(json_file)

# Check if any overlay has to be built
if len(overlays) == 0:
    print("No overlays to be built found, quitting...")
    exit(0)

print(f"Running in {os.getcwd()}")
print(f"Total overlays to be built: {len(overlays)}")

os.makedirs(OVERLAY_DIR, exist_ok=True)

# Building overlays
for overlay_dir in overlays:
    # Cleaning up old files
    shutil.rmtree("build/app/src/main/res", ignore_errors=True)

    # Set overlay details
    overlay = overlays[overlay_dir]
    name = overlay["name"]
    targetPackage = overlay["targetPackage"]
    package = PACKAGE_BASE + name.lower()
    label = LABEL + name

    print(f"Building overlay for {name} ({targetPackage})... ", end="")

    # Copy overlay files to build directory
    shutil.copytree(os.path.join(overlay_dir, "res"), "build/app/src/main/res")
    
    # Generate AndroidManifest.xml
    with open(MANIFEST, "w") as manifest_file:
        manifest = generate_manifest(package, targetPackage, label)
        manifest_file.write(manifest)
    
    # Generate build.gradle
    with open(GRADLE, "w") as gradle_file:
        gradle = generate_gradle(package)
        gradle_file.write(gradle)

    # Build overlay and wait
    p = subprocess.Popen(EXEC, cwd="build", stdout=DEVNULL)
    p.wait()

    # Check exit code of gradle process
    if p.returncode != 0:
        print("Failed!")
        exit(1)
    else:
        shutil.copyfile(OUTPUT, os.path.join(OVERLAY_DIR, generate_filename(label)))

    print("Done!")

# Stop Gradle daemon from running in background
p = subprocess.Popen(["bash", "gradlew", "--stop"], cwd="build", stdout=DEVNULL)
p.wait()
