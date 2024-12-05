package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"slices"
	"strconv"
	"strings"
)

func main() {
	fmt.Println("AoC 2024 Day 1")
	// Open the file
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// Create a scanner to read the file line by line
	scanner := bufio.NewScanner(file)

	// Create an array to store the data
	var left []int
	var right []int

	// Read each line of the file
	for scanner.Scan() {
		line := scanner.Text()

		// Split the line into fields using space as the delimiter
		fields := strings.Fields(line)

		// Append the fields to the data array
		_l, _ := strconv.Atoi(fields[0])
		_r, _ := strconv.Atoi(fields[1])
		left = append(left, _l)
		right = append(right, _r)
	}
	// Check for errors during scanning
	if err := scanner.Err(); err != nil {
		panic(err)
	}

	slices.Sort(left)
	slices.Sort(right)

	totalDist := 0

	for i, num := range left {
		totalDist += int(math.Abs(float64(num - right[i])))
	}

	// Print the resulting array
	fmt.Print("P1: ")
	fmt.Println(totalDist)

	// do n iterations to build a map
	r_map := make(map[int]int)
	similarity := 0
	for _, num := range right {
		r_map[num] += 1
	}

	for _, num := range left {
		similarity += r_map[num] * num
	}
	fmt.Print("P2: ")
	fmt.Println(similarity)

}
