package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func main() {
	fmt.Println("AoC 2024 Day 3")
	// Open the file
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// Create a scanner to read the file line by line
	scanner := bufio.NewScanner(file)

	re := regexp.MustCompile(`mul\((\d{1,3}),(\d{1,3})\)`)
	re_2 := regexp.MustCompile(`mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)`)
	sum_prod := 0
	sum_prod_2 := 0
	// Read each line of the file
	do := true
	for scanner.Scan() {
		line := scanner.Text()

		// Split the line into fields using space as the delimiter
		// fields := strings.Fields(line)
		for _, match := range re.FindAllStringSubmatch(line, -1) {
			_l, _r := func() (int, int) {
				x1, _ := strconv.Atoi(match[1])
				x2, _ := strconv.Atoi(match[2])

				return x1, x2
			}()
			sum_prod += _l * _r
		}

		for _, match := range re_2.FindAllStringSubmatch(line, -1) {
			if match[0] == "do()" {
				fmt.Printf("%q\n", match[0])
				do = true
			} else if match[0] == "don't()" {
				fmt.Printf("%q\n", match[0])
				do = false
			} else if do {
				fmt.Printf("%q\n", match)
				_l, _r := func() (int, int) {
					x1, _ := strconv.Atoi(match[1])
					x2, _ := strconv.Atoi(match[2])

					return x1, x2
				}()

				sum_prod_2 += _l * _r
			}
		}
	}
	fmt.Printf("P1 %d\n", sum_prod)
	fmt.Printf("P2 %d\n", sum_prod_2)

}
