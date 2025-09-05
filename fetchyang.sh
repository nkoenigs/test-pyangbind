#!/usr/bin/env bash
set -e  # exit on error

# Folder where models will be stored
TARGET_DIR="yang-models"

# GitHub repo for standard YANG models
REPO_URL="https://github.com/YangModels/yang.git"

# If target dir exists, refresh it
if [ -d "$TARGET_DIR" ]; then
    echo "Updating existing YANG models repo..."
    cd "$TARGET_DIR"
    git pull origin main
    cd ..
else
    echo "Cloning YANG models repo..."
    git clone --depth=1 "$REPO_URL" "$TARGET_DIR"
fi

echo "Copying standard YANG modules into ./std-yang"
mkdir -p std-yang
cp -r "$TARGET_DIR"/standard/ietf/RFC/* std-yang/ 2>/dev/null || true
cp -r "$TARGET_DIR"/standard/ieee/* std-yang/ 2>/dev/null || true

echo "Done. Standard YANG models are in ./std-yang"