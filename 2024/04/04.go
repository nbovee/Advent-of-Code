package main

import (
	"bufio"
	"fmt"
	"os"
)

type xy struct {
	x int
	y int
}

func main() {
	fmt.Println("AoC 2024 Day 4")
	// Open the file
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// Read each line of the file
	xmas_found := 0
	y := 0
	m := make(map[xy]rune)
	var starts = []xy{}
	// Create a scanner to read the file line by line
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()

		for x, char := range line {
			// Enter into map
			m[xy{x, y}] = char
			if char == 'X' {
				starts = append(starts, xy{x, y})
			}

		}
		y += 1
	}
	for _, s := range starts {
		// from each start point, check the cardinal directions for "X, M, A, S"
		// then check the diagonals
		xmas_found += checkOffset(0, 1, s, m)
		xmas_found += checkOffset(1, 0, s, m)
		xmas_found += checkOffset(0, -1, s, m)
		xmas_found += checkOffset(-1, 0, s, m)
		xmas_found += checkOffset(1, 1, s, m)
		xmas_found += checkOffset(1, -1, s, m)
		xmas_found += checkOffset(-1, 1, s, m)
		xmas_found += checkOffset(-1, -1, s, m)

	}
	fmt.Printf("P1 starts=%d, %d\n", len(starts), xmas_found)
	fmt.Printf("P2 %q\n", 0)

}

func checkOffset(o_x int, o_y int, start xy, m map[xy]rune) int {
	_mas := "MAS"
	var disp string
	disp = " X"
	for i, char := range _mas {
		this := xy{start.x + (i+1)*o_x, start.y + (i+1)*o_y}
		if m[this] != char {
			return 0
		} else {
			disp = disp + string(char)
		}
	}
	return 1
}
