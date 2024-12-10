package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type xy struct {
	x int
	y int
}

// tecnnically weight is implicit for this one but we'll use unique weights soon
type xy_w struct {
	xy xy
	w  int
}

func main() {
	fmt.Println("AoC 2024 Day 10")
	// Open the file
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	answer_1 := 0
	answer_2 := 0
	y := 0
	m := make(map[xy]int)
	trailheads := []xy_w{}

	// Create a scanner to read the file line by line
	scanner := bufio.NewScanner(file)
	// Read each line of the file
	for scanner.Scan() {
		line := scanner.Text()
		// Split the line into fields using space as the delimiter
		for x, val := range line {
			i, err := strconv.Atoi(string(val))
			if err != nil {
				i = -1
			}
			// Enter into map
			m[xy{x, y}] = i
			if i == 0 {
				trailheads = append(trailheads, xy_w{xy{x, y}, 0})
			}
		}
		y += 1
	}
	fmt.Printf("Num trailheads = %d\n", len(trailheads))
	// now that we have found all trailheads we can build the length of each with ease by performing BFS search
	// make a slice of locations to inspect and the distance to that location
	for _, head := range trailheads {
		candidates := []xy_w{}
		candidates = append(candidates, head)
		fmt.Printf("Trailhead %d", head)
	process:
		for {
			candidates = trailAscent(m, candidates)
			// since new candidates are added to the end, the first 9 we see means the rest of the slice is 9's
			if m[candidates[0].xy] == 9 {
				break process
			}
		}
		// at this point there can be many dupes in the candidate list. Easy dedupe is make it into a map
		peak_map := make(map[xy]int)
		for _, w := range candidates {
			peak_map[w.xy] = w.w
		}
		// convienantly, tracking duplicate paths to the same peak is the answer for part 2!
		fmt.Printf(" reaches %d peaks with rating %d\n", len(peak_map), len(candidates))
		answer_1 += len(peak_map)
		answer_2 += len(candidates)
	}

	fmt.Printf("P1 %d\n", answer_1)
	fmt.Printf("P2 %d\n", answer_2)

}

func trailAscent(m map[xy]int, locs []xy_w) []xy_w {
	// consume the first value ( unless it is a peak), and add all valid neighbors
	loc_w, locs := pop(locs)
	// check NESW locations
	if m[xy{loc_w.xy.x, loc_w.xy.y - 1}] == m[loc_w.xy]+1 {
		locs = append(locs, xy_w{xy{loc_w.xy.x, loc_w.xy.y - 1}, loc_w.w + 1})
	}
	if m[xy{loc_w.xy.x + 1, loc_w.xy.y}] == m[loc_w.xy]+1 {
		locs = append(locs, xy_w{xy{loc_w.xy.x + 1, loc_w.xy.y}, loc_w.w + 1})
	}
	if m[xy{loc_w.xy.x, loc_w.xy.y + 1}] == m[loc_w.xy]+1 {
		locs = append(locs, xy_w{xy{loc_w.xy.x, loc_w.xy.y + 1}, loc_w.w + 1})
	}
	if m[xy{loc_w.xy.x - 1, loc_w.xy.y}] == m[loc_w.xy]+1 {
		locs = append(locs, xy_w{xy{loc_w.xy.x - 1, loc_w.xy.y}, loc_w.w + 1})
	}
	return locs
}

func pop(s []xy_w) (xy_w, []xy_w) {
	if len(s) == 0 {
		return xy_w{xy{-1, -1}, -1}, s // Return 0 and the original slice if it's empty
	}
	return s[0], s[1:]
}
