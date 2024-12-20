#!/bin/bash
# Create the directory for a new day's code.
#
YEAR="2024"

usage () {
    echo "Usage: $0 <day>"
    echo "Create the directory for the given day."
    exit 0
}

error () {
    echo "Error: $*"
    exit 1
}

test -n "$1" || usage
DAY="$1"

dir="day${DAY}"
prog="$dir/day${DAY}.py"
infile="$dir/input.txt"
desc="$dir/day${DAY}.md"

mkdir -p "$dir" || error "Unable to create $dir"
echo "Created $dir"

test -f "$prog" || \
    sed -E 's!%DAY%!'$DAY'!' dayN.py | \
    sed -E 's!%YEAR%!'$YEAR'!' > "$prog" || \
    error "Unable to install $prog"

chmod +x "$prog"
echo "Wrote $prog"

./download.py -y $YEAR -d "$DAY" --outfile "$desc" || \
    error "Unable to download puzzle description"

./download.py -y $YEAR -d "$DAY" --input --outfile "$infile" || \
    error "Unable to download input data"
echo "$infile has $(wc -l $infile | awk '{print $1}') lines"

git add "$prog" "$desc" "$infile"

vim "$prog" "$desc" "$infile"


