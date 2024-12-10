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
	fmt.Println("AoC 2024 Day 4")
	// Open the file
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	answer_1 := 0
	answer_2 := 0
	y := 0

	// Create a scanner to read the file line by line
	scanner := bufio.NewScanner(file)
	// Read each line of the file
	for scanner.Scan() {
		line := scanner.Text()
		// Split the line into fields using space as the delimiter
		fields := strings.Fields(line)

	}

	fmt.Printf("P1 %d\n", answer_1)
	fmt.Printf("P2 %d\n", answer_2)

}
