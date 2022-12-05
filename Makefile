test:
	@echo \# testing day??/solve.py
	flake8 day??/solve.py
	for script in day??/solve.py; do python3 -m doctest "$$script"; done
.PHONY: test

day = $(shell day="$*"; echo $${day#0})

day%: day%/input.txt day%/solve.py
	touch "$@"
.PRECIOUS: day%/input.txt day%/solve.py

day%/solve.py:
	mkdir --parents "$(@D)"
	sed "s/{{day}}/$(day)/" <stub.py >"$@"
	chmod +x "$@"

day%/input.txt: session.txt
	mkdir --parents "$(@D)"
	curl --cookie "session.txt" --output "$@" \
		"https://adventofcode.com/2022/day/$(day)/input"

day%/output1.txt: day%/input.txt day%/solve.py
	cd "$(@D)"; python3 solve.py 1
	cat "$@"

day%/output2.txt: day%/input.txt day%/solve.py
	cd "$(@D)"; python3 solve.py 2
	cat "$@"
