#!/bin/sh
# Make a portable distribution of the annotation tools

# Create distribution directory
dist_dir=local/dist
if [[ -d "${dist_dir}" ]]; then
    rm -rf "${dist_dir}"/*
fi
mkdir -p "${dist_dir}"

# Find the location of the `find' binary because on Windows it defaults to the Windows find utility, which is something different
if [[ $(uname) == *MSYS* ]]; then
    find=/bin/find
else
    find=$(which find)
fi

# Copy labelImg
cp -r tools/labelImg "${dist_dir}"

# Copy annotation_tool
cp tools/annotation_tool.py "${dist_dir}"
sed -i 's/PORTABLE=False/PORTABLE=True/' "${dist_dir}/annotation_tool.py"

# Copy geom_tools
mkdir -p "${dist_dir}/util"
cp util/geom_tools.py "${dist_dir}/util/"

# Remove unnecessary files
"$find" "${dist_dir}" -type f -name "*.pyc" -exec rm -f {} \;
"$find" "${dist_dir}" -type d -name __pycache__ -prune -exec rmdir {} \;
"$find" "${dist_dir}" -type d -name .vscode -prune -exec rm -rf {} \;

# Package everything
cd "${dist_dir}"
tar czvf tools.tar.gz annotation_tool.py util labelImg