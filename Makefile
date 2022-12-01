all:
.PHONY: all

day0%/input.txt day%/input.txt: session.txt
	mkdir --parents $(@D)
	curl --cookie "session.txt" --output "$@" \
		"https://adventofcode.com/2022/day/$*/input"

day%/output1.txt: day%/input.txt day%/solve.py
	cd $(@D); python3 solve.py 1
	cat "$@"

day%/output2.txt: day%/input.txt day%/solve.py
	cd $(@D); python3 solve.py 2
	cat "$@"
