#!/usr/bin/env bash

# set flag to exit when error
set -eo pipefail

# help function
show_help() {
	cat <<EOF
Usage: create.sh DAY

EOF
	exit 1
}

[[ -z $1 ]] && show_help

day=$(printf "%02d" $1)
srcfile="./src/day${day}.py"

if ! [[ -f "${srcfile}" ]]; then
	cp "./src/template.py" "${srcfile}"
	sed -i -l 12 -l 32 "s/1/${1}/" "${srcfile}"
fi

touch "./input/day${day}.txt"
touch "./input/day${day}_test.txt"

echo "AOC Day${day} created"

if [[ $(date +%d:%H:%M) > "${1}:06:00" ]]; then
	echo "getting input"
	./get_input.sh $1
fi

exit 0
