package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type xy struct {
	x int
	y int
}

func main() {
	fmt.Println("AoC 2024 Day 6")
	// Open the file
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	dir_map := make(map[rune]xy)
	dir_map['^'] = xy{0, -1}
	dir_map['v'] = xy{0, 1}
	dir_map['<'] = xy{-1, 0}
	dir_map['>'] = xy{1, 0}

	answer_1 := 0
	answer_2 := 0
	y := 0
	var location xy
	// var current_direction rune
	m := make(map[xy]rune)
	// occupied := 'X'
	answer_2_locations := make(map[xy]rune)
	// Create a scanner to read the file line by line
	scanner := bufio.NewScanner(file)
	// Read each line of the file
	for scanner.Scan() {
		line := scanner.Text()
		for x, char := range line {
			// Enter into map
			m[xy{x, y}] = char
			if char == '^' {
				location = xy{x, y}
			}
		}
		y += 1
	}
	// now that the map is made, we can run the process loop
	answer_1, _, answer_2_locations = processMap(m, location, dir_map)

	// for part two we will take the walked map locations, and iterate through
	// for each location, change the walked point from X to #, and reprocess the map
	// if the new map causes the guard to walk over a repeat location WITH THE SAME DIRECTION
	// we have detected a cycle. if they do not cycle, eventually they will exit the map.
	for _l := range answer_2_locations {
		cycleDetected := false
		if _l == location {
			// cannot be considered as an obstacle location
			continue
		}
		// set map location to obstacle
		m[_l] = '#'
		// test map
		_, cycleDetected, _ = processMap(m, location, dir_map)
		if cycleDetected {
			answer_2++
		}
		// unset location
		m[_l] = '.'
	}

	fmt.Printf("P1 %d\n", answer_1)
	fmt.Printf("P2 %d\n", answer_2)

}

func turnToOpen(m map[xy]rune, loc xy, cur_dir rune, dir_map map[rune]xy) (xy, rune) {
	// rotate until a clear direction is found
	dir_order := "^>v<^"
	ahead := m[xy{loc.x + dir_map[cur_dir].x, loc.y + dir_map[cur_dir].y}]
	// fmt.Printf("%c\t%c\n", ahead, cur_dir)

	for ahead == '#' {
		cur_dir = rune(dir_order[strings.Index(dir_order, string(cur_dir))+1])
		ahead = m[xy{loc.x + dir_map[cur_dir].x, loc.y + dir_map[cur_dir].y}]
		// fmt.Printf("%c\t%c\n", ahead, cur_dir)
	}
	return xy{loc.x + dir_map[cur_dir].x, loc.y + dir_map[cur_dir].y}, cur_dir
}

func processMap(m map[xy]rune, location xy, dir_map map[rune]xy) (int, bool, map[xy]rune) {
	scorable := "^>v<^"
	answer := 0
	current_direction := m[location]
	cycle := false
	travelled := make(map[xy]rune)
maploop:
	for m[location] != 0 {
		// we already have current direction, fill location with travelled value
		travelled[location] = current_direction
		// return next direction based on a check of obstacles in front of heading
		location, current_direction = turnToOpen(m, location, current_direction, dir_map)
		if travelled[location] == current_direction {
			cycle = true
			break maploop // if the direction for the next location is already set to our direction, a cycle has been formed
		}
	}

	// walk loop is complete, now we tally the number of occupied symbols.

	for _, key := range travelled {
		if strings.Contains(scorable, string(key)) {
			answer++
		}
	}
	return answer, cycle, travelled
}
