#!/bin/bash
outfile=wagtail_env.sh
printenv | sed 's/^\(.*\)$/export \1/g' > "$outfile"
echo "export PYTHON_INTERPRETER=$(which python)" >> "$outfile"
chmod +x "$outfile"
