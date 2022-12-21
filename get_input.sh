#!/usr/bin/env bash

# set flag to exit when error
set -eo pipefail

# help function
show_help() {
	cat <<EOF
Usage: get_input.sh DAY

EOF
	exit 1
}

[[ -z $1 ]] && show_help

year=2022
day=$(printf "%02d" $1)

session=0

curl --silent "https://adventofcode.com/${year}/day/${day}/input" --cookie "session=${session}" -A 'abidkyo @ github.com/abidkyo' -o "./input/day${day}.txt"

exit 0
