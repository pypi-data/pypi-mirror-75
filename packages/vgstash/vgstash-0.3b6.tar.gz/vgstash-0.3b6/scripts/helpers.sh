#!/usr/bin/env bash

# This is a set of helper bash functions that are too small for their own file,
# but useful enough to be worth `source`ing in your bashrc.

# Faster general searching
function vgsrc() {
	case $# in
		1)
			vgstash list | grep -iE "$1"
			;;
		2)
			vgstash list "$1" | grep -iE "$2"
			;;
		*)
			echo "usage: vgsrc [game name]"
			echo " or    vgsrc [view name] [game name]"
			echo
			echo "Ex: vgsrc physical Borderlands"
			;;
	esac
}

# Faster adding
function vgadd() {
	vgstash add "$@"
}

# Shows you a list of *unique* game titles that you have beaten or completed.
# This allows you to weed out the games you own or have beaten on more than one
# platform.
function vgub() {
	# TODO: improve
	vgstash list -w 80 | head -n 2
	vgstash list done -w 80 | sed -e '1,2d' | sort | uniq -w50 | sort -b -t'|' -k 2,2
}

# Shows you the games that have more than one entry (by title) in vgstash.
# Helpful for seeing games you own or have owned more than one copy of.
function vgmulti() {
	# TODO: improve
	if [ -n $1 ]; then
		local filter="$1"
	else
		local filter="allgames"
	fi
	vgstash list -w 80 | head -n 2
	vgstash list $filter -w 80 | sort | uniq -D -w50
}

# Prints the title and system of a random game that you need to beat.
# This tool is great for deciding what to play to knock out the backlog.
function vgrand() {
	local game=$(vgstash list playlog | sed -e '1,2d' | shuf -n 1 --random-source=/dev/random | cut -d '|' -f 1-2 | tr -s ' ' | sed -e 's: | :, for :' -e 's:\s$::')
	echo "You should play ${game}!"
}
