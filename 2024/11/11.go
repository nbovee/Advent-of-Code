package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	fmt.Println("AoC 2024 Day 11")
	// Open the file
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	answer_1 := 0
	answer_2 := 0
	var start_stones []int

	// Create a scanner to read the file line by line
	scanner := bufio.NewScanner(file)
	// Read each line of the file
	for scanner.Scan() {
		line := scanner.Text()
		// Split the line into fields using space as the delimiter
		fields := strings.Fields(line)
		for _, f := range fields {
			int_field, _ := strconv.Atoi(f)
			start_stones = append(start_stones, int_field)
		}
	}
	// starting slice is created.
	blinks := 25
	p1_stones := make(map[int]int)

	for _, stone := range start_stones {
		p1_stones[stone] += 1
	}
	for range blinks {
		p1_stones = blink(p1_stones)
	}

	for _, count := range p1_stones {
		answer_1 += count
	}
	// p2 optimized
	// instead of tracking everything, each stone can be calculated in isolation
	blinks = 75
	p2_stones := make(map[int]int)

	for _, stone := range start_stones {
		p2_stones[stone] += 1
	}
	for range blinks {
		p2_stones = blink(p2_stones)
	}

	for _, count := range p2_stones {
		answer_2 += count
	}
	fmt.Printf("P1 %d\n", answer_1)
	fmt.Printf("P2 %d\n", answer_2)
}

// use dicts to cheat on math
func blink(stones map[int]int) map[int]int {
	result := make(map[int]int)
	for stone, count := range stones {
		blinked := blinkStone(stone)
		for _, _s := range blinked {
			result[_s] += count
		}
	}
	return result
}

// return the resulting stone(s) from an input stone
func blinkStone(stone int) []int {
	str_stone := strconv.Itoa(stone)
	if stone == 0 {
		return []int{1}
	} else if len(str_stone)%2 == 0 {
		l_stone, _ := strconv.Atoi(str_stone[:len(str_stone)/2])
		r_stone, _ := strconv.Atoi(str_stone[len(str_stone)/2:])
		return []int{l_stone, r_stone}
	} else {
		return []int{stone * 2024}
	}
}
